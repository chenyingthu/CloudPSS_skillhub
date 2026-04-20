#!/usr/bin/env python3
"""
完全真实的result_compare测试
使用同一job对象避免plot数据丢失问题
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, setToken
import numpy as np

RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"


def run_emt_and_compare():
    """运行两个EMT仿真并直接对比结果"""
    print("="*70)
    print("完全真实的result_compare测试")
    print(f"时间: {datetime.now()}")
    print("="*70)

    # 加载token
    token = Path(".cloudpss_token").read_text().strip()
    setToken(token)

    results = []

    # 运行两个EMT仿真
    for case_num in [1, 2]:
        print(f"\n{'='*70}")
        print(f"运行EMT仿真 Case {case_num}")
        print('='*70)

        model = Model.fetch("model/holdme/IEEE3")
        job = model.runEMT()
        print(f"Job ID: {job.id}")

        # 等待完成
        print("等待完成...", end="", flush=True)
        for i in range(60):
            status = job.status()
            if status == 1:
                print(f" ✓ ({(i+1)*2}s)")
                break
            elif status == 2:
                print(" ✗ 失败")
                return False
            time.sleep(2)
        else:
            print(" ⚠ 超时")
            return False

        # 立即获取结果（关键：使用同一个job对象）
        result = job.result
        plots = list(result.getPlots())
        print(f"波形分组数: {len(plots)}")

        # 收集所有通道数据
        channels_data = {}
        for plot_idx in range(len(plots)):
            channel_names = result.getPlotChannelNames(plot_idx)
            print(f"  Plot {plot_idx}: {len(channel_names)} 个通道")

            for channel in channel_names:
                channel_data = result.getPlotChannelData(plot_idx, channel)
                if channel_data:
                    y_values = channel_data.get('y', [])
                    if y_values:
                        arr = np.array(y_values)
                        channels_data[channel] = {
                            "max": float(np.max(arr)),
                            "min": float(np.min(arr)),
                            "mean": float(np.mean(arr)),
                            "rms": float(np.sqrt(np.mean(arr**2))),
                        }

        results.append({
            "label": f"Case_{case_num}",
            "job_id": job.id,
            "channels": channels_data,
        })

        print(f"✓ Case {case_num} 完成，收集 {len(channels_data)} 个通道")

    # 生成对比报告
    print("\n" + "="*70)
    print("生成对比报告")
    print("="*70)

    # 收集所有通道名
    all_channels = set()
    for r in results:
        all_channels.update(r["channels"].keys())

    print(f"总通道数: {len(all_channels)}")

    # 对比每个通道
    comparison = {}
    for channel in sorted(all_channels):
        channel_comparison = {}

        for metric in ["max", "min", "mean", "rms"]:
            values = {}
            for r in results:
                val = r["channels"].get(channel, {}).get(metric)
                if val is not None:
                    values[r["label"]] = val

            if values:
                channel_comparison[metric] = {
                    "values": values,
                    "max": max(values.values()),
                    "min": min(values.values()),
                    "diff": max(values.values()) - min(values.values()),
                }

        comparison[channel] = channel_comparison

    # 导出Markdown报告
    report_path = f"{RESULTS_DIR}/comparison_direct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    lines = [
        "# 仿真结果对比报告（完全真实）",
        "",
        f"生成时间: {datetime.now().isoformat()}",
        "",
        "## 对比概览",
        "",
        f"- 对比任务数: {len(results)}",
        f"- 对比通道数: {len(all_channels)}",
        "",
        "## 任务列表",
        "",
    ]

    for r in results:
        lines.append(f"- **{r['label']}**: `{r['job_id']}`")

    lines.extend(["", "## 通道对比", ""])

    for channel, channel_data in sorted(comparison.items()):
        lines.append(f"### {channel}")
        lines.append("")

        for metric, metric_data in channel_data.items():
            lines.append(f"**{metric.upper()}**:")
            lines.append("")
            lines.append("| 任务 | 值 |")
            lines.append("|------|-----|")

            for label, value in metric_data["values"].items():
                lines.append(f"| {label} | {value:.6f} |")

            lines.append("")
            lines.append(f"- 范围: [{metric_data['min']:.6f}, {metric_data['max']:.6f}]")
            lines.append(f"- 差值: {metric_data['diff']:.6f}")
            lines.append("")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"\n✓ 报告已保存: {report_path}")

    # 显示摘要
    print("\n" + "="*70)
    print("对比摘要")
    print("="*70)

    for channel in list(sorted(all_channels))[:5]:
        if channel in comparison:
            print(f"\n{channel}:")
            for metric, data in comparison[channel].items():
                print(f"  {metric}: diff={data['diff']:.6f}")

    print("\n" + "="*70)
    print("✅ 完全真实测试完成！")
    print("="*70)
    print(f"对比了 {len(results)} 个真实EMT仿真结果")
    print(f"总共 {len(all_channels)} 个通道")
    print(f"报告: {report_path}")

    return True


if __name__ == "__main__":
    success = run_emt_and_compare()
    sys.exit(0 if success else 1)
