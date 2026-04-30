"""
加密模块测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudpss_skills_v3.master_organizer.core import (
    CryptoManager, MockCryptoManager, get_crypto_manager
)


class TestMockCryptoManager:
    """模拟加密管理器测试"""

    def setup_method(self):
        self.cm = MockCryptoManager()

    def test_encrypt_decrypt(self):
        """测试加密解密"""
        plaintext = "test_secret"
        ciphertext = self.cm.encrypt(plaintext)
        decrypted = self.cm.decrypt(ciphertext)
        assert decrypted == plaintext

    def test_encrypt_empty_string(self):
        """测试加密空字符串"""
        ciphertext = self.cm.encrypt("")
        assert ciphertext.startswith("MOCK:")
        decrypted = self.cm.decrypt(ciphertext)
        assert decrypted == ""

    def test_decrypt_plaintext(self):
        """测试解密明文（未加密内容）"""
        plaintext = "not_encrypted"
        # MockCryptoManager 直接返回明文
        assert self.cm.decrypt(plaintext) == plaintext


class TestCryptoManagerReal:
    """真实加密管理器测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.key_path = self.temp_dir / "test.key"

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_key_generation(self):
        """测试密钥生成"""
        try:
            cm = CryptoManager(self.key_path)
            # 触发密钥生成
            key = cm._get_or_create_key()
            assert key is not None
            assert len(key) == 32  # AES-256

            # 密钥文件应已创建
            assert self.key_path.exists()
        except ImportError:
            pytest.skip("cryptography not installed")

    def test_key_persistence(self):
        """测试密钥持久化"""
        try:
            # 第一个实例生成密钥
            cm1 = CryptoManager(self.key_path)
            key1 = cm1._get_or_create_key()

            # 第二个实例应读取相同密钥
            cm2 = CryptoManager(self.key_path)
            key2 = cm2._get_or_create_key()

            assert key1 == key2
        except ImportError:
            pytest.skip("cryptography not installed")

    def test_encrypt_decrypt_roundtrip(self):
        """测试加密解密往返"""
        try:
            cm = CryptoManager(self.key_path)
            plaintext = "sensitive_data_123"
            ciphertext = cm.encrypt(plaintext)
            decrypted = cm.decrypt(ciphertext)
            assert decrypted == plaintext
        except ImportError:
            pytest.skip("cryptography not installed")


class TestCryptoManagerAdvanced:
    """加密管理器高级测试"""

    def setup_method(self):
        self.cm = MockCryptoManager()

    def test_encrypt_dict_flat(self):
        """测试扁平字典加密"""
        data = {
            "user": "admin",
            "password": "secret123",
            "token": "abc456"
        }
        encrypted = self.cm.encrypt_dict(data)

        # 验证所有字符串值被加密
        assert encrypted["user"].startswith("MOCK:")
        assert encrypted["password"].startswith("MOCK:")
        assert encrypted["token"].startswith("MOCK:")

        # 验证解密
        decrypted = self.cm.decrypt_dict(encrypted)
        assert decrypted == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
