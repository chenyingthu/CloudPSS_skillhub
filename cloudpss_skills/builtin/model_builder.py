#!/usr/bin/env python3
"""
模型构建器技能

功能：基于现有模型创建新算例，支持添加/修改/删除组件
适用：批量生成测试算例、新能源接入模型、保护配置模型等

作者: Claude Code
日期: 2026-03-31
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from copy import deepcopy
import itertools

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult
from cloudpss_skills.metadata.integration import get_metadata_integration

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
        "model/CloudPSS/PV_Inverter",  # 旧版光伏逆变器示例别名
        "model/CloudPSS/PVStation_external_ctrl",  # 光伏电站外部控制模型
        "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",  # 支持潮流的公开风机封装模型
        "model/open-cloudpss/PVS_01-avm-stdm-v1b5",  # 支持潮流的公开光伏封装模型
        # 保护装置
        "model/CloudPSS/DistanceRelay",  # 距离保护
        "model/CloudPSS/OvercurrentRelay",  # 过流保护
    ]

    COMPONENT_TYPE_ALIASES = {
        # WGSource 已知不适合做潮流算例，自动映射到公开可用的 PMSG 封装模型
        "model/CloudPSS/WGSource": "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",
        "model/CloudPSS/DFIG_WindFarm_Equivalent_Model": "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",
        # 旧文档/示例里的光伏类型统一映射到公开可访问且可参与潮流的封装模型
        "model/CloudPSS/PVStation": "model/open-cloudpss/PVS_01-avm-stdm-v1b5",
        "model/CloudPSS/PV_Inverter": "model/open-cloudpss/PVS_01-avm-stdm-v1b5",
    }

    CONNECTABLE_BUS_RIDS = {
        "model/CloudPSS/_newBus_3p",
    }

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
                        },
                        "pin_connection": {
                            "type": "object",
                            "description": "引脚连接配置",
                            "properties": {
                                "target_bus": {"type": "string", "description": "目标母线名称或ID"},
                                "pin_name": {"type": "string", "default": "0", "description": "引脚名称"}
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
        self._metadata_integration = get_metadata_integration()
        self._metadata_integration.initialize()

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
                        # 捕获所有修改操作异常并记录后重新抛出
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
            # run()方法顶层异常捕获，确保任何错误都返回FAILED状态
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
        """添加组件（集成元数据验证和自动补全）"""
        raw_comp_type = config["component_type"]
        label = config["label"]
        raw_params = config.get("parameters", {})
        position = config.get("position", {})
        pin_connection = config.get("pin_connection", {})
        comp_type, params = self._prepare_component_definition(raw_comp_type, raw_params)

        logger.debug(f"添加组件: {label} ({comp_type})")

        # ========== 元数据集成：参数自动补全 ==========
        completed_params = self._metadata_integration.auto_complete_parameters(comp_type, params)
        if completed_params != params:
            added_keys = set(completed_params.keys()) - set(params.keys())
            if added_keys:
                logger.info(f"  自动补全参数: {', '.join(added_keys)}")
            params = completed_params

        # ========== 元数据集成：参数验证 ==========
        validation = self._metadata_integration.validate_parameters(comp_type, params)
        if not validation.valid:
            error_msg = f"组件 {label} 参数验证失败: {'; '.join(validation.errors)}"
            logger.error(f"  ❌ {error_msg}")
            raise ValueError(error_msg)

        # 检查必需参数
        required = self._metadata_integration.get_required_parameters(comp_type)
        missing_required = [p for p in required if p not in params or params[p] is None]
        if missing_required:
            error_msg = f"组件 {label} 缺少必需参数: {', '.join(missing_required)}"
            logger.error(f"  ❌ {error_msg}")
            raise ValueError(error_msg)

        # ========== 元数据集成：引脚验证 ==========
        pin_requirements = self._metadata_integration.get_pin_requirements(comp_type)
        if pin_requirements:
            logger.debug(f"  引脚要求: {pin_requirements['total_pins']} 个引脚, "
                        f"{len(pin_requirements['required_pins'])} 个必需")

            # 验证引脚连接
            pins = {}
            if pin_connection:
                target_bus = pin_connection.get("target_bus")
                pin_name = pin_connection.get("pin_name", "0")
                if target_bus:
                    pins[pin_name] = target_bus

            pin_validation = self._metadata_integration.validate_pin_connection(comp_type, pins)
            if not pin_validation.valid:
                error_msg = f"组件 {label} 引脚连接验证失败: {'; '.join(pin_validation.errors)}"
                logger.error(f"  ❌ {error_msg}")
                # 引脚连接失败不阻止，只警告（因为可能有内部连接机制）
                logger.warning(f"  ⚠️ {error_msg}")

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

        # 处理引脚连接
        pins = {}
        if pin_connection:
            target_bus = self._resolve_target_bus(pin_connection.get("target_bus"))
            pin_name = pin_connection.get("pin_name", "0")
            if target_bus:
                pins[pin_name] = target_bus
                logger.info(f"  配置引脚 {pin_name} -> 母线 {target_bus}")

        # 调用 SDK 添加组件
        try:
            self.model.addComponent(
                definition=comp_type,
                label=label,
                args=params,
                pins=pins,
                position=position or None,
            )
            self.modifications_applied.append(f"add:{label}")
            if pins:
                self.modifications_applied.append(f"connect:{label}->{target_bus}")

            # 记录元数据使用情况
            summary = self._metadata_integration.get_component_summary(comp_type)
            logger.debug(f"  元数据: {summary}")

        except (AttributeError, TypeError, KeyError) as e:
            # SDK添加组件失败，尝试备用方法
            logger.warning(f"SDK添加组件失败，尝试备用方法: {e}")
            component_def["data"]["pins"] = pins
            self._add_component_direct(component_def)

    def _prepare_component_definition(
        self,
        component_type: str,
        params: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """为新增元件准备真实可用的组件类型和参数。"""
        effective_type = self.COMPONENT_TYPE_ALIASES.get(component_type, component_type)
        effective_params = deepcopy(params)

        if effective_type != component_type:
            logger.info(f"  组件类型映射: {component_type} -> {effective_type}")

        if effective_type == "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1":
            effective_params = self._prepare_public_wind_parameters(effective_params)
        elif effective_type == "model/open-cloudpss/PVS_01-avm-stdm-v1b5":
            effective_params = self._prepare_public_pv_parameters(effective_params)

        return effective_type, effective_params

    @staticmethod
    def _prepare_public_wind_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
        """把旧风电配置翻译成公开 PMSG 模型可用的潮流参数。"""
        prepared = deepcopy(params)
        capacity = ModelBuilderSkill._first_present(
            prepared,
            ["pf_P", "P_cmd", "Pnom", "额定容量", "capacity_mw", "有功功率参考值"]
        )
        if capacity is not None:
            prepared["P_cmd"] = capacity
            prepared["pf_P"] = capacity

        if "Vpcc" in prepared and "Vbase" not in prepared:
            prepared["Vbase"] = prepared.pop("Vpcc")

        prepared.setdefault("Pctrl_mode", "0")
        prepared.setdefault("pf_Q", 0.0)
        prepared.setdefault("Q_cmd", 0.0)
        return ModelBuilderSkill._drop_keys(
            prepared,
            {"Pnom", "额定容量", "capacity_mw", "有功功率参考值"}
        )

    @staticmethod
    def _prepare_public_pv_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
        """把旧 PVStation 风格参数翻译成公开光伏封装模型的潮流参数。"""
        prepared = deepcopy(params)
        capacity = ModelBuilderSkill._first_present(
            prepared,
            ["pf_P", "P_cmd", "Pnom", "额定容量", "capacity_mw", "有功功率参考值"]
        )
        if capacity is not None:
            prepared["P_cmd"] = capacity
            prepared["pf_P"] = capacity

        if "Vpcc" in prepared and "Vbase" not in prepared:
            prepared["Vbase"] = prepared.pop("Vpcc")

        prepared.setdefault("Pctrl_mode", "0")
        prepared.setdefault("pf_Q", 0.0)
        prepared.setdefault("Q_cmd", 0.0)
        return ModelBuilderSkill._drop_keys(
            prepared,
            {"Pnom", "额定容量", "capacity_mw", "有功功率参考值", "Irradiance"}
        )

    @staticmethod
    def _first_present(params: Dict[str, Any], candidates: List[str]) -> Optional[Any]:
        """从一组候选键中读取第一个非空值。"""
        for key in candidates:
            value = params.get(key)
            if value is not None:
                return value
        return None

    @staticmethod
    def _drop_keys(params: Dict[str, Any], keys: set) -> Dict[str, Any]:
        """移除已经翻译过的旧参数键，避免传给新组件定义。"""
        return {key: value for key, value in params.items() if key not in keys}

    @staticmethod
    def _normalize_lookup_value(value: Any) -> str:
        """把用户输入和模型内部名字归一化后再做匹配。"""
        if value is None:
            return ""
        return re.sub(r"[^a-z0-9]+", "", str(value).lower())

    def _resolve_target_bus(self, target_bus: Optional[str]) -> Optional[str]:
        """把文档里的 Bus14 之类写法解析成模型真实可连接的 pin 信号名。"""
        if not target_bus:
            return None

        normalized_target = self._normalize_lookup_value(target_bus)
        if not normalized_target:
            return target_bus

        try:
            bus_components = {}
            for bus_rid in self.CONNECTABLE_BUS_RIDS:
                try:
                    bus_components.update(self.model.getComponentsByRid(bus_rid) or {})
                except Exception as exc:
                    logger.debug(f"获取母线组件 {bus_rid} 失败: {exc}")

            for key, comp in bus_components.items():
                args = getattr(comp, "args", {}) or {}
                pins = getattr(comp, "pins", {}) or {}
                candidates = [
                    key,
                    getattr(comp, "label", None),
                    args.get("Name"),
                    pins.get("0"),
                ]

                if target_bus in candidates:
                    return pins.get("0") or args.get("Name") or target_bus

                normalized_candidates = {
                    self._normalize_lookup_value(candidate): candidate
                    for candidate in candidates
                    if candidate is not None
                }
                if normalized_target in normalized_candidates:
                    return pins.get("0") or args.get("Name") or str(normalized_candidates[normalized_target])

        except Exception as exc:
            logger.error(f"解析目标母线失败: {exc}")

        raise ValueError(
            f"找不到目标母线 '{target_bus}'。"
            "请传入母线 key，或使用如 'bus14' / 'Bus14' 这类可映射到现有母线的名称。"
        )

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
        except (AttributeError, TypeError) as e:
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
        except (AttributeError, TypeError) as e:
            # SDK删除组件失败
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
                except (AttributeError, KeyError) as e:
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

        except (KeyError, AttributeError, TypeError) as e:
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

        except (ConnectionError, RuntimeError, ValueError) as e:
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
            except FileNotFoundError as e:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")

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
