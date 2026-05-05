"""
错误诊断 (Error Diagnosis)

提供错误诊断、自动重试和恢复建议功能。
"""

import logging
from typing import Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(str, Enum):
    """错误类型枚举"""
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication"
    MODEL_NOT_FOUND = "model_not_found"
    INVALID_PARAMETERS = "invalid_parameters"
    CALCULATION_FAILED = "calculation_failed"
    SERVER_ERROR = "server_error"
    UNKNOWN = "unknown"


@dataclass
class DiagnosisResult:
    """诊断结果"""
    error_type: ErrorType
    is_recoverable: bool
    can_retry: bool
    message: str
    suggestions: list[str]
    retry_count: int = 0
    max_retries: int = 3


class ErrorDiagnoser:
    """错误诊断器"""

    # 错误模式映射
    ERROR_PATTERNS = {
        "timeout": (ErrorType.TIMEOUT, True),
        "timed out": (ErrorType.TIMEOUT, True),
        "connection": (ErrorType.NETWORK_ERROR, True),
        "network": (ErrorType.NETWORK_ERROR, True),
        "unauthorized": (ErrorType.AUTHENTICATION, False),
        "auth": (ErrorType.AUTHENTICATION, False),
        "token": (ErrorType.AUTHENTICATION, False),
        "model not found": (ErrorType.MODEL_NOT_FOUND, False),
        "no such model": (ErrorType.MODEL_NOT_FOUND, False),
        "invalid parameter": (ErrorType.INVALID_PARAMETERS, False),
        "parameter error": (ErrorType.INVALID_PARAMETERS, False),
        "calculation failed": (ErrorType.CALCULATION_FAILED, False),
        "diverged": (ErrorType.CALCULATION_FAILED, True),
        "not converge": (ErrorType.CALCULATION_FAILED, True),
        "server error": (ErrorType.SERVER_ERROR, True),
        "internal error": (ErrorType.SERVER_ERROR, True),
    }

    # 恢复建议
    RECOVERY_SUGGESTIONS = {
        ErrorType.TIMEOUT: [
            "增加超时时间设置（timeout 参数）",
            "检查网络连接状态",
            "稍后重试"
        ],
        ErrorType.NETWORK_ERROR: [
            "检查网络连接",
            "确认 CloudPSS 服务可用",
            "稍后重试"
        ],
        ErrorType.AUTHENTICATION: [
            "检查 API Token 是否有效",
            "重新配置 Token 文件",
            "确认账号权限"
        ],
        ErrorType.MODEL_NOT_FOUND: [
            "检查模型 RID 是否正确",
            "使用 model_search 查找可用模型",
            "确认模型访问权限"
        ],
        ErrorType.INVALID_PARAMETERS: [
            "检查参数格式",
            "使用 model_analysis 获取参数建议",
            "参考文档示例"
        ],
        ErrorType.CALCULATION_FAILED: [
            "检查系统参数是否合理",
            "尝试调整初始值",
            "简化模型或分步计算"
        ],
        ErrorType.SERVER_ERROR: [
            "服务器内部错误，请稍后重试",
            "如果问题持续，请联系技术支持"
        ],
        ErrorType.UNKNOWN: [
            "未知错误，请检查日志",
            "稍后重试",
            "联系技术支持"
        ]
    }

    @classmethod
    def diagnose(cls, error: Exception, context: Optional[dict] = None) -> DiagnosisResult:
        """诊断错误

        Args:
            error: 异常对象
            context: 上下文信息（可选）

        Returns:
            DiagnosisResult: 诊断结果
        """
        error_msg = str(error).lower()
        error_type = ErrorType.UNKNOWN
        is_recoverable = False

        # 匹配错误模式
        for pattern, (etype, recoverable) in cls.ERROR_PATTERNS.items():
            if pattern in error_msg:
                error_type = etype
                is_recoverable = recoverable
                break

        # 获取恢复建议
        suggestions = cls.RECOVERY_SUGGESTIONS.get(error_type, [])

        # 根据上下文添加额外建议
        if context:
            suggestions = cls._add_context_suggestions(suggestions, context, error_type)

        # 是否可以重试
        can_retry = is_recoverable and error_type in [
            ErrorType.TIMEOUT,
            ErrorType.NETWORK_ERROR,
            ErrorType.CALCULATION_FAILED,
            ErrorType.SERVER_ERROR
        ]

        logger.info(f"错误诊断: {error_type.value}, 可恢复: {is_recoverable}, 可重试: {can_retry}")

        return DiagnosisResult(
            error_type=error_type,
            is_recoverable=is_recoverable,
            can_retry=can_retry,
            message=cls._get_error_message(error_type, str(error)),
            suggestions=suggestions
        )

    @classmethod
    def _add_context_suggestions(cls, suggestions: list[str], context: dict,
                                  error_type: ErrorType) -> list[str]:
        """根据上下文添加额外建议"""
        result = suggestions.copy()

        # 根据任务类型添加建议
        task_type = context.get("task_type")
        if task_type == "powerflow" and error_type == ErrorType.CALCULATION_FAILED:
            result.append("尝试使用平坦启动（flat start）")
            result.append("检查PV节点设置是否正确")

        if task_type == "emt" and error_type == ErrorType.CALCULATION_FAILED:
            result.append("减小仿真步长")
            result.append("检查故障设置是否合理")

        # 根据系统规模添加建议
        if context.get("bus_count", 0) > 100:
            result.append("大规模系统建议使用简化模型")

        return result

    @classmethod
    def _get_error_message(cls, error_type: ErrorType, original_msg: str) -> str:
        """获取错误消息"""
        messages = {
            ErrorType.TIMEOUT: "请求超时",
            ErrorType.NETWORK_ERROR: "网络连接错误",
            ErrorType.AUTHENTICATION: "认证失败",
            ErrorType.MODEL_NOT_FOUND: "模型未找到",
            ErrorType.INVALID_PARAMETERS: "参数无效",
            ErrorType.CALCULATION_FAILED: "计算失败",
            ErrorType.SERVER_ERROR: "服务器错误",
            ErrorType.UNKNOWN: f"未知错误: {original_msg}"
        }
        return messages.get(error_type, original_msg)


