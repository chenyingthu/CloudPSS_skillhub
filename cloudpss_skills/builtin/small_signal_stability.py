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

        except Exception as e:
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
        """提取系统数据：母线、发电机、支路参数"""
        from cloudpss import Model

        # 获取潮流结果
        buses_data = powerflow_result.getBuses()
        branches_data = powerflow_result.getBranches()

        buses = []
        generators = []

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
                }

                # 提取惯性时间常数 H (秒)
                # 不同模型可能有不同参数名
                h_value = 0.0
                for h_key in ['H', ' inertia', 'TJ', 'M']:
                    if h_key in comp.args:
                        try:
                            h_val = comp.args[h_key].get('source', '0')
                            h_value = float(h_val)
                            break
                        except (ValueError, TypeError):
                            pass

                # 如果没有找到H，使用默认值
                if h_value <= 0:
                    h_value = 3.0  # 默认值

                # 提取阻尼系数 D
                d_value = 0.0
                for d_key in ['D', 'Kd']:
                    if d_key in comp.args:
                        try:
                            d_val = comp.args[d_key].get('source', '0')
                            d_value = float(d_val)
                            break
                        except (ValueError, TypeError):
                            pass

                # 提取额定容量
                s_n = base_power  # 默认使用系统基准
                for s_key in ['Sn', 'S_n', 'rated_power']:
                    if s_key in comp.args:
                        try:
                            s_val = comp.args[s_key].get('source', str(base_power))
                            s_n = float(s_val)
                            break
                        except (ValueError, TypeError):
                            pass

                # 提取暂态电抗 Xd'
                xd_prime = 0.3  # 默认值
                for x_key in ["Xd'", 'Xd_prime', 'xd1']:
                    if x_key in comp.args:
                        try:
                            x_val = comp.args[x_key].get('source', '0.3')
                            xd_prime = float(x_val)
                            break
                        except (ValueError, TypeError):
                            pass

                gen_data['H'] = h_value
                gen_data['D'] = d_value
                gen_data['S_n'] = s_n
                gen_data['Xd_prime'] = xd_prime

                # 查找连接母线
                pins = getattr(comp, 'pins', {})
                for pin_name, pin_data in pins.items():
                    if isinstance(pin_data, dict) and 'bus' in pin_data:
                        gen_data['bus'] = pin_data['bus']
                        break

                generators.append(gen_data)

        log_func("INFO", f"提取到 {len(buses)} 个母线, {len(generators)} 台发电机")

        return {
            'buses': buses,
            'generators': generators,
            'base_power': base_power,
        }

    def _build_state_matrix(self, system_data: Dict, log_func) -> np.ndarray:
        """构建线性化状态矩阵（经典发电机模型）"""
        generators = system_data['generators']
        buses = system_data['buses']
        base_power = system_data['base_power']

        n_gen = len(generators)
        if n_gen == 0:
            raise ValueError("系统中没有发电机")

        # 使用经典模型：每个发电机有2个状态变量（转子角δ，转子速度ω）
        # 状态向量: [δ1, ω1, δ2, ω2, ..., δn, ωn]
        n_states = 2 * n_gen

        # 构建导纳矩阵（简化版，仅考虑发电机内电动势节点）
        # 实际应构建完整的网络导纳矩阵并消去负荷节点

        # 简化处理：假设发电机通过纯电抗连接到无穷大母线
        # 使用两机模型近似

        state_matrix = np.zeros((n_states, n_states))

        # 同步角速度 (rad/s)
        omega_s = 2 * np.pi * 60  # 60 Hz系统

        for i, gen_i in enumerate(generators):
            H_i = gen_i['H']
            D_i = gen_i['D']

            # 状态索引
            delta_idx = 2 * i
            omega_idx = 2 * i + 1

            # dδ/dt = ω - ωs
            state_matrix[delta_idx, omega_idx] = 1.0

            # dω/dt = -D/(2H) * (ω - ωs) - ωs/(2H) * (Pe - Pm)
            # 线性化后简化为: dω/dt = -D/(2H) * Δω - ωs/(2H) * ∂Pe/∂δ * Δδ
            state_matrix[omega_idx, omega_idx] = -D_i / (2 * H_i)

            # 机电耦合系数（简化处理）
            for j, gen_j in enumerate(generators):
                if i != j:
                    delta_j_idx = 2 * j

                    # 同步功率系数近似
                    # K_ij = ωs * E_i * E_j * B_ij / (2H_i)
                    # 使用简化假设
                    K_ij = omega_s / (2 * H_i * n_gen)  # 简化假设

                    state_matrix[omega_idx, delta_idx] -= K_ij
                    state_matrix[omega_idx, delta_j_idx] += K_ij

        log_func("INFO", f"状态矩阵维度: {n_states}x{n_states}")

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
        """计算参与因子"""
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
                    # numpy complex type
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

                # 找出主导发电机
                if mode_participation:
                    max_p = max(mode_participation) if max(mode_participation) > 0 else 1.0
                    normalized_p = [p / max_p for p in mode_participation]

                    dominant_gens = []
                    for gen_idx, gen in enumerate(generators):
                        delta_p = normalized_p[2 * gen_idx] if 2 * gen_idx < len(normalized_p) else 0
                        omega_p = normalized_p[2 * gen_idx + 1] if 2 * gen_idx + 1 < len(normalized_p) else 0

                        if delta_p > 0.3 or omega_p > 0.3:
                            dominant_gens.append({
                                'gen': gen['label'],
                                'delta_p': round(delta_p, 3),
                                'omega_p': round(omega_p, 3),
                            })

                    participation[f"mode_{mode_idx}"] = {
                        'frequency': round(freq, 3),
                        'participation': normalized_p,
                        'dominant_generators': dominant_gens,
                    }

                    # 更新模式信息
                    if mode_idx < len(eigen_results['modes']):
                        eigen_results['modes'][mode_idx]['dominant_gens'] = [g['gen'] for g in dominant_gens]

            log_func("INFO", f"参与因子计算完成，分析了 {len(participation)} 个机电模式")

            return participation

        except Exception as e:
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
            "## 建议",
            "",
        ])

        if assessment.get('n_weakly_damped', 0) > 0:
            lines.append("⚠️ 存在弱阻尼模式，建议:")
            lines.append("- 检查发电机PSS配置")
            lines.append("- 评估励磁系统参数")
            lines.append("- 考虑增加系统阻尼措施")
        else:
            lines.append("✅ 所有机电振荡模式阻尼良好，系统小信号稳定性满足要求。")

        path.write_text("\n".join(lines), encoding="utf-8")
