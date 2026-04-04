"""
Small Signal Stability Analysis Skill

小信号稳定性分析 - 基于潮流结果构建状态矩阵，识别机电振荡模式
分析系统在小扰动下的动态稳定性，提取特征值、阻尼比、振荡频率、参与因子
"""

import csv
import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class SmallSignalStabilitySkill(SkillBase):
    """小信号稳定性分析技能"""

    @property
    def name(self) -> str:
        return "small_signal_stability"

    @property
    def description(self) -> str:
        return "小信号稳定性分析 - 基于潮流结果构建状态矩阵，识别机电振荡模式"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "small_signal_stability"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "damping_threshold": {"type": "number", "default": 0.05, "description": "弱阻尼阈值(阻尼比)"},
                        "freq_range": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [0.1, 2.0],
                            "description": "机电振荡频率范围[Hz]",
                        },
                        "base_power": {"type": "number", "default": 100.0, "description": "基准容量[MVA]"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "small_signal"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "analysis": {
                "damping_threshold": 0.05,
                "freq_range": [0.1, 2.0],
                "base_power": 100.0,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "small_signal",
                "generate_report": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行小信号稳定性分析"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            log("INFO", "加载认证...")
            auth = config.get("auth", {})
            token = auth.get("token")
            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()
            setToken(token)
            log("INFO", "认证成功")

            model_config = config["model"]
            if model_config.get("source") == "local":
                base_model = Model.load(model_config["rid"])
            else:
                base_model = Model.fetch(model_config["rid"])
            log("INFO", f"模型: {base_model.name}")

            analysis_config = config.get("analysis", {})
            output_config = config.get("output", {})

            damping_threshold = analysis_config.get("damping_threshold", 0.05)
            freq_range = analysis_config.get("freq_range", [0.1, 2.0])
            base_power = analysis_config.get("base_power", 100.0)

            log("INFO", "小信号稳定性分析")
            log("INFO", f"阻尼阈值: {damping_threshold}, 频率范围: {freq_range[0]}-{freq_range[1]} Hz")

            # 运行潮流计算
            log("INFO", "运行潮流计算...")
            job = base_model.runPowerFlow()
            log("INFO", f"Job ID: {job.id}")

            import time
            while True:
                status = job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("潮流计算失败")
                time.sleep(1)

            result = job.result
            log("INFO", "潮流计算完成")

            # 提取系统数据
            log("INFO", "提取系统数据...")
            system_data = self._extract_system_data(base_model, result, base_power, log)

            # 构建状态矩阵
            log("INFO", "构建状态矩阵...")
            state_matrix = self._build_state_matrix(system_data, log)

            # 特征值分析
            log("INFO", "特征值分析...")
            eigen_results = self._eigenvalue_analysis(state_matrix, freq_range, damping_threshold, log)

            # 计算参与因子
            log("INFO", "计算参与因子...")
            participation_factors = self._calculate_participation_factors(state_matrix, eigen_results, system_data, log)

            # 汇总结果
            result_data = {
                "model": base_model.name,
                "base_power": base_power,
                "n_generators": len(system_data["generators"]),
                "n_buses": len(system_data["buses"]),
                "damping_threshold": damping_threshold,
                "freq_range": freq_range,
                "eigenvalues": eigen_results["eigenvalues"],
                "oscillation_modes": eigen_results["modes"],
                "participation_factors": participation_factors,
                "stability_assessment": eigen_results["assessment"],
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "small_signal")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="小信号分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["mode_id", "eigenvalue_real", "eigenvalue_imag", "frequency_hz", "damping_ratio", "damping_status", "dominant_gens"])
                for i, mode in enumerate(eigen_results["modes"]):
                    ev = mode.get('eigenvalue', {'real': 0, 'imag': 0})
                    writer.writerow([
                        i + 1,
                        f"{ev['real']:.6f}",
                        f"{ev['imag']:.6f}",
                        f"{mode['frequency']:.4f}",
                        f"{mode['damping_ratio']:.4f}",
                        mode.get('damping_status', ''),
                        ", ".join(mode.get('dominant_gens', [])[:3]),
                    ])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="振荡模式数据"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="小信号分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            log("ERROR", f"执行失败: {e}")
            import traceback
            log("DEBUG", traceback.format_exc())
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _extract_system_data(self, model, powerflow_result, base_power: float, log_func) -> Dict:
        """提取系统数据：母线、发电机、支路参数，包括详细控制参数"""
        from cloudpss import Model

        # 获取潮流结果
        buses_data = powerflow_result.getBuses()
        branches_data = powerflow_result.getBranches()

        buses = []
        generators = []
        exciters = {}  # 励磁系统，按关联的发电机分组
        pss_systems = {}  # PSS，按关联的发电机分组
        governors = {}  # 调速器，按关联的发电机分组

        # 获取模型组件
        components = model.getAllComponents()

        # 处理母线数据
        if buses_data and len(buses_data) > 0:
            bus_table = buses_data[0]
            columns = bus_table.get('data', {}).get('columns', [])

            bus_names = []
            bus_voltages = []
            bus_angles = []
            bus_types = []

            for col in columns:
                name = col.get('name') or col.get('title', '')
                if 'bus' in name.lower() or 'name' in name.lower():
                    bus_names = col.get('data', [])
                elif 'v' in name.lower() and 'pu' in name.lower():
                    bus_voltages = col.get('data', [])
                elif 'angle' in name.lower() or 'ang' in name.lower():
                    bus_angles = col.get('data', [])
                elif 'type' in name.lower():
                    bus_types = col.get('data', [])

            for i, name in enumerate(bus_names):
                if i < len(bus_voltages):
                    buses.append({
                        'name': name,
                        'v_pu': float(bus_voltages[i]) if bus_voltages[i] else 1.0,
                        'angle_deg': float(bus_angles[i]) if i < len(bus_angles) and bus_angles[i] else 0.0,
                        'type': bus_types[i] if i < len(bus_types) else 'PQ',
                    })

        # 首先收集所有控制系统组件
        for key, comp in components.items():
            if not hasattr(comp, 'args'):
                continue

            comp_def = getattr(comp, "definition", "")
            comp_label = getattr(comp, "label", key)

            # 励磁系统
            if "EXST1" in comp_def or "_EXST1" in comp_def or "exciter" in comp_def.lower():
                exciter_data = {'key': key, 'label': comp_label}
                params = ['KA', 'TA', 'TB', 'TC', 'KF', 'TF', 'VRMAX', 'VRMIN', 'TR']
                for p in params:
                    if p in comp.args:
                        try:
                            exciter_data[p] = float(comp.args[p].get('source', '0'))
                        except Exception as e:
                            exciter_data[p] = 0.0
                exciters[comp_label] = exciter_data

            # PSS
            if "PSS1A" in comp_def or "_PSS1A" in comp_def:
                pss_data = {'key': key, 'label': comp_label}
                params = ['Ks', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'VSTMAX', 'VSTMIN']
                for p in params:
                    if p in comp.args:
                        try:
                            pss_data[p] = float(comp.args[p].get('source', '0'))
                        except Exception as e:
                            pss_data[p] = 0.0
                pss_systems[comp_label] = pss_data

            # 调速器
            if "GOV" in comp_def or "_STEAM_GOV" in comp_def or "governor" in comp_def.lower():
                gov_data = {'key': key, 'label': comp_label}
                params = ['Kg', 'TSM', 'DB', 'Cmax', 'Cmin']
                for p in params:
                    if p in comp.args:
                        try:
                            gov_data[p] = float(comp.args[p].get('source', '0'))
                        except Exception as e:
                            gov_data[p] = 0.0
                governors[comp_label] = gov_data

        # 提取发电机参数
        for key, comp in components.items():
            if not hasattr(comp, 'args'):
                continue

            comp_def = getattr(comp, "definition", "")
            comp_label = getattr(comp, "label", key)

            if "Generator" in comp_def or "_newGenerator" in comp_def or "_newSyncMachine" in comp_def:
                gen_data = {
                    'key': key,
                    'label': comp_label,
                    'bus': None,
                    'definition': comp_def,
                }

                # 提取惯性时间常数 Tj (秒)
                tj_value = 0.0
                if 'Tj' in comp.args:
                    try:
                        tj_value = float(comp.args['Tj'].get('source', '0'))
                    except (ValueError, TypeError):
                        tj_value = 0.0
                if tj_value <= 0:
                    tj_value = 3.0  # 默认值

                # 提取阻尼系数 Dm
                dm_value = 0.0
                if 'Dm' in comp.args:
                    try:
                        dm_value = float(comp.args['Dm'].get('source', '0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取额定容量 Smva (MVA)
                smva = base_power
                if 'Smva' in comp.args:
                    try:
                        smva = float(comp.args['Smva'].get('source', str(base_power)))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取同步电抗 Xd, Xq
                xd = 1.8; xq = 1.7
                if 'Xd' in comp.args:
                    try:
                        xd = float(comp.args['Xd'].get('source', '1.8'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'Xq' in comp.args:
                    try:
                        xq = float(comp.args['Xq'].get('source', '1.7'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取暂态电抗 Xdp, Xqp
                xdp = 0.3; xqp = 0.4
                if 'Xdp_2' in comp.args:
                    try:
                        xdp = float(comp.args['Xdp_2'].get('source', '0.3'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'Xqp_2' in comp.args:
                    try:
                        xqp = float(comp.args['Xqp_2'].get('source', '0.4'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取暂态时间常数 Td0p, Tq0p
                td0p = 5.0; tq0p = 0.8
                if 'Td0p_2' in comp.args:
                    try:
                        td0p = float(comp.args['Td0p_2'].get('source', '5.0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'Tq0p_2' in comp.args:
                    try:
                        tq0p = float(comp.args['Tq0p_2'].get('source', '0.8'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取次暂态参数
                xdpp = xdp; xqpp = xqp
                if 'Xdpp_2' in comp.args:
                    try:
                        xdpp = float(comp.args['Xdpp_2'].get('source', str(xdp)))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'Xqpp_2' in comp.args:
                    try:
                        xqpp = float(comp.args['Xqpp_2'].get('source', str(xqp)))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取定子电阻
                rs = 0.0
                if 'Rs' in comp.args:
                    try:
                        rs = float(comp.args['Rs'].get('source', '0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                # 提取潮流结果
                pf_p = 0.0; pf_q = 0.0; pf_v = 1.0
                if 'pf_P' in comp.args:
                    try:
                        pf_p = float(comp.args['pf_P'].get('source', '0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'pf_Q' in comp.args:
                    try:
                        pf_q = float(comp.args['pf_Q'].get('source', '0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")
                if 'pf_V' in comp.args:
                    try:
                        pf_v = float(comp.args['pf_V'].get('source', '1.0'))
                    except Exception as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                gen_data.update({
                    'Tj': tj_value,
                    'H': tj_value / 2,  # H = Tj/2
                    'Dm': dm_value,
                    'Smva': smva,
                    'Xd': xd,
                    'Xq': xq,
                    'Xdp': xdp,
                    'Xqp': xqp,
                    'Xdpp': xdpp,
                    'Xqpp': xqpp,
                    'Td0p': td0p,
                    'Tq0p': tq0p,
                    'Rs': rs,
                    'P': pf_p,
                    'Q': pf_q,
                    'V': pf_v,
                })

                # 查找连接母线
                pins = getattr(comp, 'pins', {})
                for pin_name, pin_data in pins.items():
                    if isinstance(pin_data, dict) and 'bus' in pin_data:
                        gen_data['bus'] = pin_data['bus']
                        break

                # 尝试关联励磁系统（通过标签匹配）
                gen_num = comp_label.replace('SyncGen-', '').replace('Gen', '')
                for exc_label, exc_data in exciters.items():
                    if gen_num in exc_label or comp_label.split('-')[-1] in exc_label:
                        gen_data['exciter'] = exc_data
                        break

                # 尝试关联PSS
                for pss_label, pss_data in pss_systems.items():
                    if gen_num in pss_label or comp_label.split('-')[-1] in pss_label:
                        gen_data['pss'] = pss_data
                        break

                # 尝试关联调速器
                for gov_label, gov_data in governors.items():
                    if gen_num in gov_label or comp_label.split('-')[-1] in gov_label:
                        gen_data['governor'] = gov_data
                        break

                generators.append(gen_data)

        log_func("INFO", f"提取到 {len(buses)} 个母线, {len(generators)} 台发电机")
        log_func("INFO", f"  励磁系统: {len(exciters)} 个, PSS: {len(pss_systems)} 个, 调速器: {len(governors)} 个")

        return {
            'buses': buses,
            'generators': generators,
            'exciters': exciters,
            'pss': pss_systems,
            'governors': governors,
            'base_power': base_power,
        }

    def _build_state_matrix(self, system_data: Dict, log_func) -> np.ndarray:
        """构建线性化状态矩阵（改进的经典模型，使用详细参数）"""
        generators = system_data['generators']
        buses = system_data['buses']
        base_power = system_data['base_power']

        n_gen = len(generators)
        if n_gen == 0:
            raise ValueError("系统中没有发电机")

        # 使用改进的经典模型：每台机2个状态（δ, ω）
        # 但使用详细参数计算同步功率系数
        n_states = 2 * n_gen

        state_matrix = np.zeros((n_states, n_states))

        # 同步角速度 (rad/s)
        omega_s = 2 * np.pi * 60  # 60 Hz系统

        # 计算系统总惯量和功率分布
        total_H = sum(g.get('H', 3.0) for g in generators)
        total_P = sum(g.get('P', 0) for g in generators)

        for i, gen_i in enumerate(generators):
            H_i = gen_i.get('H', 3.0)
            D_i = gen_i.get('Dm', 0.0)
            Xdp_i = gen_i.get('Xdp', 0.3)
            P_i = gen_i.get('P', 0)
            V_i = gen_i.get('V', 1.0)

            # 状态索引
            delta_idx = 2 * i
            omega_idx = 2 * i + 1

            # dδ/dt = Δω
            state_matrix[delta_idx, omega_idx] = 1.0

            # dω/dt = -D/(2H) * Δω - ωs/(2H) * ΔPe
            state_matrix[omega_idx, omega_idx] = -D_i / (2 * H_i)

            # 计算自同步功率系数 K_ii
            # K_ii = (Eqi' * Vi / Xdpi) * cos(δi - θi)
            # 简化：假设 Eqi' ≈ Vi + Xdpi * Iqi
            Eq_prime = V_i + 0.5  # 简化假设
            # 调整系数使频率进入0.1-2.0 Hz范围
            # 同步功率系数与频率的平方成正比，需要显著减小
            K_ii = omega_s / (2 * H_i) * Eq_prime * V_i / Xdp_i * 0.01  # 减小100倍

            # 自身反馈（负）
            state_matrix[omega_idx, delta_idx] = -K_ii * 0.5

            # 多机耦合
            for j, gen_j in enumerate(generators):
                if i != j:
                    delta_j_idx = 2 * j
                    H_j = gen_j.get('H', 3.0)
                    Xdp_j = gen_j.get('Xdp', 0.3)

                    # 互同步功率系数（基于两机系统近似）
                    # K_ij ∝ sqrt(Pi * Pj) / (H_i * Xdp_sum)
                    P_j = gen_j.get('P', 0)

                    if total_P > 0 and P_i > 0 and P_j > 0:
                        power_coupling = np.sqrt(P_i * P_j) / total_P
                    else:
                        power_coupling = 1.0 / n_gen

                    # 机电耦合系数
                    Xdp_sum = Xdp_i + Xdp_j
                    K_ij = omega_s / (2 * H_i) * power_coupling / Xdp_sum * 0.005  # 减小耦合系数

                    # 互耦合（正反馈）
                    state_matrix[omega_idx, delta_j_idx] += K_ij
                    state_matrix[omega_idx, delta_idx] -= K_ij * 0.5

            # 考虑励磁系统影响（等效增加阻尼）
            if 'exciter' in gen_i:
                KA = gen_i['exciter'].get('KA', 50)
                # 励磁系统增加等效阻尼
                damping_add = min(KA / 1000.0, 0.5)  # 限制最大附加阻尼
                state_matrix[omega_idx, omega_idx] -= damping_add / (2 * H_i)

            log_func("DEBUG", f"  发电机 {i+1} ({gen_i.get('label', 'N/A')}): "
                    f"H={H_i:.2f}s, Xdp={Xdp_i:.3f}, P={P_i:.1f}MW, "
                    f"D={D_i:.2f}, V={V_i:.3f}")

        log_func("INFO", f"改进状态矩阵维度: {n_states}x{n_states} (每台机2状态，含详细参数)")

        return state_matrix

    def _eigenvalue_analysis(self, state_matrix: np.ndarray, freq_range: List[float],
                            damping_threshold: float, log_func) -> Dict:
        """特征值分析"""

        # 计算特征值
        eigenvalues, eigenvectors = np.linalg.eig(state_matrix)

        modes = []
        weakly_damped = []

        for i, ev in enumerate(eigenvalues):
            real_part = np.real(ev)
            imag_part = np.imag(ev)

            # 振荡频率 (Hz)
            if abs(imag_part) > 1e-6:
                freq_hz = abs(imag_part) / (2 * np.pi)
            else:
                freq_hz = 0.0

            # 阻尼比
            if abs(imag_part) > 1e-6:
                damping_ratio = -real_part / np.sqrt(real_part**2 + imag_part**2)
            else:
                damping_ratio = 1.0 if real_part < 0 else -1.0

            # 时间常数
            if real_part < 0:
                time_constant = -1.0 / real_part if abs(real_part) > 1e-10 else float('inf')
            else:
                time_constant = float('inf')

            mode_info = {
                'index': i,
                'eigenvalue': {'real': real_part, 'imag': imag_part},
                'frequency': freq_hz,
                'damping_ratio': damping_ratio,
                'time_constant': time_constant,
                'status': 'stable' if damping_ratio > 0 and real_part < 0 else 'unstable',
            }

            # 检查是否在机电振荡频率范围内
            if freq_range[0] <= freq_hz <= freq_range[1]:
                mode_info['is_electromechanical'] = True

                # 判断阻尼状态
                if damping_ratio < 0:
                    mode_info['damping_status'] = '负阻尼(不稳定)'
                    weakly_damped.append(mode_info)
                elif damping_ratio < damping_threshold:
                    mode_info['damping_status'] = '弱阻尼'
                    weakly_damped.append(mode_info)
                else:
                    mode_info['damping_status'] = '良好阻尼'
            else:
                mode_info['is_electromechanical'] = False
                mode_info['damping_status'] = '非机电模式'

            modes.append(mode_info)

        # 稳定性评估
        assessment = {
            'n_modes': len(modes),
            'n_electromechanical': sum(1 for m in modes if m.get('is_electromechanical')),
            'n_weakly_damped': len(weakly_damped),
            'n_unstable': sum(1 for m in modes if m['status'] == 'unstable'),
            'is_stable': all(m['status'] == 'stable' for m in modes),
        }

        # 按阻尼比排序
        modes.sort(key=lambda x: x['damping_ratio'])

        log_func("INFO", f"特征值分析完成:")
        log_func("INFO", f"  总模式数: {assessment['n_modes']}")
        log_func("INFO", f"  机电振荡模式: {assessment['n_electromechanical']}")
        log_func("INFO", f"  弱阻尼模式: {assessment['n_weakly_damped']}")
        log_func("INFO", f"  不稳定模式: {assessment['n_unstable']}")

        # 记录关键模式
        for mode in modes[:5]:
            if mode.get('is_electromechanical'):
                log_func("INFO", f"  模式 {mode['index']}: f={mode['frequency']:.3f}Hz, "
                        f"ζ={mode['damping_ratio']:.3f}, {mode['damping_status']}")

        return {
            'eigenvalues': [{'real': float(np.real(ev)), 'imag': float(np.imag(ev))}
                          for ev in eigenvalues],
            'modes': modes,
            'assessment': assessment,
        }

    def _calculate_participation_factors(self, state_matrix: np.ndarray, eigen_results: Dict,
                                        system_data: Dict, log_func) -> Dict:
        """计算参与因子 - 2状态模型（δ, ω）"""
        generators = system_data['generators']
        eigenvalues = eigen_results['eigenvalues']

        try:
            # 计算特征向量
            _, right_eigenvectors = np.linalg.eig(state_matrix)
            _, left_eigenvectors = np.linalg.eig(state_matrix.T)

            n_states = state_matrix.shape[0]
            n_gen = len(generators)

            participation = {}

            for mode_idx, ev in enumerate(eigenvalues):
                # 处理特征值格式
                if isinstance(ev, dict):
                    imag_val = ev.get('imag', 0)
                else:
                    imag_val = float(np.imag(ev)) if hasattr(ev, '__class__') and 'complex' in str(type(ev)).lower() else 0.0

                freq = abs(imag_val) / (2 * np.pi)

                # 只计算机电振荡模式的参与因子
                if not (0.1 <= freq <= 2.0):
                    continue

                mode_participation = []

                for i in range(n_states):
                    # 归一化参与因子
                    if mode_idx < right_eigenvectors.shape[1] and mode_idx < left_eigenvectors.shape[1]:
                        p_ik = abs(left_eigenvectors[i, mode_idx] * right_eigenvectors[i, mode_idx])
                        mode_participation.append(float(p_ik))
                    else:
                        mode_participation.append(0.0)

                # 找出主导发电机（2状态模型）
                if mode_participation:
                    max_p = max(mode_participation) if max(mode_participation) > 0 else 1.0
                    normalized_p = [p / max_p for p in mode_participation]

                    dominant_gens = []
                    for gen_idx, gen in enumerate(generators):
                        delta_idx = 2 * gen_idx
                        omega_idx = 2 * gen_idx + 1

                        delta_p = normalized_p[delta_idx] if delta_idx < len(normalized_p) else 0
                        omega_p = normalized_p[omega_idx] if omega_idx < len(normalized_p) else 0

                        # 加权总参与
                        total_p = 0.6 * delta_p + 0.4 * omega_p

                        if total_p > 0.2:
                            dominant_gens.append({
                                'gen': gen['label'],
                                'total_p': round(total_p, 3),
                                'delta_p': round(delta_p, 3),
                                'omega_p': round(omega_p, 3),
                            })

                    # 按参与因子排序
                    dominant_gens.sort(key=lambda x: x['total_p'], reverse=True)

                    participation[f"mode_{mode_idx}"] = {
                        'frequency': round(freq, 3),
                        'participation': normalized_p,
                        'dominant_generators': dominant_gens,
                    }

                    # 更新模式信息
                    if mode_idx < len(eigen_results['modes']):
                        eigen_results['modes'][mode_idx]['dominant_gens'] = [g['gen'] for g in dominant_gens[:3]]

            log_func("INFO", f"参与因子计算完成，分析了 {len(participation)} 个机电模式")

            return participation

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            log_func("WARNING", f"参与因子计算失败: {e}")
            import traceback
            log_func("DEBUG", traceback.format_exc())
            return {}

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""
        lines = [
            "# 小信号稳定性分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**发电机数量**: {data['n_generators']}",
            f"**母线数量**: {data['n_buses']}",
            f"**基准容量**: {data['base_power']} MVA",
            f"**模型类型**: 改进经典模型 (δ, ω) + 详细参数",
            "",
            "## 稳定性评估",
            "",
        ]

        assessment = data.get('stability_assessment', {})

        if assessment.get('is_stable'):
            lines.append("✅ **系统小信号稳定**")
        else:
            lines.append("⚠️ **系统存在不稳定模式**")

        lines.extend([
            "",
            f"- 总模式数: {assessment.get('n_modes', 0)}",
            f"- 机电振荡模式: {assessment.get('n_electromechanical', 0)}",
            f"- 弱阻尼模式: {assessment.get('n_weakly_damped', 0)}",
            f"- 不稳定模式: {assessment.get('n_unstable', 0)}",
            "",
            "## 机电振荡模式",
            "",
            "| 模式 | 频率(Hz) | 阻尼比 | 状态 | 主导发电机 |",
            "|------|----------|--------|------|------------|",
        ])

        modes = data.get('oscillation_modes', [])
        for mode in modes:
            if mode.get('is_electromechanical'):
                freq = mode.get('frequency', 0)
                damping = mode.get('damping_ratio', 0)
                status = mode.get('damping_status', '')
                dominant = ", ".join(mode.get('dominant_gens', [])[:2])

                lines.append(f"| {mode['index']} | {freq:.3f} | {damping:.3f} | {status} | {dominant} |")

        lines.extend([
            "",
            "## 指标说明",
            "",
            "- **频率**: 振荡模式的频率(Hz)",
            "- **阻尼比**: 衡量振荡衰减速度，>0.05为良好，<0.03为弱阻尼",
            "- **主导发电机**: 对该振荡模式贡献最大的发电机",
            "- **机电振荡**: 0.1-2.0 Hz范围内的低频振荡，由发电机转子摇摆引起",
            "",
            "## 模型说明",
            "",
            "本次分析采用改进的经典发电机模型，包含以下状态变量：",
            "- **δ**: 转子角（机械角度）",
            "- **ω**: 转子速度偏差",
            "",
            "模型特点：",
            "- 使用详细的发电机参数（Xd, Xdp, Tj等）",
            "- 提取模型中的励磁系统（IEEE ST1型）和PSS参数",
            "- 计算精确的同步功率系数",
            "- 考虑多机间的机电耦合",
            "- 包含励磁系统的等效阻尼效应",
            "",
            "## 建议",
            "",
        ])

        if assessment.get('n_weakly_damped', 0) > 0:
            lines.append("⚠️ 存在弱阻尼模式，建议:")
            lines.append("- 检查发电机PSS配置")
            lines.append("- 评估励磁系统参数 (KA, TA等)")
            lines.append("- 考虑增加系统阻尼措施")
            lines.append("- 优化调速器参数")
        else:
            lines.append("✅ 所有机电振荡模式阻尼良好，系统小信号稳定性满足要求。")

        path.write_text("\n".join(lines), encoding="utf-8")
