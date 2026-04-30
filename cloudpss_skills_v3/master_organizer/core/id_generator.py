"""
ID 生成器 - 收纳大师计划核心组件

生成符合规范的实体ID:
{entity}_{YYYYMMDD}_{HHMMSS}_{hash8}

实体类型:
- server_{hash8}
- case_{YYYYMMDD}_{HHMMSS}_{hash8}
- task_{YYYYMMDD}_{HHMMSS}_{hash8}
- result_{YYYYMMDD}_{HHMMSS}_{hash8}
- variant_{hash8}
"""

import re
import secrets
from datetime import datetime
from enum import Enum
from typing import Optional


class EntityType(Enum):
    """实体类型枚举"""
    SERVER = "server"
    CASE = "case"
    TASK = "task"
    RESULT = "result"
    VARIANT = "variant"


class IDGenerator:
    """
    ID 生成器

    遵循收纳大师命名规范，确保全局唯一性和可读性。
    """

    # ID 格式验证正则表达式
    ID_PATTERNS = {
        EntityType.SERVER: r"^server_[a-f0-9]{8}$",
        EntityType.CASE: r"^case_[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$",
        EntityType.TASK: r"^task_[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$",
        EntityType.RESULT: r"^result_[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$",
        EntityType.VARIANT: r"^variant_[a-f0-9]{8}$",
    }

    @staticmethod
    def generate(
        entity_type: EntityType,
        timestamp: Optional[datetime] = None
    ) -> str:
        """
        生成实体ID

        Args:
            entity_type: 实体类型
            timestamp: 可选的时间戳，默认为当前时间

        Returns:
            符合规范的实体ID

        Example:
            >>> IDGenerator.generate(EntityType.CASE)
            'case_20260430_143052_a3f7b2d9'
        """
        if timestamp is None:
            timestamp = datetime.now()

        hash_part = secrets.token_hex(4)  # 8位十六进制

        if entity_type in (EntityType.SERVER, EntityType.VARIANT):
            # server 和 variant 使用简化格式
            return f"{entity_type.value}_{hash_part}"
        else:
            # case, task, result 使用时间戳格式
            date_part = timestamp.strftime("%Y%m%d")
            time_part = timestamp.strftime("%H%M%S")
            return f"{entity_type.value}_{date_part}_{time_part}_{hash_part}"

    @staticmethod
    def validate(entity_id: str, entity_type: Optional[EntityType] = None) -> bool:
        """
        验证ID格式

        Args:
            entity_id: 待验证的ID
            entity_type: 可选的实体类型，如果提供则验证类型匹配

        Returns:
            ID格式是否正确
        """
        if not entity_id or not isinstance(entity_id, str):
            return False

        if entity_type:
            pattern = IDGenerator.ID_PATTERNS.get(entity_type)
            if not pattern:
                return False
            return bool(re.match(pattern, entity_id))
        else:
            # 验证是否为任何一种有效ID
            for pattern in IDGenerator.ID_PATTERNS.values():
                if re.match(pattern, entity_id):
                    return True
            return False

    @staticmethod
    def parse(entity_id: str) -> Optional[dict]:
        """
        解析ID获取元信息

        Args:
            entity_id: 实体ID

        Returns:
            包含实体类型和时间信息的字典，如果ID无效则返回None
        """
        if not IDGenerator.validate(entity_id):
            return None

        parts = entity_id.split("_")
        entity_type_str = parts[0]

        try:
            entity_type = EntityType(entity_type_str)
        except ValueError:
            return None

        result = {
            "entity_type": entity_type,
            "entity_id": entity_id,
        }

        # 对于有时间戳的实体，解析时间
        if entity_type in (EntityType.CASE, EntityType.TASK, EntityType.RESULT):
            if len(parts) >= 4:
                try:
                    date_str = parts[1]
                    time_str = parts[2]
                    result["created_at"] = datetime.strptime(
                        f"{date_str}_{time_str}",
                        "%Y%m%d_%H%M%S"
                    )
                except ValueError:
                    pass

        return result

    @staticmethod
    def get_entity_type(entity_id: str) -> Optional[EntityType]:
        """
        获取ID对应的实体类型

        Args:
            entity_id: 实体ID

        Returns:
            实体类型，如果ID无效则返回None
        """
        parsed = IDGenerator.parse(entity_id)
        return parsed.get("entity_type") if parsed else None


# 便捷函数
def generate_id(entity_type: EntityType, timestamp: Optional[datetime] = None) -> str:
    """便捷函数：生成ID"""
    return IDGenerator.generate(entity_type, timestamp)


def validate_id(entity_id: str, entity_type: Optional[EntityType] = None) -> bool:
    """便捷函数：验证ID"""
    return IDGenerator.validate(entity_id, entity_type)


def parse_id(entity_id: str) -> Optional[dict]:
    """便捷函数：解析ID"""
    return IDGenerator.parse(entity_id)
