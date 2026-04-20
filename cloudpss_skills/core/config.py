"""
CloudPSS Skill System - Configuration Module

配置加载、验证和模板生成。
"""

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import jsonschema
import logging

from .base import ValidationResult

logger = logging.getLogger(__name__)


class ConfigLoader:
    """配置加载器"""

    # 配置搜索路径（按优先级排序）
    SEARCH_PATHS = [
        "{cwd}/skill.yaml",
        "{cwd}/.cloudpss/skill.yaml",
        "{home}/.cloudpss/skill.yaml",
    ]

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        加载配置

        加载顺序（优先级从高到低）：
        1. 指定的配置文件路径
        2. 环境变量 CLOUDPSS_SKILL_CONFIG
        3. 当前目录 skill.yaml
        4. 当前目录 .cloudpss/skill.yaml
        5. 用户目录 ~/.cloudpss/skill.yaml

        Args:
            config_path: 指定的配置文件路径

        Returns:
            配置字典

        Raises:
            FileNotFoundError: 找不到配置文件
            yaml.YAMLError: YAML解析错误
        """
        # 1. 使用指定的路径
        if config_path:
            path = Path(config_path).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(f"配置文件不存在: {config_path}")
            return cls._load_file(path)

        # 2. 环境变量
        env_config = os.environ.get("CLOUDPSS_SKILL_CONFIG")
        if env_config:
            path = Path(env_config).expanduser().resolve()
            if path.exists():
                return cls._load_file(path)
            logger.warning(f"环境变量指向的配置文件不存在: {env_config}")

        # 3. 搜索默认路径
        search_paths = cls._get_search_paths()
        for path in search_paths:
            if path.exists():
                logger.debug(f"使用配置文件: {path}")
                return cls._load_file(path)

        raise FileNotFoundError(
            f"找不到配置文件。请创建以下文件之一:\n" +
            "\n".join(f"  - {p}" for p in search_paths)
        )

    @classmethod
    def _load_file(cls, path: Path) -> Dict[str, Any]:
        """加载并解析YAML文件"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析YAML
        config = yaml.safe_load(content)

        if not isinstance(config, dict):
            raise ValueError(f"配置文件必须是字典格式: {path}")

        # 处理环境变量替换
        config = cls._expand_env_vars(config)

        logger.info(f"已加载配置: {path}")
        return config

    @classmethod
    def _get_search_paths(cls) -> List[Path]:
        """获取配置搜索路径"""
        cwd = Path.cwd()
        home = Path.home()

        paths = []
        for template in cls.SEARCH_PATHS:
            path = template.format(cwd=cwd, home=home)
            paths.append(Path(path).expanduser().resolve())

        return paths

    @classmethod
    def _expand_env_vars(cls, obj: Any) -> Any:
        """递归展开环境变量"""
        if isinstance(obj, str):
            # 支持 ${VAR} 和 ${VAR:-default} 语法
            pattern = r'\$\{([^}]+)\}'

            def replace(match):
                var_expr = match.group(1)
                if ':-' in var_expr:
                    var_name, default = var_expr.split(':-', 1)
                    return os.environ.get(var_name, default)
                else:
                    return os.environ.get(var_expr, match.group(0))

            return re.sub(pattern, replace, obj)

        elif isinstance(obj, dict):
            return {k: cls._expand_env_vars(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return [cls._expand_env_vars(item) for item in obj]

        return obj


class ConfigValidator:
    """配置验证器"""

    @classmethod
    def validate(cls, config: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """
        使用JSON Schema验证配置

        Args:
            config: 配置字典
            schema: JSON Schema字典

        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult(valid=True)

        try:
            jsonschema.validate(instance=config, schema=schema)
        except jsonschema.ValidationError as e:
            result.add_error(f"配置验证失败: {e.message} (路径: {list(e.path)})")
        except jsonschema.SchemaError as e:
            result.add_error(f"Schema错误: {e.message}")

        return result

    @classmethod
    def validate_with_defaults(cls, config: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证配置并填充默认值

        Args:
            config: 配置字典
            schema: JSON Schema字典

        Returns:
            填充默认值后的配置
        """
        validator = jsonschema.Draft7Validator(schema)
        defaults = cls._extract_defaults(schema)

        # 合并默认值
        merged = cls._deep_merge(defaults, config)

        # 验证
        errors = list(validator.iter_errors(merged))
        if errors:
            raise ValueError(f"配置验证失败: {errors[0].message}")

        return merged

    @classmethod
    def _extract_defaults(cls, schema: Dict[str, Any]) -> Dict[str, Any]:
        """从schema中提取默认值"""
        if schema.get("type") != "object":
            return schema.get("default", {})

        defaults = {}
        props = schema.get("properties", {})
        for key, prop_schema in props.items():
            if "default" in prop_schema:
                defaults[key] = prop_schema["default"]
            elif prop_schema.get("type") == "object":
                nested = cls._extract_defaults(prop_schema)
                if nested:
                    defaults[key] = nested

        return defaults

    @classmethod
    def _deep_merge(cls, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并字典"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._deep_merge(result[key], value)
            else:
                result[key] = value

        return result


class ConfigGenerator:
    """配置生成器"""

    TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

    @classmethod
    def generate(
        cls,
        skill_name: str,
        output_path: Optional[str] = None,
        values: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成配置文件

        Args:
            skill_name: 技能名称
            output_path: 输出路径，默认为 {skill_name}.yaml
            values: 要填充的值

        Returns:
            生成的配置文件路径
        """
        # 查找模板
        template_path = cls.TEMPLATES_DIR / f"{skill_name}.yaml"
        if not template_path.exists():
            # 使用默认模板
            template_path = cls.TEMPLATES_DIR / "default.yaml"
            if not template_path.exists():
                raise FileNotFoundError(f"找不到技能 '{skill_name}' 的模板")

        # 加载模板
        with open(template_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 应用自定义值
        if values:
            config = cls._apply_values(config, values)

        # 确定输出路径
        if output_path:
            out_path = Path(output_path).expanduser().resolve()
        else:
            out_path = Path(f"{skill_name}.yaml")

        # 确保目录存在
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        with open(out_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return str(out_path)

    @classmethod
    def _apply_values(cls, config: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        """应用自定义值到配置"""
        result = config.copy()

        for key_path, value in values.items():
            keys = key_path.split(".")
            target = result

            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]

            target[keys[-1]] = value

        return result


class InteractiveConfigBuilder:
    """交互式配置构建器"""

    @classmethod
    def build(
        cls,
        skill_name: str,
        defaults: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        交互式构建配置

        Args:
            skill_name: 技能名称
            defaults: 默认值

        Returns:
            配置字典
        """
        print(f"\n为技能 '{skill_name}' 创建配置")
        print("=" * 50)

        config = {"skill": skill_name}

        # 认证
        print("\n[认证设置]")
        use_env = input("使用环境变量 CLOUDPSS_TOKEN? (y/n, 默认y): ").strip().lower() != "n"
        if use_env:
            config["auth"] = {"token": "${CLOUDPSS_TOKEN}"}
        else:
            token_file = input("Token文件路径 (默认: .cloudpss_token): ").strip()
            config["auth"] = {"token_file": token_file or ".cloudpss_token"}

        # 模型
        print("\n[模型设置]")
        default_rid = defaults.get("model", {}).get("rid", "model/holdme/IEEE3") if defaults else "model/holdme/IEEE3"
        rid = input(f"模型RID (默认: {default_rid}): ").strip()
        config["model"] = {"rid": rid or default_rid, "source": "cloud"}

        # 输出
        print("\n[输出设置]")
        output_format = input("输出格式 (csv/json/yaml, 默认csv): ").strip() or "csv"
        output_path = input("输出目录 (默认: ./results/): ").strip() or "./results/"
        config["output"] = {"format": output_format, "path": output_path}

        return config
