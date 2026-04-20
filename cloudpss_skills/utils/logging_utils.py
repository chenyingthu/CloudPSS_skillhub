"""
日志工具函数模块

提供统一的日志记录工具函数
"""

import logging
from typing import Callable


def create_log_func(logger: logging.Logger) -> Callable[[str, str], None]:
    """
    创建标准日志函数

    Args:
        logger: 日志记录器实例

    Returns:
        日志函数，接受level和message参数

    Example:
        log = create_log_func(logger)
        log('info', '开始执行任务')
        log('debug', '详细调试信息')
    """
    def log(level: str, message: str) -> None:
        getattr(logger, level)(message)
    return log


def log_debug(logger: logging.Logger, message: str) -> None:
    """记录DEBUG级别日志"""
    logger.debug(message)


def log_info(logger: logging.Logger, message: str) -> None:
    """记录INFO级别日志"""
    logger.info(message)


def log_warning(logger: logging.Logger, message: str) -> None:
    """记录WARNING级别日志"""
    logger.warning(message)


def log_error(logger: logging.Logger, message: str) -> None:
    """记录ERROR级别日志"""
    logger.error(message)
