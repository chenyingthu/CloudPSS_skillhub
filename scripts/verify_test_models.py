#!/usr/bin/env python3
"""
验证测试算例

验证刚刚创建的测试算例是否可用。

运行: python scripts/verify_test_models.py
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss import setToken, Model


def verify_test_models():
    """验证测试算例"""

    # 加载创建的模型列表
    if not os.path.exists("test_models_created.json"):
        print("错误: 找不到 test_models_created.json 文件")
        return False

    with open("test_models_created.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    models = data.get("created", [])

    if not models:
        print("没有需要验证的模型")
        return True

    # 设置认证
    with open(".cloudpss_token", "r") as f:
        setToken(f.read().strip())

    print("=" * 60)
    print("验证测试算例")
    print("=" * 60)

    verified = []
    failed = []

    for i, model_info in enumerate(models, 1):
        print(f"\n[{i}/{len(models)}] 验证: {model_info['name']}")
        print(f"      RID: {model_info['rid']}")

        try:
            # 尝试获取模型
            model = Model.fetch(model_info['rid'])
            model_name = getattr(model, 'name', 'Unknown')
            print(f"      ✅ 成功获取模型")
            print(f"      模型名称: {model_name}")

            # 获取模型拓扑
            topology = model.fetchTopology()
            comp_count = len(topology.components) if hasattr(topology, 'components') else 0
            print(f"      组件数量: {comp_count}")

            verified.append({
                "name": model_info['name'],
                "rid": model_info['rid'],
                "model_name": model_name,
                "component_count": comp_count
            })

        except Exception as e:
            print(f"      ❌ 失败: {e}")
            failed.append({
                "name": model_info['name'],
                "rid": model_info['rid'],
                "error": str(e)
            })

    # 汇总结果
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)
    print(f"成功: {len(verified)} 个")
    print(f"失败: {len(failed)} 个")

    if failed:
        print("\n失败的算例:")
        for model in failed:
            print(f"  - {model['name']}: {model['error']}")

    # 保存验证结果
    with open("test_models_verified.json", "w", encoding="utf-8") as f:
        json.dump({
            "verified": verified,
            "failed": failed
        }, f, indent=2, ensure_ascii=False)

    print(f"\n验证结果已保存到 test_models_verified.json")

    return len(failed) == 0


if __name__ == "__main__":
    if not os.path.exists(".cloudpss_token"):
        print("错误: 需要 .cloudpss_token 文件进行认证")
        sys.exit(1)

    success = verify_test_models()
    sys.exit(0 if success else 1)
