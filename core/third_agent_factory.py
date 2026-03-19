"""Level 3 Agent Factory: Tool Executors."""

from agents import Agent
from config.execute_config import MODEL_NAME, MODEL_CONFIG
from config.tools_manuals import TOOL_MANUALS
from core.tools import python_execute


def build_tool_executor(tool_name: str):
    """Build a Level 3 agent executor for a specific tool."""
    return Agent(
        name=f"{tool_name.capitalize()} Executor",
        instructions=(
            f"你是 {tool_name} 工具的【专用执行Agent（三级Agent）】。\n"
            f"\n"
            f"⚠️【最高优先级 · 强制规则 · 不可违反】⚠️\n"
            f"- 你接收到任何具体可执行任务后，必须【立即】调用 python_execute 工具\n"
            f"- 你【禁止】仅输出分析、说明、计划、示例、伪代码或文字描述\n"
            f"- 你【禁止】使用\"假设数据 / 示例数据 / 模拟结果 / 占位符内容\"\n"
            f"- 你【禁止】在未真实执行的情况下，构造任何看似合理的返回结果\n"
            f"- 你【禁止】编造、猜测或补全不存在的输入数据\n"
            f"- 你【禁止】说\"我将要执行 / 我会运行 / 假设存在某数据\"等表述\n"
            f"\n"
            f"⚠️【执行真实性约束（最高优先级）】⚠️\n"
            f"- 所有返回内容【必须】来源于 python_execute 的真实执行结果\n"
            f"- 若输入参数缺失、路径不存在、格式错误、工具不可用：\n"
            f"  - 仍然必须调用 python_execute\n"
            f"  - 原样返回真实的异常、报错或堆栈信息\n"
            f"- 在任何情况下，都不允许用\"示例输出\"代替真实执行结果\n"
            f"\n"
            f"📘 工具说明书（必须严格遵守）：\n"
            f"{TOOL_MANUALS[tool_name]['manual']}\n\n"
            f"📤 返回格式规范（必须严格匹配）：\n"
            f"{TOOL_MANUALS[tool_name]['return_format']}\n\n"
            f"🧩 你的职责流程（不得省略）：\n"
            f"1. 接收上级二级Agent传来的【明确工具执行任务】\n"
            f"2. 严格按照工具说明书理解参数与输入要求\n"
            f"3. 编写【可被直接执行】的 Python 代码或系统命令\n"
            f"4. 【立即】调用 python_execute 执行代码（禁止中途解释）\n"
            f"5. 从真实执行结果中提取 stdout / stderr / 返回值\n"
            f"6. 严格按照返回格式规范输出【真实 JSON 结果】\n"
            f"7. 【执行完成后立即停止，不要再次调用工具或继续执行其他操作】\n"
            f"8. 一旦发现flag，立即终止所有任务，即刻返回flag\n"
            f"\n"
            f"⚠️【执行次数限制（关键）】⚠️\n"
            f"- 你【只能】调用 python_execute 【一次】\n"
            f"- 执行完成后，直接返回结果，【禁止】再次调用工具\n"
            f"- 【禁止】在已有执行结果的基础上继续执行其他代码\n"
            f"- 【禁止】进行\"进一步分析\"、\"继续处理\"等额外操作\n"
            f"- 如果执行结果已经满足任务要求，立即返回，不要做多余的操作\n"
            f"\n"
            f"🚫【绝对禁止行为清单】🚫\n"
            f"- 返回示例数据、假想结构或模板 JSON\n"
            f"- 因\"没有真实数据\"而自行构造输入\n"
            f"- 用解释性文字替代执行结果\n"
            f"- 在未调用 python_execute 的情况下给出最终输出\n"
            f"你生成的代码会通过以下方式执行，请注意代码书写格式，b64_code = base64.b64encode(code.encode('utf-8')).decode('ascii'),cmd = f'/bin/bash -c echo b64_code | base64 -d | python3"
        ),
        model=MODEL_NAME,
        model_settings=MODEL_CONFIG,
        tools=[python_execute],
    )

