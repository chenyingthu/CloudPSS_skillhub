#!/usr/bin/env python3
"""
完全真实的IEEE3 EMT测试 + 后处理
一次性运行仿真并立即处理结果，避免Job.fetch()导致数据丢失
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, setToken
import matplotlib.pyplot as plt

RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"


def run_emt_and_process():
    """运行EMT仿真并立即处理结果"""
    print("="*70)
    print("完全真实的IEEE3 EMT测试 + 后处理")
    print(f"开始时间: {datetime.now()}")
    print("="*70)

    # 1. 加载token
    token_path = Path(".cloudpss_token")
    token = token_path.read_text().strip()
    setToken(token)
    print(f"\n✓ Token已加载 ({len(token)} 字符)")

    # 2. 获取模型
    print("\n" + "="*70)
    print("步骤1: 获取IEEE3模型")
    print("="*70)
    model = Model.fetch('model/holdme/IEEE3')
    print(f"✓ 模型: {model.rid}")
    print(f"  名称: {model.name}")

    # 3. 运行EMT仿真
    print("\n" + "="*70)
    print("步骤2: 运行EMT仿真")
    print("="*70)
    print("  正在启动...")
    job = model.runEMT()
    job_id = job.id
    print(f"✓ 仿真已启动")
    print(f"  Job ID: {job_id}")

    # 4. 等待完成
    print("\n" + "="*70)
    print("步骤3: 等待仿真完成")
    print("="*70)
    print("  等待中...")

    waited = 0
    while waited < 120:
        status = job.status()
        if waited % 10 == 0:
            print(f"    [{waited}s] 状态: {status}")
        if status == 1:
            print(f"\n✓ 仿真完成（{waited}秒）")
            break
        elif status == 2:
            print("\n✗ 仿真失败")
            return False
        time.sleep(2)
        waited += 2
    else:
        print("\n⚠ 超时")
        return False

    # 5. 立即获取结果（必须在同一job对象上）
    print("\n" + "="*70)
    print("步骤4: 提取仿真结果")
    print("="*70)

    result = job.result
    plots = list(result.getPlots())
    print(f"✓ 波形分组数: {len(plots)}")

    if not plots:
        print("✗ 没有波形数据")
        return False

    # 获取第一个分组的通道
    channels = result.getPlotChannelNames(0)
    print(f"✓ 通道数: {len(channels)}")
    print(f"\n  通道列表:")
    for ch in channels:
        print(f"    - {ch}")

    # 6. 真实导出CSV
    print("\n" + "="*70)
    print("步骤5: 真实导出CSV (waveform_export)")
    print("="*70)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    all_data = {}
    time_array = None

    for ch in channels:
        data = result.getPlotChannelData(0, ch)
        all_data[ch] = data['y']
        if time_array is None:
            time_array = data['x']

    csv_path = f"{RESULTS_DIR}/ieee3_{job_id[:8]}.csv"
    with open(csv_path, 'w') as f:
        f.write("time," + ",".join(channels) + "\n")
        for i in range(len(time_array)):
            row = [str(time_array[i])]
            for ch in channels:
                row.append(str(all_data[ch][i]))
            f.write(",".join(row) + "\n")

    file_size = os.path.getsize(csv_path)
    print(f"✓ CSV导出成功")
    print(f"  路径: {csv_path}")
    print(f"  大小: {file_size:,} bytes")
    print(f"  行数: {len(time_array):,}")

    # 7. 真实生成PNG
    print("\n" + "="*70)
    print("步骤6: 真实生成图像 (visualize)")
    print("="*70)

    fig, axes = plt.subplots(len(channels), 1, figsize=(12, 3*len(channels)))
    if len(channels) == 1:
        axes = [axes]

    for idx, ch in enumerate(channels):
        data = result.getPlotChannelData(0, ch)
        axes[idx].plot(data['x'], data['y'], linewidth=0.8, label=ch)
        axes[idx].set_title(f'Channel: {ch}')
        axes[idx].set_xlabel('Time (s)')
        axes[idx].set_ylabel('Value (pu)')
        axes[idx].grid(True, alpha=0.3)
        axes[idx].legend()

    plt.tight_layout()
    png_path = f"{RESULTS_DIR}/ieee3_{job_id[:8]}.png"
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close()

    png_size = os.path.getsize(png_path)
    print(f"✓ PNG生成成功")
    print(f"  路径: {png_path}")
    print(f"  大小: {png_size:,} bytes")

    # 8. 汇总
    print("\n" + "="*70)
    print("完全真实测试总结")
    print("="*70)
    print(f"✅ EMT仿真: 成功")
    print(f"   Job ID: {job_id}")
    print(f"   耗时: {waited}秒")
    print(f"✅ 波形导出: 成功")
    print(f"   文件: {csv_path}")
    print(f"   大小: {file_size:,} bytes")
    print(f"✅ 可视化: 成功")
    print(f"   文件: {png_path}")
    print(f"   大小: {png_size:,} bytes")
    print(f"\n📝 所有步骤完全真实执行，无mock，无fallback")
    print(f"   输出文件可验证存在:")
    print(f"   - CSV: {os.path.exists(csv_path)}")
    print(f"   - PNG: {os.path.exists(png_path)}")

    return True


if __name__ == "__main__":
    success = run_emt_and_process()
    sys.exit(0 if success else 1)
