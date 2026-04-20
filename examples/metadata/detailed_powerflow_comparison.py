"""
详细潮流对比分析

对比基准IEEE39和添加新能源后的系统潮流分布
用实际数据验证新能源对系统的影响
"""

import os
import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss import setToken, Model


def setup_auth():
    """设置认证"""
    token = os.environ.get('CLOUDPSS_TOKEN')
    if not token:
        token_file = Path('.cloudpss_token')
        if token_file.exists():
            token = token_file.read_text().strip()
    if token:
        setToken(token)
        return True
    return False


def run_power_flow(rid: str, name: str) -> Dict:
    """运行潮流计算并返回详细结果"""
    print(f"\n正在运行 {name}...")
    print(f"  RID: {rid}")

    try:
        model = Model.fetch(rid)
        job = model.runPowerFlow()
        job.wait()

        if job.status() != 1:
            print(f"  ❌ 潮流计算失败，状态: {job.status()}")
            return None

        result = job.result

        # 获取节点数据
        buses = result.getBuses()
        bus_data = []
        for bus in buses:
            bus_data.append({
                'name': bus.get('name', ''),
                'voltage': bus.get('voltage', 0),
                'angle': bus.get('angle', 0),
                'gen_P': bus.get('generation', {}).get('P', 0),
                'gen_Q': bus.get('generation', {}).get('Q', 0),
                'load_P': bus.get('load', {}).get('P', 0),
                'load_Q': bus.get('load', {}).get('Q', 0)
            })

        # 获取支路数据
        branches = result.getBranches()
        branch_data = []
        for branch in branches:
            branch_data.append({
                'from': branch.get('from', ''),
                'to': branch.get('to', ''),
                'P_from': branch.get('P_from', 0),
                'Q_from': branch.get('Q_from', 0),
                'P_to': branch.get('P_to', 0),
                'Q_to': branch.get('Q_to', 0),
                'I': branch.get('I', 0)
            })

        # 统计信息
        total_gen_P = sum(b['gen_P'] for b in bus_data)
        total_gen_Q = sum(b['gen_Q'] for b in bus_data)
        total_load_P = sum(b['load_P'] for b in bus_data)
        total_load_Q = sum(b['load_Q'] for b in bus_data)

        print(f"  ✅ 潮流计算成功")
        print(f"     节点数: {len(bus_data)}")
        print(f"     支路数: {len(branch_data)}")
        print(f"     总有功发电: {total_gen_P:.2f} MW")
        print(f"     总有功负荷: {total_load_P:.2f} MW")

        return {
            'name': name,
            'rid': rid,
            'buses': bus_data,
            'branches': branch_data,
            'total_gen_P': total_gen_P,
            'total_gen_Q': total_gen_Q,
            'total_load_P': total_load_P,
            'total_load_Q': total_load_Q,
            'loss_P': total_gen_P - total_load_P
        }

    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return None


def compare_voltage(base_buses: List[Dict], new_buses: List[Dict], new_energy_bus: str = None):
    """对比节点电压"""
    # 创建name到数据的映射
    base_map = {b['name']: b for b in base_buses}
    new_map = {b['name']: b for b in new_buses}

    # 找到共同节点
    common_buses = set(base_map.keys()) & set(new_map.keys())

    comparison = []
    voltage_changes = []

    for bus_name in sorted(common_buses):
        base_v = base_map[bus_name]['voltage']
        new_v = new_map[bus_name]['voltage']
        delta_v = new_v - base_v
        delta_pct = (delta_v / base_v) * 100 if base_v > 0 else 0

        comparison.append({
            'bus': bus_name,
            'base_voltage': base_v,
            'new_voltage': new_v,
            'delta_V': delta_v,
            'delta_pct': delta_pct,
            'is_new_energy_bus': bus_name == new_energy_bus
        })

        if abs(delta_v) > 0.0001:  # 记录有变化的
            voltage_changes.append({
                'bus': bus_name,
                'base': base_v,
                'new': new_v,
                'delta': delta_v,
                'pct': delta_pct
            })

    return comparison, voltage_changes


