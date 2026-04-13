# Model Hub 算例中心

## 设计背景

在电力系统仿真研究中，用户通常需要：
1. 使用多个 CloudPSS 服务器（如公共云、内部服务器）
2. 管理多个算例（IEEE 标准算例、项目算例、测试算例）
3. 在不同服务器之间同步算例
4. 保持本地算例备份

`model_hub` 技能提供了一个统一的算例管理中心，支持多服务器、多算例的统一管理。

## 功能特性

### 1. 服务器管理
- 添加/移除 CloudPSS 服务器
- 多服务器 Token 管理
- 快速切换当前服务器
- 服务器优先级配置

### 2. 算例注册表
- 算例名称到 RID 的映射
- 跨服务器 RID 记录
- 算例元数据（描述、标签）
- 版本历史追踪

### 3. 本地算例库
- 本地 YAML 格式存储
- 自动备份到 `~/.cloudpss-hub/models/`
- 元数据文件管理
- 导入/导出功能

### 4. 跨服务器同步
- `push`: 本地算例上传到服务器
- `pull`: 服务器算例下载到本地
- `clone`: 跨服务器复制算例
- `sync`: 批量同步算例

## 快速开始

### 初始化算例中心

```yaml
# config.yaml
skill: model_hub
action: init
```

### 添加服务器

```yaml
# 添加公共云服务器
skill: model_hub
action: add_server
server:
  name: public_cloud
  url: https://cloudpss.net
  token_file: .cloudpss_token
  priority: 1

---
# 添加内部服务器
skill: model_hub
action: add_server
server:
  name: internal_cloud
  url: http://166.111.60.76:50001
  token_file: .cloudpss_token_internal
  priority: 2
```

### 切换服务器

```yaml
skill: model_hub
action: use_server
server:
  name: public_cloud
```

### 查看状态

```yaml
skill: model_hub
action: status
```

输出示例：
```
当前服务器: public_cloud
已配置服务器: 2
已注册算例: 5
```

## 配置 Schema

```yaml
skill: model_hub                    # 技能名称 (必需)
action: init | status | list_servers | add_server | remove_server | use_server | 
       list_models | list_local | list_remote | push | pull | clone | sync |
       register | unregister | info | export | import

# 服务器配置 (add_server, remove_server, use_server)
server:
  name: string                      # 服务器名称
  url: string                       # 服务器地址
  token_file: string                # Token 文件路径
  token: string                     # Token 值 (可选)
  priority: integer                 # 优先级 (默认: 10)

# 算例配置
model:
  name: string                      # 算例名称
  rid: string                       # 算例 RID
  local_path: string                # 本地路径
  source_server: string             # 源服务器
  target_server: string             # 目标服务器
  description: string               # 描述
  tags: [string]                   # 标签
  force: boolean                    # 强制覆盖 (默认: false)

# 输出配置
output:
  format: json | yaml               # 输出格式
  path: string                      # 输出目录
```

## Agent 使用指南

### 场景 1: 配置新的测试环境

```yaml
# 1. 初始化
skill: model_hub
action: init

# 2. 添加服务器
skill: model_hub
action: add_server
server:
  name: test_server
  url: https://cloudpss.net
  token_file: .cloudpss_token

# 3. 注册测试算例
skill: model_hub
action: register
model:
  name: IEEE39
  rid: model/holdme/IEEE39
  source_server: test_server
  description: IEEE 39节点标准测试系统
  tags: [ieee, standard, 39-bus]
```

### 场景 2: 下载服务器算例到本地

```yaml
skill: model_hub
action: pull
model:
  name: IEEE39
  rid: model/holdme/IEEE39
  source_server: public_cloud
```

### 场景 3: 上传本地算例到服务器

```yaml
skill: model_hub
action: push
model:
  name: my_custom_model
  target_server: internal_cloud
  force: true  # 覆盖已存在的算例
```

### 场景 4: 跨服务器克隆

```yaml
skill: model_hub
action: clone
model:
  rid: model/holdme/IEEE39
  name: IEEE39_backup
  source_server: public_cloud
  target_server: internal_cloud
```

### 场景 5: 查看算例信息

```yaml
skill: model_hub
action: info
model:
  name: IEEE39
```

