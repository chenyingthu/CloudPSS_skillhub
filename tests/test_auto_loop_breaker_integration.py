#!/usr/bin/env python3
"""
Auto Loop Breaker Skill - 集成测试

测试自动解环技能的基本功能。
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 先导入builtin模块以注册技能
import cloudpss_skills.builtin
from cloudpss_skills import get_skill
from cloudpss_skills.core import ValidationResult


class TestAutoLoopBreakerConfig:
    """测试配置生成和验证"""

    def test_skill_registration(self):
        """测试技能是否正确注册"""
        skill = get_skill("auto_loop_breaker")
        assert skill is not None
        assert skill.name == "auto_loop_breaker"
        assert "解环" in skill.description or "loop" in skill.description.lower()

    def test_default_config_generation(self):
        """测试默认配置生成"""
        skill = get_skill("auto_loop_breaker")
        config = skill.get_default_config()

        assert config["skill"] == "auto_loop_breaker"
        assert "model" in config
        assert "algorithm" in config
        assert "loop_node" in config
        assert "output" in config

        # 验证算法默认配置
        assert config["algorithm"]["max_iterations"] == 500
        assert config["algorithm"]["strategy"] == "degree"

        # 验证解环点默认配置
        assert config["loop_node"]["init_value"] == "0"
        assert config["loop_node"]["name_prefix"] == "LoopBreaker"

    def test_config_schema_validation(self):
        """测试配置schema验证"""
        skill = get_skill("auto_loop_breaker")
        schema = skill.config_schema

        assert schema["type"] == "object"
        assert "model" in schema["properties"]
        assert "algorithm" in schema["properties"]
        assert "loop_node" in schema["properties"]
        assert "output" in schema["properties"]

        # 验证算法配置项
        algo_props = schema["properties"]["algorithm"]["properties"]
        assert "max_iterations" in algo_props
        assert "strategy" in algo_props
        assert "random_seed" in algo_props

    def test_empty_rid_validation(self):
        """测试空RID验证失败"""
        skill = get_skill("auto_loop_breaker")
        config = skill.get_default_config()
        config["model"]["rid"] = ""

        result = skill.validate(config)
        assert not result.valid
        assert any("rid" in error.lower() for error in result.errors)

    def test_valid_config_validation(self):
        """测试有效配置验证通过"""
        skill = get_skill("auto_loop_breaker")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        result = skill.validate(config)
        assert result.valid, f"验证失败: {result.errors}"

    def test_different_strategies(self):
        """测试不同算法策略"""
        skill = get_skill("auto_loop_breaker")

        strategies = ["degree", "random", "hybrid"]
        for strategy in strategies:
            config = skill.get_default_config()
            config["model"]["rid"] = "model/holdme/IEEE39"
            config["algorithm"]["strategy"] = strategy

            result = skill.validate(config)
            assert result.valid, f"策略 {strategy} 验证失败: {result.errors}"

    def test_custom_loop_node_config(self):
        """测试自定义解环点配置"""
        skill = get_skill("auto_loop_breaker")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["loop_node"]["init_value"] = "1.0"
        config["loop_node"]["name_prefix"] = "CustomBreaker"

        result = skill.validate(config)
        assert result.valid

    def test_dry_run_mode(self):
        """测试试运行模式"""
        skill = get_skill("auto_loop_breaker")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["output"]["dry_run"] = True

        result = skill.validate(config)
        assert result.valid


class TestAutoLoopBreakerGraphAlgorithm:
    """测试图论算法（不需要API）"""

    def test_fvs_algorithm_degree_strategy(self):
        """测试度数优先FVS算法"""
        try:
            import networkx as nx
        except ImportError:
            pytest.skip("需要networkx库")

        # 构建测试图（有环）
        g = nx.DiGraph()
        g.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)])

        # 验证有环
        assert not nx.is_directed_acyclic_graph(g)

        # 使用简单FVS算法
        skill = get_skill("auto_loop_breaker")
        fvs = skill._compute_fvs(g, max_iter=100, strategy="degree", random_seed=None)

        # 验证FVS打破了所有环
        g_copy = g.copy()
        g_copy.remove_nodes_from(fvs)
        assert nx.is_directed_acyclic_graph(g_copy), f"FVS未打破所有环: {fvs}"

    def test_fvs_algorithm_no_loops(self):
        """测试无环图"""
        try:
            import networkx as nx
        except ImportError:
            pytest.skip("需要networkx库")

        # 构建无环图
        g = nx.DiGraph()
        g.add_edges_from([(1, 2), (2, 3), (1, 3)])

        # 验证无环
        assert nx.is_directed_acyclic_graph(g)

        skill = get_skill("auto_loop_breaker")
        fvs = skill._compute_fvs(g, max_iter=100, strategy="degree", random_seed=None)

        # 无环图应该返回空FVS
        assert len(fvs) == 0, f"无环图不应有FVS: {fvs}"


@pytest.mark.integration
class TestAutoLoopBreakerIntegration:
    """集成测试 - 需要CloudPSS API访问"""

    def test_skill_loads_correctly(self):
        """测试技能正确加载"""
        skill = get_skill("auto_loop_breaker")
        assert skill is not None
        assert skill.name == "auto_loop_breaker"
        assert "解环" in skill.description or "loop" in skill.description.lower()

    def test_model_fetch_and_topology(self, live_auth, integration_model):
        """测试模型获取和拓扑分析（使用conftest fixtures）"""
        model = integration_model
        assert model is not None
        assert model.name is not None

        # 获取母线元件（用于后续拓扑分析）
        buses = model.getComponentsByRid("model/CloudPSS/_newBus_3p")
        assert len(buses) > 0, "模型应该包含母线"


if __name__ == "__main__":
    # 运行基本测试
    print("=" * 70)
    print("Auto Loop Breaker Skill - 配置测试")
    print("=" * 70)

    skill = get_skill("auto_loop_breaker")
    print(f"\n✓ 技能已注册: {skill.name}")
    print(f"✓ 技能描述: {skill.description}")

    # 测试配置验证
    config = skill.get_default_config()
    config["model"]["rid"] = "model/holdme/IEEE39"

    result = skill.validate(config)
    if result.valid:
        print("✓ 默认配置验证通过")
    else:
        print(f"✗ 配置验证失败: {result.errors}")

    # 测试不同策略
    strategies = ["degree", "random", "hybrid"]
    for strategy in strategies:
        config["algorithm"]["strategy"] = strategy
        result = skill.validate(config)
        if result.valid:
            print(f"✓ 策略 '{strategy}' 验证通过")
        else:
            print(f"✗ 策略 '{strategy}' 验证失败: {result.errors}")

    # 测试图论算法
    try:
        import networkx as nx

        g = nx.DiGraph()
        g.add_edges_from([(1, 2), (2, 3), (3, 1)])

        fvs = skill._compute_fvs(g, max_iter=100, strategy="degree", random_seed=None)
        g_copy = g.copy()
        g_copy.remove_nodes_from(fvs)

        if nx.is_directed_acyclic_graph(g_copy):
            print(f"✓ FVS算法测试通过 (FVS: {fvs})")
        else:
            print(f"✗ FVS算法测试失败")
    except ImportError:
        print("⚠ 跳过FVS算法测试 (需要networkx)")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
