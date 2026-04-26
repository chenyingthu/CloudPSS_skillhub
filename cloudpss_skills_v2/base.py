"""
Base Classes - 技能基类定义

提供统一的技能接口：
- ToolBase: 工具类技能基类
- AnalysisBase: 分析类技能基类

所有技能必须继承自相应的基类，确保接口一致性。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime

from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus, LogEntry, Artifact


class SkillBase(ABC):
    """技能基类
    
    所有技能的抽象基类，定义统一接口。
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """技能名称（唯一标识）"""
        pass
    
    @property
    def description(self) -> str:
        """技能描述"""
        return ""
    
    @property
    def version(self) -> str:
        """技能版本"""
        return "2.0.0"
    
    @property
    def category(self) -> str:
        """技能类别"""
        return "unknown"
    
    @abstractmethod
    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """验证配置
        
        Args:
            config: 配置字典
            
        Returns:
            (是否有效, 错误列表)
        """
        pass
    
    @abstractmethod
    def run(self, config: dict[str, Any]) -> SkillResult:
        """执行技能
        
        Args:
            config: 配置字典
            
        Returns:
            SkillResult 结果对象
        """
        pass
    
    def get_default_config(self) -> dict[str, Any] | None:
        """获取默认配置
        
        Returns:
            默认配置字典，如果没有返回 None
        """
        return None
    
    def get_config_schema(self) -> dict[str, Any] | None:
        """获取配置Schema (JSON Schema格式)
        
        Returns:
            JSON Schema 字典，如果没有返回 None
        """
        return None

    @property
    def config_schema(self) -> dict[str, Any]:
        """配置JSON Schema.

        This property keeps the runtime interface aligned with the design docs
        while preserving the existing get_config_schema() extension point.
        """
        return self.get_config_schema() or {}


class ToolBase(SkillBase):
    """工具类技能基类
    
    工具类技能继承此类，提供数据处理、导出、转换等功能。
    
    示例：
        class HDF5ExportTool(ToolBase):
            name = "hdf5_export"
            
            def validate(self, config):
                errors = []
                if not config.get("source"):
                    errors.append("缺少 source 配置")
                return len(errors) == 0, errors
            
            def run(self, config):
                # 实现导出逻辑
                return SkillResult.success(self.name, {...})
    """
    
    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []
    
    @property
    def category(self) -> str:
        return "tool"
    
    def _log(self, level: str, message: str, context: dict[str, Any] | None = None):
        """添加日志
        
        Args:
            level: 日志级别 (debug/info/warning/error)
            message: 日志消息
            context: 上下文信息
        """
        self.logs.append(LogEntry(
            timestamp=datetime.now(),
            level=level,
            message=message,
            context=context
        ))
    
    def _add_artifact(
        self,
        name: str,
        path: str,
        type_: str,
        size_bytes: int | None = None,
        description: str | None = None
    ):
        """添加产物
        
        Args:
            name: 产物名称
            path: 文件路径
            type_: 产物类型
            size_bytes: 文件大小
            description: 描述
        """
        self.artifacts.append(Artifact(
            name=name,
            path=path,
            type=type_,
            size_bytes=size_bytes,
            description=description
        ))
    
    def _success_result(
        self,
        data: dict[str, Any],
        metrics: dict[str, Any] | None = None
    ) -> SkillResult:
        """创建成功结果
        
        Args:
            data: 结果数据
            metrics: 指标数据
            
        Returns:
            SkillResult 成功结果
        """
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data=data,
            logs=self.logs,
            artifacts=self.artifacts,
            metrics=metrics or {}
        )
    
    def _failure_result(
        self,
        error: str,
        stage: str | None = None
    ) -> SkillResult:
        """创建失败结果
        
        Args:
            error: 错误信息
            stage: 失败阶段
            
        Returns:
            SkillResult 失败结果
        """
        data = {"stage": stage} if stage else {}
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            data=data,
            logs=self.logs,
            artifacts=self.artifacts,
            error=error
        )


class AnalysisBase(SkillBase):
    """分析类技能基类
    
    分析类技能继承此类，提供电力系统分析功能。
    
    示例：
        class N1SecurityAnalysis(AnalysisBase):
            name = "n1_security"
            
            def validate(self, config):
                errors = []
                if not config.get("model", {}).get("rid"):
                    errors.append("缺少 model.rid")
                return len(errors) == 0, errors
            
            def run(self, config):
                # 实现分析逻辑
                return SkillResult.success(self.name, {...})
    """
    
    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []
    
    @property
    def category(self) -> str:
        return "poweranalysis"
    
    def _log(self, level: str, message: str, context: dict[str, Any] | None = None):
        """添加日志"""
        self.logs.append(LogEntry(
            timestamp=datetime.now(),
            level=level,
            message=message,
            context=context
        ))
    
    def _add_artifact(
        self,
        name: str,
        path: str,
        type_: str,
        size_bytes: int | None = None,
        description: str | None = None
    ):
        """添加产物"""
        self.artifacts.append(Artifact(
            name=name,
            path=path,
            type=type_,
            size_bytes=size_bytes,
            description=description
        ))
    
    def _success_result(
        self,
        data: dict[str, Any],
        metrics: dict[str, Any] | None = None
    ) -> SkillResult:
        """创建成功结果"""
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data=data,
            logs=self.logs,
            artifacts=self.artifacts,
            metrics=metrics or {}
        )
    
    def _failure_result(
        self,
        error: str,
        stage: str | None = None
    ) -> SkillResult:
        """创建失败结果"""
        data = {"stage": stage} if stage else {}
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            data=data,
            logs=self.logs,
            artifacts=self.artifacts,
            error=error
        )


__all__ = [
    "SkillBase",
    "ToolBase",
    "AnalysisBase",
]
