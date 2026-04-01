# 组件目录技能 (component_catalog)

## 功能概述

获取 CloudPSS 平台上所有可用的元件模型 RID 和描述，支持按标签过滤、名称搜索，导出为 JSON/CSV 格式。

## 核心特性

- ✅ **全面发现**: 获取平台上所有可用组件（已发现 1049 个模型）
- ✅ **智能过滤**: 支持标签、名称正则、所有者多维度过滤
- ✅ **批量导出**: 支持 JSON、CSV、Console 三种输出格式
- ✅ **统计分组**: 按标签分组统计，快速了解组件分布

## 实际应用案例

### 发现保护组件

使用此技能成功发现了 **12个保护相关组件**：

```
1. 多边形距离保护判断元件 (model/wyl2000/DistanceProtectPolygon)
2. 零序电压保护(接零序PT) (model/wyl2000/zero_sequenceOV)
3. 经方向零序电流保护new (model/wyl2000/ZeroSequenceCurrentProtection)
4. 零序电流保护(接外接电流) (model/wyl2000/zero_sequence)
5. 电流保护new (model/wyl2000/over_current_protection)
6. 距离保护new (model/wyl2000/DistanceProtection)
7. 母线差动保护new (model/wyl2000/DifferentialProtection_BUS)
8. 纵联差动保护new (model/wyl2000/DifferentialProtection)
9. 复压过流保护new (model/wyl2000/CompoundVoltageOverCurrentProtection)
10. 差动保护 (model/CloudPSS/DifferentialProtection)
11. 复压过流保护 (model/CloudPSS/CompoundVoltageOverCurrentProtection)
12. 零序电压保护 (model/CloudPSS/ZeroSequenceOverVoltageProtection)
```

### 发现新能源组件

常用新能源组件 RID：

| 组件名称 | RID |
|---------|-----|
| 光伏发电站 | `model/CloudPSS/PVStation` |
| DFIG风电场等值模型 | `model/CloudPSS/DFIG_WindFarm_Equivalent_Model` |
| 风电场电源 | `model/CloudPSS/WGSource` |
| 光伏外部控制 | `model/CloudPSS/PVStation_external_ctrl` |
| DFIG外部控制 | `model/CloudPSS/DFIG_external_ctrl` |
| WGSource外部控制 | `model/CloudPSS/WGSource_external_ctrl` |

## 配置说明

```yaml
skill: component_catalog

auth:
  token_file: .cloudpss_token

filters:
  # 按标签过滤（可选）
  tags:
    - project-category:component

  # 按名称正则表达式过滤（可选）
  name_pattern: ".*PV.*"

  # 按所有者过滤（可选）
  owner: "*"

options:
  page_size: 1000
  max_results: 100
  include_details: true

output:
  format: json  # json, csv, console
  path: ./components.json
  group_by_tag: false
```

## 过滤器说明

### 1. 按标签过滤

只获取指定标签的组件：

```yaml
filters:
  tags:
    - project-category:component  # 标准组件
    - project-category:project    # 项目/算例
    - type:renewable              # 新能源
    - type:protection             # 保护装置
```

### 2. 按名称正则表达式过滤

使用正则表达式按名称过滤：

```yaml
filters:
  # 名称包含"光伏"
  name_pattern: ".*光伏.*"

  # 名称以"IEEE"开头
  name_pattern: "^IEEE.*"

  # 名称包含"PV"或"Wind"
  name_pattern: ".*PV.*|.*Wind.*"

  # 保护相关组件
  name_pattern: ".*保护.*|.*Relay.*|.*protection.*"
```

### 3. 按所有者过滤

```yaml
filters:
  owner: "holdme"  # 只获取指定用户的组件
  owner: "*"       # 获取所有用户的组件
```

## 输出格式

### Console 格式（默认）

直接输出到控制台：

```
CloudPSS 组件目录 (共 575 个)
================================================================================

1. 光伏发电站
   RID: model/CloudPSS/PVStation
   标签: project-category:component, type:renewable
   描述: 光伏发电站模型

2. 双馈风电场等值模型
   RID: model/CloudPSS/DFIG_WindFarm_Equivalent_Model
   标签: project-category:component, type:renewable
   描述: DFIG风电场等值模型
```

### JSON 格式

