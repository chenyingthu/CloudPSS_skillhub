#!/usr/bin/env python3
"""
模型构建器技能

功能：基于现有模型创建新算例，支持添加/修改/删除组件
适用：批量生成测试算例、新能源接入模型、保护配置模型等

作者: Claude Code
日期: 2026-03-31
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from copy import deepcopy
import itertools

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ComponentModification:
    """组件修改操作"""
    action: str  # add, modify, remove
    component_type: Optional[str] = None
    label: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    selector: Optional[Dict[str, Any]] = None  # 用于modify/remove定位组件
    position: Optional[Dict[str, float]] = None  # x, y坐标


@dataclass
class GeneratedModel:
    """生成的模型信息"""
    name: str
    rid: str
    description: str
    modifications_applied: List[str]


class ModelBuilderSkill(SkillBase):
    """
    模型构建器技能

    功能特性:
    1. 从基础模型克隆
    2. 添加新组件（光伏、风电、保护装置等）
    3. 修改现有组件参数
    4. 删除组件
    5. 批量生成变体模型
    6. 保存为新模型

    配置示例:
        skill: model_builder
        base_model:
          rid: model/holdme/IEEE39
          config_index: 0

        modifications:
          - action: add_component
            component_type: model/CloudPSS/PV_Inverter
            label: PV_Bus10
            parameters:
              额定容量: 100
              有功功率参考值: 0.8
            position:
              x: 400
              y: 300

          - action: modify_component
            selector:
              label: "TLine_3p-17"
            parameters:
              线路长度: 150

          - action: remove_component
            selector:
              key: "canvas_0_10"

        output:
          save: true
          branch: feature/pv_integration
          name: "IEEE39_with_100MW_PV"
          description: "IEEE39系统母线10添加100MW光伏电站"

    """

    name = "model_builder"
    description = "模型构建、组件添加修改删除、测试算例生成"
    version = "1.0.0"

    # 默认组件类型列表，可通过配置扩展
    DEFAULT_COMPONENT_TYPES = [
        "model/CloudPSS/_newBus_3p",
        "model/CloudPSS/TransmissionLine",
        "model/CloudPSS/_newGenerator",
        "model/CloudPSS/_newLoad_3p",
        "model/CloudPSS/_newTransformer_3p",
        # 新能源模型
        "model/CloudPSS/WGSource",  # 风电场电源模型
        "model/CloudPSS/WGSource_external_ctrl",  # 风电场外部控制模型
        "model/CloudPSS/DFIG_external_ctrl",  # DFIG外部控制模型
        "model/CloudPSS/DFIG_WindFarm_Equivalent_Model",  # DFIG风电场等值模型
        "model/CloudPSS/PVStation",  # 光伏电站模型
        "model/CloudPSS/PVStation_external_ctrl",  # 光伏电站外部控制模型
        # 保护装置
        "model/CloudPSS/DistanceRelay",  # 距离保护
        "model/CloudPSS/OvercurrentRelay",  # 过流保护
    ]

    config_schema = {
        "type": "object",
        "required": ["base_model"],
        "properties": {
            "base_model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string"},
                    "config_index": {"type": "integer", "default": 0}
                }
            },
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"}
                }
            },
            "modifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["add_component", "modify_component", "remove_component"]
                        },
                        "component_type": {"type": "string"},
                        "label": {"type": "string"},
                        "parameters": {"type": "object"},
                        "selector": {"type": "object"},
                        "position": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"}
                            }
                        }
                    }
                }
            },
            "batch": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean", "default": False},
                    "parameter_sweep": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "param_name": {"type": "string"},
                                "values": {"type": "array"}
                            }
                        }
                    }
                }
            },
            "output": {
                "type": "object",
                "properties": {
                    "save": {"type": "boolean", "default": True},
                    "branch": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.model = None
        self.base_model_rid = None
        self.modifications_applied = []
        self._original_modifications = []

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        if not config.get("base_model", {}).get("rid"):
            errors.append("必须指定基础模型RID")

        modifications = config.get("modifications", [])
        for i, mod in enumerate(modifications):
            action = mod.get("action")
            if action == "add_component":
                if not mod.get("component_type"):
                    errors.append(f"modifications[{i}]: add_component需要指定component_type")
                if not mod.get("label"):
                    errors.append(f"modifications[{i}]: add_component需要指定label")
            elif action in ["modify_component", "remove_component"]:
                if not mod.get("selector"):
                    errors.append(f"modifications[{i}]: {action}需要指定selector")
            elif action not in ["add_component", "modify_component", "remove_component"]:
                errors.append(f"modifications[{i}]: 未知的action '{action}'")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行模型构建"""
        start_time = datetime.now()
        try:
            self._setup_auth(config)

            # 获取基础模型
            base_rid = config["base_model"]["rid"]
            self.base_model_rid = base_rid
            logger.info(f"获取基础模型: {base_rid}")
            self.model = self._fetch_model(base_rid)

            # 记录原始模型信息
            original_name = getattr(self.model, 'name', 'Unknown')
            logger.info(f"基础模型名称: {original_name}")

            # 执行修改操作
            modifications = config.get("modifications", [])
            # 存储原始修改配置，供批量生成使用
            self._original_modifications = deepcopy(modifications)
            if modifications:
                logger.info(f"执行 {len(modifications)} 个修改操作...")
                for i, mod_config in enumerate(modifications, 1):
                    try:
                        self._apply_modification(mod_config)
                        logger.info(f"  [{i}/{len(modifications)}] {mod_config['action']} 完成")
                    except Exception as e:
                        logger.error(f"  [{i}/{len(modifications)}] {mod_config['action']} 失败: {e}")
                        raise

            # 处理批量生成
            generated_models = []
            batch_config = config.get("batch", {})
            if batch_config.get("enabled", False):
                logger.info("执行批量生成...")
                generated_models = self._batch_generate(batch_config, config.get("output", {}))
            else:
                # 单次保存
                output_config = config.get("output", {})
                if output_config.get("save", True):
                    model_info = self._save_model(output_config)
                    generated_models.append(model_info)

            # 构建结果
            result_data = {
                "base_model": base_rid,
                "modifications_count": len(modifications),
                "modifications_applied": self.modifications_applied,
                "generated_models": [
                    {
                        "name": m.name,
                        "rid": m.rid,
                        "description": m.description,
                        "modifications": m.modifications_applied
                    }
                    for m in generated_models
                ]
            }

            logger.info(f"模型构建完成，生成了 {len(generated_models)} 个模型")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data
            )

        except Exception as e:
            logger.error(f"模型构建失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )

    def _apply_modification(self, mod_config: Dict):
        """应用单个修改操作"""
        action = mod_config["action"]

        if action == "add_component":
            self._add_component(mod_config)
        elif action == "modify_component":
            self._modify_component(mod_config)
        elif action == "remove_component":
            self._remove_component(mod_config)
        else:
            raise ValueError(f"未知的action: {action}")

    def _add_component(self, config: Dict):
        """添加组件"""
        comp_type = config["component_type"]
        label = config["label"]
        params = config.get("parameters", {})
        position = config.get("position", {})

        logger.debug(f"添加组件: {label} ({comp_type})")

        # 构建组件定义
        component_def = {
            "label": label,
            "type": "standard.Image",
            "data": {
                "rid": comp_type,
                "label": label,
                "args": params
            }
        }

        # 添加位置信息
        if position:
            component_def["position"] = {
                "x": position.get("x", 0),
                "y": position.get("y", 0)
            }

        # 调用 SDK 添加组件
        try:
            # 使用 model.addComponent 方法
            self.model.addComponent(
                definition=comp_type,
                label=label,
                args=params,
                pins={}  # 暂不处理引脚连接
            )
            self.modifications_applied.append(f"add:{label}")
        except Exception as e:
            logger.warning(f"SDK添加组件失败，尝试备用方法: {e}")
            # 备用：直接修改模型内部结构
            self._add_component_direct(component_def)

    def _add_component_direct(self, component_def: Dict):
        """直接修改模型内部结构添加组件"""
        # TODO: 当前 SDK 不支持直接添加组件
        # 需要通过模型编辑 API 实现
        logger.warning("直接添加组件功能当前不可用，需要 CloudPSS SDK 支持")
        # 暂时记录修改但不实际添加
        self.modifications_applied.append(f"add:{component_def.get('label', 'unknown')}(skipped)")

    def _modify_component(self, config: Dict):
        """修改组件参数"""
        selector = config["selector"]
        params = config.get("parameters", {})

        logger.debug(f"修改组件: {selector} -> {params}")

        # 查找组件
        component_key = self._find_component(selector)
        if not component_key:
            raise ValueError(f"找不到匹配的组件: {selector}")

        # 更新参数
        try:
            self.model.updateComponent(component_key, **params)
            self.modifications_applied.append(f"modify:{component_key}")
        except Exception as e:
            logger.warning(f"SDK修改组件失败，尝试备用方法: {e}")
            self._modify_component_direct(component_key, params)

    def _modify_component_direct(self, key: str, params: Dict):
        """直接修改组件参数"""
        # TODO: 当前 SDK 不支持直接修改组件参数
        # 需要通过模型编辑 API 实现
        logger.warning(f"直接修改组件功能当前不可用，需要 CloudPSS SDK 支持")
        self.modifications_applied.append(f"modify:{key}(skipped)")

    def _remove_component(self, config: Dict):
        """删除组件"""
        selector = config["selector"]

        logger.debug(f"删除组件: {selector}")

        # 查找组件
        component_key = self._find_component(selector)
        if not component_key:
            raise ValueError(f"找不到匹配的组件: {selector}")

        # 删除组件
        try:
            self.model.removeComponent(component_key)
            self.modifications_applied.append(f"remove:{component_key}")
        except Exception as e:
            logger.warning(f"SDK删除组件失败: {e}")
            raise

    def _find_component(self, selector: Dict) -> Optional[str]:
        """
        根据选择器查找组件key

        selector支持:
        - {label: "组件名称"}
        - {type: "组件类型"}
        - {key: "canvas_xxx"}
        """
        try:
            # 使用 SDK 的 getComponentsByRid 获取所有组件
            # 首先尝试通过类型获取
            all_components = {}

            # 获取组件类型列表（类默认 + 实例配置）
            component_types = list(self.DEFAULT_COMPONENT_TYPES)
            if hasattr(self, '_additional_component_types'):
                component_types.extend(self._additional_component_types)

            for comp_type in component_types:
                try:
                    components = self.model.getComponentsByRid(comp_type)
                    if components:
                        # components 是 Component 对象字典
                        for key, comp in components.items():
                            all_components[key] = comp
                except Exception as e:
                    logger.debug(f"获取组件类型 {comp_type} 失败: {e}")

            # 遍历所有组件进行匹配
            for key, comp in all_components.items():
                # Component 对象有直接的属性访问
                comp_label = getattr(comp, 'label', None)
                comp_type = getattr(comp, 'definition', None)  # 组件类型RID

                # 匹配 label
                if "label" in selector:
                    if comp_label == selector["label"]:
                        return key

                # 匹配 type (rid)
                if "type" in selector:
                    if comp_type == selector["type"]:
                        return key

                # 匹配 key
                if "key" in selector:
                    if key == selector["key"]:
                        return key

            return None

        except Exception as e:
            logger.error(f"查找组件失败: {e}")
            return None

    def _batch_generate(self, batch_config: Dict, output_config: Dict) -> List[GeneratedModel]:
        """批量生成模型变体"""
        models = []

        # 获取参数扫描配置
        sweep_params = batch_config.get("parameter_sweep", [])
        if not sweep_params:
            logger.warning("批量生成启用但没有指定参数扫描")
            return models

        # 生成参数组合
        param_names = [p["param_name"] for p in sweep_params]
        param_values = [p["values"] for p in sweep_params]

        for i, combination in enumerate(itertools.product(*param_values)):
            # 创建参数映射
            params = dict(zip(param_names, combination))

            # 应用参数
            for mod in self._get_modifications_with_params(params):
                self._apply_modification(mod)

            # 保存模型
            output = deepcopy(output_config)
            output["name"] = output_config.get("name", "model") + f"_{i+1}"
            output["description"] = output_config.get("description", "") + f" (params: {params})"

            model_info = self._save_model(output)
            models.append(model_info)

            logger.info(f"批量生成 [{i+1}]: {model_info.name}")

        return models

    def _get_modifications_with_params(self, params: Dict) -> List[Dict]:
        """获取替换参数后的修改配置"""
        # 复制当前已应用的修改配置
        modifications = []

        for mod in self._original_modifications:
            # 深拷贝修改配置
            new_mod = deepcopy(mod)

            # 替换参数占位符
            if "parameters" in new_mod:
                for key, value in new_mod["parameters"].items():
                    if isinstance(value, str):
                        # 替换 {param_name} 格式的占位符
                        for param_name, param_value in params.items():
                            placeholder = f"{{{param_name}}}"
                            if placeholder in value:
                                new_mod["parameters"][key] = value.replace(placeholder, str(param_value))

            # 替换 label 中的占位符
            if "label" in new_mod:
                label = new_mod["label"]
                if isinstance(label, str):
                    for param_name, param_value in params.items():
                        placeholder = f"{{{param_name}}}"
                        if placeholder in label:
                            label = label.replace(placeholder, str(param_value))
                    new_mod["label"] = label

            # 替换 selector 中的占位符
            if "selector" in new_mod:
                selector = new_mod["selector"]
                for key, value in selector.items():
                    if isinstance(value, str):
                        for param_name, param_value in params.items():
                            placeholder = f"{{{param_name}}}"
                            if placeholder in value:
                                selector[key] = value.replace(placeholder, str(param_value))

            modifications.append(new_mod)

        return modifications

    def _save_model(self, output_config: Dict) -> GeneratedModel:
        """保存模型"""
        branch = output_config.get("branch", f"auto_generated_{datetime.now().strftime('%Y%m%d')}")
        name = output_config.get("name", f"Model_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        description = output_config.get("description", "Auto-generated model")

        logger.info(f"保存模型到分支: {branch}")

        try:
            # 保存模型
            result = self.model.save(branch)
            # 构建正确的 RID: model/<user>/<branch>
            # base_model_rid 格式: model/<user>/<original_branch>
            base_parts = self.base_model_rid.split('/')
            if len(base_parts) >= 2:
                new_rid = f"{base_parts[0]}/{base_parts[1]}/{branch}"
            else:
                new_rid = result.get("rid", f"model/{branch}")

            logger.info(f"模型已保存: {new_rid}")

            return GeneratedModel(
                name=name,
                rid=new_rid,
                description=description,
                modifications_applied=self.modifications_applied.copy()
            )

        except Exception as e:
            logger.error(f"保存模型失败: {e}")
            raise

    def _setup_auth(self, config: Dict):
        """设置认证"""
        from cloudpss import setToken

        auth = config.get("auth", {})
        token = auth.get("token")

        if not token and auth.get("token_file"):
            try:
                with open(auth["token_file"], "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                pass

        if not token:
            try:
                with open(".cloudpss_token", "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                raise ValueError("未找到CloudPSS token")

        setToken(token)

    def _fetch_model(self, rid: str):
        """获取模型"""
        from cloudpss import Model
        return Model.fetch(rid)
