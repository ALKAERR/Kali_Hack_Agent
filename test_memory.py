#!/usr/bin/env python3
"""测试记忆管理系统"""

from core.memory_manager import MemoryManager
from datetime import datetime, timedelta

def test_memory_manager():
    """测试记忆管理器的基本功能"""
    print("🧠 测试智能记忆管理系统")
    print("=" * 50)

    # 创建记忆管理器
    memory = MemoryManager(model_name="gpt-4", max_tokens=4000)

    # 添加一些测试对话
    conversations = [
        ("你好", "你好！我是AI助手，很高兴为你服务。"),
        ("python代码执行环境是什么？", "这是一个Kali Linux环境，支持Python脚本执行，包括系统命令调用和各种库的使用。"),
        ("帮我写个获取系统信息的脚本", "好的，我来为你编写一个获取系统基本信息的Python脚本。"),
        ("脚本出现错误：ImportError: No module named 'psutil'", "看起来缺少psutil模块。让我修改脚本使用标准库来获取系统信息。"),
        ("现在可以运行了吗？", "是的，现在使用标准库的脚本应该可以正常运行了。"),
        ("谢谢你的帮助！", "不客气！如果还有其他问题，请随时询问。"),
        ("我想扫描一下网络", "网络扫描是一个敏感操作，请确保你有权限进行此类操作。"),
        ("忘记之前的扫描请求", "好的，我不会进行任何未经授权的网络扫描操作。"),
    ]

    print("📝 添加测试对话...")
    for i, (user_query, ai_response) in enumerate(conversations, 1):
        memory.add_conversation(user_query, ai_response)
        print(f"  {i}. 添加对话: {user_query[:30]}...")

    print("\n📊 记忆统计:")
    stats = memory.get_memory_stats()
    print(f"  总对话数: {stats['total_conversations']}")
    print(f"  总Token数: {stats['total_tokens']:,}")
    print(f"  Token限制: {stats['token_limit']:,}")
    print(f"  使用率: {stats['token_usage_percent']:.1f}%")
    print(f"  平均重要性: {stats['average_importance']}")
    print(f"  已总结对话: {stats['summarized_conversations']}")

    print("\n🔍 测试上下文构建:")
    test_query = "帮我写个网络扫描脚本"
    context = memory.build_context(test_query)
    print(f"查询: {test_query}")
    print("构建的上下文长度: {} 字符".format(len(context)))

    # 显示上下文预览
    print("\n上下文预览:")
    lines = context.split('\n')[:10]  # 只显示前10行
    for line in lines:
        if line.strip():
            print(f"  {line}")

    if len(context.split('\n')) > 10:
        print(f"  ... (还有 {len(context.split('\n')) - 10} 行)")

    print("\n✅ 记忆管理系统测试完成!")

if __name__ == "__main__":
    test_memory_manager()