```json
[
  {
    "name": "光伏发电站",
    "rid": "model/CloudPSS/PVStation",
    "description": "光伏发电站模型",
    "tags": ["project-category:component", "type:renewable"],
    "owner": "holdme"
  }
]
```

### CSV 格式

```csv
名称,RID,描述,标签,所有者
光伏发电站,model/CloudPSS/PVStation,光伏发电站模型,project-category:component;type:renewable,holdme
```

## 使用示例

### 示例1: 获取所有组件

```yaml
skill: component_catalog

auth:
  token_file: .cloudpss_token

output:
  format: console
```

### 示例2: 获取所有标准组件

```yaml
skill: component_catalog

filters:
  tags:
    - project-category:component

output:
  format: json
  path: ./standard_components.json
```

### 示例3: 搜索新能源组件

```yaml
skill: component_catalog

filters:
  tags:
    - project-category:component
  name_pattern: ".*光伏|.*风电|.*PV|.*Wind.*"

output:
  format: json
  path: ./renewable_components.json
  group_by_tag: true
```

### 示例4: 获取保护装置组件（实际使用）

```yaml
skill: component_catalog

filters:
  tags:
    - project-category:component
  name_pattern: ".*保护.*|.*Relay.*|.*protection.*|.*relay.*"

output:
  format: console
  group_by_tag: false
```

## 输出结果

### 成功响应

```json
{
  "total_fetched": 1049,
  "filtered_count": 575,
  "output_path": "./components.json",
  "tag_statistics": {
    "project-category:component": 575,
    "type:renewable": 15,
    "type:protection": 12
  },
  "components": [
    {
      "name": "光伏发电站",
      "rid": "model/CloudPSS/PVStation",
      "description": "光伏发电站模型",
      "tags": ["project-category:component", "type:renewable"],
      "owner": "holdme"
    }
  ]
}
```

## 常用标签

| 标签 | 说明 | 发现数量 |
|------|------|---------|
| project-category:component | 标准组件 | 575 |
| project-category:project | 项目/算例 | ~400 |
| type:renewable | 新能源 | 15 |
| type:protection | 保护装置 | 12 |
| type:generator | 发电机 | 8 |
| type:transmission | 输电设备 | 10 |

## 技术实现

### 获取组件列表

```python
def _fetch_components(self, config: Dict) -> List[ComponentInfo]:
    from cloudpss import Model

    options = config.get("options", {})
    page_size = options.get("page_size", 1000)
    owner = config.get("filters", {}).get("owner", "*")

    # 使用 fetchMany 获取所有模型
    models = Model.fetchMany(pageSize=page_size, owner=owner)

    # 转换为 ComponentInfo
    components = []
    for m in models:
        comp = ComponentInfo(
            name=m.get("name", ""),
            rid=m.get("rid", ""),
            description=m.get("description", ""),
            tags=m.get("tags", []),
            owner=m.get("owner", ""),
            updated_at=m.get("updatedAt", "")
        )
        components.append(comp)

    return components
```

### 应用过滤器

```python
def _apply_filters(self, components: List[ComponentInfo], filters: Dict) -> List[ComponentInfo]:
    result = components

    # 按标签过滤
    tags = filters.get("tags", [])
    if tags:
        result = [
            c for c in result
            if any(tag in c.tags for tag in tags)
        ]

    # 按名称正则表达式过滤
    pattern = filters.get("name_pattern")
    if pattern:
        regex = re.compile(pattern, re.IGNORECASE)
        result = [
            c for c in result
            if regex.search(c.name)
        ]

    return result
```

## 注意事项

1. **API 限制**: `page_size` 最大支持 999999，但建议设置合理值避免超时
2. **详细信息**: `include_details` 会逐个获取模型拓扑，较慢但信息更完整
3. **权限**: 需要有效的 CloudPSS token 才能获取组件列表
4. **过滤性能**: 建议先使用标签过滤减少数据量，再用名称过滤

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 获取失败 | Token 无效 | 检查 `.cloudpss_token` 文件 |
| 无结果显示 | 过滤器太严格 | 放宽过滤条件 |
| 超时 | page_size 太大 | 减小 page_size |
| 权限不足 | 无访问权限 | 联系管理员获取权限 |

## 配套技能

- **[model_builder](model_builder.md)**: 使用发现的 RID 创建测试算例
- **[model_validator](model_validator.md)**: 验证创建的模型有效性
