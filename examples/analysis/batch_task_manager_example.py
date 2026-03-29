"""
批量任务管理示例

演示如何使用 batch_task_manager 技能批量运行 CloudPSS 仿真任务。
支持并行/串行执行模式，自动状态轮询和结果回收。
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills import get_skill

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """基本使用示例"""
    logger.info("=" * 60)
    logger.info("示例: 基本使用")
    logger.info("=" * 60)

    skill = get_skill("batch_task_manager")

    # 配置任务
    config = {
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "tasks": [
            {
                "name": "Base_PowerFlow",
                "type": "power_flow",
                "config": {},
                "max_retries": 2
            },
            {
                "name": "EMT_Fault_Scenario",
                "type": "emt",
                "config": {
                    "end_time": 10.0,
                    "step_time": 0.0001
                },
                "max_retries": 1
            }
        ],
        "execution": {
            "mode": "parallel",
            "max_concurrent": 2,
            "polling_interval": 2.0,
            "timeout": 600.0,
            "enable_retry": True
        },
        "output": {
            "format": "json",
            "path": "./results/",
            "prefix": "batch_example",
            "save_partial": True
        }
    }

    # 验证配置
    validation = skill.validate(config)
    if not validation.valid:
        logger.error(f"配置验证失败: {validation.errors}")
        return

    logger.info("✓ 配置验证通过")
    logger.info(f"任务数量: {len(config['tasks'])}")
    logger.info(f"执行模式: {config['execution']['mode']}")
    logger.info(f"最大并发: {config['execution']['max_concurrent']}")

    # 注意: 实际运行需要 CloudPSS token
    # result = skill.run(config)
    # logger.info(f"执行结果: {result.status}")


def example_n1_tasks():
    """N-1分析任务示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 创建N-1分析任务")
    logger.info("=" * 60)

    skill = get_skill("batch_task_manager")

    # 创建N-1任务
    n1_tasks = skill.create_n1_tasks(
        model_rid="model/holdme/IEEE39",
        bus_labels=["Bus_16", "Bus_15", "Bus_26"],
        line_keys=["line_1", "line_2", "line_3", "line_4", "line_5"]
    )

    logger.info(f"创建了 {len(n1_tasks)} 个N-1任务")
    for task in n1_tasks:
        logger.info(f"  - {task['name']}: {task['type']}")

    # 构建完整配置
    config = {
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "tasks": n1_tasks,
        "execution": {
            "mode": "parallel",
            "max_concurrent": 5,
            "polling_interval": 2.0,
            "timeout": 300.0,
            "enable_retry": True
        },
        "output": {
            "format": "json",
            "path": "./results/",
            "prefix": "n1_batch"
        }
    }

    logger.info("✓ N-1任务配置已生成")
    logger.info("  可使用: python -m cloudpss_skills run --config config/batch_task_manager.yaml")


def example_vsi_tasks():
    """VSI弱母线分析任务示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 创建VSI测试任务")
    logger.info("=" * 60)

    skill = get_skill("batch_task_manager")

    # 创建VSI任务
    vsi_tasks = skill.create_vsi_tasks(
        model_rid="model/holdme/IEEE39",
        bus_labels=["Bus_16", "Bus_15", "Bus_26", "Bus_17", "Bus_18"]
    )

    logger.info(f"创建了 {len(vsi_tasks)} 个VSI任务")
    for task in vsi_tasks:
        logger.info(f"  - {task['name']}: {task['type']}, "
                   f"injection_time={task['config']['injection_time']}")

    # 构建完整配置
    config = {
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "tasks": vsi_tasks,
        "execution": {
            "mode": "sequential",  # EMT任务建议串行执行
            "polling_interval": 2.0,
            "timeout": 900.0,
            "enable_retry": True
        },
        "output": {
            "format": "json",
            "path": "./results/",
            "prefix": "vsi_batch"
        }
    }

    logger.info("✓ VSI任务配置已生成")
    logger.info("  执行模式: sequential (EMT任务建议串行)")


def example_sequential_mode():
    """串行执行模式示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 串行执行模式")
    logger.info("=" * 60)

    config = {
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "tasks": [
            {"name": f"Task_{i+1}", "type": "power_flow", "max_retries": 2}
            for i in range(5)
        ],
        "execution": {
            "mode": "sequential",  # 串行执行
            "polling_interval": 1.0,
            "timeout": 300.0,
            "enable_retry": True
        },
        "output": {
            "format": "json",
            "path": "./results/",
            "prefix": "sequential_batch"
        }
    }

    logger.info(f"任务数量: {len(config['tasks'])}")
    logger.info(f"执行模式: {config['execution']['mode']}")
    logger.info("  串行模式特点:")
    logger.info("    - 任务按顺序逐个执行")
    logger.info("    - 资源占用较低")
    logger.info("    - 适合资源受限环境")


def main():
    """主函数"""
    logger.info("批量任务管理技能示例")
    logger.info("=" * 60)

    examples = [
        ("基本使用", example_basic_usage),
        ("N-1任务创建", example_n1_tasks),
        ("VSI任务创建", example_vsi_tasks),
        ("串行执行模式", example_sequential_mode),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            logger.error(f"示例 '{name}' 失败: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("示例运行完成")
    logger.info("=" * 60)
    logger.info("\n提示: 实际运行需要有效的 CloudPSS token")
    logger.info("      配置 token 文件: .cloudpss_token")


if __name__ == "__main__":
    main()