class RetryHandler:
    """重试处理器"""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_counts: dict[str, int] = {}

    def should_retry(self, task_id: str, diagnosis: DiagnosisResult) -> bool:
        """判断是否应该重试"""
        if not diagnosis.can_retry:
            return False

        current_count = self.retry_counts.get(task_id, 0)
        return current_count < self.max_retries

    def record_attempt(self, task_id: str):
        """记录重试尝试"""
        self.retry_counts[task_id] = self.retry_counts.get(task_id, 0) + 1
        logger.info(f"任务 {task_id} 重试次数: {self.retry_counts[task_id]}")

    def get_retry_count(self, task_id: str) -> int:
        """获取重试次数"""
        return self.retry_counts.get(task_id, 0)

    def reset(self, task_id: str):
        """重置重试计数"""
        if task_id in self.retry_counts:
            del self.retry_counts[task_id]


# 全局实例
diagnoser = ErrorDiagnoser()
retry_handler = RetryHandler()


def diagnose_error(error: Exception, context: Optional[dict] = None) -> DiagnosisResult:
    """诊断错误的便捷函数"""
    return diagnoser.diagnose(error, context)


def should_retry_task(task_id: str, diagnosis: DiagnosisResult) -> bool:
    """判断是否应该重试任务"""
    return retry_handler.should_retry(task_id, diagnosis)


def format_diagnosis(diagnosis: DiagnosisResult) -> str:
    """格式化诊断结果为文本"""
    lines = [
        f"**错误类型**: {diagnosis.error_type.value}",
        f"**错误信息**: {diagnosis.message}",
        "",
        "**恢复建议**:",
    ]

    for i, suggestion in enumerate(diagnosis.suggestions, 1):
        lines.append(f"{i}. {suggestion}")

    if diagnosis.can_retry:
        lines.append("")
        lines.append(f"💡 此错误可自动重试（{diagnosis.retry_count}/{diagnosis.max_retries}）")

    return "\n".join(lines)
