"""
对比可视化技能示例

演示如何使用 compare_visualization 技能生成多场景对比图表。
"""

import yaml
from pathlib import Path

from cloudpss import Model, setToken
from cloudpss_skills import SkillExecutor


def run_fault_comparison():
    """运行故障场景对比可视化"""

    # 配置
    config = {
        "skill": "compare_visualization",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "sources": [
            {
                "job_id": "your-base-job-id",  # 替换为实际的Job ID
                "label": "基态",
                "color": "#2E86AB"
            },
            {
                "job_id": "your-fault-job-id",  # 替换为实际的Job ID
                "label": "三相故障",
                "color": "#A23B72"
            },
            {
                "job_id": "your-delayed-job-id",  # 替换为实际的Job ID
                "label": "延迟切除",
                "color": "#F18F01"
            }
        ],
        "compare": {
            "channels": ["Bus7_V", "Bus8_V", "Bus2_V"],
            "metrics": ["max", "min", "mean"],
            "time_range": {
                "start": 0.0,
                "end": 3.0
            }
        },
        "charts": {
            "time_series": {
                "enabled": True,
                "per_channel": False,
                "title": "故障场景电压对比"
            },
            "bar_chart": {
                "enabled": True,
                "group_by": "metric",
                "title": "电压指标对比"
            },
            "heatmap": {
                "enabled": True,
                "metric": "min",
                "title": "电压跌落热力图"
            },
            "radar": {
                "enabled": True,
                "title": "综合响应评估"
            }
        },
        "output": {
            "format": "png",
            "path": "./results/",
            "filename_prefix": "fault_comparison",
            "dpi": 150,
            "width": 14,
            "height": 8
        }
    }

    # 保存配置
    config_path = Path("config_compare_visualization.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"配置已保存: {config_path}")
    print("\n请修改配置文件中的 job_id 为实际的仿真任务ID")
    print("然后运行: python -m cloudpss_skills run --config config_compare_visualization.yaml")


if __name__ == "__main__":
    run_fault_comparison()
