# Web UI 参考项目

**用途**: 为后续 Phase 5 (Web 界面) 提供参考  
**状态**: 待评估  

---

## 参考项目列表

### 1. Claude Code Web UI (sugyan)
- **GitHub**: https://github.com/sugyan/claude-code-web-ui
- **特点**:
  - 为现有 Claude CLI 提供 Web 前端
  - 支持本地环境通过浏览器运行
  - 移动端优化布局
- **适用场景**: 远程访问本地 Claude Code

### 2. Cloud CLI / Claude Code UI (siteboon)
- **GitHub**: https://github.com/siteboon/claude-code-ui
- **特点**:
  - 更高级的管理界面
  - 自动发现 ~/.claude 文件夹中的会话
  - 包含文件浏览器
  - Git 集成
  - MCP (Model Context Protocol) 管理
- **适用场景**: 综合管理界面，功能丰富

### 3. claude-code-web (vultuk)
- **GitHub**: https://github.com/vultuk/claude-code-web
- **特点**:
  - VS Code 风格的分割视图
  - 使用 WebSocket 实时终端模拟
  - 浏览器中的终端体验
- **适用场景**: 需要终端体验的 Web 界面

---

## 评估维度

| 项目 | 活跃度 | 功能丰富度 | 可定制性 | 推荐度 |
|------|--------|-----------|---------|--------|
| sugyan/claude-code-web-ui | 待查 | 基础 | 高 | ⭐⭐⭐ |
| siteboon/claude-code-ui | 待查 | 丰富 | 中 | ⭐⭐⭐⭐ |
| vultuk/claude-code-web | 待查 | 中等 | 高 | ⭐⭐⭐ |

---

## Phase 5 决策要点

### 方案选择

**方案 A**: 基于开源项目修改
- 优点: 开发快，有现成基础
- 缺点: 依赖第三方，可能需要适配

**方案 B**: 自研 Web 界面
- 优点: 完全可控，可按需定制
- 缺点: 开发周期长

### 技术栈建议

| 层级 | 推荐技术 |
|------|---------|
| 前端框架 | React + TypeScript |
| UI 组件 | shadcn/ui (符合 DESIGN.md) |
| 状态管理 | Zustand / Redux Toolkit |
| 实时通信 | WebSocket (Socket.io) |
| 后端 | FastAPI (Python) |
| Agent 集成 | Claude API SDK |
| 部署 | Docker + Nginx |

---

## 后续行动

- [ ] Phase 1-4 完成后评估这些项目
- [ ] 选择是否基于开源项目修改或自研
- [ ] 设计 Web 界面原型
- [ ] 实现用户认证系统
- [ ] 部署测试

---

**注意**: 本文档仅作参考，Phase 5 的实施需等 Phase 1-4 稳定后再启动。
