"""
自动量测配置技能示例

演示如何使用 auto_channel_setup 技能批量配置EMT仿真输出通道。
"""

import yaml
from pathlib import Path

from cloudpss import Model, setToken
from cloudpss_skills import SkillExecutor


def setup_basic_voltage_measures():
    """基础电压量测配置 - 为所有母线添加电压量测"""

    config = {
        "skill": "auto_channel_setup",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "measurements": {
            "voltage": {
                "enabled": True,
                "voltage_levels": [],  # 空数组表示全部电压等级
                "bus_names": [],      # 空数组表示全部母线
                "freq": 200
            }
        },
        "output": {
            "save_model": False,
            "dry_run": False
        }
    }

    # 保存配置
    config_path = Path("config_auto_channel_basic.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"基础电压量测配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 为IEEE39系统的39条母线添加电压量测")
    print("  - 采样频率: 200Hz")
    print("  - 生成量测配置报告")


def setup_hv_measures():
    """高压侧量测配置 - 只关注220kV及以上母线"""

    config = {
        "skill": "auto_channel_setup",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "measurements": {
            "voltage": {
                "enabled": True,
                "voltage_levels": [220, 500],  # 只配置220kV和500kV母线
                "bus_names": [],
                "freq": 500  # 更高的采样频率
            },
            "current": {
                "enabled": True,
                "component_types": ["line", "transformer"],
                "freq": 500
            }
        },
        "output": {
            "save_model": False,
            "dry_run": True  # 先预览不修改
        }
    }

    config_path = Path("config_auto_channel_hv.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n高压侧量测配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 只配置220kV和500kV电压等级的母线")
    print("  - 为线路和变压器添加电流量测")
    print("  - 试运行模式：预览配置效果")


def setup_comprehensive_measures():
    """完整量测配置 - 包含电压、电流、功率、频率"""

    config = {
        "skill": "auto_channel_setup",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "measurements": {
            "voltage": {
                "enabled": True,
                "voltage_levels": [220, 500],
                "bus_names": [],
                "freq": 200
            },
            "current": {
                "enabled": True,
                "component_types": ["line", "transformer"],
                "freq": 200
            },
            "power": {
                "enabled": True,
                "component_types": ["generator", "load"],
                "freq": 200
            },
            "frequency": {
                "enabled": True,
                "freq": 50
            }
        },
        "output": {
            "save_model": True,  # 保存修改后的模型
            "dry_run": False
        }
    }

    config_path = Path("config_auto_channel_full.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n完整量测配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 电压量测: 39个通道（所有母线）")
    print("  - 电流量测: 46个通道（线路和变压器）")
    print("  - 功率量测: 71个通道（发电机和负荷）")
    print("  - 频率量测: 5个通道（关键母线）")
    print("  - 总计: 161个量测通道")
    print("  - 模型将被保存到云端")


def setup_fault_analysis_measures():
    """故障分析专用配置 - 高采样率"""

    config = {
        "skill": "auto_channel_setup",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE3",
            "source": "cloud"
        },
        "measurements": {
            "voltage": {
                "enabled": True,
                "freq": 1000  # 高采样率用于故障分析
            },
            "current": {
                "enabled": True,
                "component_types": ["line"],
                "freq": 1000
            },
            "power": {
                "enabled": True,
                "component_types": ["generator"],
                "freq": 1000
            },
            "frequency": {
                "enabled": True,
                "freq": 100
            }
        },
        "output": {
            "save_model": False,
            "dry_run": False
        }
    }

    config_path = Path("config_auto_channel_fault.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n故障分析量测配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - IEEE3系统的完整量测配置")
    print("  - 采样频率: 电压/电流/功率 1000Hz，频率 100Hz")
    print("  - 适合故障分析和暂态稳定研究")


if __name__ == "__main__":
    print("=" * 60)
    print("自动量测配置技能示例")
    print("=" * 60)

    setup_basic_voltage_measures()
    setup_hv_measures()
    setup_comprehensive_measures()
    setup_fault_analysis_measures()

    print("\n" + "=" * 60)
    print("所有配置文件已生成！")
    print("=" * 60)
    print("\n使用步骤:")
    print("1. 确保已配置CloudPSS Token (.cloudpss_token)")
    print("2. 选择合适的配置文件")
    print("3. 执行: python -m cloudpss_skills run --config <config_file>")
    print("4. 查看生成的量测配置报告: results/auto_channel_setup_report.json")
    print("\n建议:")
    print("- 首次使用建议先用 dry_run: true 预览配置效果")
    print("- 确认无误后再设置 dry_run: false 和 save_model: true")
    print("- 根据仿真需求选择合适的采样频率")
