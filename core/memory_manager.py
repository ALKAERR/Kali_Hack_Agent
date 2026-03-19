"""智能记忆管理系统，避免上下文超出token限制。"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import tiktoken


@dataclass
class ConversationEntry:
    """对话条目数据类"""
    user_query: str
    ai_response: Optional[str]
    timestamp: datetime
    importance_score: float = 1.0  # 重要性评分 (0-1)
    token_count: int = 0  # 总token数
    summary: Optional[str] = None  # 总结内容
    is_summarized: bool = False  # 是否已被总结


class MemoryManager:
    """
    智能记忆管理系统

    支持多种记忆管理策略：
    1. 滑动窗口：保留最近的对话
    2. 重要性评估：保留重要的对话
    3. 总结机制：对旧对话进行总结
    4. Token计数：精确控制上下文长度
    """

    def __init__(self, model_name: str = "gpt-4", max_tokens: int = None):
        """
        初始化记忆管理器

        Args:
            model_name: 模型名称，用于token编码
            max_tokens: 最大上下文token数，默认根据模型自动设置
        """
        self.model_name = model_name
        self.max_tokens = max_tokens or self._get_default_max_tokens(model_name)
        self.conversation_history: List[ConversationEntry] = []
        self.token_encoder = self._get_token_encoder(model_name)

        # 保留给系统提示和当前查询的token数
        self.reserved_tokens = 1000

        # 总结相关配置
        self.summary_threshold_days = 7  # 7天前的对话会被考虑总结
        self.min_conversations_before_summary = 5  # 最少保留5个对话再开始总结

    def _get_default_max_tokens(self, model_name: str) -> int:
        """根据模型名称获取默认的最大token数"""
        model_limits = {
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-turbo": 128000,
            "gpt-4-turbo-preview": 128000,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384,
            "claude-3-opus": 200000,
            "claude-3-sonnet": 200000,
            "claude-3-haiku": 200000,
        }
        return model_limits.get(model_name, 4096)  # 默认4K tokens

    def _get_token_encoder(self, model_name: str):
        """获取token编码器"""
        try:
            # 尝试使用tiktoken
            if "gpt" in model_name.lower():
                return tiktoken.encoding_for_model(model_name)
            else:
                # 对于其他模型，使用cl100k_base编码（GPT-4的编码）
                return tiktoken.get_encoding("cl100k_base")
        except Exception:
            # 如果tiktoken不可用，使用简单的字符估算
            return None

    def _count_tokens(self, text: str) -> int:
        """计算文本的token数量"""
        if self.token_encoder:
            try:
                return len(self.token_encoder.encode(text))
            except Exception:
                pass

        # 简单估算：1个中文字符≈1.5个token，英文单词≈1.3个token
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'\b\w+\b', re.sub(r'[\u4e00-\u9fff]', '', text)))
        return int(chinese_chars * 1.5 + english_words * 1.3)

    def add_conversation(self, user_query: str, ai_response: Optional[str] = None):
        """
        添加新的对话到记忆中

        Args:
            user_query: 用户查询
            ai_response: AI响应
        """
        # 计算token数
        query_tokens = self._count_tokens(user_query)
        response_tokens = self._count_tokens(ai_response) if ai_response else 0
        total_tokens = query_tokens + response_tokens

        # 计算重要性评分
        importance_score = self._calculate_importance(user_query, ai_response)

        # 创建对话条目
        entry = ConversationEntry(
            user_query=user_query,
            ai_response=ai_response,
            timestamp=datetime.now(),
            importance_score=importance_score,
            token_count=total_tokens
        )

        self.conversation_history.append(entry)

        # 执行记忆管理，控制上下文长度
        self._manage_memory()

    def _calculate_importance(self, user_query: str, ai_response: Optional[str]) -> float:
        """
        计算对话的重要性评分

        评分标准：
        - 包含代码执行的任务：高重要性 (0.9)
        - 包含错误或异常：高重要性 (0.8)
        - 包含工具调用的响应：高重要性 (0.8)
        - 一般对话：中等重要性 (0.6)
        - 简单问候或确认：低重要性 (0.3)
        """
        # 检查用户查询的重要性
        query_lower = user_query.lower()
        if any(keyword in query_lower for keyword in [
            'python', '代码', '执行', '运行', '脚本', 'program', 'code', 'execute', 'run'
        ]):
            return 0.9

        if any(keyword in query_lower for keyword in [
            '错误', '失败', '问题', 'bug', 'error', 'fail', 'problem'
        ]):
            return 0.8

        # 检查AI响应的内容
        if ai_response:
            response_lower = ai_response.lower()
            if any(keyword in response_lower for keyword in [
                '执行完成', '成功', '结果', 'output', 'completed', 'success', 'result'
            ]):
                return 0.8

            if any(keyword in response_lower for keyword in [
                '错误', '失败', '异常', 'error', 'fail', 'exception'
            ]):
                return 0.8

        # 一般对话
        if len(user_query) > 50:  # 较长的查询可能更重要
            return 0.6

        return 0.4  # 默认重要性

    def _manage_memory(self):
        """执行记忆管理，控制上下文长度"""
        # 计算当前总token数
        total_tokens = sum(entry.token_count for entry in self.conversation_history)

        # 如果没有超出限制，不需要管理
        if total_tokens <= self.max_tokens - self.reserved_tokens:
            return

        # 执行多种记忆管理策略
        self._apply_memory_strategies()

    def _apply_memory_strategies(self):
        """应用多种记忆管理策略"""
        # 策略1: 删除低重要性的旧对话
        self._remove_low_importance_entries()

        # 策略2: 对旧对话进行总结
        self._summarize_old_conversations()

        # 策略3: 如果仍然超出限制，使用滑动窗口
        self._apply_sliding_window()

    def _remove_low_importance_entries(self):
        """删除低重要性（<0.5）的对话条目"""
        # 只删除超过7天的低重要性对话
        cutoff_date = datetime.now() - timedelta(days=self.summary_threshold_days)

        self.conversation_history = [
            entry for entry in self.conversation_history
            if not (entry.importance_score < 0.5 and entry.timestamp < cutoff_date)
        ]

    def _summarize_old_conversations(self):
        """对旧对话进行总结"""
        if len(self.conversation_history) < self.min_conversations_before_summary:
            return

        # 找出超过7天的对话进行总结
        cutoff_date = datetime.now() - timedelta(days=self.summary_threshold_days)
        old_entries = [entry for entry in self.conversation_history if entry.timestamp < cutoff_date]

        if len(old_entries) >= 3:  # 至少3个旧对话才进行总结
            summary_text = self._generate_conversation_summary(old_entries)

            # 创建总结条目
            summary_entry = ConversationEntry(
                user_query="[历史对话总结]",
                ai_response=summary_text,
                timestamp=min(entry.timestamp for entry in old_entries),
                importance_score=0.7,  # 总结有中等重要性
                token_count=self._count_tokens(summary_text),
                summary=summary_text,
                is_summarized=True
            )

            # 替换旧条目为总结
            self.conversation_history = [
                entry for entry in self.conversation_history
                if entry.timestamp >= cutoff_date
            ]
            self.conversation_history.insert(0, summary_entry)

    def _generate_conversation_summary(self, entries: List[ConversationEntry]) -> str:
        """生成对话总结"""
        if not entries:
            return "无历史对话"

        # 提取关键信息
        code_executions = []
        errors = []
        topics = []

        for entry in entries:
            if entry.ai_response:
                response_lower = entry.ai_response.lower()
                query_lower = entry.user_query.lower()

                # 记录代码执行
                if '执行完成' in response_lower or 'success' in response_lower:
                    code_executions.append(entry.user_query[:50] + "...")

                # 记录错误
                if '错误' in response_lower or 'error' in response_lower:
                    errors.append(entry.user_query[:50] + "...")

                # 记录话题
                if '代码' in query_lower or 'code' in query_lower:
                    topics.append("代码执行")
                elif '扫描' in query_lower or 'scan' in query_lower:
                    topics.append("安全扫描")
                elif '渗透' in query_lower or 'exploit' in query_lower:
                    topics.append("渗透测试")

        # 生成总结文本
        summary_parts = []

        if topics:
            unique_topics = list(set(topics))
            summary_parts.append(f"讨论了以下主题：{', '.join(unique_topics)}")

        if code_executions:
            summary_parts.append(f"成功执行了{len(code_executions)}个代码任务")

        if errors:
            summary_parts.append(f"遇到了{len(errors)}个问题或错误")

        if not summary_parts:
            summary_parts.append(f"进行了{len(entries)}次对话交互")

        period = f"{min(entry.timestamp for entry in entries).strftime('%Y-%m-%d')}至{max(entry.timestamp for entry in entries).strftime('%Y-%m-%d')}"

        return f"📋 历史对话总结 ({period})：{'；'.join(summary_parts)}"

    def _apply_sliding_window(self):
        """应用滑动窗口策略，保留最近的对话"""
        total_tokens = sum(entry.token_count for entry in self.conversation_history)

        # 如果仍然超出限制，从最旧的开始删除
        while (total_tokens > self.max_tokens - self.reserved_tokens and
               len(self.conversation_history) > 3):  # 至少保留3个对话

            # 优先删除低重要性的条目
            low_importance_entries = [entry for entry in self.conversation_history if entry.importance_score < 0.6]
            if low_importance_entries:
                # 删除最旧的低重要性条目
                oldest_low_importance = min(low_importance_entries, key=lambda x: x.timestamp)
                self.conversation_history.remove(oldest_low_importance)
            else:
                # 如果没有低重要性条目，删除最旧的条目
                oldest_entry = min(self.conversation_history, key=lambda x: x.timestamp)
                self.conversation_history.remove(oldest_entry)

            total_tokens = sum(entry.token_count for entry in self.conversation_history)

    def build_context(self, current_query: str, max_history_items: int = None) -> str:
        """
        构建上下文字符串，用于发送给LLM

        Args:
            current_query: 当前用户查询
            max_history_items: 最大历史条目数，默认自动计算

        Returns:
            完整的上下文字符串
        """
        if not self.conversation_history:
            return current_query

        # 选择要包含的历史条目
        selected_entries = self._select_relevant_history(current_query, max_history_items)

        if not selected_entries:
            return current_query

        # 构建历史上下文
        history_parts = []

        for i, entry in enumerate(selected_entries, 1):
            if entry.is_summarized and entry.summary:
                # 总结条目
                history_parts.append(f"[历史总结 {i}]\n{entry.summary}")
            else:
                # 普通对话条目
                history_parts.append(f"[对话 {i}]\n用户: {entry.user_query}")
                if entry.ai_response:
                    # 控制响应长度
                    response = entry.ai_response
                    if len(response) > 800:  # 放宽字符限制，因为我们控制token
                        response = response[:800] + "...(已截断)"
                    history_parts.append(f"助手: {response}")

        history_text = "\n\n📋 对话历史上下文：\n" + "\n\n".join(history_parts)
        history_text += f"\n\n[当前查询]\n用户: {current_query}"

        return history_text

    def _select_relevant_history(self, current_query: str, max_items: int = None) -> List[ConversationEntry]:
        """选择相关历史条目"""
        if not max_items:
            # 根据可用token空间自动计算最大条目数
            available_tokens = self.max_tokens - self.reserved_tokens - self._count_tokens(current_query)
            # 估算每个条目平均使用150个token
            max_items = max(3, available_tokens // 150)

        # 按时间倒序排序（最新的在前）
        sorted_entries = sorted(self.conversation_history, key=lambda x: x.timestamp, reverse=True)

        # 选择相关性最高的条目
        selected = []
        total_tokens = 0

        for entry in sorted_entries:
            # 计算相关性评分
            relevance_score = self._calculate_relevance(entry, current_query)

            # 如果相关性足够高，或者是最近的条目，加入选择
            if (relevance_score > 0.6 or len(selected) < 3 or
                entry.timestamp > datetime.now() - timedelta(hours=1)):

                if total_tokens + entry.token_count <= self.max_tokens * 0.8:  # 留80%的空间
                    selected.append(entry)
                    total_tokens += entry.token_count

                    if len(selected) >= max_items:
                        break

        # 按时间正序返回（最早的在前）
        return sorted(selected, key=lambda x: x.timestamp)

    def _calculate_relevance(self, entry: ConversationEntry, current_query: str) -> float:
        """计算历史条目与当前查询的相关性"""
        current_lower = current_query.lower()
        query_lower = entry.user_query.lower()

        # 关键词匹配
        current_words = set(re.findall(r'\b\w+\b', current_lower))
        query_words = set(re.findall(r'\b\w+\b', query_lower))

        if not current_words or not query_words:
            return 0.5  # 默认相关性

        # 计算Jaccard相似度
        intersection = current_words.intersection(query_words)
        union = current_words.union(query_words)

        jaccard_similarity = len(intersection) / len(union) if union else 0

        # 时间衰减因子（越新的相关性越高）
        time_diff_hours = (datetime.now() - entry.timestamp).total_seconds() / 3600
        time_decay = max(0.3, 1.0 - (time_diff_hours / 24))  # 24小时内线性衰减

        # 重要性加成
        importance_boost = entry.importance_score

        return (jaccard_similarity * 0.6 + time_decay * 0.3 + importance_boost * 0.1)

    def clear_memory(self):
        """清空所有记忆"""
        self.conversation_history = []

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        total_conversations = len(self.conversation_history)
        total_tokens = sum(entry.token_count for entry in self.conversation_history)
        summarized_count = sum(1 for entry in self.conversation_history if entry.is_summarized)

        avg_importance = (sum(entry.importance_score for entry in self.conversation_history) /
                         total_conversations) if total_conversations > 0 else 0

        oldest_date = min((entry.timestamp for entry in self.conversation_history), default=None)
        newest_date = max((entry.timestamp for entry in self.conversation_history), default=None)

        return {
            "total_conversations": total_conversations,
            "total_tokens": total_tokens,
            "token_limit": self.max_tokens,
            "token_usage_percent": (total_tokens / self.max_tokens * 100) if self.max_tokens > 0 else 0,
            "summarized_conversations": summarized_count,
            "average_importance": round(avg_importance, 2),
            "date_range": {
                "oldest": oldest_date.isoformat() if oldest_date else None,
                "newest": newest_date.isoformat() if newest_date else None
            }
        }

    def optimize_for_model(self, model_name: str):
        """为特定模型优化记忆设置"""
        self.model_name = model_name
        self.max_tokens = self._get_default_max_tokens(model_name)
        self.token_encoder = self._get_token_encoder(model_name)

        # 重新评估当前记忆是否需要优化
        self._manage_memory()
