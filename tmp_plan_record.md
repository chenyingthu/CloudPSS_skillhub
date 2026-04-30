📦 收纳大师计划：从零构建整洁体系

  第一原则：万物皆有定位，事事皆有流程

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                           收纳哲学                                      │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  1. 【分类明确】 每个数据对象必须有清晰的类别归属                        │
  │  2. 【定位唯一】 每个对象有且只有一个存放位置                            │
  │  3. 【命名规范】 所有命名遵循统一规则，一目了然                          │
  │  4. 【关联清晰】 对象之间的关系明确可追溯                                │
  │  5. 【生命周期】 每个对象有明确的创建、使用、归档、销毁流程                │
  │  6. 【可视整洁】 无论后台存储还是前端展示，都必须整洁有序                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ---
  第一章：数据模型定义

  1.1 核心实体分类

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        核心实体关系图                                    │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │   ┌──────────────┐                                                      │
  │   │   Server     │  ← 计算资源（多环境支持）                              │
  │   │   (服务器)    │                                                      │
  │   └──────┬───────┘                                                      │
  │          │ 1:N                                                          │
  │          ▼                                                              │
  │   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐           │
  │   │    Case      │────►│    Task      │────►│   Result     │           │
  │   │   (算例)      │ 1:N │   (任务)      │ 1:1 │   (结果)      │           │
  │   └──────────────┘     └──────────────┘     └──────────────┘           │
  │          │                                              │              │
  │          │ 1:N                                          │ 1:N          │
  │          ▼                                              ▼              │
  │   ┌──────────────┐                             ┌──────────────┐       │
  │   │   Variant    │                             │   Artifact   │       │
  │   │   (变体)      │                             │   (产物)      │       │
  │   └──────────────┘                             └──────────────┘       │
  │                                                                         │
  │   ┌──────────────┐     ┌──────────────┐                                │
  │   │  Workspace   │────►│   Session    │                                │
  │   │  (工作空间)   │ 1:N │   (会话)      │                                │
  │   └──────────────┘     └──────────────┘                                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  1.2 实体属性定义

  Server (服务器)

  entity: Server
  description: CloudPSS仿真服务器配置

  attributes:
    id: string              # 唯一标识 (server_id)
    name: string            # 显示名称 (production/testing/dev)
    url: string             # API地址 (https://cloudpss.net/)
    type: enum              # 类型: public/internal/enterprise

  auth:
    credential_id: string   # 凭据引用ID (指向加密存储)
    username: string        # 用户名 (从token解析缓存)
    expires_at: datetime    # Token过期时间

  capabilities:             # 服务器能力
    max_workers: integer    # 最大并行任务
    supported_skills: []    # 支持的技能列表
    storage_quota:          # 存储配额
      total: bytes
      used: bytes

  status:
    state: enum             # online/offline/maintenance
    last_check: datetime    # 最后健康检查时间
    latency_ms: integer     # 响应延迟

  Case (算例)

  entity: Case
  description: 电力系统仿真算例

  identity:
    case_id: string         # 全局唯一ID (case_{timestamp}_{hash})
    name: string            # 显示名称 (IEEE39/IEEE39_with_PV)
    version: string         # 版本号 (semver: 1.0.0)

  classification:
    domain: enum            # 领域: transmission/distribution/microgrid
    voltage_level: enum     # 电压等级: 10kV/35kV/110kV/220kV/500kV/1000kV
    analysis_type: []       # 适用分析类型: [powerflow, transient, emt]

  lineage:
    base_case_id: string    # 父算例ID (继承关系)
    created_from: enum      # 来源: scratch/import/clone/variant
    owner: string           # 所有者
    created_at: datetime    # 创建时间

  content:
    local_path: string      # 本地存储路径
    model_rid:              # 云端RID映射
      server_id: rid        # {server_name: rid}

  metadata:
    description: string     # 描述
    tags: []                # 标签
    components:             # 元件统计
      buses: integer
      lines: integer
      generators: integer

  Task (任务)

  entity: Task
  description: 仿真任务执行实例

  identity:
    task_id: string         # 全局唯一ID (task_{timestamp}_{hash})
    case_id: string         # 关联算例ID

  execution:
    skill: string           # 执行技能 (emt_simulation/n1_security)
    server_id: string       # 执行服务器
    job_id: string          # CloudPSS Job ID

  configuration:
    config_hash: string     # 配置哈希 (用于缓存和复现)
    config_snapshot: {}     # 配置快照 (完整配置)

  lifecycle:
    state: enum             # pending/submitted/running/completed/failed/cancelled
    created_at: datetime    # 创建时间
    submitted_at: datetime  # 提交时间
    started_at: datetime    # 开始时间
    completed_at: datetime  # 完成时间

  results:
    result_id: string       # 关联结果ID
    metrics: {}             # 执行指标 (duration/convergence/etc)

  Result (结果)

  entity: Result
  description: 仿真结果数据集

  identity:
    result_id: string       # 全局唯一ID (result_{timestamp}_{hash})
    task_id: string         # 关联任务ID
    case_id: string         # 关联算例ID

  classification:
    result_type: enum       # 类型: powerflow/emt/stability/frequency
    data_format: enum       # 格式: raw/processed/summary

  storage:
    local_path: string      # 本地存储路径
    size_bytes: integer     # 数据大小
    checksum: string        # 校验和

  content:
    artifacts: []           # 产物文件列表
    metrics: {}             # 关键指标
    summary: {}             # 结果摘要

  lifecycle:
    created_at: datetime    # 创建时间
    retention: datetime     # 保留期限
    archived: boolean       # 是否归档

  ---
  第二章：目录结构设计

  2.1 根目录布局

  ~/.cloudpss/
  ├── config/                    # 配置目录
  │   ├── servers.yaml           # 服务器配置
  │   ├── defaults.yaml          # 默认设置
  │   └── keys/                  # 加密密钥
  │       └── master.key
  │
  ├── registry/                  # 注册表目录
  │   ├── index.yaml             # 主索引
  │   ├── cases.yaml             # 算例注册表
  │   ├── tasks.yaml             # 任务注册表
  │   └── results.yaml           # 结果注册表
  │
  ├── cases/                     # 算例存储
  │   └── {case_id}/             # 每个算例独立目录
  │       ├── v{version}/        # 版本目录
  │       │   ├── model.yaml     # 算例定义
  │       │   ├── meta.yaml      # 元数据
  │       │   └── variants/      # 变体目录
  │       └── snapshots/         # 快照目录
  │
  ├── tasks/                     # 任务存储
  │   └── {year}/{month}/        # 按时间分层
  │       └── {task_id}/
  │           ├── config.yaml    # 任务配置
  │           ├── status.yaml    # 状态记录
  │           └── logs/          # 日志文件
  │
  ├── results/                   # 结果存储
  │   └── {case_id}/             # 按算例组织
  │       └── {result_id}/
  │           ├── meta.yaml      # 结果元数据
  │           ├── data/          # 数据文件
  │           │   ├── raw.h5     # 原始数据
  │           │   └── processed/ # 处理后数据
  │           ├── exports/       # 导出文件
  │           │   ├── waveforms.csv
  │           │   └── report.md
  │           └── viz/           # 可视化
  │
  ├── cache/                     # 缓存目录
  │   ├── models/                # 模型缓存
  │   ├── results/               # 结果缓存
  │   └── temp/                  # 临时文件
  │
  ├── logs/                      # 日志目录
  │   └── {year}/{month}/
  │       └── cloudpss-{date}.log
  │
  └── trash/                     # 回收站
      └── {deleted_at}/

  2.2 详细目录规范

  算例目录结构 (cases/)

  cases/
  └── case_20260401_103045_a1b2c3d4/     # case_id = case_{timestamp}_{hash8}
      ├── v1.0.0/                         # 版本目录 (semver)
      │   ├── model.yaml                  # 算例定义文件
      │   ├── meta.yaml                   # 算例元数据
      │   ├── diagram.png                 # 拓扑图
      │   └── README.md                   # 说明文档
      │
      ├── v1.1.0/                         # 新版本
      │   ├── model.yaml
      │   ├── meta.yaml
      │   └── variants/                   # 变体目录
      │       ├── variant_pv100mw/        # 具体变体
      │       │   ├── model.yaml
      │       │   └── delta.yaml          # 与父本的差异
      │       └── variant_pv200mw/
      │
      ├── snapshots/                      # 运行时快照
      │   └── 20260401_120000/
      │       └── model.yaml
      │
      └── results/ -> ../../results/case_20260401_103045_a1b2c3d4/  # 软链接

  结果目录结构 (results/)

  results/
  └── case_20260401_103045_a1b2c3d4/      # 与算例ID对应
      └── result_20260401_110000_e5f6g7h8/  # result_id
          ├── meta.yaml                   # 结果元数据 (关键!)
          ├── provenance.yaml             # 溯源信息
          │
          ├── data/
          │   ├── raw.h5                  # 原始数据 (HDF5)
          │   ├── processed/
          │   │   ├── voltages.csv
          │   │   └── currents.csv
          │   └── summary.json            # 摘要统计
          │
          ├── exports/                    # 导出文件
          │   ├── waveforms_20260401_110000.csv
          │   ├── comtrade_20260401_110000.cfg
          │   ├── comtrade_20260401_110000.dat
          │   └── report_20260401_110000.md
          │
          ├── viz/                        # 可视化
          │   ├── overview.png
          │   └── waveforms/
          │       ├── bus1_voltage.png
          │       └── bus2_voltage.png
          │
          └── logs/
              └── execution.log

  ---
  第三章：命名规范

  3.1 ID生成规则

  ┌────────────┬────────────────────────────────────┬─────────────────────────────────┬───────────────────┐
  │    实体    │                格式                │              示例               │       说明        │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Server ID  │ srv_{env}_{name}                   │ srv_prod_main                   │ env:              │
  │            │                                    │                                 │ prod/test/dev     │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Case ID    │ case_{YYYYMMDD}_{HHMMSS}_{hash8}   │ case_20260401_103045_a1b2c3d4   │ hash为内容哈希    │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Task ID    │ task_{YYYYMMDD}_{HHMMSS}_{hash8}   │ task_20260401_110000_e5f6g7h8   │                   │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Result ID  │ result_{YYYYMMDD}_{HHMMSS}_{hash8} │ result_20260401_110000_e5f6g7h8 │ 与Task时间相同    │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Variant ID │ variant_{case_id}_{desc}           │ variant_pv100mw                 │                   │
  ├────────────┼────────────────────────────────────┼─────────────────────────────────┼───────────────────┤
  │ Snapshot   │ snap_{YYYYMMDD}_{HHMMSS}           │ snap_20260401_120000            │                   │
  │ ID         │                                    │                                 │                   │
  └────────────┴────────────────────────────────────┴─────────────────────────────────┴───────────────────┘

  3.2 文件名规范

  ┌──────────┬───────────────────────────────────────────┬──────────────────────────────────────────┐
  │   类型   │                 命名格式                  │                   示例                   │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ 算例定义 │ {case_name}_v{version}.yaml               │ IEEE39_v1.0.0.yaml                       │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ 配置文件 │ config_{purpose}.yaml                     │ config_emt_fault.yaml                    │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ 波形数据 │ {case}_{skill}_waveforms_{timestamp}.csv  │ IEEE39_emt_waveforms_20260401_110000.csv │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ COMTRADE │ {case}_{skill}_comtrade_{timestamp}.{ext} │ IEEE39_emt_comtrade_20260401_110000.cfg  │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ 报告     │ {case}_{skill}_report_{timestamp}.md      │ IEEE39_emt_report_20260401_110000.md     │
  ├──────────┼───────────────────────────────────────────┼──────────────────────────────────────────┤
  │ 可视化   │ {case}_{skill}_{metric}_{timestamp}.png   │ IEEE39_emt_voltage_20260401_110000.png   │
  └──────────┴───────────────────────────────────────────┴──────────────────────────────────────────┘

  3.3 命名约束

  naming_constraints:
    allowed_characters: "a-zA-Z0-9_-."  # 只允许字母数字下划线点
    max_length: 100                     # 最大长度
    reserved_names:                     # 保留名称
      - "CON"
      - "PRN"
      - "AUX"
      - "NUL"
      - "COM1-9"
      - "LPT1-9"

    case_sensitive: false               # 不区分大小写（避免冲突）

    prohibited_patterns:                # 禁止模式
      - "^\\d+$"                        # 纯数字
      - "^\\."                          # 以点开头
      - "\\.$"                          # 以点结尾
      - "\\s"                           # 包含空格
      - "[^a-zA-Z0-9_\\-\\.]"           # 特殊字符

  ---
  第四章：注册表设计

  4.1 主索引 (registry/index.yaml)

  # 系统主索引 - 快速定位
  version: "2.0.0"
  last_updated: "2026-04-01T12:00:00Z"

  indexes:
    cases:
      file: "cases.yaml"
      count: 15
      last_updated: "2026-04-01T11:30:00Z"

    tasks:
      file: "tasks.yaml"
      count: 128
      last_updated: "2026-04-01T11:45:00Z"

    results:
      file: "results.yaml"
      count: 96
      last_updated: "2026-04-01T11:50:00Z"

  references:
    current_workspace: "ws_default"
    default_server: "srv_prod_main"

  4.2 算例注册表 (registry/cases.yaml)

  # 算例注册表
  cases:
    case_20260401_103045_a1b2c3d4:
      name: "IEEE39"
      version: "1.0.0"
      current_version_path: "cases/case_20260401_103045_a1b2c3d4/v1.0.0"

      identity:
        created_at: "2026-04-01T10:30:45Z"
        created_by: "user@example.com"
        owner: "holdme"

      classification:
        domain: "transmission"
        voltage_level: "345kV"
        analysis_types: ["powerflow", "transient", "emt"]

      lineage:
        base_case_id: null           # 根算例
        created_from: "import"
        import_source: "cloud"
        original_rid: "model/holdme/IEEE39"

      content:
        local_path: "cases/case_20260401_103045_a1b2c3d4"
        versions: ["1.0.0", "1.1.0"]
        variants: ["pv100mw", "pv200mw"]

      remote_mappings:
        production: "model/holdme/IEEE39"
        testing: "model/user123/IEEE39"

      statistics:
        components:
          buses: 39
          lines: 46
          generators: 10
        results_count: 12

      metadata:
        description: "IEEE 39节点标准测试系统"
        tags: ["standard", "transient", "stability"]
        custom: {}

      lifecycle:
        state: "active"              # active/archived/deleted
        last_accessed: "2026-04-01T11:00:00Z"
        last_modified: "2026-04-01T10:30:45Z"

  4.3 任务注册表 (registry/tasks.yaml)

  # 任务注册表 - 所有仿真任务
  tasks:
    task_20260401_110000_e5f6g7h8:
      # 关联关系
      case_id: "case_20260401_103045_a1b2c3d4"
      result_id: "result_20260401_110000_e5f6g7h8"

      # 执行配置
      execution:
        skill: "emt_simulation"
        server_id: "srv_prod_main"
        job_id: "job-12345678-abcd-1234-efgh-123456789012"
        priority: "normal"           # low/normal/high

      # 配置快照
      configuration:
        config_hash: "sha256:abc123..."
        config_path: "tasks/2026/04/task_20260401_110000_e5f6g7h8/config.yaml"
        parameters:
          duration: 10.0
          fault_bus: "Bus_16"
          fault_type: "3ph"

      # 生命周期
      lifecycle:
        state: "completed"
        created_at: "2026-04-01T11:00:00Z"
        submitted_at: "2026-04-01T11:00:05Z"
        started_at: "2026-04-01T11:00:10Z"
        completed_at: "2026-04-01T11:05:30Z"
        duration_seconds: 320

      # 结果摘要
      results:
        result_path: "results/case_20260401_103045_a1b2c3d4/result_20260401_110000_e5f6g7h8"
        convergence: true
        metrics:
          max_voltage_dip: 0.15
          recovery_time: 2.5

      # 元数据
      metadata:
        description: "Bus 16三相短路故障仿真"
        tags: ["fault", "bus16", "3ph"]
        notes: ""

  4.4 结果注册表 (registry/results.yaml)

  # 结果注册表 - 所有仿真结果
  results:
    result_20260401_110000_e5f6g7h8:
      # 关联关系 (关键!)
      task_id: "task_20260401_110000_e5f6g7h8"
      case_id: "case_20260401_103045_a1b2c3d4"

      # 结果分类
      classification:
        result_type: "emt"
        data_format: "raw+processed"
        analysis_types: ["fault", "transient"]

      # 存储信息
      storage:
        local_path: "results/case_20260401_103045_a1b2c3d4/result_20260401_110000_e5f6g7h8"
        size_bytes: 52428800
        checksum: "md5:def456..."

      # 内容清单
      content:
        data_files:
          - "data/raw.h5"
          - "data/processed/voltages.csv"
          - "data/processed/currents.csv"
          - "data/summary.json"

        exports:
          - "exports/waveforms_20260401_110000.csv"
          - "exports/comtrade_20260401_110000.cfg"
          - "exports/comtrade_20260401_110000.dat"
          - "exports/report_20260401_110000.md"

        visualizations:
          - "viz/overview.png"
          - "viz/waveforms/bus1_voltage.png"

        artifacts_count: 8

      # 关键指标
      metrics:
        simulation:
          duration_seconds: 10.0
          step_size: 1e-6
          convergence: true
        electrical:
          max_voltage_dip: 0.15
          min_frequency: 49.2
          recovery_time: 2.5

      # 生命周期
      lifecycle:
        created_at: "2026-04-01T11:05:30Z"
        retention_days: 365
        expires_at: "2027-04-01T11:05:30Z"
        archived: false

      # 溯源
      provenance:
        task_config_hash: "sha256:abc123..."
        model_version: "1.0.0"
        executed_by: "user@example.com"
        server: "production"

      # 元数据
      metadata:
        description: "IEEE39 Bus 16三相短路故障EMT仿真结果"
        tags: ["fault", "bus16", "transient", "emt"]
        quality_score: 0.95

  ---
  第五章：生命周期流程

  5.1 算例生命周期

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        Case Lifecycle (算例生命周期)                     │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │   [Create] ───────► [Import] ───────► [Edit] ───────► [Version]        │
  │       │                │                │                │              │
  │       │            从云端导入          修改参数        创建新版本        │
  │       │            或本地创建          拓扑变更                         │
  │       ▼                ▼                ▼                ▼              │
  │   ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐          │
  │   │草稿状态 │      │本地存储 │      │变更追踪 │      │版本分支 │          │
  │   └────────┘      └────────┘      └────────┘      └────────┘          │
  │                                                                         │
  │       │                │                │                │              │
  │       └────────────────┴────────────────┴────────────────┘              │
  │                          │                                              │
  │                          ▼                                              │
  │                    [Validate] ──────► [Register]                        │
  │                    验证有效性           注册到系统                        │
  │                          │                                              │
  │                          ▼                                              │
  │       ┌────────────────────────────────────────┐                        │
  │       ▼                                        ▼                        │
  │   [Active] ──────► [Archive] ──────► [Delete]                          │
  │   活跃状态          归档存储           删除回收                           │
  │       │                │                │                               │
  │   可以被使用      保留但只读         移入回收站                           │
  │       │                │                │                               │
  │       └────────────────┴────────────────┘                               │
  │                    可逆操作                                             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  5.2 任务-结果生命周期

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     Task-Result Lifecycle                               │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  User submits task                                                      │
  │       │                                                                 │
  │       ▼                                                                 │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
  │  │  1. CREATE  │───►│ 2. SUBMIT   │───►│ 3. RUNNING  │                 │
  │  │  创建任务    │    │ 提交云端     │    │ 执行中       │                 │
  │  │             │    │             │    │             │                 │
  │  │ • 生成task_id│    │ • CloudPSS  │    │ • 轮询状态   │                 │
  │  │ • 保存配置   │    │   Job创建   │    │ • 记录日志   │                 │
  │  │ • 注册到表   │    │ • 关联job_id│    │ • 更新状态   │                 │
  │  └─────────────┘    └─────────────┘    └─────────────┘                 │
  │       │                                     │                           │
  │       │         ┌───────────────────────────┘                           │
  │       │         │                                                       │
  │       │         ▼                                                       │
  │       │    ┌─────────────┐                                              │
  │       │    │  4a. FAILED │────────────────────┐                         │
  │       │    │  执行失败    │                     │                         │
  │       │    │             │                     │                         │
  │       │    │ • 记录错误   │                     │                         │
  │       │    │ • 更新状态   │                     │                         │
  │       │    │ • 触发重试?  │                     │                         │
  │       │    └─────────────┘                     │                         │
  │       │                                        │                         │
  │       └────────────────────────────────────────┤                         │
  │                                                │                         │
  │       ┌────────────────────────────────────────┘                         │
  │       │                                                                  │
  │       ▼                                                                  │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
  │  │ 4b.COMPLETED│───►│ 5. FETCH    │───►│ 6. EXPORT   │                  │
  │  │  执行完成    │    │ 获取结果     │    │ 导出数据     │                  │
  │  │             │    │             │    │             │                  │
  │  │ • 状态更新   │    │ • 下载数据   │    │ • HDF5      │                  │
  │  │ • 记录指标   │    │ • 解析波形   │    │ • CSV       │                  │
  │  │             │    │ • 创建result │    │ • COMTRADE  │                  │
  │  └─────────────┘    └─────────────┘    └─────────────┘                  │
  │                            │                                            │
  │                            ▼                                            │
  │                     ┌─────────────┐                                     │
  │                     │ 7. REGISTER │                                     │
  │                     │  注册结果    │                                     │
  │                     │             │                                     │
  │                     │ • 关联task  │                                     │
  │                     │ • 关联case  │                                     │
  │                     │ • 记录元数据│                                     │
  │                     │ • 更新索引  │                                     │
  │                     └─────────────┘                                     │
  │                            │                                            │
  │                            ▼                                            │
  │  ┌─────────────────────────────────────────────────────────────┐       │
  │  │                      8. AVAILABLE                           │       │
  │  │                      结果可用                                │       │
  │  │                                                             │       │
  │  │  • 可被查询    • 可被分析    • 可被对比    • 可被可视化        │       │
  │  │  • 可被导出    • 可被报告    • 可被归档    • 可被删除          │       │
  │  └─────────────────────────────────────────────────────────────┘       │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ---
  第六章：管理技能设计

  基于以上架构，重新设计管理技能体系：

  6.1 核心管理技能

  ┌───────────┬────────────┬─────────────────────────────────────────────────┐
  │   技能    │    功能    │                     子命令                      │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ system    │ 系统管理   │ init, status, config, cleanup                   │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ server    │ 服务器管理 │ add, remove, list, use, test                    │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ case      │ 算例管理   │ create, import, list, show, edit, clone, delete │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ variant   │ 变体管理   │ create, list, apply, compare                    │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ task      │ 任务管理   │ submit, list, show, status, cancel, retry       │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ result    │ 结果管理   │ list, show, export, analyze, compare, delete    │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ query     │ 统一查询   │ search, filter, navigate                        │
  ├───────────┼────────────┼─────────────────────────────────────────────────┤
  │ workspace │ 工作空间   │ create, switch, save, restore                   │
  └───────────┴────────────┴─────────────────────────────────────────────────┘

  6.2 命令设计示例

  # 系统初始化
  cloudpss system init

  # 服务器管理
  cloudpss server add production https://cloudpss.net --token-file .token_prod
  cloudpss server list
  cloudpss server use production

  # 算例管理
  cloudpss case import model/holdme/IEEE39 --name IEEE39 --server production
  cloudpss case list --filter "voltage_level=345kV"
  cloudpss case show IEEE39
  cloudpss case clone IEEE39 IEEE39_with_PV --edit "add_pv_bus10.yaml"

  # 变体管理
  cloudpss variant create IEEE39 pv100mw --modifications mods/pv100mw.yaml
  cloudpss variant list IEEE39

  # 任务管理
  cloudpss task submit IEEE39 emt_simulation --config configs/fault_bus16.yaml
  cloudpss task list --case IEEE39 --status completed
  cloudpss task show task_20260401_110000_e5f6g7h8

  # 结果管理
  cloudpss result list --case IEEE39 --skill emt_simulation
  cloudpss result show result_20260401_110000_e5f6g7h8
  cloudpss result export result_20260401_110000_e5f6g7h8 --format comtrade

  # 统一查询
  cloudpss query "case=IEEE39 AND skill=emt AND date>2026-04-01"
  cloudpss navigate case_xxx/task_xxx/result_xxx  # 关联导航

  ---
  第七章：交互界面设计

  7.1 目录树视图

  ~/.cloudpss/
  ├── 📁 config/
  │   ├── 📄 servers.yaml          [3 servers]
  │   └── 📁 keys/
  │       └── 🔑 master.key
  │
  ├── 📁 registry/
  │   ├── 📄 index.yaml            [15 cases, 128 tasks, 96 results]
  │   ├── 📄 cases.yaml
  │   ├── 📄 tasks.yaml
  │   └── 📄 results.yaml
  │
  ├── 📁 cases/
  │   ├── 📁 case_20260401_103045_a1b2c3d4/ [IEEE39]
  │   │   ├── 📁 v1.0.0/
  │   │   │   ├── 📄 model.yaml
  │   │   │   ├── 📄 meta.yaml
  │   │   │   └── 📄 README.md
  │   │   ├── 📁 v1.1.0/
  │   │   │   └── 📁 variants/
  │   │   │       ├── 📁 variant_pv100mw/
  │   │   │       └── 📁 variant_pv200mw/
  │   │   └── 🔗 results -> ../../results/case_20260401_103045_a1b2c3d4/
  │   │
  │   └── 📁 case_20260402_.../ [IEEE118]
  │
  ├── 📁 tasks/
  │   └── 📁 2026/
  │       └── 📁 04/
  │           ├── 📁 task_20260401_110000_e5f6g7h8/
  │           │   ├── 📄 config.yaml
  │           │   ├── 📄 status.yaml
  │           │   └── 📁 logs/
  │           └── 📁 task_20260401_120000_...
  │
  ├── 📁 results/
  │   └── 📁 case_20260401_103045_a1b2c3d4/
  │       ├── 📁 result_20260401_110000_e5f6g7h8/
  │       │   ├── 📄 meta.yaml
  │       │   ├── 📁 data/
  │       │   │   ├── 💾 raw.h5 [50MB]
  │       │   │   └── 📁 processed/
  │       │   ├── 📁 exports/
  │       │   │   ├── 📊 waveforms.csv
  │       │   │   └── 📄 report.md
  │       │   └── 📁 viz/
  │       │       └── 📈 overview.png
  │       │
  │       └── 📁 result_20260401_120000_...
  │
  ├── 📁 cache/
  ├── 📁 logs/
  └── 📁 trash/

  7.2 状态面板设计

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     CloudPSS SkillHub Dashboard                         │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  📊 System Status                                         [healthy ✓]  │
  │  ├── Workspace: default                                                 │
  │  ├── Active Server: production (cloudpss.net)                          │
  │  ├── Storage Used: 2.3GB / 10GB                                        │
  │  └── Last Sync: 2026-04-01 12:00:00                                    │
  │                                                                         │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  📁 Cases (15)                                                          │
  │  ├── IEEE39 [v1.1.0] ────── 39 buses ─── 12 results ─── [active]       │
  │  ├── IEEE118 [v1.0.0] ───── 118 buses ─── 8 results ─── [active]       │
  │  └── ...                                                                │
  │                                                                         │
  │  ⚡ Recent Tasks (5)                                                     │
  │  ├── task_...e5f6 [emt] ─── IEEE39 ─── completed ─── 10 min ago        │
  │  ├── task_...a1b2 [n1] ──── IEEE118 ── completed ─── 1 hour ago        │
  │  └── ...                                                                │
  │                                                                         │
  │  📈 Recent Results (5)                                                  │
  │  ├── result_...e5f6 ─── EMT fault ─── 50MB ─── 10 min ago              │
  │  └── ...                                                                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ---
  第八章：实施路线图

  阶段1：基础架构（2周）

  1. 创建新的目录结构和存储规范
  2. 实现加密存储系统（Token安全）
  3. 开发注册表管理模块
  4. 实现 ID 生成和管理工具

  阶段2：核心技能（2周）

  1. 开发 system 技能（初始化、配置）
  2. 开发 server 技能（服务器管理）
  3. 开发 case 技能（算例管理）
  4. 开发 task 技能（任务管理）
  5. 开发 result 技能（结果管理）

  阶段3：关联体系（1周）

  1. 实现 Case↔Task↔Result 自动关联
  2. 开发 query 统一查询技能
  3. 实现导航和追溯功能
  4. 开发数据一致性检查工具

  阶段4：界面优化（1周）

  1. 开发整洁的 CLI 界面
  2. 实现状态面板和仪表盘
  3. 添加进度显示和日志管理
  4. 开发数据可视化展示

  ---
  总结

  这套"收纳"方案提供了：

  1. 清晰的分类体系 - 五大核心实体，各司其职
  2. 严格的目录结构 - 每个对象有唯一存放位置
  3. 规范的命名规则 - 一目了然，便于检索
  4. 完整的关联机制 - Case↔Task↔Result 三元关联
  5. 明确的生命周期 - 创建→使用→归档→销毁
  6. 整洁的界面设计 - 无论是目录结构还是交互界面

  这样的体系应该能满足您对"严谨、清晰、准确、整洁"的要求。您觉得这个收纳方案如何？需要我针对某个部分进一步细化
  吗？
