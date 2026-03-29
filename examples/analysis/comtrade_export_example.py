"""
COMTRADE导出技能示例

演示如何使用 comtrade_export 技能将EMT仿真结果导出为COMTRADE标准格式。
"""

import yaml
from pathlib import Path

from cloudpss import Model, setToken
from cloudpss_skills import SkillExecutor


def export_to_comtrade():
    """导出故障仿真结果为COMTRADE格式"""

    # 配置
    config = {
        "skill": "comtrade_export",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "source": {
            "job_id": "your-emt-job-id",  # 替换为实际的EMT Job ID
            "plot_index": 0
        },
        "comtrade": {
            "station_name": "IEEE39_Test",
            "rec_dev_id": "CloudPSS_EMT",
            "rev_year": 1999,
            "frequency": 50.0,
            "time_mult": 1.0
        },
        "channels": {
            "selected": [],  # 空数组表示导出所有通道
            "uu_map": {
                # 可以自定义单位映射
                # "Bus30_V": "kV",
                # "Gen1_P": "MW",
            },
            "ph_map": {
                # 可以自定义相别映射
                # "Bus30_V": "A",
            },
            "ratio_map": {
                # 可以自定义变比映射
                # "Bus30_V": [220.0, 1.0],
            }
        },
        "output": {
            "file_type": "BINARY",
            "path": "./results/",
            "filename": "fault_record"
        }
    }

    # 保存配置
    config_path = Path("config_comtrade_export.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"配置已保存: {config_path}")
    print("\n请修改配置文件中的 job_id 为实际的EMT仿真任务ID")
    print("然后运行: python -m cloudpss_skills run --config config_comtrade_export.yaml")
    print("\n生成的COMTRADE文件可用于:")
    print("  1. 导入OMICRON、Doble等继电保护测试仪")
    print("  2. 导入SEL、Beckwith等故障录波分析软件")
    print("  3. 与其他仿真平台（RTDS、PSCAD等）进行数据交换")


if __name__ == "__main__":
    export_to_comtrade()
