"""
加密模块 - 收纳大师计划核心组件

提供安全的认证信息存储，使用 AES-256-GCM 加密。
确保服务器 token 等敏感信息不会明文存储。
"""

import base64
import os
from pathlib import Path
from typing import Optional, Union


class CryptoManager:
    """
    加密管理器

    使用 AES-256-GCM 加密敏感数据，确保认证信息安全存储。
    密钥存储在用户主目录，与加密数据分离。
    """

    KEY_FILE = ".cloudpss_key"
    KEY_SIZE = 32  # 256 bits for AES-256

    def __init__(self, key_path: Optional[Path] = None):
        """
        初始化加密管理器

        Args:
            key_path: 密钥文件路径，默认为 ~/.cloudpss_key
        """
        if key_path:
            self._key_path = Path(key_path).expanduser()
        else:
            self._key_path = Path.home() / self.KEY_FILE

        self._key: Optional[bytes] = None

    def _get_or_create_key(self) -> bytes:
        """获取或创建加密密钥"""
        if self._key is not None:
            return self._key

        if self._key_path.exists():
            # 读取现有密钥
            with open(self._key_path, 'rb') as f:
                self._key = base64.b64decode(f.read())
        else:
            # 生成新密钥
            self._key = os.urandom(self.KEY_SIZE)
            # 保存密钥
            self._key_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._key_path, 'wb') as f:
                f.write(base64.b64encode(self._key))
            # 设置文件权限（仅限 Unix）
            if os.name != 'nt':
                os.chmod(self._key_path, 0o600)

        return self._key

    def encrypt(self, plaintext: str) -> str:
        """
        加密字符串

        Args:
            plaintext: 明文

        Returns:
            加密后的 Base64 字符串格式：nonce:ciphertext:tag

        Example:
            >>> cm = CryptoManager()
            >>> encrypted = cm.encrypt("secret_token")
            >>> decrypted = cm.decrypt(encrypted)
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            raise ImportError(
                "cryptography package is required. "
                "Install with: pip install cryptography"
            )

        key = self._get_or_create_key()
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # 96 bits for GCM
        plaintext_bytes = plaintext.encode('utf-8')

        # 加密（返回 ciphertext + tag）
        ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)

        # 组合：nonce + ciphertext
        # ciphertext 的最后 16 字节是 authentication tag
        encrypted = nonce + ciphertext

        # Base64 编码
        return base64.b64encode(encrypted).decode('ascii')

    def decrypt(self, ciphertext: str) -> str:
        """
        解密字符串

        Args:
            ciphertext: 加密后的 Base64 字符串

        Returns:
            解密后的明文

        Raises:
            ValueError: 解密失败（密钥错误或数据损坏）
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            raise ImportError(
                "cryptography package is required. "
                "Install with: pip install cryptography"
            )

        try:
            key = self._get_or_create_key()
            aesgcm = AESGCM(key)

            # Base64 解码
            encrypted = base64.b64decode(ciphertext.encode('ascii'))

            # 分离 nonce 和 ciphertext
            nonce = encrypted[:12]
            ciphertext_bytes = encrypted[12:]

            # 解密
            plaintext = aesgcm.decrypt(nonce, ciphertext_bytes, None)

            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    def encrypt_dict(self, data: dict) -> dict:
        """
        加密字典中的敏感字段

        Args:
            data: 包含敏感字段的字典

        Returns:
            加密后的字典，敏感字段以 ENC: 前缀标记
        """
        encrypted = {}
        for key, value in data.items():
            if isinstance(value, str) and value:
                # 加密所有非空字符串值
                encrypted[key] = f"ENC:{self.encrypt(value)}"
            elif isinstance(value, dict):
                encrypted[key] = self.encrypt_dict(value)
            else:
                encrypted[key] = value
        return encrypted

    def decrypt_dict(self, data: dict) -> dict:
        """
        解密字典中的加密字段

        Args:
            data: 包含加密字段的字典

        Returns:
            解密后的字典
        """
        decrypted = {}
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("ENC:"):
                # 解密
                encrypted = value[4:]  # 去掉 "ENC:" 前缀
                decrypted[key] = self.decrypt(encrypted)
            elif isinstance(value, dict):
                decrypted[key] = self.decrypt_dict(value)
            else:
                decrypted[key] = value
        return decrypted

    def rotate_key(self) -> bool:
        """
        轮换加密密钥

        生成新密钥并重新加密所有数据。
        返回是否成功。

        Note: 此方法需要在调用方控制下使用，
              因为需要访问所有加密数据。
        """
        # 备份旧密钥
        old_key = self._get_or_create_key()
        old_key_path = self._key_path

        # 生成新密钥
        new_key = os.urandom(self.KEY_SIZE)

        try:
            # 这里需要调用方提供重新加密逻辑
            # 我们只是准备新密钥
            backup_path = old_key_path.with_suffix('.key.backup')
            old_key_path.rename(backup_path)

            # 保存新密钥
            with open(old_key_path, 'wb') as f:
                f.write(base64.b64encode(new_key))
            if os.name != 'nt':
                os.chmod(old_key_path, 0o600)

            # 更新当前密钥
            self._key = new_key

            return True
        except Exception:
            # 恢复旧密钥
            if backup_path.exists():
                backup_path.rename(old_key_path)
            self._key = old_key
            return False


class MockCryptoManager:
    """
    模拟加密管理器（用于测试或 cryptograph 未安装时）

    仅做 base64 编码，不提供真正加密。
    生产环境必须使用 CryptoManager。
    """

    def __init__(self, key_path: Optional[Path] = None):
        self._key_path = key_path

    def encrypt(self, plaintext: str) -> str:
        """模拟加密（仅 base64）"""
        return f"MOCK:{base64.b64encode(plaintext.encode()).decode()}"

    def decrypt(self, ciphertext: str) -> str:
        """模拟解密"""
        if ciphertext.startswith("MOCK:"):
            return base64.b64decode(ciphertext[5:]).decode()
        return ciphertext

    def encrypt_dict(self, data: dict) -> dict:
        """模拟加密字典"""
        return {k: self.encrypt(v) if isinstance(v, str) else v
                for k, v in data.items()}

    def decrypt_dict(self, data: dict) -> dict:
        """模拟解密字典"""
        return {k: self.decrypt(v) if isinstance(v, str) and v.startswith("MOCK:") else v
                for k, v in data.items()}


def get_crypto_manager(key_path: Optional[Path] = None, *, allow_mock: bool = False) -> Union[CryptoManager, MockCryptoManager]:
    """
    获取加密管理器实例

    生产路径必须使用 CryptoManager。测试需要 mock 时显式传入
    allow_mock=True。
    """
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        del AESGCM
        return CryptoManager(key_path)
    except ImportError:
        if allow_mock:
            return MockCryptoManager(key_path)
        raise ImportError(
            "cryptography package is required for production encryption. "
            "Install with: pip install cryptography, or pass allow_mock=True "
            "only in tests."
        )
