"""Agent Runner for three-level agent system."""

import json
import os
import re
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Any
from colorama import Fore, Style
from agents import Agent, RunConfig, Runner, ModelSettings, ModelProvider
from openai.types.responses import ResponseTextDeltaEvent, ResponseContentPartDoneEvent
from openai import RateLimitError, APIConnectionError, APITimeoutError

from core.level1_agent import task_classifier_agent
from core.level2_agent import (
    agent_information_collection,
    agent_scanning,
    agent_enumeration,
    agent_web_exploitation,
    agent_exploitation,
    agent_password_crypto,
    agent_wireless_attack,
    agent_reverse_engineering,
    agent_forensics,
    agent_post_exploitation,
    agent_custom_code,
)
from core.memory_manager import MemoryManager


TARGET_TO_AGENT = {
    "information_collection": agent_information_collection,
    "scanning": agent_scanning,
    "enumeration": agent_enumeration,
    "web_exploitation": agent_web_exploitation,
    "exploitation": agent_exploitation,
    "password_crypto": agent_password_crypto,
    "wireless_attack": agent_wireless_attack,
    "reverse_engineering": agent_reverse_engineering,
    "forensics": agent_forensics,
    "post_exploitation": agent_post_exploitation,
    "custom_code": agent_custom_code,
}


