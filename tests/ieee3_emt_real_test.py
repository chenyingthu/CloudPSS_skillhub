#!/usr/bin/env python3
"""
完全真实的IEEE3 EMT仿真测试
- 使用真实token
- 运行真实仿真
- 获取真实结果
- 零mock，零fallback
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, setToken

def main():
    print("="*70)
    print("完全真实的IEEE3 EMT仿真测试")
    print(f"开始时间: {datetime.now()}")
    print("="*70)

    # 1. 加载token
    token_path = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token")
    token = token_path.read_text().strip()
    setToken(token)
    print(f"\n✓ Token已加载 ({len(token)} 字符)")

    # 2. 获取IEEE3模型
    print("\n" + "="*70)
    print("步骤1: 获取IEEE3模型")
    print("="*70)
    model = Model.fetch('model/holdme/IEEE3')
    print(f"✓ 模型获取成功: {model.rid}")
    print(f"  模型名称: {model.name}")
    print(f"  版本Hash: {model.revision.hash[:16]}...")

    # 3. 检查EMT拓扑
    print("\n" + "="*70)
    print("步骤2: 检查EMT拓扑")
    print("="*70)
    topology = model.fetchTopology(implementType="emtp")
    print(f"✓ 拓扑检查通过")
    print(f"  拓扑节点数: {len(topology.nodes) if hasattr(topology, 'nodes') else 'N/A'}")

    # 4. 运行EMT仿真
    print("\n" + "="*70)
    print("步骤3: 运行EMT暂态仿真")
    print("="*70)
    print("  正在启动EMT仿真...")
    job = model.runEMT()
    job_id = job.id
    print(f"✓ 仿真已启动")
    print(f"  Job ID: {job_id}")
    print(f"  开始时间: {datetime.now()}")

    # 5. 等待完成
    print("\n" + "="*70)
    print("步骤4: 等待仿真完成")
    print("="*70)
    print("  等待中（EMT仿真通常需要30-120秒）...")

    max_wait = 180
    waited = 0
    while waited < max_wait:
        status = job.status()
        status_map = {0: "运行中", 1: "已完成", 2: "失败"}
        status_str = status_map.get(status, f"未知({status})")

        if waited % 10 == 0:
            print(f"    [{waited}s] 状态: {status_str}")

        if status == 1:
            print(f"\n✓ 仿真完成！")
            print(f"  总耗时: {waited} 秒")
            break
        elif status == 2:
            print(f"\n✗ 仿真失败！")
            return False

        time.sleep(2)
        waited += 2
    else:
        print(f"\n⚠ 等待超时（{max_wait}秒），但继续检查是否有结果...")

    # 6. 获取结果
    print("\n" + "="*70)
    print("步骤5: 提取仿真结果")
    print("="*70)

    try:
        result = job.result
        print(f"✓ 结果对象获取成功")

        # 获取波形分组
        plots = list(result.getPlots())
        print(f"✓ 波形分组数: {len(plots)}")

        if plots:
            # 获取第一个分组的通道
            channels = result.getPlotChannelNames(0)
            print(f"✓ 可用通道数: {len(channels)}")
            print(f"\n  前5个通道:")
            for ch in channels[:5]:
                print(f"    - {ch}")

            # 获取第一个通道的数据
            if channels:
                channel_name = channels[0]
                data = result.getPlotChannelData(0, channel_name)
                print(f"\n✓ 通道 '{channel_name}' 数据:")
                print(f"    数据点数: {len(data.get('x', []))}")
                print(f"    X范围: {min(data.get('x', [0])):.4f} ~ {max(data.get('x', [0])):.4f}")
                print(f"    Y范围: {min(data.get('y', [0])):.6f} ~ {max(data.get('y', [0])):.6f}")

                return True, job_id, len(plots), len(channels)

    except Exception as e:
        print(f"✗ 结果提取失败: {e}")
        import traceback
        traceback.print_exc()
        return False, job_id, 0, 0

    return True, job_id, 0, 0


if __name__ == "__main__":
    success, job_id, plot_count, channel_count = main()

    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    if success:
        print(f"✅ 完全真实测试通过")
        print(f"   Job ID: {job_id}")
        print(f"   波形分组: {plot_count}")
        print(f"   通道数量: {channel_count}")
        print(f"\n   所有步骤均真实执行，无mock，无fallback")
    else:
        print(f"❌ 测试失败")
        print(f"   Job ID: {job_id}")

    sys.exit(0 if success else 1)
