"""
元数据注册表单元测试
"""

import json
import pytest
import tempfile
from pathlib import Path

from cloudpss_skills.metadata.registry import (
    ComponentMetadataRegistry,
    get_registry,
    reset_registry,
    RegistryStats
)
from cloudpss_skills.metadata.models import (
    ComponentMetadata,
    Parameter,
    ParameterGroup,
    PinDefinition
)


class TestComponentMetadataRegistry:
    """组件元数据注册表测试"""

    def setup_method(self):
        """每个测试方法前重置注册表"""
        reset_registry()
        self.registry = ComponentMetadataRegistry()

    def test_register_component(self):
        """测试注册组件"""
        metadata = ComponentMetadata(
            component_id='model/test/component1',
            name='测试组件1',
            category='test'
        )

        self.registry.register(metadata)
        assert 'model/test/component1' in self.registry
        assert self.registry.has_component('model/test/component1')

    def test_unregister_component(self):
        """测试注销组件"""
        metadata = ComponentMetadata(
            component_id='model/test/component2',
            name='测试组件2'
        )

        self.registry.register(metadata)
        assert self.registry.unregister('model/test/component2') is True
        assert 'model/test/component2' not in self.registry
        assert self.registry.unregister('model/test/component2') is False

    def test_get_component(self):
        """测试获取组件"""
        metadata = ComponentMetadata(
            component_id='model/test/component3',
            name='测试组件3',
            description='用于测试的组件'
        )

        self.registry.register(metadata)
        retrieved = self.registry.get_component('model/test/component3')
        assert retrieved is not None
        assert retrieved.name == '测试组件3'
        assert retrieved.description == '用于测试的组件'

        # 获取不存在的组件
        assert self.registry.get_component('nonexistent') is None

    def test_list_components(self):
        """测试列出组件"""
        # 注册多个组件
        for i in range(3):
            self.registry.register(ComponentMetadata(
                component_id=f'model/test/comp{i}',
                name=f'组件{i}',
                category='category_a' if i < 2 else 'category_b'
            ))

        # 列出所有组件
        all_components = self.registry.list_components()
        assert len(all_components) == 3

        # 按类别过滤
        category_a = self.registry.list_components(category='category_a')
        assert len(category_a) == 2

        category_b = self.registry.list_components(category='category_b')
        assert len(category_b) == 1

    def test_get_components_by_category(self):
        """测试按类别获取组件"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp1',
            name='组件1',
            category='renewable'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp2',
            name='组件2',
            category='renewable'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp3',
            name='组件3',
            category='generator'
        ))

        renewable = self.registry.get_components_by_category('renewable')
        assert len(renewable) == 2
        assert all(c.category == 'renewable' for c in renewable)

    def test_search(self):
        """测试搜索功能"""
        self.registry.register(ComponentMetadata(
            component_id='model/CloudPSS/WGSource',
            name='风场等值模型',
            description='风场等值模型I：PMSG网侧变流器模型'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/CloudPSS/PVSource',
            name='光伏等值模型',
            description='光伏发电等值模型'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/test/Load',
            name='负荷模型',
            description='综合负荷模型'
        ))

        # 按ID搜索
        results = self.registry.search('WGSource')
        assert len(results) == 1
        assert results[0].component_id == 'model/CloudPSS/WGSource'

        # 按名称搜索
        results = self.registry.search('风场')
        assert len(results) == 1
        assert '风场' in results[0].name

        # 按描述搜索
        results = self.registry.search('等值模型')
        assert len(results) == 2

    def test_load_from_file_single(self):
        """测试从文件加载单个组件"""
        metadata = ComponentMetadata(
            component_id='model/test/single',
            name='单组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='p1', display_name='参数1', type='real')
                    ]
                )
            ]
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f)
            temp_path = f.name

        try:
            count = self.registry.load_from_file(temp_path)
            assert count == 1
            assert self.registry.has_component('model/test/single')
        finally:
            Path(temp_path).unlink()

    def test_load_from_file_list(self):
        """测试从文件加载组件列表"""
        data = {
            'components': [
                ComponentMetadata(
                    component_id=f'model/test/comp{i}',
                    name=f'组件{i}'
                ).to_dict()
                for i in range(3)
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            count = self.registry.load_from_file(temp_path)
            assert count == 3
            assert len(self.registry) == 3
        finally:
            Path(temp_path).unlink()

    def test_load_from_file_not_found(self):
        """测试加载不存在的文件"""
        with pytest.raises(FileNotFoundError):
            self.registry.load_from_file('/nonexistent/path/file.json')

    def test_load_from_directory(self):
        """测试从目录加载"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建几个JSON文件
            for i in range(3):
                metadata = ComponentMetadata(
                    component_id=f'model/test/comp{i}',
                    name=f'组件{i}'
                )
                filepath = Path(temp_dir) / f'comp{i}.json'
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(metadata.to_dict(), f)

            count = self.registry.load_from_directory(temp_dir)
            assert count == 3
            assert len(self.registry) == 3

    def test_save_to_file(self):
        """测试保存到文件"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp1',
            name='组件1'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp2',
            name='组件2'
        ))

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            self.registry.save_to_file(temp_path)

            # 验证文件内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert 'components' in data
            assert len(data['components']) == 2
        finally:
            Path(temp_path).unlink()

    def test_export_component(self):
        """测试导出单个组件"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/export',
            name='导出测试组件'
        ))

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            success = self.registry.export_component('model/test/export', temp_path)
            assert success is True

            # 验证文件内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert data['component_id'] == 'model/test/export'
            assert data['name'] == '导出测试组件'

            # 导出不存在的组件
            success = self.registry.export_component('nonexistent', temp_path)
            assert success is False
        finally:
            Path(temp_path).unlink()

    def test_get_stats(self):
        """测试获取统计信息"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp1',
            name='组件1',
            category='category_a'
        ))
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp2',
            name='组件2',
            category='category_b'
        ))

        stats = self.registry.get_stats()
        assert isinstance(stats, RegistryStats)
        assert stats.total_components == 2
        assert 'category_a' in stats.categories
        assert 'category_b' in stats.categories

    def test_clear(self):
        """测试清空注册表"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp',
            name='组件'
        ))

        assert len(self.registry) == 1
        self.registry.clear()
        assert len(self.registry) == 0
        assert 'model/test/comp' not in self.registry

    def test_len(self):
        """测试__len__方法"""
        assert len(self.registry) == 0

        self.registry.register(ComponentMetadata(
            component_id='model/test/comp',
            name='组件'
        ))
        assert len(self.registry) == 1

    def test_contains(self):
        """测试__contains__方法"""
        self.registry.register(ComponentMetadata(
            component_id='model/test/comp',
            name='组件'
        ))

        assert 'model/test/comp' in self.registry
        assert 'nonexistent' not in self.registry


class TestGlobalRegistry:
    """全局注册表测试"""

    def setup_method(self):
        """重置全局注册表"""
        reset_registry()

    def test_get_registry_singleton(self):
        """测试全局注册表单例"""
        registry1 = get_registry()
        registry2 = get_registry()
        assert registry1 is registry2

    def test_reset_registry(self):
        """测试重置全局注册表"""
        registry = get_registry()
        registry.register(ComponentMetadata(
            component_id='model/test/comp',
            name='组件'
        ))
        assert 'model/test/comp' in registry

        reset_registry()
        registry2 = get_registry()
        assert 'model/test/comp' not in registry2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
