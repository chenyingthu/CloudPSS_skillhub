# CloudPSS 收纳大师 Portal 交接记录

日期: 2026-05-03 15:48 CST  
范围: 仅 `cloudpss_skills_v3/master_organizer`，不要处理 `cloudpss_skills_v2`

## 当前目标

Portal 的方向已经明确：它不是 CLI 外壳，而是面向电力系统研究者的仿真研究工作台。核心体验是让用户对模型、配置、任务、结果、分析、报告形成全过程掌控。当前用户指出下一阶段要处理“模型管理”的问题，建议重启会话后从模型工作台继续。

## 工作区状态

- 当前分支工作区不干净。
- `cloudpss_skills_v2` 有多处修改和未跟踪测试文件，是其他同事的工作，本轮不要碰。
- 本轮 v3 Portal 相关修改集中在:
  - `cloudpss_skills_v3/master_organizer/portal/static/index.html`
  - `cloudpss_skills_v3/master_organizer/portal/static/app.js`
  - `cloudpss_skills_v3/master_organizer/portal/static/styles.css`
- Portal 服务当前运行在:
  - `http://127.0.0.1:8766/?token=organizer-review`
  - 启动命令: `python -m cloudpss_skills_v3.master_organizer.portal.server --host 0.0.0.0 --port 8766 --token organizer-review`

## 已完成的 v3 Portal 改造

1. 结果页
   - 从“左列表 + 右详情”改为多 tab 工作簿结构。
   - 页签包括: `结果表`、`摘要`、`曲线与表格`、`Artifacts`、`Metadata`、`报告`。
   - `曲线与表格` 页签修复了内容裁剪问题。
   - EMT 曲线由只显示前 4 条改为全部显示。
   - 图表 canvas 会按实际容器尺寸重绘。

2. 任务弹窗
   - 修复右上角“新建任务”弹窗内容不完整的问题。
   - 任务弹窗改为三段式: 固定标题、滚动内容、固定底部按钮。
   - 弹窗宽度调整为更适合配置表单的 920px，并适配小屏单列。

3. 模型工作台已有基础
   - Case 页面有二级 tab: `算例信息`、`元件列表`、`修改记录`。
   - 模型元件按类型过滤: 母线、线路、变压器、发电机、负荷、控制器、测量、通道、故障等。
   - 参数表支持列视图定制，配置保存在浏览器 `localStorage`。
   - 复杂对象不再显示 `[object Object]`，而是显示摘要并只读。
   - 本地模型参数可编辑、dirty 标记、保存、备份。
   - 保存接口会校验 `case_id` 和当前 Case 的 `model_source`，避免误写其他模型文件。

## 最近验证

已通过:

```bash
node --check cloudpss_skills_v3/master_organizer/portal/static/app.js
pytest cloudpss_skills_v3/master_organizer/tests/test_portal_server.py cloudpss_skills_v3/master_organizer/tests/test_portal_state.py -q
pytest cloudpss_skills_v3/master_organizer/tests -q
```

最近全量结果:

```text
109 passed, 3 skipped
```

接口抽查:

- 当前 workspace 有 `2` 个 Case、`3` 个 Task、`3` 个 Result。
- 有 EMT 结果包含 `6` 条 series 和 `6` 个 channel，前端已改为全部渲染。

## 模型管理当前问题

用户下一步明确要处理模型管理。当前模型工作台虽然能展示和编辑，但还不够像“生产级模型管理”。

主要缺口:

1. 模型页面信息架构仍弱
   - `算例信息`、`元件列表`、`修改记录`已有，但模型对象、模型文件、Case、Task 的关系还不够直观。
   - 用户需要清楚知道: 当前编辑的到底是哪一个模型文件、属于哪个 Case、对应哪个 CloudPSS RID、是否有本地可编辑源。

2. 模型视图配置只保存在 localStorage
   - 当前 key: `cloudpss.portal.modelView.${modelPath}.${componentType}`。
   - 这能解决单机快速使用，但不利于团队复现、换浏览器、归档。
   - 下一步应设计 workspace 级模型视图配置，例如 `.cloudpss/portal/model_views.json` 或跟 Case 绑定的 view 配置。

3. 修改记录不够生产级
   - 当前前端有 dirty 列表和保存，但还没有完整历史时间线。
   - 需要把每次保存的备份、修改人、修改摘要、影响元件和参数都归档为可查看记录。

4. 模型 diff / rollback 缺失
   - 后端已能备份，但前端缺少差异查看、版本对比、恢复到指定版本。
   - 这是模型管理必须补齐的核心能力。

5. 批量编辑和参数筛选缺失
   - 当前能选择显示列、编辑单元格。
   - 还需要按参数名过滤、批量修改同类元件参数、对一组元件应用同一规则。

6. 校验能力不足
   - 当前只做基础保存。
   - 需要在保存前做模型参数校验，例如数值范围、必填项、类型、单位、关联对象是否存在。

## 建议的下一步切入顺序

1. 先整理模型管理的数据契约
   - 明确 Case、ModelSource、ModelSnapshot、ModelView、ModelRevision、ModelDiff 的结构。
   - 不急着做大 UI，先把“模型管理的对象”定义清楚。

2. 增加模型视图配置持久化
   - 后端新增读取/保存 view 配置 API。
   - 前端从 localStorage 迁移到 workspace 配置，localStorage 只作为 fallback。

3. 增强修改记录
   - 后端为每次保存写入 revision manifest。
   - 前端 `修改记录` tab 改为真实时间线，显示每次保存的参数变更摘要。

4. 做 diff 和 rollback
   - 后端比较两个 revision 或当前模型与上一版。
   - 前端提供“查看差异”“恢复此版本”。

5. 再做批量编辑与校验
   - 在已有表格上加参数筛选和批量应用。
   - 保存前展示校验结果。

## 关键文件入口

- 前端模型表:
  - `cloudpss_skills_v3/master_organizer/portal/static/app.js`
  - 入口函数: `renderParameterTable`, `renderParameterCell`, `bindModelColumnControls`, `saveModelEdits`, `backupModel`
- 前端结构:
  - `cloudpss_skills_v3/master_organizer/portal/static/index.html`
  - 关注 `casesView`、`model-workbench`、`edit-panel`
- 前端样式:
  - `cloudpss_skills_v3/master_organizer/portal/static/styles.css`
  - 关注 `.workbook-case-sheet`, `.model-viewbar`, `.model-table-wrap`, `.model-param`
- 后端模型编辑:
  - `cloudpss_skills_v3/master_organizer/portal/model_editor.py`
  - `cloudpss_skills_v3/master_organizer/portal/state.py`
  - `cloudpss_skills_v3/master_organizer/portal/server.py`
- 测试:
  - `cloudpss_skills_v3/master_organizer/tests/test_portal_state.py`
  - `cloudpss_skills_v3/master_organizer/tests/test_portal_server.py`

## 重启会话后的建议提示词

```text
请阅读 docs/PORTAL_HANDOFF_2026-05-03.md 和 docs/PORTAL_DESIGN.md。只处理 cloudpss_skills_v3，不要碰 v2。现在继续做 Portal 的模型管理生产化：先 review 当前模型工作台的数据契约和实现，再提出并实现第一步改造。重点是模型视图配置持久化、修改历史、diff/rollback 的路线，不要再做零散 UI 微调。
```
