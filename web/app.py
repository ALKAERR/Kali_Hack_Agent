"""FastAPI web application for displaying conversation history."""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import json
import asyncio
from datetime import datetime
import uuid

# 导入agent_runner以访问对话历史
from core.agent_runner import agent_runner

app = FastAPI(title="Kali Code Executor Web Interface")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储查询任务的状态和输出
query_tasks: Dict[str, Dict[str, Any]] = {}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页面"""
    import os
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(html_path)


@app.get("/api/history")
async def get_history():
    """获取对话历史"""
    history = agent_runner.conversation_history
    return {
        "status": "success",
        "count": len(history),
        "history": history
    }


@app.get("/api/history/summary")
async def get_history_summary():
    """获取对话历史摘要"""
    summary = agent_runner.get_history_summary()
    return {
        "status": "success",
        "summary": summary
    }

@app.get("/api/memory/stats")
async def get_memory_stats():
    """获取记忆统计信息"""
    try:
        stats = agent_runner.get_memory_stats()
        return {
            "status": "success",
            "stats": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"获取记忆统计失败: {str(e)}"
        }

@app.post("/api/history/clear")
async def clear_history():
    """清空对话历史"""
    agent_runner.clear_history()
    return {
        "status": "success",
        "message": "历史已清空"
    }


@app.post("/api/query")
async def submit_query(request: Request):
    """提交查询并执行agent"""
    try:
        body = await request.json()
        query = body.get("query", "").strip()
    except:
        return {
            "status": "error",
            "message": "无效的请求格式"
        }
    
    if not query:
        return {
            "status": "error",
            "message": "查询不能为空"
        }
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    # 初始化任务状态
    query_tasks[task_id] = {
        "status": "running",
        "query": query,
        "output": [],
        "final_response": None,
        "error": None
    }
    
    # 在后台任务中执行agent
    asyncio.create_task(run_agent_task(task_id, query))
    
    return {
        "status": "success",
        "task_id": task_id,
        "message": "查询已提交"
    }


async def run_agent_task(task_id: str, query: str):
    """在后台运行agent任务"""
    try:
        # 创建一个自定义的输出收集器
        output_collector = OutputCollector(task_id)
        agent_runner.output_collector = output_collector
        
        # 执行agent
        result = await agent_runner.run_agent(query, task_id=task_id)
        
        # 等待一小段时间，确保所有异步输出都被添加
        await asyncio.sleep(0.5)
        
        # 获取最终输出
        final_output = getattr(result, "final_output", "") if result else ""
        
        # 再次等待，确保所有输出都添加完成
        await asyncio.sleep(0.3)
        
        # 打印最终输出统计
        if task_id in query_tasks:
            output_count = len(query_tasks[task_id]["output"])
            tool_call_count = sum(1 for item in query_tasks[task_id]["output"] if item.get("type") == "tool_call")
            tool_output_count = sum(1 for item in query_tasks[task_id]["output"] if item.get("type") == "tool_output")
            print(f"[run_agent_task] 任务 {task_id} 完成，总输出数: {output_count}, 工具调用: {tool_call_count}, 工具输出: {tool_output_count}")
        
        # 更新任务状态
        query_tasks[task_id]["status"] = "completed"
        query_tasks[task_id]["final_response"] = final_output
        
    except Exception as e:
        query_tasks[task_id]["status"] = "error"
        query_tasks[task_id]["error"] = str(e)
        import traceback
        traceback.print_exc()


class OutputCollector:
    """收集agent执行过程中的输出"""
    def __init__(self, task_id: str):
        self.task_id = task_id
    
    async def add_output(self, output_type: str, data: Any):
        """添加输出到任务"""
        if self.task_id not in query_tasks:
            print(f"[OutputCollector ERROR] Task {self.task_id} 不存在于 query_tasks 中")
            return
        
        output_item = {
            "type": output_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        query_tasks[self.task_id]["output"].append(output_item)
        
        # 只在非text_delta类型时打印调试信息（避免输出过多）
        if output_type != "text_delta":
            print(f"[OutputCollector] Task {self.task_id}: {output_type} - {str(data)[:200]}")
        
        # 对于工具调用和工具输出，额外打印确认信息
        if output_type in ["tool_call", "tool_output"]:
            print(f"[OutputCollector] ✓ {output_type} 已添加到任务 {self.task_id}，当前输出数量: {len(query_tasks[self.task_id]['output'])}")


@app.get("/api/query/{task_id}/stream")
async def stream_query_output(task_id: str):
    """SSE流式输出查询结果"""
    print(f"[SSE Stream] 开始为任务 {task_id} 建立SSE连接")
    async def event_generator():
        last_index = 0
        max_wait_time = 300  # 最大等待时间30秒（300 * 0.1秒）
        wait_count = 0
        
        # 立即发送已存在的输出
        if task_id in query_tasks:
            task = query_tasks[task_id]
            if len(task["output"]) > 0:
                for i, output_item in enumerate(task["output"]):
                    try:
                        json_str = json.dumps(output_item, ensure_ascii=False)
                        yield f"data: {json_str}\n\n"
                    except Exception as e:
                        print(f"[SSE Stream ERROR] 发送已存在输出失败: {e}, 输出项: {output_item.get('type')}")
                        import traceback
                        traceback.print_exc()
                last_index = len(task["output"])
        
        while True:
            if task_id not in query_tasks:
                yield f"data: {json.dumps({'type': 'error', 'data': {'error': '任务不存在'}})}\n\n"
                break
            
            task = query_tasks[task_id]
            
            # 发送新的输出
            if len(task["output"]) > last_index:
                for i in range(last_index, len(task["output"])):
                    output_item = task["output"][i]
                    try:
                        json_str = json.dumps(output_item, ensure_ascii=False)
                        yield f"data: {json_str}\n\n"
                    except Exception as e:
                        print(f"[SSE Stream ERROR] 发送输出失败: {e}, 输出项: {output_item.get('type')}")
                        import traceback
                        traceback.print_exc()
                last_index = len(task["output"])
                wait_count = 0  # 有输出时重置等待计数
            else:
                wait_count += 1
            
            # 检查任务是否完成
            if task["status"] == "completed":
                # 等待一小段时间，确保所有输出都被添加
                await asyncio.sleep(0.2)
                
                # 确保发送所有剩余输出
                if len(task["output"]) > last_index:
                    for i in range(last_index, len(task["output"])):
                        output_item = task["output"][i]
                        try:
                            json_str = json.dumps(output_item, ensure_ascii=False)
                            yield f"data: {json_str}\n\n"
                        except Exception as e:
                            print(f"[SSE Stream ERROR] 发送剩余输出失败: {e}, 输出项: {output_item.get('type')}")
                            import traceback
                            traceback.print_exc()
                
                yield f"data: {json.dumps({'type': 'completed', 'data': {'response': task.get('final_response', '')}})}\n\n"
                break
            elif task["status"] == "error":
                yield f"data: {json.dumps({'type': 'error', 'data': {'error': task.get('error', '未知错误')}})}\n\n"
                break
            
            # 如果等待时间过长，可能是任务卡住了
            if wait_count > max_wait_time:
                yield f"data: {json.dumps({'type': 'error', 'data': {'error': '任务执行超时'}})}\n\n"
                break
            
            # 减少轮询间隔，提高实时性
            await asyncio.sleep(0.05)  # 50ms轮询间隔，提高响应速度
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# 挂载静态文件
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