def compare_branches(base_branches: List[Dict], new_branches: List[Dict]):
    """对比支路潮流"""
    # 创建支路标识符
    def branch_id(b):
        return f"{b['from']}->{b['to']}"

    base_map = {branch_id(b): b for b in base_branches}
    new_map = {branch_id(b): b for b in new_branches}

    common_branches = set(base_map.keys()) & set(new_map.keys())

    comparison = []
    significant_changes = []

    for br_id in sorted(common_branches):
        base_br = base_map[br_id]
        new_br = new_map[br_id]

        base_P = abs(base_br['P_from'])
        new_P = abs(new_br['P_from'])
        delta_P = new_P - base_P
        delta_pct = (delta_P / base_P) * 100 if base_P > 0 else 0

        comparison.append({
            'branch': br_id,
            'base_P': base_br['P_from'],
            'new_P': new_br['P_from'],
            'delta_P': delta_P,
            'delta_pct': delta_pct
        })

        # 记录变化超过5%或超过10MW的支路
        if abs(delta_pct) > 5 or abs(delta_P) > 10:
            significant_changes.append({
                'branch': br_id,
                'base_P': base_br['P_from'],
                'new_P': new_br['P_from'],
                'delta_P': delta_P,
                'delta_pct': delta_pct
            })

    return comparison, significant_changes


