# 组件目录技能 (component_catalog)

## 功能概述

获取 CloudPSS 平台上所有可用的元件模型 RID 和描述，支持按标签过滤、名称搜索，导出为 JSON/CSV 格式。

## 适用场景

- 查找可用元件模型
- 获取组件 RID 参考
- 批量导出组件列表
- 了解平台支持的组件类型

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
  max_results: 100  # 可选
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
    - project-category:project    # 项目
```

### 2. 按名称过滤

使用正则表达式按名称过滤：

```yaml
filters:
  name_pattern: ".*光伏.*"  # 名称包含"光伏"
  name_pattern: "^IEEE.*"   # 名称以"IEEE"开头
  name_pattern: ".*PV.*|.*光伏.*"  # 名称包含"PV"或"光伏"
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
CloudPSS 组件目录 (共 150 个)
================================================================================

1. 光伏发电站
   RID: model/CloudPSS/PVStation
   标签: project-category:component, type:renewable
   描述: 光伏发电站模型 (组件数: 596)

2. 双馈风电场等值模型
   RID: model/CloudPSS/DFIG_WindFarm_Equivalent_Model
   标签: project-category:component, type:renewable
   描述: DFIG风电场等值模型 (组件数: 856)
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

### 示例2: 获取所有标准组件并导出为 JSON

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

### 示例4: 获取保护装置组件

```yaml
skill: component_catalog

filters:
  tags:
    - project-category:component
  name_pattern: ".*保护|.*Relay.*"

output:
  format: csv
  path: ./protection_components.csv
```

## 输出结果

### 成功响应

```json
{
  "total_fetched": 1000,
  "filtered_count": 150,
  "output_path": "./components.json",
  "tag_statistics": {
    "project-category:component": 120,
    "type:renewable": 15,
    "type:protection": 10
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

| 标签 | 说明 |
|------|------|
| project-category:component | 标准组件 |
| project-category:project | 项目/算例 |
| type:renewable | 新能源 |
| type:protection | 保护装置 |
| type:generator | 发电机 |
| type:transmission | 输电设备 |

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
