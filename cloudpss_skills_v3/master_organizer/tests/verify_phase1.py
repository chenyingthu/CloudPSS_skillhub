#!/usr/bin/env python3
"""
Phase 1 验证脚本 - 验证核心基础设施
"""

import sys
import tempfile
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType, validate_id,
    PathManager,
    ConfigManager,
    MockCryptoManager
)


def test_id_generator():
    """测试 ID 生成器"""
    print("🧪 测试 ID 生成器...")

    # 测试生成各种ID
    case_id = IDGenerator.generate(EntityType.CASE)
    print(f"  算例ID: {case_id}")
    assert case_id.startswith("case_")

    task_id = IDGenerator.generate(EntityType.TASK)
    print(f"  任务ID: {task_id}")
    assert task_id.startswith("task_")

    server_id = IDGenerator.generate(EntityType.SERVER)
    print(f"  服务器ID: {server_id}")
    assert server_id.startswith("server_")

    # 测试验证
    assert validate_id(case_id, EntityType.CASE)
    assert not validate_id("invalid_id")

    print("✅ ID 生成器测试通过")


def test_path_manager():
    """测试路径管理器"""
    print("🧪 测试路径管理器...")

    with tempfile.TemporaryDirectory() as temp_dir:
        pm = PathManager(temp_dir)

        # 检查目录结构
        assert pm.config_dir.exists()
        assert pm.registry_dir.exists()
        assert pm.cases_dir.exists()
        print(f"  配置目录: {pm.config_dir}")
        print(f"  算例目录: {pm.cases_dir}")

        # 测试路径生成
        case_id = "case_20260430_143052_a3f7b2d9"
        case_path = pm.get_case_path(case_id)
        assert str(case_path).endswith(case_id)
        print(f"  算例路径: {case_path}")

    print("✅ 路径管理器测试通过")


def test_config_manager():
    """测试配置管理器"""
    print("🧪 测试配置管理器...")

    with tempfile.TemporaryDirectory() as temp_dir:
        cm = ConfigManager(temp_dir)

        # 测试保存和加载
        test_data = {"name": "test", "value": 123}
        cm.save("test_config", test_data)

        loaded = cm.load("test_config")
        assert loaded == test_data
        print(f"  配置数据: {loaded}")

        # 测试用户配置
        config = cm.get_user_config()
        assert config.api_version == "v1.0"
        print(f"  用户配置版本: {config.api_version}")

    print("✅ 配置管理器测试通过")


def test_crypto_manager():
    """测试加密管理器"""
    print("🧪 测试加密管理器...")

    cm = MockCryptoManager()

    # 测试加密解密
    plaintext = "secret_token_123"
    ciphertext = cm.encrypt(plaintext)
    decrypted = cm.decrypt(ciphertext)

    assert decrypted == plaintext
    print(f"  原文: {plaintext}")
    print(f"  密文: {ciphertext}")
    print(f"  解密: {decrypted}")

    print("✅ 加密管理器测试通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Phase 1 核心基础设施验证")
    print("=" * 60)

    try:
        test_id_generator()
        test_path_manager()
        test_config_manager()
        test_crypto_manager()

        print("=" * 60)
        print("✅ 所有 Phase 1 基础设施自检通过")
        print("=" * 60)
        return 0

    except Exception as e:
        print("=" * 60)
        print(f"❌ 测试失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