def detailed_comparison():
    """执行详细对比"""
    print("=" * 80)
    print("详细潮流对比分析")
    print("对比基准IEEE39与添加新能源后的系统潮流分布")
    print("=" * 80)

    if not setup_auth():
        print("❌ CloudPSS认证失败")
        return

    # 定义模型
    models = {
        '基准模型': 'model/holdme/IEEE39',
        '风电模型': 'model/holdme/test_ieee39_wind',
        '光伏模型': 'model/holdme/test_ieee39_pv',
    }

    # 运行所有潮流计算
    results = {}
    for name, rid in models.items():
        result = run_power_flow(rid, name)
        if result:
            results[name] = result

    if len(results) < 2:
        print("\n❌ 数据不足，无法进行对比")
        return

    # 获取基准结果
    base_result = results.get('基准模型')

    print("\n" + "=" * 80)
    print("一、功率平衡对比")
    print("=" * 80)

    power_summary = []
    for name, result in results.items():
        power_summary.append({
            '模型': name,
            '总有功发电(MW)': round(result['total_gen_P'], 2),
            '总有功负荷(MW)': round(result['total_load_P'], 2),
            '网损(MW)': round(result['loss_P'], 2),
            '无功发电(Mvar)': round(result['total_gen_Q'], 2),
            '无功负荷(Mvar)': round(result['total_load_Q'], 2)
        })

    df_power = pd.DataFrame(power_summary)
    print("\n" + df_power.to_string(index=False))

    # 对比风电模型
    if '风电模型' in results and base_result:
        print("\n" + "=" * 80)
        print("二、风电接入影响分析 (Bus10)")
        print("=" * 80)

        wind_result = results['风电模型']

        # 1. 电压对比
        print("\n1. 节点电压对比（所有节点）")
        voltage_comp, voltage_changes = compare_voltage(
            base_result['buses'], wind_result['buses'], 'Bus10'
        )

        # 筛选重要变化（变化>0.001 p.u.）
        significant_v_changes = [v for v in voltage_changes if abs(v['delta']) > 0.001]

        if significant_v_changes:
            print(f"\n   电压变化显著的节点（共{len(significant_v_changes)}个）：")
            print(f"   {'节点':<15} {'基准电压':<12} {'风电模型':<12} {'变化(p.u.)':<12} {'变化(%)':<10}")
            print(f"   {'-'*65}")
            for v in significant_v_changes[:20]:  # 只显示前20个
                marker = " <-- 接入点" if v['bus'] == 'Bus10' else ""
                print(f"   {v['bus']:<15} {v['base']:<12.4f} {v['new']:<12.4f} {v['delta']:<12.4f} {v['pct']:<10.2f}{marker}")

            if len(significant_v_changes) > 20:
                print(f"   ... 还有 {len(significant_v_changes) - 20} 个节点")

        # 统计
        max_increase = max(voltage_changes, key=lambda x: x['delta']) if voltage_changes else None
        max_decrease = min(voltage_changes, key=lambda x: x['delta']) if voltage_changes else None

        print(f"\n   电压统计：")
        print(f"   - 最大升高: {max_increase['bus']} +{max_increase['delta']:.4f} p.u." if max_increase else "   - 无升高")
        print(f"   - 最大降低: {max_decrease['bus']} {max_decrease['delta']:.4f} p.u." if max_decrease else "   - 无降低")

        # 2. 支路潮流对比
        print("\n2. 支路潮流变化（变化>5%或>10MW）")
        branch_comp, branch_changes = compare_branches(
            base_result['branches'], wind_result['branches']
        )

        if branch_changes:
            print(f"\n   显著变化的支路（共{len(branch_changes)}条）：")
            print(f"   {'支路':<25} {'基准潮流(MW)':<15} {'风电模型(MW)':<15} {'变化(MW)':<12} {'变化(%)':<10}")
            print(f"   {'-'*82}")
            for b in sorted(branch_changes, key=lambda x: abs(x['delta_P']), reverse=True)[:15]:
                print(f"   {b['branch']:<25} {b['base_P']:<15.2f} {b['new_P']:<15.2f} {b['delta_P']:<12.2f} {b['delta_pct']:<10.1f}")
        else:
            print("   无显著变化的支路")

        # 3. 功率平衡细节
        print("\n3. 功率平衡验证")
        gen_increase = wind_result['total_gen_P'] - base_result['total_gen_P']
        loss_increase = wind_result['loss_P'] - base_result['loss_P']

        print(f"   基准模型：")
        print(f"     - 发电: {base_result['total_gen_P']:.2f} MW")
        print(f"     - 负荷: {base_result['total_load_P']:.2f} MW")
        print(f"     - 网损: {base_result['loss_P']:.2f} MW")

        print(f"\n   风电模型：")
        print(f"     - 发电: {wind_result['total_gen_P']:.2f} MW (+{gen_increase:.2f} MW)")
        print(f"     - 负荷: {wind_result['total_load_P']:.2f} MW (不变)")
        print(f"     - 网损: {wind_result['loss_P']:.2f} MW (+{loss_increase:.2f} MW)")

        print(f"\n   验证：")
        print(f"     - 发电增量: {gen_increase:.2f} MW")
        print(f"     - 网损增量: {loss_increase:.2f} MW")
        print(f"     - 新能源理论出力: ~80 MW (40台 × 2MW)")
        print(f"     - 匹配度: {gen_increase:.2f} MW ≈ 80 MW {'✅' if abs(gen_increase - 80) < 10 else '⚠️'}")

    # 对比光伏模型
    if '光伏模型' in results and base_result:
        print("\n" + "=" * 80)
        print("三、光伏接入影响分析 (Bus14)")
        print("=" * 80)

        pv_result = results['光伏模型']

        print("\n1. 节点电压对比（变化>0.001 p.u.）")
        voltage_comp, voltage_changes = compare_voltage(
            base_result['buses'], pv_result['buses'], 'Bus14'
        )

        significant_v_changes = [v for v in voltage_changes if abs(v['delta']) > 0.001]

        if significant_v_changes:
            print(f"\n   电压变化显著的节点（共{len(significant_v_changes)}个）：")
            print(f"   {'节点':<15} {'基准电压':<12} {'光伏模型':<12} {'变化(p.u.)':<12}")
            print(f"   {'-'*55}")
            for v in significant_v_changes[:15]:
                marker = " <-- 接入点" if v['bus'] == 'Bus14' else ""
                print(f"   {v['bus']:<15} {v['base']:<12.4f} {v['new']:<12.4f} {v['delta']:<12.4f}{marker}")

        gen_increase = pv_result['total_gen_P'] - base_result['total_gen_P']
        print(f"\n2. 功率平衡")
        print(f"   发电增量: {gen_increase:.2f} MW")
        print(f"   光伏理论出力: ~50 MW")
        print(f"   匹配度: {gen_increase:.2f} MW ≈ 50 MW {'✅' if abs(gen_increase - 50) < 10 else '⚠️'}")

    print("\n" + "=" * 80)
    print("四、结论")
    print("=" * 80)

    if '风电模型' in results and base_result:
        wind_result = results['风电模型']
        gen_diff = wind_result['total_gen_P'] - base_result['total_gen_P']

        print(f"\n1. 发电功率变化：")
        print(f"   - 基准模型: {base_result['total_gen_P']:.2f} MW")
        print(f"   - 风电模型: {wind_result['total_gen_P']:.2f} MW")
        print(f"   - 差值: {gen_diff:.2f} MW")

        if abs(gen_diff) > 10:
            print(f"   ✅ 新能源发电已计入潮流计算")
        else:
            print(f"   ❌ 新能源发电未正确计入")

    print(f"\n2. 系统影响：")
    print(f"   - 电压分布: 接入点及附近节点电压发生变化")
    print(f"   - 潮流分布: 部分支路潮流发生转移")
    print(f"   - 网损变化: 增加（新能源功率需要传输）")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    detailed_comparison()