输出示例：
```json
{
  "name": "IEEE39",
  "rids": {
    "public_cloud": "model/holdme/IEEE39",
    "internal_cloud": "model/chenying/IEEE39"
  },
  "metadata": {
    "description": "IEEE 39节点标准测试系统",
    "tags": ["ieee", "standard"]
  },
  "local_exists": true,
  "local_path": "~/.cloudpss-hub/models/IEEE39"
}
```

## 输出结果

### status 操作

```json
{
  "hub_dir": "~/.cloudpss-hub",
  "current_server": {
    "name": "public_cloud",
    "url": "https://cloudpss.net",
    "token": "***",
    "priority": 1
  },
  "servers": [...],
  "model_count": 5,
  "models": [...]
}
```

### push/pull 操作

```json
{
  "status": "uploaded",
  "name": "IEEE39",
  "rid": "model/holdme/IEEE39",
  "server": "public_cloud"
}
```

### clone 操作

```json
{
  "status": "cloned",
  "name": "IEEE39_backup",
  "source_rid": "model/holdme/IEEE39",
  "target_rid": "model/chenying/IEEE39"
}
```

## 与其他技能的关联

### 与 model_creator 的关系
- `model_hub` 负责管理算例的存储和同步
- `model_creator` 负责创建新算例
- 创建的新算例可以通过 `model_hub` 注册和同步

### 与 model_validator 的关系
- `model_hub` 提供算例的获取接口
- `model_validator` 验证算例的有效性
- 验证结果可以更新到 `model_hub` 的元数据中

### 与 study_pipeline 的关系
- `study_pipeline` 可以调用 `model_hub` 来准备算例
- 使用 `model_hub` 确保所有步骤使用正确版本的算例

## 性能特点

- **本地操作**: 注册表读写、列表查询 < 100ms
- **网络操作**: push/pull/clone 取决于网络和算例大小
- **批量同步**: sync 操作支持多算例并行同步

## 常见问题

### Q: 如何处理 Token 过期？
A: 更新对应的 Token 文件，然后运行 `add_server` 重新配置。

### Q: 本地算例和服务器算例冲突怎么办？
A: 使用 `force: true` 强制覆盖，或使用 `clone` 创建新副本。

### Q: 如何备份整个算例库？
A: 直接备份 `~/.cloudpss-hub/` 目录即可。

### Q: 能否在多个设备间同步算例库？
A: 可以将 `~/.cloudpss-hub/` 目录放入 Git 进行版本控制。

## 完整示例

### 完整的工作流程

```yaml
# Step 1: 初始化
skill: model_hub
action: init

# Step 2: 配置多个服务器
skill: model_hub
action: add_server
server:
  name: public
  url: https://cloudpss.net
  token_file: .cloudpss_token

skill: model_hub
action: add_server
server:
  name: internal
  url: http://166.111.60.76:50001
  token_file: .cloudpss_token_internal

# Step 3: 下载标准算例到本地
skill: model_hub
action: pull
model:
  name: IEEE39
  rid: model/holdme/IEEE39
  source_server: public

skill: model_hub
action: pull
model:
  name: IEEE3
  rid: model/holdme/IEEE3
  source_server: public

# Step 4: 修改本地算例后上传
skill: model_hub
action: push
model:
  name: IEEE39
  target_server: internal
  force: true

# Step 5: 查看同步结果
skill: model_hub
action: info
model:
  name: IEEE39
```

## 目录结构

```
~/.cloudpss-hub/
├── config.yaml          # 服务器配置
│   ├── servers:
│   │   ├── public:
│   │   │   ├── url: https://cloudpss.net
│   │   │   ├── token: ***
│   │   │   └── priority: 1
│   │   └── internal:
│   │       ├── url: http://166.111.60.76:50001
│   │       ├── token_file: .cloudpss_token_internal
│   │       └── priority: 2
│   └── current_server: public
│
├── registry.yaml        # 算例注册表
│   ├── IEEE39:
│   │   ├── rids:
│   │   │   ├── public: model/holdme/IEEE39
│   │   │   └── internal: model/chenying/IEEE39
│   │   └── metadata:
│   │       ├── description: IEEE 39节点标准测试系统
│   │       └── tags: [ieee, standard]
│   └── IEEE3:
│       └── ...
│
└── models/             # 本地算例库
    ├── IEEE39/
    │   ├── model.yaml  # 算例数据
    │   └── meta.yaml   # 元数据
    └── IEEE3/
        ├── model.yaml
        └── meta.yaml
```
