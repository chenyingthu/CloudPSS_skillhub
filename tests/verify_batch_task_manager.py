"""
验证批量任务管理技能

使用方法:
    python verify_batch_task_manager.py
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import BatchTaskManagerSkill
from cloudpss_skills.builtin.batch_task_manager import BatchTask, TaskStatus

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_skill_initialization():
    """测试技能初始化"""
    logger.info("=" * 60)
    logger.info("测试技能初始化")
    logger.info("=" * 60)

    skill = BatchTaskManagerSkill()

    logger.info(f"技能名称: {skill.name}")
    logger.info(f"技能描述: {skill.description}")

    # 测试配置验证
    valid_config = {
        "tasks": [
            {"name": "task1", "type": "emt"},
            {"name": "task2", "type": "power_flow"}
        ]
    }

    result = skill.validate(valid_config)
    assert result.valid, f"有效配置应该通过验证: {result.errors}"
    logger.info("✓ 配置验证通过")

    # 测试无效配置
    invalid_config = {}
    result = skill.validate(invalid_config)
    assert not result.valid, "空配置应该验证失败"
    logger.info("✓ 无效配置正确识别")

    return True


def test_config_schema():
    """测试配置Schema"""
    logger.info("=" * 60)
    logger.info("测试配置Schema")
    logger.info("=" * 60)

    skill = BatchTaskManagerSkill()
    schema = skill.config_schema

    logger.info(f"配置Schema属性数: {len(schema.get('properties', {}))}")

    # 检查必需的配置项
    assert "tasks" in schema["required"], "tasks应该是必需的"
    assert "execution" in schema["properties"], "应该有execution配置"
    assert "output" in schema["properties"], "应该有output配置"

    logger.info("✓ Schema结构正确")
    return True


def test_task_creation():
    """测试任务创建"""
    logger.info("=" * 60)
    logger.info("测试任务创建")
    logger.info("=" * 60)

    skill = BatchTaskManagerSkill()

    # 测试N-1任务创建
    n1_tasks = skill.create_n1_tasks(
        model_rid="model/holdme/IEEE39",
        bus_labels=["Bus_16", "Bus_15"],
        line_keys=["line_1", "line_2", "line_3"]
    )

    logger.info(f"创建的N-1任务数: {len(n1_tasks)}")
    for task in n1_tasks:
        logger.info(f"  - {task['name']}: {task['type']}")

    assert len(n1_tasks) == 3, "应该有3个N-1任务"

    # 测试VSI任务创建
    vsi_tasks = skill.create_vsi_tasks(
        model_rid="model/holdme/IEEE39",
        bus_labels=["Bus_16", "Bus_15", "Bus_26"]
    )

    logger.info(f"创建的VSI任务数: {len(vsi_tasks)}")
    for task in vsi_tasks:
        logger.info(f"  - {task['name']}: {task['type']}, end_time={task['config']['end_time']}")

    assert len(vsi_tasks) == 3, "应该有3个VSI任务"

    logger.info("✓ 任务创建测试通过")
    return True


def test_batch_task_dataclass():
    """测试BatchTask数据类"""
    logger.info("=" * 60)
    logger.info("测试BatchTask数据类")
    logger.info("=" * 60)

    task = BatchTask(
        task_id="task_001",
        name="测试任务",
        task_type="emt",
        config={"end_time": 10.0},
        max_retries=3
    )

    logger.info(f"任务ID: {task.task_id}")
    logger.info(f"任务名称: {task.name}")
    logger.info(f"任务类型: {task.task_type}")
    logger.info(f"初始状态: {task.status.value}")
    logger.info(f"最大重试: {task.max_retries}")

    assert task.status == TaskStatus.PENDING, "初始状态应为PENDING"
    assert task.retry_count == 0, "初始重试次数应为0"

    logger.info("✓ BatchTask数据类测试通过")
    return True


def main():
    """主测试函数"""
    logger.info("批量任务管理技能验证")
    logger.info("=" * 60)

    tests = [
        ("技能初始化", test_skill_initialization),
        ("配置Schema", test_config_schema),
        ("任务创建", test_task_creation),
        ("BatchTask数据类", test_batch_task_dataclass),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            logger.info(f"\n运行测试: {name}")
            if test_func():
                passed += 1
                logger.info(f"✓ {name} 通过")
            else:
                failed += 1
                logger.error(f"✗ {name} 失败")
        except Exception as e:
            failed += 1
            logger.error(f"✗ {name} 失败: {e}", exc_info=True)

    logger.info("\n" + "=" * 60)
    logger.info(f"测试结果: {passed}/{len(tests)} 通过")
    logger.info("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
