"""
Skill Result Output Validator

验证技能输出是否符合标准规范。
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    """验证问题"""

    severity: str  # error, warning, info
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """验证结果"""

    valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)
    skill_name: Optional[str] = None
    category: Optional[str] = None

    def add_error(self, field: str, message: str, suggestion: Optional[str] = None):
        self.valid = False
        self.issues.append(
            ValidationIssue(
                severity="error", field=field, message=message, suggestion=suggestion
            )
        )

    def add_warning(self, field: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(
            ValidationIssue(
                severity="warning", field=field, message=message, suggestion=suggestion
            )
        )

    def add_info(self, field: str, message: str):
        self.issues.append(
            ValidationIssue(severity="info", field=field, message=message)
        )

    def get_errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    def get_warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]


class SkillOutputValidator:
    """
    技能输出验证器

    验证 SkillResult 是否符合输出标准：
    1. 必需字段检查
    2. Schema 一致性检查
    3. 数据完整性检查
    4. 命名规范检查
    """

    # 所有技能必需的字段
    REQUIRED_BASE_FIELDS = [
        "skill_name",
        "success",
        "timestamp",
    ]

    # 推荐的字段
    RECOMMENDED_FIELDS = [
        "message",
        "execution_id",
    ]

    # 按技能类别的必需字段
    CATEGORY_REQUIRED_FIELDS = {
        "simulation": [
            "converged",
            "model_info",
            "summary",
        ],
        "security": [
            "total_cases",
            "pass_rate",
        ],
        "stability": [
            "stable",
            "stability_margin",
        ],
        "analysis": [
            "summary",
        ],
        "processing": [
            "processed_items",
        ],
        "model_management": [
            "model",
        ],
    }

    # 推荐的命名模式
    NAMING_PATTERNS = {
        "snake_case": r"^[a-z][a-z0-9_]*$",
        "camelCase": r"^[a-z][a-zA-Z0-9]*$",
    }

    def __init__(self):
        self.field_patterns: Dict[str, Set[str]] = {}  # skill_name -> fields
        self.schema_registry: Dict[str, Dict[str, type]] = {}  # skill_name -> schema

    def validate(
        self,
        skill_name: str,
        data: Dict[str, Any],
        category: Optional[str] = None,
        status: str = "SUCCESS",
    ) -> ValidationResult:
        """
        验证技能输出数据

        Args:
            skill_name: 技能名称
            data: SkillResult.data
            category: 技能类别 (simulation, security, stability, analysis, processing, model_management)
            status: 执行状态 (SUCCESS, FAILED, RUNNING)

        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult(skill_name=skill_name, category=category)

        # 1. 基础字段检查（不包括 skill_name，因为它在 SkillResult 层级）
        self._validate_success_field(result, data)

        # 2. 必需字段检查（按类别）
        if category and status == "SUCCESS":
            self._validate_category_fields(result, data, category)

        # 3. 命名规范检查
        self._validate_naming(result, data)

        # 4. 数据完整性检查
        self._validate_completeness(result, data, status)

        # 5. 检查 mock/假数据
        self._validate_no_fake_data(result, data)

        return result

    def _validate_success_field(self, result: ValidationResult, data: Dict[str, Any]):
        """验证 success 字段"""
        if "success" in data:
            if not isinstance(data["success"], bool):
                result.add_error(
                    field="success",
                    message=f"success 字段必须是布尔类型，实际为: {type(data['success']).__name__}",
                    suggestion="将 success 设置为 True 或 False",
                )

    def _validate_category_fields(
        self, result: ValidationResult, data: Dict[str, Any], category: str
    ):
        """验证类别特定字段"""
        required = self.CATEGORY_REQUIRED_FIELDS.get(category, [])
        for field in required:
            if field not in data:
                result.add_error(
                    field=field,
                    message=f"类别 '{category}' 缺少必需字段: {field}",
                    suggestion=f"在 data 中添加 '{field}' 字段",
                )

    def _validate_naming(self, result: ValidationResult, data: Dict[str, Any]):
        """验证命名规范"""
        import re

        for key in data.keys():
            # 跳过已知合法的复合字段名
            if key in ["execution_id", "timestamp", "skill_name"]:
                continue

            # 检查 snake_case
            if not re.match(self.NAMING_PATTERNS["snake_case"], key):
                # 可能是 camelCase 或其他格式
                if re.match(self.NAMING_PATTERNS["camelCase"], key):
                    result.add_warning(
                        field=key,
                        message=f"字段名 '{key}' 使用了 camelCase，建议使用 snake_case",
                        suggestion=f"将 '{key}' 重命名为 '{self._camel_to_snake(key)}'",
                    )
                elif "_" in key and not re.match(
                    self.NAMING_PATTERNS["snake_case"], key
                ):
                    result.add_warning(
                        field=key,
                        message=f"字段名 '{key}' 命名不规范",
                        suggestion="使用小写字母、数字和下划线，如 'bus_count'",
                    )

    def _validate_completeness(
        self, result: ValidationResult, data: Dict[str, Any], status: str
    ):
        """验证数据完整性"""
        # SUCCESS 状态不应返回空 data
        if status == "SUCCESS" and not data:
            result.add_warning(
                field="data",
                message="SUCCESS 状态下 data 为空，可能缺少有效的计算结果",
                suggestion="确保所有有效数据都被添加到 data 中",
            )

        # 检查是否有未实现的占位符
        placeholder_keys = ["todo", "todo_", "_todo", "not_implemented", "placeholder"]
        for key in data.keys():
            if key.lower() in placeholder_keys:
                result.add_error(
                    field=key,
                    message=f"字段 '{key}' 是占位符，表示功能未实现",
                    suggestion="实现该功能或删除该字段",
                )

    def _validate_no_fake_data(self, result: ValidationResult, data: Dict[str, Any]):
        """检查是否有假数据"""
        import re

        # 检查明显硬编码的值模式
        fake_patterns = [
            (r"Bus_\d+", "sensitivity"),  # Bus_1, Bus_2... 配合 sensitivity
            (r"0\.01\s*\*\s*\d+", None),  # 0.01 * i 模式
            (r"\[.*for.*in.*range", None),  # 列表推导式作为返回值
        ]

        # 检查是否有假数据
        for key, value in data.items():
            if isinstance(value, list):
                for item in value[:3] if len(value) > 3 else value:  # 只检查前3个
                    if isinstance(item, dict):
                        # 检查 bus 字段
                        if "bus" in item:
                            bus = str(item.get("bus", ""))
                            if re.match(r"Bus_\d+", bus):
                                result.add_error(
                                    field=key,
                                    message=f"发现疑似硬编码的 bus 名称: {bus}",
                                    suggestion="确保 bus 名称来自真实计算",
                                )

            # 检查字符串值
            if isinstance(value, str):
                if value in ["TODO", "FIXME", "placeholder", "N/A"]:
                    result.add_info(
                        field=key, message=f"字段 '{key}' 包含占位符值: {value}"
                    )

    def _camel_to_snake(self, name: str) -> str:
        """camelCase 转 snake_case"""
        import re

        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def register_schema(self, skill_name: str, schema: Dict[str, type]):
        """注册技能 schema"""
        self.schema_registry[skill_name] = schema
        self.field_patterns[skill_name] = set(schema.keys())

    def compare_with_previous(
        self, skill_name: str, current_data: Dict[str, Any]
    ) -> ValidationResult:
        """与之前注册的 schema 比较"""
        result = ValidationResult(skill_name=skill_name)

        if skill_name not in self.schema_registry:
            result.add_info(
                field="schema", message=f"技能 '{skill_name}' 未注册 schema"
            )
            return result

        expected_fields = self.field_patterns[skill_name]
        actual_fields = set(current_data.keys())

        # 检查缺失的字段
        missing = expected_fields - actual_fields
        if missing:
            result.add_warning(
                field="schema",
                message=f"缺少字段: {', '.join(missing)}",
                suggestion="添加缺失的字段以保持一致性",
            )

        # 检查新增的字段
        new_fields = actual_fields - expected_fields
        if new_fields:
            result.add_info(
                field="schema", message=f"发现新字段: {', '.join(new_fields)}"
            )

        return result


def validate_skill_output(
    skill_name: str,
    data: Dict[str, Any],
    category: Optional[str] = None,
    status: str = "SUCCESS",
) -> ValidationResult:
    """
    便捷函数：验证技能输出

    Example:
        result = validate_skill_output(
            skill_name="power_flow",
            data={"success": True, "converged": True},
            category="simulation",
            status="SUCCESS"
        )
        if not result.valid:
            for issue in result.get_errors():
                print(f"Error: {issue.message}")
    """
    validator = SkillOutputValidator()
    return validator.validate(skill_name, data, category, status)
