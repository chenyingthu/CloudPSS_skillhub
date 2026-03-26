#!/usr/bin/env python3
"""
使用真实Job ID完全真实测试后处理技能
- waveform_export: 真实导出CSV
- visualize: 真实生成PNG图像
"""

import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Job, setToken
import matplotlib.pyplot as plt

# 真实Job ID
JOB_ID = "5d5ac539-5767-4df7-a486-f3bd4d97ae38"
RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"

def test_waveform_export_real():
    """真实导出波形数据到CSV"""
    print("\n" + "="*70)
    print("真实测试: waveform_export")
    print("="*70)

    # 获取Job结果
    print(f"1. 获取Job结果 (ID: {JOB_ID})...")
    job = Job.fetch(JOB_ID)
    result = job.result
    print(f"   ✓ 结果获取成功")

    # 获取通道数据
    print("\n2. 提取通道数据...")
    channels = result.getPlotChannelNames(0)
    print(f"   ✓ 找到 {len(channels)} 个通道")

    # 真实导出CSV
    print("\n3. 导出CSV文件...")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    all_data = {}
    time_array = None

    for ch in channels:
        data = result.getPlotChannelData(0, ch)
        all_data[ch] = data['y']
        if time_array is None:
            time_array = data['x']
        print(f"   ✓ 通道 '{ch}': {len(data['y'])} 数据点")

    # 写入CSV
    csv_path = f"{RESULTS_DIR}/ieee3_waveforms_{JOB_ID[:8]}.csv"
    with open(csv_path, 'w') as f:
        # 写入header
        f.write("time," + ",".join(channels) + "\n")
        # 写入数据
        for i in range(len(time_array)):
            row = [str(time_array[i])]
            for ch in channels:
                row.append(str(all_data[ch][i]))
            f.write(",".join(row) + "\n")

    print(f"   ✓ CSV导出成功: {csv_path}")
    print(f"   ✓ 文件大小: {os.path.getsize(csv_path)} bytes")

    return True


def test_visualize_real():
    """真实生成可视化图像"""
    print("\n" + "="*70)
    print("真实测试: visualize")
    print("="*70)

    # 获取Job结果
    print(f"1. 获取Job结果 (ID: {JOB_ID})...")
    job = Job.fetch(JOB_ID)
    result = job.result
    print(f"   ✓ 结果获取成功")

    # 获取通道数据
    print("\n2. 提取通道数据...")
    channels = result.getPlotChannelNames(0)
    print(f"   ✓ 找到 {len(channels)} 个通道")

    # 真实生成图像
    print("\n3. 生成PNG图像...")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    fig, axes = plt.subplots(len(channels), 1, figsize=(12, 3*len(channels)))
    if len(channels) == 1:
        axes = [axes]

    for idx, ch in enumerate(channels):
        data = result.getPlotChannelData(0, ch)
        axes[idx].plot(data['x'], data['y'], linewidth=0.8)
        axes[idx].set_title(f'Channel: {ch}')
        axes[idx].set_xlabel('Time (s)')
        axes[idx].set_ylabel('Value (pu)')
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    png_path = f"{RESULTS_DIR}/ieee3_waveforms_{JOB_ID[:8]}.png"
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"   ✓ PNG生成成功: {png_path}")
    print(f"   ✓ 文件大小: {os.path.getsize(png_path)} bytes")

    return True


def main():
    print("="*70)
    print("真实后处理技能测试")
    print(f"使用Job ID: {JOB_ID}")
    print(f"开始时间: {datetime.now()}")
    print("="*70)

    # 加载token
    token_path = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token")
    token = token_path.read_text().strip()
    setToken(token)
    print(f"\n✓ Token已加载 ({len(token)} 字符)")

    results = {}

    # 测试waveform_export
    try:
        results['waveform_export'] = test_waveform_export_real()
    except Exception as e:
        print(f"\n✗ waveform_export 失败: {e}")
        import traceback
        traceback.print_exc()
        results['waveform_export'] = False

    # 测试visualize
    try:
        results['visualize'] = test_visualize_real()
    except Exception as e:
        print(f"\n✗ visualize 失败: {e}")
        import traceback
        traceback.print_exc()
        results['visualize'] = False

    # 汇总
    print("\n" + "="*70)
    print("真实后处理测试总结")
    print("="*70)

    for skill, ok in results.items():
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"  {skill}: {status}")

    passed = sum(results.values())
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print(f"\n✅ 所有后处理技能真实执行成功！")
        print(f"   输出目录: {RESULTS_DIR}")
        print(f"   真实文件已生成，可验证")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