class AgentRunner:
    """Handles three-level agent query processing and execution."""
    
    def __init__(self, model_name: str = "gpt-4"):
        """Initialize the agent runner."""
        self.memory_manager = MemoryManager(model_name=model_name)  # 智能记忆管理器
        self.output_collector = None  # 输出收集器，用于收集执行过程中的输出

    def _extract_json_from_text(self, text: str) -> str:
        """
        从文本中提取JSON，处理markdown代码块等情况。
        
        Args:
            text: 可能包含JSON的文本
            
        Returns:
            提取出的JSON字符串
        """
        if not text:
            return text
        
        # 移除前后空白
        text = text.strip()
        
        # 尝试匹配markdown代码块中的JSON（支持```json和```两种格式）
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            # 验证是否是有效的JSON
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                pass
        
        # 尝试直接匹配JSON对象（更精确的匹配）
        # 找到第一个{和最后一个}之间的内容
        start_idx = text.find('{')
        if start_idx != -1:
            # 从第一个{开始，找到匹配的}
            brace_count = 0
            for i in range(start_idx, len(text)):
                if text[i] == '{':
                    brace_count += 1
                elif text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_str = text[start_idx:i+1]
                        # 验证是否是有效的JSON
                        try:
                            json.loads(json_str)
                            return json_str
                        except json.JSONDecodeError:
                            pass
        
        # 如果都没匹配到，返回原文本（让json.loads来处理）
        return text

    def _build_query_with_history(self, query: str) -> str:
        """
        构建包含历史记录的查询。

        Args:
            query: 当前查询

        Returns:
            包含历史记录的完整查询
        """
        return self.memory_manager.build_context(query)

    async def route_and_run_level2(self, query: str, task_id: str = None):
        """
        1）用一级 agent 生成 JSON 决策
        2）解析 JSON 拿到 target
        3）根据 target 映射到对应二级 Agent，并再跑一次 Runner
        
        Args:
            query: User query
            task_id: Optional task ID for output collection
        """
        # 构建包含历史记录的查询
        query_with_history = self._build_query_with_history(query)
        
        # 通知Level 1开始
        await self._add_output(task_id, "agent_thinking", {
            "agent": "Level 1 Classifier",
            "status": "thinking",
            "message": "正在执行代码..."
        })

        # 1. 先跑一级 agent（不需要 handoffs，只是普通 LLM 输出）
        classify_result = await self._run_streaming(
            task_classifier_agent,
            query_with_history,
            task_id=task_id,
            silent=True  # Level 1 Agent 的流式输出不显示给用户
        )

        # 取出一级 agent 的最终文本
        decision_text = getattr(classify_result, "final_output", "")

        # 提取JSON（处理markdown代码块等情况）
        json_text = self._extract_json_from_text(decision_text)

        try:
            decision = json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"一级Agent输出不是合法JSON: {decision_text}\n提取的JSON文本: {json_text}\n错误: {e}")

        if decision.get("action") != "handoff":
            raise ValueError(f"一级Agent输出action不为handoff: {decision}")

        target = decision.get("target")
        if target not in TARGET_TO_AGENT:
            raise ValueError(f"未知target: {target}")

        # 显示Level 1的决策结果（简洁版）
        await self._add_output(task_id, "agent_message", {
            "agent": "Level 1 Classifier",
            "content": f"任务分类完成 → **{target}**"
        })

        # 通知Level 2开始
        await self._add_output(task_id, "agent_thinking", {
            "agent": f"Level 2 {target.title()} Agent",
            "status": "thinking",
            "message": f"正在执行 {target} 任务..."
        })

        level2_agent = TARGET_TO_AGENT[target]

        # 2. 调用对应的二级 Agent（这里才是真正的 handoff）
        level2_result = await self._run_streaming(
            level2_agent,
            query_with_history,  # 使用包含历史的查询
            task_id=task_id
        )

        # Level 2完成 - 只显示简短确认，避免与流式输出重复
        await self._add_output(task_id, "agent_message", {
            "agent": f"Level 2 {target.title()} Agent",
            "content": "✅ 执行完成"
        })

        return classify_result, level2_result

    async def run_agent(self, query: str, task_id: str = None) -> Any:
        """
        Run the three-level agent system.
        
        Args:
            query: User's natural language query
            websocket_id: Optional WebSocket connection ID for real-time updates
            
        Returns:
            Agent execution result
        """
        print(f"{Fore.CYAN}\nProcessing query: {Fore.WHITE}{query}{Style.RESET_ALL}\n")

        # 前端已经显示了用户消息，这里不再重复发送
        # await self._add_output(task_id, "user_message", {"content": query})

        try:
            classify_result, level2_result = await self.route_and_run_level2(query, task_id)

            # 保存对话历史
            ai_response = getattr(level2_result, "final_output", "")
            self._add_to_history(query, ai_response)

            # 任务完成
            await self._add_output(task_id, "task_completed", {"success": True})

            return level2_result
        except Exception as e:
            error_msg = str(e)
            print(f"{Fore.RED}Error processing agent request: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            # 即使出错也保存查询（但不保存响应）
            self._add_to_history(query, None)

            # 显示错误
            await self._add_output(task_id, "agent_message", {
                "agent": "System",
                "content": f"❌ 执行出错：{error_msg}",
                "is_error": True
            })
            await self._add_output(task_id, "task_completed", {"success": False, "error": error_msg})

            return None
    
    def _add_to_history(self, user_query: str, ai_response: Optional[str] = None):
        """
        添加对话到历史记录。

        Args:
            user_query: 用户查询
            ai_response: AI响应（可选）
        """
        self.memory_manager.add_conversation(user_query, ai_response)
    
    def clear_history(self):
        """清空对话历史。"""
        self.memory_manager.clear_memory()
        print(f"{Fore.YELLOW}对话历史已清空{Style.RESET_ALL}")

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息。

        Returns:
            记忆统计字典
        """
        return self.memory_manager.get_memory_stats()

    def get_history_summary(self) -> str:
        """
        获取对话历史摘要。

        Returns:
            历史记录摘要文本
        """
        stats = self.memory_manager.get_memory_stats()

        if stats["total_conversations"] == 0:
            return "暂无对话历史"

        summary = f"""📊 记忆统计信息：
总对话数: {stats["total_conversations"]}
总Token数: {stats["total_tokens"]:,} / {stats["token_limit"]:,} ({stats["token_usage_percent"]:.1f}%)
平均重要性: {stats["average_importance"]}
已总结对话: {stats["summarized_conversations"]}

时间范围: {stats["date_range"]["oldest"]} 至 {stats["date_range"]["newest"]}
"""

        return summary

    async def _run_streaming(self, agent: Agent, query: str, max_turns: int = None, task_id: str = None, silent: bool = False) -> Any:
        """
        Run agent with streaming output.
        
        Args:
            agent: Agent to run
            query: Input query
            max_turns: Maximum number of turns (None for default)
            websocket_id: Optional WebSocket connection ID for real-time updates
        """
        from config.execute_config import client
        from agents import OpenAIChatCompletionsModel
        
        class SimpleModelProvider(ModelProvider):
            def get_model(self, model_name: str):
                return OpenAIChatCompletionsModel(
                    model=model_name or os.getenv("MODEL_NAME", "gpt-4o"),
                    openai_client=client
                )
        
        model_provider = SimpleModelProvider()
        
        # 根据Agent类型设置不同的max_turns
        # 三级Agent（工具执行器）应该只执行一次
        if max_turns is None:
            # 检查是否是三级Agent（通过名称判断）
            agent_name = getattr(agent, 'name', '')
            if 'Executor' in agent_name and 'Custom Code' not in agent_name:
                max_turns = 2  # 三级Agent最多2轮：1轮执行，1轮返回结果
            elif 'Custom Code Executor' in agent_name:
                max_turns = 3  # Custom Code Agent需要3轮：1轮思考，1轮调用工具，1轮返回结果
            else:
                max_turns = 5  # 一级和二级Agent可以多轮
        
        result = Runner.run_streamed(
            agent,
            input=query,
            max_turns=max_turns,
            run_config=RunConfig(
                model_provider=model_provider,
                trace_include_sensitive_data=True,
                handoff_input_filter=None
            )
        )

        print(f"{Fore.GREEN}Reply:{Style.RESET_ALL}", end="", flush=True)
        
        try:
            async for event in result.stream_events():
                if not silent:
                    await self._handle_stream_event(event, task_id)
        except (RateLimitError, APITimeoutError, APIConnectionError) as e:
            print(f"\n{Fore.RED}Stream error detected: {type(e).__name__}{Style.RESET_ALL}")
            await self._add_output(task_id, "error", {"message": f"Stream error: {type(e).__name__}"})
            raise e
        except Exception as e:
            await self._handle_stream_error(e, task_id)

        print(f"\n\n{Fore.GREEN}Query completed!{Style.RESET_ALL}")
        await self._add_output(task_id, "completed", {"message": "Query completed"})
        return result
    
    async def _handle_stream_event(self, event: Any, task_id: str = None) -> None:
        """Handle individual stream events with ChatGPT-like behavior."""
        try:
            if event.type == "raw_response_event":
                # 处理文本流式输出
                if isinstance(event.data, ResponseTextDeltaEvent):
                    delta = event.data.delta
                    print(f"{Fore.WHITE}{delta}{Style.RESET_ALL}", end="", flush=True)
                    await self._add_output(task_id, "text_delta", {"delta": delta})
                elif isinstance(event.data, ResponseContentPartDoneEvent):
                    print(f"\n", end="", flush=True)
                    await self._add_output(task_id, "text_delta", {"delta": "\n"})

            elif event.type == "run_item_stream_event":
                # 处理handoff类型的工具调用
                if event.item.type == "tool_call_item":
                    await self._handle_tool_call(event.item, task_id)
                elif event.item.type == "tool_call_output_item":
                    await self._handle_tool_output(event.item, task_id)

            # 处理直接工具调用（custom_code agent等）
            elif event.type in ["tool_call_event", "function_call_event"]:
                await self._handle_any_tool_call(event, task_id)

            elif event.type in ["tool_call_output_event", "function_call_output_event"]:
                await self._handle_any_tool_output(event, task_id)

        except Exception as e:
            print(f"{Fore.RED}[ERROR] 处理事件失败: {e}{Style.RESET_ALL}", flush=True)
            import traceback
            traceback.print_exc()

    async def _handle_any_tool_call(self, event: Any, task_id: str = None) -> None:
        """Handle any type of tool call event."""
        try:
            # 尝试多种方式获取工具信息
            tool_name = getattr(event, 'tool_name', None) or \
                       getattr(event, 'function_name', None) or \
                       getattr(event, 'name', 'Unknown tool')

            tool_args = getattr(event, 'arguments', None) or \
                       getattr(event, 'tool_args', None) or \
                       getattr(event, 'args', {})

            print(f"\n{Fore.CYAN}[TOOL CALL] {tool_name}{Style.RESET_ALL}", flush=True)
            if tool_args:
                print(f"{Fore.CYAN}[PARAMS] {tool_args}{Style.RESET_ALL}", flush=True)

            # 发送工具调用到前端
            if task_id:
                await self._add_output(task_id, "tool_call", {
                    "tool_name": tool_name,
                    "tool_args": tool_args or {}
                })
        except Exception as e:
            print(f"{Fore.RED}[ERROR] 处理工具调用失败: {e}{Style.RESET_ALL}", flush=True)

    async def _handle_any_tool_output(self, event: Any, task_id: str = None) -> None:
        """Handle any type of tool output event."""
        try:
            # 尝试多种方式获取工具输出信息
            tool_id = getattr(event, 'tool_call_id', None) or \
                     getattr(event, 'function_name', None) or \
                     getattr(event, 'tool_id', None) or \
                     getattr(event, 'call_id', 'Unknown tool')

            output = getattr(event, 'output', 'Unknown output')
            output_text = self._parse_tool_output(output)

            print(f"\n{Fore.GREEN}[TOOL RESULT] {tool_id}: {output_text[:100]}{'...' if len(output_text) > 100 else ''}{Style.RESET_ALL}", flush=True)

            # 发送工具输出到前端
            if task_id:
                await self._add_output(task_id, "tool_output", {
                    "tool_id": tool_id,
                    "output": output_text
                })
        except Exception as e:
            print(f"{Fore.RED}[ERROR] 处理工具输出失败: {e}{Style.RESET_ALL}", flush=True)

    async def _handle_tool_call(self, item: Any, task_id: str = None) -> None:
        """Handle tool call events."""
        raw_item = getattr(item, "raw_item", None)
        tool_name = ""
        tool_args = {}
        
        if raw_item:
            tool_name = getattr(raw_item, "name", "Unknown tool")
            tool_str = getattr(raw_item, "arguments", "{}")
            if isinstance(tool_str, str):
                try:
                    tool_args = json.loads(tool_str)
                except json.JSONDecodeError:
                    tool_args = {"raw_arguments": tool_str}
        
        print(f"\n{Fore.CYAN}Tool name: {tool_name}{Style.RESET_ALL}", flush=True)
        print(f"\n{Fore.CYAN}Tool parameters: {tool_args}{Style.RESET_ALL}", flush=True)
        
        # 发送工具调用信息到输出收集器
        if task_id:
            await self._add_output(task_id, "tool_call", {
                "tool_name": tool_name,
                "tool_args": tool_args
            })
            print(f"{Fore.YELLOW}[DEBUG] 工具调用已发送到输出收集器: {tool_name}, task_id: {task_id}{Style.RESET_ALL}", flush=True)
        else:
            print(f"{Fore.RED}[WARNING] task_id 为 None，工具调用信息未发送到前端{Style.RESET_ALL}", flush=True)
    
    async def _handle_tool_output(self, item: Any, task_id: str = None) -> None:
        """Handle tool output events."""
        raw_item = getattr(item, "raw_item", None)
        tool_id = "Unknown tool ID"
        
        if isinstance(raw_item, dict) and "call_id" in raw_item:
            tool_id = raw_item["call_id"]
        
        output = getattr(item, "output", "Unknown output")
        output_text = self._parse_tool_output(output)
        
        print(f"\n{Fore.GREEN}Tool call {tool_id} returned result: {output_text}{Style.RESET_ALL}", flush=True)
        
        # 发送工具输出到输出收集器
        if task_id:
            await self._add_output(task_id, "tool_output", {
                "tool_id": tool_id,
                "output": output_text
            })
            print(f"{Fore.YELLOW}[DEBUG] 工具输出已发送到输出收集器: {tool_id}, task_id: {task_id}{Style.RESET_ALL}", flush=True)
        else:
            print(f"{Fore.RED}[WARNING] task_id 为 None，工具输出未发送到前端{Style.RESET_ALL}", flush=True)
    
    def _parse_tool_output(self, output: Any) -> str:
        """Parse tool output into readable text."""
        if isinstance(output, str) and (output.startswith("{") or output.startswith("[")):
            try:
                output_data = json.loads(output)
                if isinstance(output_data, dict):
                    if 'type' in output_data and output_data['type'] == 'text' and 'text' in output_data:
                        return output_data['text']
                    elif 'text' in output_data:
                        return output_data['text']
                    elif 'content' in output_data:
                        return output_data['content']
                    else:
                        return json.dumps(output_data, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                return f"Unparsable JSON output: {output}"
        return str(output)

    async def _handle_stream_error(self, error: Exception, task_id: str = None) -> None:
        """Handle streaming errors."""
        error_msg = f"Error processing streamed response event: {error}"
        print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}", flush=True)
        await self._add_output(task_id, "error", {"message": error_msg})
    
    async def _add_output(self, task_id: str, output_type: str, data: Any) -> None:
        """添加输出到收集器"""
        if not task_id:
            print(f"{Fore.YELLOW}[WARNING] _add_output: task_id 为 None, 输出类型: {output_type}{Style.RESET_ALL}", flush=True)
            return
        
        if self.output_collector:
            try:
                await self.output_collector.add_output(output_type, data)
                if output_type in ["tool_call", "tool_output"]:
                    print(f"{Fore.GREEN}[DEBUG] 输出已添加到收集器: {output_type}, task_id: {task_id}{Style.RESET_ALL}", flush=True)
            except Exception as e:
                print(f"{Fore.RED}[ERROR] 添加输出到收集器失败: {e}, 输出类型: {output_type}{Style.RESET_ALL}", flush=True)
                import traceback
                traceback.print_exc()


# Create singleton instance
agent_runner = AgentRunner()

