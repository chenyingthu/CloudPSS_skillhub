// Theme initialization
const savedTheme = localStorage.getItem("cloudpss.portal.theme");
const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
const initialTheme = savedTheme || (prefersDark ? "dark" : "light");
document.documentElement.setAttribute("data-theme", initialTheme);

const state = {
  snapshot: null,
  selectedCaseId: null,
  selectedResultId: null,
  view: "dashboard",
  caseTab: "case",
  resultTab: "table",
  activeComponentType: "all",
  activeModelEditor: null,
  selectedResultDetail: null,
  token: new URLSearchParams(window.location.search).get("token") || "",
  modelEdits: {},
  theme: initialTheme,
};

const titles = {
  dashboard: ["总览", "模型、配置、任务、结果、分析和报告的统一工作台"],
  cases: ["模型与算例", "围绕 Case 组织模型、变体、任务和结果"],
  tasks: ["任务", "创建、运行并追踪 CloudPSS 作业"],
  results: ["结果", "查看 manifest、metadata、潮流表和 EMT 通道"],
  reports: ["报告与归档", "生成报告、归档结果、导出证据"],
  servers: ["服务", "查看 Server、owner、默认服务和 token 来源"],
  audit: ["审计", "收纳大师的操作账本"],
};

function $(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const node = $(id);
  if (node) node.textContent = value;
}

function setHtml(id, value) {
  const node = $(id);
  if (node) node.innerHTML = value;
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers["X-Portal-Token"] = state.token;
  const response = await fetch(path, {
    ...options,
    headers,
  });

  // Check if response is HTML (static file server fallback)
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("text/html")) {
    throw new Error("API not available - using static mode");
  }

  let data;
  try {
    data = await response.json();
  } catch (e) {
    throw new Error("Invalid response from server");
  }

  if (!response.ok || data.error) {
    throw new Error(data.error?.message || data.error || `HTTP ${response.status}`);
  }
  return data.data;
}

function showNotice(message, type = "info") {
  const notice = $("notice");
  notice.textContent = message;
  notice.className = `notice ${type === "error" ? "error" : ""}`;
  window.clearTimeout(showNotice.timer);
  showNotice.timer = window.setTimeout(() => notice.classList.add("hidden"), 4500);
}

function pill(status) {
  return `<span class="pill ${status || ""}">${status || "-"}</span>`;
}

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function compactId(id) {
  if (!id) return "-";
  return id.length > 30 ? `${id.slice(0, 18)}...${id.slice(-8)}` : id;
}

function taskChannels(task) {
  const channels = (task.config || {}).channels || [];
  return Array.isArray(channels) ? channels.join(",") : String(channels || "");
}

function controlMetric(label, value) {
  return `<div class="control-metric"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
}

function editKey(componentId, arg) {
  return `${componentId}::${arg}`;
}

const defaultModelColumns = {
  all: ["Name", "name", "base", "rated", "U", "V", "P", "Q", "R", "X", "L", "C"],
  bus: ["Name", "name", "baseV", "baseVoltage", "V", "U", "angle", "type"],
  line: ["Name", "name", "R", "X", "L", "C", "length", "Length", "Imax"],
  transformer: ["Name", "name", "Sn", "rated", "R", "X", "ratio", "tap"],
  generator: ["Name", "name", "P", "Q", "V", "H", "D", "Sn"],
  load: ["Name", "name", "P", "Q", "p", "q", "V"],
  control: ["Name", "name", "K", "T", "T1", "T2", "T3", "T4"],
  meter: ["Name", "name", "target", "channel", "unit"],
  channel: ["Name", "name", "target", "variable", "unit"],
  fault: ["Name", "name", "time", "duration", "R", "X", "type"],
};

function scalarLike(value) {
  return value === null || ["string", "number", "boolean", "undefined"].includes(typeof value);
}

function modelViewKey(editor, type) {
  const path = editor?.path || "default";
  return `cloudpss.portal.modelView.${path}.${type || "all"}`;
}

function modelValueSummary(value) {
  if (scalarLike(value)) return value ?? "";
  if (Array.isArray(value)) return `[array:${value.length}]`;
  if (typeof value === "object") return `{${Object.keys(value || {}).slice(0, 4).join(", ") || "object"}}`;
  return String(value ?? "");
}

function selectedModelColumns(editor, type, rows, allColumns) {
  const key = modelViewKey(editor, type);
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    if (Array.isArray(saved) && saved.length) return saved.filter((column) => allColumns.includes(column));
  } catch (_error) {
    // Ignore malformed localStorage values.
  }
  const preferred = defaultModelColumns[type] || defaultModelColumns.all;
  const byPreference = allColumns.filter((column) => preferred.some((item) => column.toLowerCase().includes(item.toLowerCase())));
  const byFrequency = allColumns
    .map((column) => ({
      column,
      count: rows.reduce((total, row) => total + (Object.prototype.hasOwnProperty.call(row.args || {}, column) ? 1 : 0), 0),
    }))
    .sort((a, b) => b.count - a.count)
    .map((item) => item.column);
  return Array.from(new Set([...byPreference, ...byFrequency])).slice(0, 10);
}

function saveModelColumnView(editor, type, columns) {
  localStorage.setItem(modelViewKey(editor, type), JSON.stringify(columns));
}

function caseDescriptionText(description) {
  try {
    const notes = JSON.parse(description || "{}");
    if (notes && typeof notes === "object" && "description_text" in notes) {
      return notes.description_text || "";
    }
  } catch (_error) {
    return description || "";
  }
  return description || "";
}

// Static mode flag
let staticMode = false;

// Loading state management
function showLoading() {
  const overlay = $("loadingOverlay");
  const bar = $("loadingBar");
  if (overlay) overlay.classList.remove("hidden");
  if (bar) bar.classList.add("active");
}

function hideLoading() {
  const overlay = $("loadingOverlay");
  const bar = $("loadingBar");
  if (overlay) {
    overlay.classList.add("hidden");
    setTimeout(() => {
      if (overlay.classList.contains("hidden")) {
        overlay.style.display = "none";
      }
    }, 300);
  }
  if (bar) bar.classList.remove("active");
}

async function refresh() {
  showLoading();
  try {
    state.snapshot = await api("/api/snapshot");
  } catch (error) {
    // Enter static mode if API is not available
    if (error.message.includes("static mode") || error.message.includes("API not available")) {
      staticMode = true;
      // Use mock data for static demo
      state.snapshot = getMockSnapshot();
    } else {
      showNotice(error.message, "error");
      return;
    }
  } finally {
    hideLoading();
  }
  render();
}

// Mock data for static demo mode
function getMockSnapshot() {
  return {
    workspace: {
      root: "/demo/workspace",
      counts: { servers: 2, cases: 3, tasks: 5, results: 4 },
      storage: { total_mb: 156 },
    },
    cases: [
      { id: "case-001", name: "IEEE 39 Bus", status: "active", rid: "model/demo/IEEE39", tags: ["ieee39", "powerflow"] },
      { id: "case-002", name: "IEEE 14 Bus", status: "active", rid: "model/demo/IEEE14", tags: ["ieee14", "powerflow"] },
      { id: "case-003", name: "3-Bus EMT", status: "draft", rid: "model/demo/Bus3", tags: ["emt", "transient"] },
    ],
    tasks: [
      { id: "task-001", name: "IEEE39 潮流计算", status: "completed", type: "powerflow", case_id: "case-001", created_at: Date.now() - 86400000 },
      { id: "task-002", name: "IEEE39 EMT仿真", status: "running", type: "emt", case_id: "case-001", created_at: Date.now() - 3600000 },
      { id: "task-003", name: "IEEE14 潮流计算", status: "failed", type: "powerflow", case_id: "case-002", created_at: Date.now() - 7200000 },
      { id: "task-004", name: "短路故障分析", status: "created", type: "emt", case_id: "case-003", created_at: Date.now() - 1800000 },
      { id: "task-005", name: "稳定性分析", status: "submitted", type: "stability", case_id: "case-001", created_at: Date.now() - 900000 },
    ],
    results: [
      { id: "result-001", name: "IEEE39 PF Result", format: "json", size_bytes: 102456, created_at: Date.now() - 86000000 },
      { id: "result-002", name: "IEEE39 EMT Data", format: "hdf5", size_bytes: 5242880, created_at: Date.now() - 3500000 },
      { id: "result-003", name: "Fault Analysis", format: "csv", size_bytes: 45678, created_at: Date.now() - 7100000 },
      { id: "result-004", name: "Stability Report", format: "json", size_bytes: 23456, created_at: Date.now() - 800000 },
    ],
    servers: [
      { id: "srv-001", name: "CloudPSS Main", url: "https://cloudpss.net", owner: "demo", status: "active", default: true },
      { id: "srv-002", name: "Internal Server", url: "http://internal:8080", owner: "lab", status: "inactive", default: false },
    ],
    recent_tasks: [
      { id: "task-002", name: "IEEE39 EMT仿真", status: "running", type: "emt", created_at: Date.now() - 3600000 },
      { id: "task-005", name: "稳定性分析", status: "submitted", type: "stability", created_at: Date.now() - 900000 },
    ],
    recent_results: [
      { id: "result-002", name: "IEEE39 EMT Data", format: "hdf5", size_bytes: 5242880, created_at: Date.now() - 3500000 },
      { id: "result-004", name: "Stability Report", format: "json", size_bytes: 23456, created_at: Date.now() - 800000 },
    ],
    tasks_by_case: {
      "case-001": [{ id: "task-001", name: "潮流计算", status: "completed" }, { id: "task-002", name: "EMT仿真", status: "running" }],
    },
    variants_by_case: {},
  };
}

function switchView(view) {
  state.view = view;
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  document.querySelectorAll(".view").forEach((section) => {
    section.classList.toggle("active", section.id === `${view}View`);
  });
  const [title, subtitle] = titles[view] || titles.dashboard;
  $("viewTitle").textContent = title;
  $("viewSubtitle").textContent = subtitle;
}

function switchCaseTab(tab) {
  state.caseTab = tab || "case";
  document.querySelectorAll(".case-subtab").forEach((button) => {
    button.classList.toggle("active", button.dataset.caseTab === state.caseTab);
  });
  document.querySelector(".case-list-panel")?.classList.toggle("hidden", state.caseTab !== "case");
  document.querySelector(".model-workbench")?.classList.toggle("hidden", state.caseTab !== "components");
  document.querySelector(".edit-panel")?.classList.toggle("hidden", state.caseTab !== "changes");
}

function switchResultTab(tab) {
  state.resultTab = tab || "table";
  document.querySelectorAll(".result-subtab").forEach((button) => {
    button.classList.toggle("active", button.dataset.resultTab === state.resultTab);
  });
  document.querySelectorAll(".result-tab-panel").forEach((panel) => {
    panel.classList.toggle("hidden", panel.dataset.resultPanel !== state.resultTab);
  });
  if (state.resultTab === "data") {
    window.requestAnimationFrame(drawCharts);
  }
}

function render() {
  const snapshot = state.snapshot;
  if (!snapshot) return;
  $("workspaceRoot").textContent = snapshot.workspace.root;
  $("countServers").textContent = snapshot.workspace.counts.servers;
  $("countCases").textContent = snapshot.workspace.counts.cases;
  $("countTasks").textContent = snapshot.workspace.counts.tasks;
  $("countResults").textContent = snapshot.workspace.counts.results;
  $("storageTotal").textContent = `${snapshot.workspace.storage.total_mb} MB`;
  renderRecent();
  renderCaseTree();
  renderTasks();
  renderResults();
  renderReports();
  renderServers();
  renderAudit();
}

function renderRecent() {
  $("recentTasks").innerHTML = taskTableRows(state.snapshot.recent_tasks || []);
  $("recentResults").innerHTML = resultTableRows(state.snapshot.recent_results || []);

  // 绑定最近结果的点击事件
  document.querySelectorAll("#recentResults [data-result-id]").forEach((node) => {
    node.addEventListener("click", () => loadResultDetail(node.dataset.resultId));
  });
}

function taskListItem(task) {
  return `
    <div class="list-item" data-task-id="${esc(task.id)}" style="position: relative; cursor: pointer;">
      <div class="list-item-title">
        <span>${esc(task.name)}</span>
        ${pill(task.status)}
      </div>
      <div class="list-item-meta">
        ${esc(compactId(task.id))} · ${esc(task.type)} · ${formatRelativeTime(task.created_at)}
      </div>
    </div>
  `;
}

function resultListItem(result) {
  return `
    <div class="list-item" data-result-id="${esc(result.id)}" style="position: relative; cursor: pointer;">
      <div class="list-item-title">
        <span>${esc(result.name)}</span>
        <span class="pill">${esc(result.format)}</span>
      </div>
      <div class="list-item-meta">
        ${esc(compactId(result.id))} · ${formatBytes(result.size_bytes)}
      </div>
    </div>
  `;
}

// 保留原有函数供其他地方使用
function taskItem(task) {
  return `
    <div class="item">
      <div class="item-title"><span>${esc(task.name)}</span>${pill(task.status)}</div>
      <div class="meta">${esc(compactId(task.id))} · ${esc(task.type)} · case ${esc(compactId(task.case_id))}</div>
    </div>
  `;
}

function resultItem(result) {
  return `
    <div class="item" data-result-id="${esc(result.id)}">
      <div class="item-title"><span>${esc(result.name)}</span><span class="pill">${esc(result.format)}</span></div>
      <div class="meta">${esc(compactId(result.id))} · ${esc(result.size_bytes)} bytes</div>
    </div>
  `;
}

function dataTable(headers, rows, emptyMessage = "暂无数据") {
  if (!rows || rows.length === 0) return empty(emptyMessage);
  return `
    <div class="sheet-table-wrap">
      <table class="sheet-table">
        <thead><tr>${headers.map((header) => `<th>${esc(header.label)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((row) => `
            <tr ${row.attrs || ""}>
              ${headers.map((header) => `<td>${header.render ? header.render(row.item) : esc(row.item[header.key] ?? "-")}</td>`).join("")}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function taskTableRows(tasks) {
  const headers = [
    { label: "任务名称", render: (task) => `<strong>${esc(task.name)}</strong>` },
    { label: "状态", render: (task) => pill(task.status) },
    { label: "类型", render: (task) => esc(task.type || "-") },
    { label: "Case", render: (task) => `<code>${esc(compactId(task.case_id || "-"))}</code>` },
    { label: "Task ID", render: (task) => `<code>${esc(compactId(task.id))}</code>` },
    { label: "Result", render: (task) => `<code>${esc(compactId(task.result_id || "-"))}</code>` },
    { label: "创建时间", render: (task) => esc(formatRelativeTime(task.created_at)) },
    { label: "操作", render: (task) => {
      const canRun = ["created", "submitted", "failed"].includes(task.status);
      return `
        <div class="inline-actions">
          ${canRun ? `<button class="button small secondary edit-task" data-task-id="${esc(task.id)}">配置</button>` : ""}
          <button class="button small secondary preflight-task" data-task-id="${esc(task.id)}">检查</button>
          ${canRun ? `<button class="button small run-task" data-task-id="${esc(task.id)}">运行</button>` : ""}
          <button class="button small secondary" onclick="openTaskDetailDialog('${esc(task.id)}')">详情</button>
        </div>
      `;
    } },
  ];
  return dataTable(headers, tasks.map((task) => ({ item: task, attrs: `data-task-id="${esc(task.id)}"` })), "暂无任务");
}

function resultTableRows(results) {
  const headers = [
    { label: "结果名称", render: (result) => `<strong>${esc(result.name)}</strong>` },
    { label: "格式", render: (result) => `<span class="pill">${esc(result.format)}</span>` },
    { label: "Result ID", render: (result) => `<code>${esc(compactId(result.id))}</code>` },
    { label: "Task", render: (result) => `<code>${esc(compactId(result.task_id || "-"))}</code>` },
    { label: "Case", render: (result) => `<code>${esc(compactId(result.case_id || "-"))}</code>` },
    { label: "大小", render: (result) => esc(formatBytes(result.size_bytes || 0)) },
    { label: "时间", render: (result) => esc(formatRelativeTime(result.created_at)) },
  ];
  return dataTable(headers, results.map((result) => ({
    item: result,
    attrs: `data-result-id="${esc(result.id)}" class="${state.selectedResultId === result.id ? "selected-row" : ""}"`,
  })), "暂无结果");
}

function caseTableRows(cases) {
  const snapshot = state.snapshot || {};
  const headers = [
    { label: "Case 名称", render: (caseRow) => `<strong>${esc(caseRow.name)}</strong>` },
    { label: "状态", render: (caseRow) => pill(caseRow.status) },
    { label: "RID", render: (caseRow) => `<code>${esc(caseRow.rid || "-")}</code>` },
    { label: "Case ID", render: (caseRow) => `<code>${esc(compactId(caseRow.id))}</code>` },
    { label: "任务数", render: (caseRow) => esc((snapshot.tasks_by_case?.[caseRow.id] || []).length) },
    { label: "变体数", render: (caseRow) => esc((snapshot.variants_by_case?.[caseRow.id] || []).length) },
    { label: "标签", render: (caseRow) => esc((caseRow.tags || []).join(", ") || "-") },
  ];
  return dataTable(headers, cases.map((caseRow) => ({ item: caseRow, attrs: `data-case-id="${esc(caseRow.id)}"` })), "暂无 Case");
}

function serverTableRows(servers) {
  const headers = [
    { label: "Server", render: (server) => `<strong>${esc(server.name)}</strong>` },
    { label: "默认", render: (server) => pill(server.default ? "default" : server.status) },
    { label: "URL", render: (server) => `<code>${esc(server.url || "-")}</code>` },
    { label: "Owner", render: (server) => esc(server.owner || "-") },
    { label: "Token 来源", render: (server) => esc((server.auth || {}).token_source || "-") },
    { label: "Server ID", render: (server) => `<code>${esc(compactId(server.id))}</code>` },
  ];
  return dataTable(headers, servers.map((server) => ({ item: server })), "暂无 Server");
}

function auditTableRows(entries) {
  const headers = [
    { label: "时间", render: (entry) => esc(entry.timestamp || "-") },
    { label: "动作", render: (entry) => `<strong>${esc(entry.action || "raw")}</strong>` },
    { label: "对象", render: (entry) => `<code>${esc(compactId(entry.entity_id || "-"))}</code>` },
    { label: "详情", render: (entry) => `<code>${esc(JSON.stringify(entry.details || entry.raw || {}))}</code>` },
  ];
  return dataTable(headers, entries.map((entry) => ({ item: entry })), "暂无审计记录");
}

// 工具函数：格式化字节
function formatBytes(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// 工具函数：格式化相对时间
function formatRelativeTime(timestamp) {
  if (!timestamp) return "-";
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes}分钟前`;
  if (hours < 24) return `${hours}小时前`;
  if (days < 30) return `${days}天前`;
  return date.toLocaleDateString("zh-CN");
}

function checkList(preflight) {
  const checks = (preflight && preflight.checks) || [];
  return `
    <div class="check-list">
      ${checks.map((item) => `
        <div class="check ${item.ok ? "ok" : "bad"}">
          <span>${item.ok ? "OK" : "!"}</span>
          <strong>${esc(item.name)}</strong>
          <em>${esc(item.message)}</em>
        </div>
      `).join("")}
    </div>
  `;
}

function renderCaseTree() {
  const snapshot = state.snapshot;
  $("caseTree").innerHTML = caseTableRows(snapshot.cases || []);

  document.querySelectorAll("[data-case-id]").forEach((node) => {
    node.addEventListener("click", async () => {
      state.selectedCaseId = node.dataset.caseId;
      await loadCaseDetail(state.selectedCaseId);
      renderCaseTree();
      switchCaseTab("components");
    });
  });
}

async function loadCaseDetail(caseId) {
  const detail = await api(`/api/cases/${caseId}`);
  const caseRow = detail.case;
  const plan = detail.simulation_plan || {};
  const model = detail.model || {};

  // Load model editor data from separate endpoint
  let editor = null;
  try {
    const modelData = await api(`/api/cases/${caseId}/model`);
    editor = modelData;
    state.model = modelData;  // Store in state for access
  } catch (e) {
    // Model may not be available
    state.model = null;
  }

  // Update workbench title
  $("workbenchTitle").textContent = `${esc(caseRow.name)} - 模型工作台`;

  // Update edit panel case info
  const caseInfoSummary = $("caseInfoSummary");
  caseInfoSummary.classList.remove("hidden");
  $("editPanelCaseName").textContent = caseRow.name;
  $("editPanelModelName").textContent = model.rid || caseRow.rid || "-";

  // Render component navigation and parameter table
  renderComponentNav(editor);
  renderParameterTable(editor, "all");

  // Bind component navigation
  bindComponentNav(editor);

  // Reset edit state
  state.modelEdits = {};
  updateEditPanel();

  // Enable action buttons
  $("saveModelBtn").disabled = !editor?.editable;
  $("backupModelBtn").disabled = !editor?.editable;
  $("discardChangesBtn").disabled = true;
  $("exportChangesBtn").disabled = true;
  $("createTaskFromCaseBtn").disabled = false;

  // Bind action buttons
  $("saveModelBtn").onclick = () => saveModelEdits(editor?.path);
  $("backupModelBtn").onclick = () => backupModel(caseId);
  $("discardChangesBtn").onclick = () => discardChanges();
  $("exportChangesBtn").onclick = () => exportChanges();
  $("createTaskFromCaseBtn").onclick = () => openTaskDialog(caseId);
}

// Component type mapping
const componentTypes = {
  bus: ["Bus", "bus", "BusFault", "bus_interface"],
  line: ["Line", "line", "LineFault", "line_interface", "LCC", "VSC", "MMC", "TLine"],
  transformer: ["Transformer", "transformer", "TwoWindingTransformer", "ThreeWindingTransformer", "PhaseShiftingTransformer"],
  generator: ["Generator", "generator", "SyncGenerator", "InductionGenerator", "WindTurbine", "SolarPV", "Battery", "BESS"],
  load: ["Load", "load", "PQLoad", "ZIPLoad", "InductionMotor", "DynamicLoad"],
  control: ["Gov", "Tur", "PSS", "Exc", "AVR", "Governor", "Turbine", "Stabilizer", "Exciter", "PrimeMover"],
  meter: ["Meter", "Multimeter", "VoltageMeter", "CurrentMeter", "PowerMeter"],
  channel: ["Channel", "PlotChannel", "Oscilloscope", "Recorder"],
  fault: ["Fault", "FaultEvent", "ShortCircuit", "Breaker"],
};

function getComponentType(definition) {
  if (!definition) return "other";
  const def = definition.toLowerCase();
  for (const [type, patterns] of Object.entries(componentTypes)) {
    for (const pattern of patterns) {
      if (def.includes(pattern.toLowerCase())) return type;
    }
  }
  return "other";
}

function renderComponentNav(editor) {
  if (!editor || !editor.groups) {
    document.querySelectorAll(".nav-count").forEach(el => el.textContent = "0");
    return;
  }

  const counts = {
    all: 0,
    bus: 0,
    line: 0,
    transformer: 0,
    generator: 0,
    load: 0,
    control: 0,
    meter: 0,
    channel: 0,
    fault: 0,
    other: 0,
  };

  Object.values(editor.groups).forEach(group => {
    (group.rows || []).forEach(row => {
      counts.all++;
      const type = getComponentType(row.definition);
      counts[type]++;
    });
  });

  // Update count displays
  $("countAll").textContent = counts.all;
  $("countBus").textContent = counts.bus;
  $("countLine").textContent = counts.line;
  $("countTransformer").textContent = counts.transformer;
  $("countGenerator").textContent = counts.generator;
  $("countLoad").textContent = counts.load;
  $("countControl").textContent = counts.control;
  $("countMeter").textContent = counts.meter;
  $("countChannel").textContent = counts.channel;
  $("countFault").textContent = counts.fault;
}

function renderParameterTable(editor, filterType) {
  state.activeModelEditor = editor;
  state.activeComponentType = filterType || "all";
  const container = $("parameterTable");
  if (!editor || !editor.groups) {
    container.innerHTML = '<div class="detail-empty">选择一个 Case 并点击元件分类查看参数</div>';
    return;
  }

  if (!editor.editable) {
    container.innerHTML = `<div class="detail-empty">${esc(editor.reason || "暂无可编辑本地模型")}</div>`;
    return;
  }

  // Collect all components based on filter
  let allRows = [];
  Object.values(editor.groups).forEach(group => {
    (group.rows || []).forEach(row => {
      const type = getComponentType(row.definition);
      if (filterType === "all" || type === filterType) {
        allRows.push({ ...row, group: group.name, type });
      }
    });
  });

  if (allRows.length === 0) {
    container.innerHTML = '<div class="detail-empty">该分类下暂无元件</div>';
    return;
  }

  // Get all unique columns
  const allColumns = new Set();
  allRows.forEach(row => {
    Object.keys(row.args || {}).forEach(key => allColumns.add(key));
  });
  const availableColumns = Array.from(allColumns).sort();
  const columns = selectedModelColumns(editor, filterType, allRows, availableColumns);

  // Render table
  container.innerHTML = `
    <div class="model-viewbar">
      <div>
        <strong>${esc(allRows.length)}</strong> 个元件 · 显示 <strong>${esc(columns.length)}</strong> / ${esc(availableColumns.length)} 个属性
      </div>
      <div class="model-view-actions">
        <select id="modelColumnPicker">
          <option value="">添加属性列...</option>
          ${availableColumns.filter((column) => !columns.includes(column)).map((column) => `<option value="${esc(column)}">${esc(column)}</option>`).join("")}
        </select>
        <button class="button small secondary" id="modelColumnReset">重置视图</button>
      </div>
    </div>
    <div class="model-column-chips">
      ${columns.map((column) => `<button class="column-chip" data-column="${esc(column)}">${esc(column)} <span>×</span></button>`).join("")}
    </div>
    <div class="model-table-wrap">
      <table class="data-table model-table">
        <thead>
          <tr>
            <th>元件</th>
            <th>定义</th>
            <th>类型</th>
            ${columns.map(col => `<th>${esc(col)}</th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${allRows.map(row => `
            <tr data-component-id="${esc(row.id)}" data-cell-key="${esc(row.cell_key || row.id)}" data-component-type="${esc(row.type)}">
              <td><strong>${esc(row.label)}</strong><div class="meta">${esc(row.id)}</div></td>
              <td>${esc(row.definition)}</td>
              <td><span class="pill">${esc(row.type)}</span></td>
              ${columns.map(col => renderParameterCell(row, col)).join("")}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;

  // Bind cell editing
  bindModelColumnControls(editor, filterType, columns, availableColumns);
  bindParameterCells();
}

function renderParameterCell(row, column) {
  const value = (row.args || {})[column];
  const encoded = esc(JSON.stringify(value));
  const key = editKey(row.cell_key || row.id, column);
  const isDirty = state.modelEdits[key] !== undefined;
  const summary = modelValueSummary(value);
  const readonly = scalarLike(value) ? "" : "readonly";
  const title = scalarLike(value) ? String(value ?? "") : JSON.stringify(value);
  return `<td><input class="model-param ${isDirty ? 'dirty' : ''} ${readonly ? 'object-param' : ''}" ${readonly} title="${esc(title)}" data-component-id="${esc(row.id)}" data-cell-key="${esc(row.cell_key || row.id)}" data-arg="${esc(column)}" data-original="${encoded}" value="${esc(summary)}" /></td>`;
}

function bindModelColumnControls(editor, type, columns, availableColumns) {
  $("modelColumnPicker")?.addEventListener("change", (event) => {
    const column = event.target.value;
    if (!column) return;
    saveModelColumnView(editor, type, Array.from(new Set([...columns, column])));
    renderParameterTable(editor, type);
  });
  $("modelColumnReset")?.addEventListener("click", () => {
    localStorage.removeItem(modelViewKey(editor, type));
    renderParameterTable(editor, type);
  });
  document.querySelectorAll(".column-chip").forEach((button) => {
    button.addEventListener("click", () => {
      const next = columns.filter((column) => column !== button.dataset.column);
      saveModelColumnView(editor, type, next.length ? next : availableColumns.slice(0, 1));
      renderParameterTable(editor, type);
    });
  });
}

function bindComponentNav(editor) {
  document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const type = tab.dataset.type;
      renderParameterTable(editor, type);
    });
  });
}

function bindParameterCells() {
  document.querySelectorAll(".model-param").forEach(input => {
    input.addEventListener("input", () => {
      const original = JSON.parse(input.dataset.original || "null");
      const value = coerceModelValue(input.value, original);
      const key = editKey(input.dataset.cellKey || input.dataset.componentId, input.dataset.arg);
      input.classList.toggle("dirty", value !== original);

      if (value === original) {
        delete state.modelEdits[key];
      } else {
        state.modelEdits[key] = {
          id: input.dataset.componentId,
          cell_key: input.dataset.cellKey,
          arg: input.dataset.arg,
          value,
          original,
          timestamp: new Date().toISOString(),
        };
      }

      updateEditPanel();
    });
  });
}

function updateEditPanel() {
  const edits = Object.values(state.modelEdits);
  const pendingCount = edits.length;
  const modifiedParamsCount = new Set(edits.map(e => e.id)).size;

  $("pendingChangesCount").textContent = pendingCount;
  $("modifiedParamsCount").textContent = modifiedParamsCount;

  // Update history list
  const historyList = $("changeHistoryList");
  if (pendingCount === 0) {
    historyList.innerHTML = '<div class="history-empty">暂无修改</div>';
    $("discardChangesBtn").disabled = true;
    $("exportChangesBtn").disabled = true;
  } else {
    historyList.innerHTML = edits.slice(-10).reverse().map(edit => `
      <div class="history-item dirty">
        <div class="history-item-header">
          <span class="history-item-title">${esc(edit.id)}</span>
          <span class="history-item-time">${formatRelativeTime(edit.timestamp)}</span>
        </div>
        <div class="history-item-detail">${esc(edit.arg)}: ${esc(JSON.stringify(edit.original))} → ${esc(JSON.stringify(edit.value))}</div>
      </div>
    `).join("");
    $("discardChangesBtn").disabled = false;
    $("exportChangesBtn").disabled = false;
  }
}

function discardChanges() {
  if (confirm("确定放弃所有未保存的修改吗？")) {
    state.modelEdits = {};
    if (state.selectedCaseId) {
      loadCaseDetail(state.selectedCaseId);
    }
    showNotice("已放弃所有修改");
  }
}

function exportChanges() {
  const edits = Object.values(state.modelEdits);
  if (edits.length === 0) return;

  const exportData = {
    timestamp: new Date().toISOString(),
    caseId: state.selectedCaseId,
    changes: edits,
  };

  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `model-changes-${state.selectedCaseId}-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);

  showNotice("差异已导出");
}

async function backupModel(caseId) {
  try {
    const result = await api(`/api/cases/${caseId}/backup`, { method: "POST" });
    showNotice(`模型已备份: ${result.backup_path}`);
  } catch (error) {
    showNotice(error.message, "error");
  }
}

function field(label, value) {
  return `<div class="field"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
}

function renderModelEditor(editor) {
  if (!editor || !editor.editable) {
    return `<div class="model-empty">${esc((editor && editor.reason) || "暂无可编辑本地模型")}</div>`;
  }
  const groups = Object.values(editor.groups || {});
  return `
    <div class="model-editor" data-model-path="${esc(editor.path)}">
      <div class="model-toolbar">
        <div>
          <strong>${esc(editor.name || "Model")}</strong>
          <span>${esc(editor.component_count)} components · ${esc(editor.path)}</span>
        </div>
        <div class="model-actions">
          <input id="modelSearch" class="model-search" placeholder="搜索元件、类型或参数" />
          <button class="button small" id="saveModelEdits">保存模型</button>
        </div>
      </div>
      <div class="model-tabs">
        ${groups.map((group, index) => `<button class="model-tab ${index === 0 ? "active" : ""}" data-model-group="${esc(group.name)}">${esc(group.name)} (${esc(group.count)})</button>`).join("")}
      </div>
      ${groups.map((group, index) => renderModelGroup(group, index === 0)).join("")}
    </div>
  `;
}

function renderModelGroup(group, active) {
  const columns = group.columns || [];
  return `
    <div class="model-group ${active ? "active" : ""}" data-model-group-panel="${esc(group.name)}">
      <div class="model-table-wrap">
        <table class="data-table model-table">
          <thead>
            <tr>
              <th>元件</th>
              <th>定义</th>
              ${columns.map((column) => `<th>${esc(column)}</th>`).join("")}
            </tr>
          </thead>
          <tbody>
            ${(group.rows || []).map((row) => `
              <tr>
                <td><strong>${esc(row.label)}</strong><div class="meta">${esc(row.id)}</div></td>
                <td>${esc(row.definition)}</td>
                ${columns.map((column) => renderModelCell(row, column)).join("")}
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderModelCell(row, column) {
  const value = (row.args || {})[column];
  const encoded = esc(JSON.stringify(value));
  return `<td><input class="model-param" data-component-id="${esc(row.id)}" data-cell-key="${esc(row.cell_key || row.id)}" data-arg="${esc(column)}" data-original="${encoded}" value="${esc(value ?? "")}" /></td>`;
}

function bindModelEditor(editor) {
  if (!editor || !editor.editable) return;
  state.modelEdits = {};
  document.querySelectorAll(".model-tab").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".model-tab").forEach((node) => node.classList.remove("active"));
      document.querySelectorAll(".model-group").forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      const escaped = window.CSS && CSS.escape ? CSS.escape(button.dataset.modelGroup) : button.dataset.modelGroup.replaceAll('"', '\\"');
      const panel = document.querySelector(`[data-model-group-panel="${escaped}"]`);
      if (panel) panel.classList.add("active");
    });
  });
  const search = $("modelSearch");
  if (search) {
    search.addEventListener("input", () => filterModelRows(search.value));
  }
  document.querySelectorAll(".model-param").forEach((input) => {
    input.addEventListener("input", () => {
      const original = JSON.parse(input.dataset.original || "null");
      const value = coerceModelValue(input.value, original);
      const key = editKey(input.dataset.cellKey || input.dataset.componentId, input.dataset.arg);
      input.classList.toggle("dirty", value !== original);
      if (value === original) delete state.modelEdits[key];
      else state.modelEdits[key] = { id: input.dataset.componentId, cell_key: input.dataset.cellKey, arg: input.dataset.arg, value };
    });
  });
  const saveButton = $("saveModelEdits");
  if (saveButton) {
    saveButton.addEventListener("click", () => saveModelEdits(editor.path));
  }
}

function filterModelRows(query) {
  const needle = String(query || "").trim().toLowerCase();
  document.querySelectorAll(".model-table tbody tr").forEach((row) => {
    row.classList.toggle("hidden-row", Boolean(needle) && !row.textContent.toLowerCase().includes(needle));
  });
}

function coerceModelValue(value, original) {
  if (typeof original === "number") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : value;
  }
  if (typeof original === "boolean") {
    return ["true", "1", "yes", "on"].includes(String(value).toLowerCase());
  }
  if (original === null && value === "") return null;
  return value;
}

async function saveModelEdits(path) {
  const updates = Object.values(state.modelEdits);
  if (!updates.length) {
    showNotice("模型没有修改");
    return;
  }
  try {
    const result = await api("/api/models/edits", {
      method: "POST",
      body: JSON.stringify({ case_id: state.selectedCaseId, path, updates }),
    });
    showNotice(`模型已保存：${result.changed} 处修改，备份 ${result.backup_path}`);
    state.modelEdits = {};
    if (state.selectedCaseId) await loadCaseDetail(state.selectedCaseId);
  } catch (error) {
    showNotice(error.message, "error");
  }
}

// Current task filter
let currentTaskFilter = "all";

function taskRow(task) {
  const canRun = ["created", "submitted", "failed"].includes(task.status);
  return `
    <div class="table-row">
      <div class="row-title"><span>${esc(task.name)}</span>${pill(task.status)}</div>
      <div class="meta">${esc(task.id)} · ${esc(task.type)} · result ${esc(compactId(task.result_id || "-"))}</div>
      <div class="subline">Config: ${esc(JSON.stringify(task.config || {}))}</div>
      <div class="subline">Job: ${esc(task.job_id || "-")} · submitted ${esc(task.submitted_at || "-")} · completed ${esc(task.completed_at || "-")}</div>
      ${canRun ? `<button class="button small secondary edit-task" data-task-id="${esc(task.id)}">配置</button>` : ""}
      <button class="button small secondary preflight-task" data-task-id="${esc(task.id)}">检查</button>
      ${canRun ? `<button class="button small run-task" data-task-id="${esc(task.id)}">运行</button>` : ""}
    </div>
  `;
}

function taskWorkbenchRow(task) {
  const canRun = ["created", "submitted", "failed"].includes(task.status);
  return `
    <div class="run-card">
      <div class="row-title"><span>${esc(task.name)}</span>${pill(task.status)}</div>
      <div class="config-grid">
        ${field("类型", task.type)}
        ${field("模型源", (task.config || {}).model_source || "CloudPSS RID")}
        ${field("通道", taskChannels(task) || "默认通道")}
        ${field("结果", task.result_id || "-")}
      </div>
      <pre class="config-preview">${esc(JSON.stringify(task.config || {}, null, 2))}</pre>
      <div class="row-actions">
        ${canRun ? `<button class="button small secondary edit-task" data-task-id="${esc(task.id)}">配置</button>` : ""}
        <button class="button small secondary preflight-task" data-task-id="${esc(task.id)}">检查</button>
        ${canRun ? `<button class="button small run-task" data-task-id="${esc(task.id)}">运行</button>` : ""}
      </div>
    </div>
  `;
}

// Enhanced Task Card for tasksView
function taskCard(task) {
  const isRunning = task.status === "running";
  const isFailed = task.status === "failed";
  const isCompleted = task.status === "completed";
  const progress = calculateTaskProgress(task);

  // Timeline mini visualization
  const hasCreated = !!task.created_at;
  const hasSubmitted = !!task.submitted_at;
  const hasStarted = !!task.started_at;
  const hasCompleted = !!task.completed_at;

  return `
    <div class="task-card ${esc(task.status)}" data-task-id="${esc(task.id)}" onclick="openTaskDetailDialog('${esc(task.id)}')">
      <div class="task-card-header">
        <span class="task-card-title">${esc(task.name)}</span>
        ${pill(task.status)}
      </div>
      <div class="task-card-meta">
        <span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          ${esc(task.type)}
        </span>
        <span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          </svg>
          ${esc(compactId(task.id))}
        </span>
        <span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          ${formatRelativeTime(task.created_at)}
        </span>
      </div>

      <div class="task-card-timeline">
        <span class="timeline-mini-dot ${hasCreated ? 'completed' : ''}"></span>
        <span class="timeline-mini-dot ${hasSubmitted ? 'completed' : ''}"></span>
        <span class="timeline-mini-dot ${hasStarted ? (isRunning ? 'active' : 'completed') : ''}"></span>
        <span class="timeline-mini-dot ${hasCompleted ? 'completed' : ''}"></span>
      </div>

      ${isRunning ? `
        <div class="task-card-progress">
          <div class="progress-header">
            <span>运行中...</span>
            <span>${progress}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill ${progress === 0 ? 'indeterminate' : ''}" style="width: ${progress}%"></div>
          </div>
        </div>
      ` : ""}

      <div class="task-card-actions" onclick="event.stopPropagation()">
        ${isRunning ? `<button class="button small danger" onclick="cancelTask('${esc(task.id)}')">取消</button>` : ""}
        ${isFailed ? `<button class="button small secondary" onclick="rerunTask('${esc(task.id)}')">重跑</button>` : ""}
        ${isCompleted ? `<button class="button small" onclick="viewTaskResult('${esc(task.id)}')">结果</button>` : ""}
        <button class="button small secondary" onclick="cloneTask('${esc(task.id)}')">复制</button>
      </div>
    </div>
  `;
}

function calculateTaskProgress(task) {
  if (task.status === "completed") return 100;
  if (task.status !== "running") return 0;
  if (task.progress !== undefined) return task.progress;

  // Estimate progress based on time if available
  if (task.started_at && task.estimated_duration) {
    const elapsed = Date.now() - new Date(task.started_at).getTime();
    const estimated = task.estimated_duration * 1000;
    return Math.min(95, Math.round((elapsed / estimated) * 100));
  }

  return 0;
}

function updateTaskStats() {
  const tasks = state.snapshot?.tasks || [];
  const running = tasks.filter((t) => t.status === "running").length;
  const completed = tasks.filter((t) => t.status === "completed").length;
  const failed = tasks.filter((t) => t.status === "failed").length;

  setText("runningCount", running);
  setText("completedCount", completed);
  setText("failedCount", failed);
}

function variantRow(variant) {
  return `
    <div class="table-row">
      <div class="row-title"><span>${esc(variant.name)}</span><span class="pill">variant</span></div>
      <div class="meta">${esc(variant.id)} · ${esc(JSON.stringify(variant.parameters || {}))}</div>
    </div>
  `;
}

function renderTasks() {
  const tasks = state.snapshot?.tasks || [];

  // Update stats
  updateTaskStats();

  // Filter tasks
  const filtered = currentTaskFilter === "all" ? tasks : tasks.filter((t) => t.status === currentTaskFilter);

  setHtml("taskCards", taskTableRows(filtered));

  // Also update the old table view if an older layout still provides it.
  setHtml("taskTable", tasks.map(taskRow).join("") || empty("暂无任务"));
  bindTaskRuns();
}

function openTaskDetailDialog(taskId) {
  const task = state.snapshot?.tasks?.find((t) => t.id === taskId);
  if (!task) return;

  // Populate dialog
  $("taskDetailTitle").textContent = task.name || "任务详情";
  $("taskDetailStatus").textContent = task.status || "-";
  $("taskDetailStatus").className = `pill ${task.status || ""}`;

  // Timeline
  const createdTime = $("taskCreatedTime");
  const submittedTime = $("taskSubmittedTime");
  const startedTime = $("taskStartedTime");
  const completedTime = $("taskCompletedTime");

  createdTime.textContent = task.created_at ? formatRelativeTime(task.created_at) : "-";
  submittedTime.textContent = task.submitted_at ? formatRelativeTime(task.submitted_at) : "-";
  startedTime.textContent = task.started_at ? formatRelativeTime(task.started_at) : "-";
  completedTime.textContent = task.completed_at ? formatRelativeTime(task.completed_at) : "-";

  // Update timeline items status
  $("timelineCreated").className = "timeline-item completed";
  $("timelineSubmitted").className = task.submitted_at ? "timeline-item completed" : "timeline-item";
  $("timelineStarted").className = task.started_at ? (task.status === "running" ? "timeline-item active" : "timeline-item completed") : "timeline-item";
  $("timelineCompleted").className = task.completed_at ? "timeline-item completed" : "timeline-item";

  // Progress
  const progressSection = $("taskProgressSection");
  if (task.status === "running") {
    progressSection.classList.remove("hidden");
    const progress = calculateTaskProgress(task);
    $("taskProgressPercent").textContent = progress + "%";
    $("taskProgressFill").style.width = progress + "%";
    $("taskProgressFill").className = "progress-fill" + (progress === 0 ? " indeterminate" : "");
  } else {
    progressSection.classList.add("hidden");
  }

  // Error message
  const errorSection = $("taskErrorSection");
  if (task.error || task.status === "failed") {
    errorSection.classList.remove("hidden");
    $("taskErrorMessage").textContent = task.error || "任务执行失败";
  } else {
    errorSection.classList.add("hidden");
  }

  // Config summary
  const configGrid = $("taskConfigGrid");
  configGrid.innerHTML = `
    <div class="field"><span>任务 ID</span><strong>${esc(task.id)}</strong></div>
    <div class="field"><span>类型</span><strong>${esc(task.type)}</strong></div>
    <div class="field"><span>Case ID</span><strong>${esc(compactId(task.case_id))}</strong></div>
    <div class="field"><span>Job ID</span><strong>${esc(task.job_id || "-")}</strong></div>
    <div class="field"><span>结果 ID</span><strong>${esc(task.result_id ? compactId(task.result_id) : "-")}</strong></div>
    <div class="field"><span>配置</span><strong>${esc(JSON.stringify(task.config || {}))}</strong></div>
  `;

  // Load logs (placeholder)
  $("taskLogsContent").textContent = task.logs || "暂无日志";

  // Show/hide action buttons based on status
  $("cancelTaskBtn").classList.toggle("hidden", task.status !== "running");
  $("rerunTaskBtn").classList.toggle("hidden", !["failed", "completed"].includes(task.status));
  $("viewResultBtn").classList.toggle("hidden", !task.result_id);

  // Store current task ID for actions
  $("taskDetailDialog").dataset.taskId = taskId;

  // Show dialog
  $("taskDetailDialog").showModal();
}

async function cancelTask(taskId) {
  if (!confirm("确定要取消此任务吗？")) return;

  try {
    await api(`/api/tasks/${taskId}/cancel`, { method: "POST" });
    showNotice("任务已取消");
    await refresh();
    // Refresh dialog if open
    if ($("taskDetailDialog").open && $("taskDetailDialog").dataset.taskId === taskId) {
      openTaskDetailDialog(taskId);
    }
  } catch (error) {
    showNotice(error.message, "error");
  }
}

async function rerunTask(taskId) {
  try {
    const result = await api(`/api/tasks/${taskId}/rerun`, {
      method: "POST",
      body: JSON.stringify({ timeout: 300 }),
    });
    showNotice(`任务已重跑，新任务 ID: ${result.new_task_id || taskId}`);
    await refresh();
    // Refresh dialog if open
    if ($("taskDetailDialog").open && $("taskDetailDialog").dataset.taskId === taskId) {
      openTaskDetailDialog(taskId);
    }
  } catch (error) {
    showNotice(error.message, "error");
  }
}

async function cloneTask(taskId) {
  const task = state.snapshot?.tasks?.find((t) => t.id === taskId);
  if (!task) return;

  // Open task dialog with cloned values
  openTaskDialog(task.case_id);

  // Pre-fill the form
  setTimeout(() => {
    const form = $("taskForm");
    if (form) {
      form.name.value = task.name + " (复制)";
      // Select appropriate sim type
      const simType = task.type || "powerflow";
      const typeRadio = form.querySelector(`input[name="sim_type"][value="${simType}"]`);
      if (typeRadio) {
        typeRadio.checked = true;
        showSimConfigForm(simType);
      }
      // Fill other fields based on task config
      const config = task.config || {};
      if (config.model_source) {
        const input = form.querySelector(`input[name="model_source"]`);
        if (input) input.value = config.model_source;
      }
    }
  }, 100);
}

function viewTaskResult(taskId) {
  const task = state.snapshot?.tasks?.find((t) => t.id === taskId);
  if (task?.result_id) {
    loadResultDetail(task.result_id);
    $("taskDetailDialog").close();
    switchView("results");
  }
}

function bindTaskRuns() {
  document.querySelectorAll(".edit-task").forEach((button) => {
    button.addEventListener("click", () => {
      const task = state.snapshot.tasks.find((item) => item.id === button.dataset.taskId);
      if (task) openEditTaskDialog(task);
    });
  });
  document.querySelectorAll(".preflight-task").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        const result = await api(`/api/tasks/${button.dataset.taskId}/preflight`);
        const failed = result.checks.filter((item) => !item.ok);
        showNotice(failed.length ? `检查未通过：${failed.map((item) => item.name).join(", ")}` : "运行前检查通过", failed.length ? "error" : "info");
      } catch (error) {
        showNotice(error.message, "error");
      }
    });
  });
  document.querySelectorAll(".run-task").forEach((button) => {
    button.addEventListener("click", async () => {
      const taskId = button.dataset.taskId;
      button.disabled = true;
      button.textContent = "运行中";
      try {
        const result = await api(`/api/tasks/${taskId}/run`, {
          method: "POST",
          body: JSON.stringify({ timeout: 300 }),
        });
        showNotice(`任务完成，结果 ${result.result_id}`);
        await refresh();
        if (state.selectedCaseId) await loadCaseDetail(state.selectedCaseId);
      } catch (error) {
        showNotice(error.message, "error");
      } finally {
        button.disabled = false;
        button.textContent = "运行";
      }
    });
  });
}

function renderResults() {
  setHtml("resultList", resultTableRows(state.snapshot.results || []));
  setText("resultSelectionHint", state.selectedResultId ? `当前选中：${state.selectedResultId}` : "选择一行查看摘要、曲线、产物和报告。");
  if (state.selectedResultDetail) renderResultDetailTabs(state.selectedResultDetail);
  bindResultClicks();
}

function bindResultClicks() {
  document.querySelectorAll("#resultList [data-result-id]").forEach((node) => {
    node.addEventListener("click", () => loadResultDetail(node.dataset.resultId));
  });
}

async function loadResultDetail(resultId) {
  state.selectedResultId = resultId;
  switchView("results");
  const detail = await api(`/api/results/${resultId}`);
  state.selectedResultDetail = detail;
  renderResults();
  renderResultDetailTabs(detail);
  switchResultTab(state.resultTab === "table" ? "summary" : state.resultTab);
}

function renderResultDetailTabs(detail) {
  if (!detail || !detail.result) return;
  const result = detail.result;
  const metadata = result.metadata || {};
  setText("resultSummaryTitle", result.name || "结果摘要");
  setText("resultSelectionHint", `当前选中：${result.id}`);
  setHtml("resultSummaryContent", `
    <div class="result-summary-grid">
      ${field("Result ID", result.id)}
      ${field("Format", result.format)}
      ${field("Task", result.task_id || "-")}
      ${field("Case", result.case_id || "-")}
      ${field("Size", formatBytes(result.size_bytes || 0))}
      ${field("Directory", detail.directory || "-")}
      ${field("Job", metadata.job_id || "-")}
      ${field("Data Source", metadata.data_source || "-")}
      ${field("Server", metadata.server_url || "-")}
      ${field("Owner", metadata.server_owner || "-")}
    </div>
    ${renderResultHeadline(detail.summary)}
  `);
  setHtml("resultDataContent", renderResultData(detail));
  setHtml("resultArtifactsContent", renderStructuredBlock(detail.artifacts || {}, "暂无 Artifacts"));
  setHtml("resultMetadataContent", renderStructuredBlock(metadata, "暂无 Metadata"));
  setHtml("resultReportContent", detail.report ? `<pre class="result-pre">${esc(detail.report)}</pre>` : empty("尚未生成报告"));
  bindResultActionButtons(result.id);
  window.requestAnimationFrame(drawCharts);
}

function bindResultActionButtons(resultId) {
  if ($("reportBtn")) $("reportBtn").onclick = () => resultAction(resultId, "report");
  if ($("archiveBtn")) $("archiveBtn").onclick = () => resultAction(resultId, "archive");
  if ($("exportCsvBtn")) $("exportCsvBtn").onclick = () => exportResultData(resultId, "csv");
  if ($("exportJsonBtn")) $("exportJsonBtn").onclick = () => exportResultData(resultId, "json");
  if ($("copyResultIdBtn")) $("copyResultIdBtn").onclick = () => {
    navigator.clipboard.writeText(resultId);
    showNotice("结果 ID 已复制到剪贴板");
  };
}

function renderStructuredBlock(value, emptyMessage) {
  if (!value || (typeof value === "object" && Object.keys(value).length === 0)) return empty(emptyMessage);
  return `<pre class="result-pre">${esc(JSON.stringify(value, null, 2))}</pre>`;
}

function renderResultHeadline(summary) {
  if (!summary) return empty("暂无摘要数据");
  if (summary.kind === "powerflow") {
    const buses = summary.buses_preview || [];
    const voltages = buses.map((b) => parseFloat(b.V || b.voltage || 0)).filter((v) => !isNaN(v));
    const maxV = voltages.length > 0 ? Math.max(...voltages) : 0;
    const minV = voltages.length > 0 ? Math.min(...voltages) : 0;
    const avgV = voltages.length > 0 ? voltages.reduce((a, b) => a + b, 0) / voltages.length : 0;
    const violations = powerflowViolations(summary);
    return `
      <div class="stats-panel result-stats-panel">
        <div class="stat-box"><span class="stat-box-label">最大电压</span><span class="stat-box-value ${maxV > 1.05 ? "text-danger" : ""}">${maxV.toFixed(3)}</span></div>
        <div class="stat-box"><span class="stat-box-label">最小电压</span><span class="stat-box-value ${minV < 0.95 ? "text-warning" : ""}">${minV.toFixed(3)}</span></div>
        <div class="stat-box"><span class="stat-box-label">平均电压</span><span class="stat-box-value">${avgV.toFixed(3)}</span></div>
        <div class="stat-box"><span class="stat-box-label">越限数量</span><span class="stat-box-value ${violations.length > 0 ? "text-danger" : ""}">${violations.length}</span></div>
      </div>
      ${renderViolations(violations)}
    `;
  }
  if (summary.kind === "emt") {
    const channels = summary.channels || [];
    return `
      <div class="stats-panel result-stats-panel">
        <div class="stat-box"><span class="stat-box-label">通道数量</span><span class="stat-box-value">${summary.channel_count || channels.length}</span></div>
        <div class="stat-box"><span class="stat-box-label">采样点数</span><span class="stat-box-value">${(summary.metadata || {}).sample_points || "-"}</span></div>
        <div class="stat-box"><span class="stat-box-label">仿真时长</span><span class="stat-box-value">${(summary.metadata || {}).duration || "-"}s</span></div>
        <div class="stat-box"><span class="stat-box-label">步长</span><span class="stat-box-value">${(summary.metadata || {}).dt || "-"}s</span></div>
      </div>
    `;
  }
  return empty("未知结果类型");
}

function renderResultData(detail) {
  const summary = detail?.summary;
  if (!summary) return empty("暂无曲线或表格数据");
  if (summary.kind === "powerflow") {
    return `
      <div class="result-data-stack">
        <section class="result-data-section">
          <div class="chart-container">
            <div class="chart-header">
              <h4>母线电压分布</h4>
              <div class="chart-controls">
                <span class="text-muted" style="font-size: 12px;">参考范围: 0.95 ~ 1.05 pu</span>
              </div>
            </div>
            ${renderChartCanvas("busVoltageChart", "bar", summary.bus_chart || {})}
          </div>
        </section>
        <section class="result-data-section">
          <h4 class="section-title">Bus 表预览</h4>
          ${renderDataTable(summary.buses_preview || [])}
        </section>
        <section class="result-data-section">
          <h4 class="section-title">Branch 表预览</h4>
          ${renderDataTable(summary.branches_preview || [])}
        </section>
      </div>
    `;
  }
  if (summary.kind === "emt") {
    const channels = summary.channels || [];
    const channelStats = emtChannelStats(summary.series || {});
    return `
      <div class="result-data-stack">
        <section class="result-data-section">
          <h4 class="section-title">通道统计</h4>
          ${renderDataTable(channelStats)}
        </section>
        <section class="result-data-section">
          <h4 class="section-title">通道曲线</h4>
          <div class="result-chart-grid">
            ${renderSeriesCharts(summary.series || {})}
          </div>
        </section>
        <section class="result-data-section">
          <h4 class="section-title">CSV 预览</h4>
          ${channels.map((channel) => `
            <div class="table-row result-channel-preview">
              <div class="row-title"><span>${esc(channel.trace_key)}</span><span class="pill">${esc(channel.point_count)} points</span></div>
              <div class="meta">${esc(channel.csv_file)} · ${esc(channel.channel_file)}</div>
              ${renderCsvPreview((summary.csv_preview || {})[channel.csv_file])}
            </div>
          `).join("") || empty("暂无通道")}
        </section>
      </div>
    `;
  }
  return empty("暂无可展示数据");
}

function powerflowViolations(summary) {
  const violations = [];
  (summary.buses_preview || []).forEach((bus) => {
    const v = parseFloat(bus.V || bus.voltage || 0);
    if (v > 1.05) {
      violations.push({ bus: bus.name || bus.bus || bus.id, voltage: v, type: "high", severity: v > 1.1 ? "critical" : "warning" });
    } else if (v < 0.95) {
      violations.push({ bus: bus.name || bus.bus || bus.id, voltage: v, type: "low", severity: v < 0.9 ? "critical" : "warning" });
    }
  });
  return violations;
}

function renderViolations(violations) {
  if (!violations.length) return "";
  return `
    <div class="violations-section">
      <h4>电压越限警告</h4>
      ${violations.map((v) => `
        <div class="violation-item ${v.type}">
          <span class="violation-bus">${esc(v.bus)}</span>
          <span class="violation-value">${v.voltage.toFixed(4)} pu</span>
          <span class="violation-severity">${v.severity === "critical" ? "严重" : "警告"}</span>
        </div>
      `).join("")}
    </div>
  `;
}

function emtChannelStats(series) {
  return Object.entries(series).map(([name, data]) => {
    const points = data?.points || [];
    const values = points.map((p) => p.y).filter((v) => Number.isFinite(v));
    return {
      name,
      max: values.length > 0 ? Math.max(...values).toFixed(4) : "-",
      min: values.length > 0 ? Math.min(...values).toFixed(4) : "-",
      avg: values.length > 0 ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(4) : "-",
      count: points.length,
    };
  });
}

async function exportResultData(resultId, format) {
  try {
    const response = await api(`/api/results/${resultId}/export?format=${format}`);
    if (response.data) {
      const blob = new Blob([response.data], { type: format === "csv" ? "text/csv" : "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `result-${resultId.slice(0, 8)}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
      showNotice(`结果已导出为 ${format.toUpperCase()}`);
    }
  } catch (error) {
    showNotice("导出失败: " + error.message, "error");
  }
}

function renderResultSummary(summary) {
  if (!summary) return "";
  if (summary.kind === "powerflow") {
    // Calculate statistics
    const buses = summary.buses_preview || [];
    const voltages = buses.map((b) => parseFloat(b.V || b.voltage || 0)).filter((v) => !isNaN(v));
    const maxV = voltages.length > 0 ? Math.max(...voltages) : 0;
    const minV = voltages.length > 0 ? Math.min(...voltages) : 0;
    const avgV = voltages.length > 0 ? voltages.reduce((a, b) => a + b, 0) / voltages.length : 0;

    // Find voltage violations
    const violations = [];
    buses.forEach((bus) => {
      const v = parseFloat(bus.V || bus.voltage || 0);
      if (v > 1.05) {
        violations.push({ bus: bus.name || bus.bus || bus.id, voltage: v, type: "high", severity: v > 1.1 ? "critical" : "warning" });
      } else if (v < 0.95) {
        violations.push({ bus: bus.name || bus.bus || bus.id, voltage: v, type: "low", severity: v < 0.9 ? "critical" : "warning" });
      }
    });

    return `
      <h4 class="section-title">潮流摘要</h4>

      <!-- Statistics Panel -->
      <div class="stats-panel">
        <div class="stat-box">
          <span class="stat-box-label">最大电压</span>
          <span class="stat-box-value ${maxV > 1.05 ? 'text-danger' : ''}">${maxV.toFixed(3)}</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">最小电压</span>
          <span class="stat-box-value ${minV < 0.95 ? 'text-warning' : ''}">${minV.toFixed(3)}</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">平均电压</span>
          <span class="stat-box-value">${avgV.toFixed(3)}</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">越限数量</span>
          <span class="stat-box-value ${violations.length > 0 ? 'text-danger' : ''}">${violations.length}</span>
        </div>
      </div>

      ${violations.length > 0 ? `
        <div class="violations-section">
          <h4>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--danger); vertical-align: middle;">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            电压越限警告
          </h4>
          ${violations
            .map(
              (v) => `
            <div class="violation-item ${v.type}">
              <span class="violation-bus">${esc(v.bus)}</span>
              <span class="violation-value">${v.voltage.toFixed(4)} pu</span>
              <span class="violation-severity">${v.severity === "critical" ? "严重" : "警告"}</span>
            </div>
          `
            )
            .join("")}
        </div>
      ` : ""}

      <div class="chart-container">
        <div class="chart-header">
          <h4>母线电压分布</h4>
          <div class="chart-controls">
            <span class="text-muted" style="font-size: 12px;">参考范围: 0.95 ~ 1.05 pu</span>
          </div>
        </div>
        ${renderChartCanvas("busVoltageChart", "bar", summary.bus_chart || {})}
        <div class="chart-legend">
          <div class="legend-item">
            <div class="legend-color" style="background: #265f9e;"></div>
            <span>正常范围</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background: #f59e0b;"></div>
            <span>越限警告</span>
          </div>
        </div>
      </div>

      <h4 class="section-title">Bus 表预览</h4>
      ${renderDataTable(summary.buses_preview || [])}
      <h4 class="section-title">Branch 表预览</h4>
      ${renderDataTable(summary.branches_preview || [])}
    `;
  }
  if (summary.kind === "emt") {
    const channels = summary.channels || [];
    const series = summary.series || {};

    // Calculate channel statistics
    const channelStats = Object.entries(series).map(([name, data]) => {
      const points = data?.points || [];
      const values = points.map((p) => p.y).filter((v) => Number.isFinite(v));
      return {
        name,
        max: values.length > 0 ? Math.max(...values) : 0,
        min: values.length > 0 ? Math.min(...values) : 0,
        avg: values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0,
        count: points.length,
      };
    });

    return `
      <h4 class="section-title">EMT 摘要</h4>

      <!-- Statistics Panel -->
      <div class="stats-panel">
        <div class="stat-box">
          <span class="stat-box-label">通道数量</span>
          <span class="stat-box-value">${summary.channel_count || channels.length}</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">采样点数</span>
          <span class="stat-box-value">${(summary.metadata || {}).sample_points || "-"}</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">仿真时长</span>
          <span class="stat-box-value">${(summary.metadata || {}).duration || "-"}s</span>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">步长</span>
          <span class="stat-box-value">${(summary.metadata || {}).dt || "-"}s</span>
        </div>
      </div>

      <!-- Channel Comparison Section -->
      <div class="channel-compare-section">
        <h4>通道统计</h4>
        <div class="data-table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>通道名称</th>
                <th>最大值</th>
                <th>最小值</th>
                <th>平均值</th>
                <th>采样数</th>
              </tr>
            </thead>
            <tbody>
              ${channelStats
                .map(
                  (s) => `
                <tr>
                  <td>${esc(s.name)}</td>
                  <td>${s.max.toFixed(4)}</td>
                  <td>${s.min.toFixed(4)}</td>
                  <td>${s.avg.toFixed(4)}</td>
                  <td>${s.count}</td>
                </tr>
              `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </div>

      <h4 class="section-title">通道曲线</h4>
      ${renderSeriesCharts(series)}
      ${channels.map((channel) => `
        <div class="table-row">
          <div class="row-title"><span>${esc(channel.trace_key)}</span><span class="pill">${esc(channel.point_count)} points</span></div>
          <div class="meta">${esc(channel.csv_file)} · ${esc(channel.channel_file)}</div>
          ${renderCsvPreview((summary.csv_preview || {})[channel.csv_file])}
        </div>
      `).join("") || empty("暂无通道")}
    `;
  }
  return "";
}

function renderChartCanvas(id, kind, data) {
  const encoded = esc(JSON.stringify({ kind, data }));
  return `<canvas class="result-chart" id="${esc(id)}" data-chart="${encoded}" width="900" height="260"></canvas>`;
}

function renderSeriesCharts(series) {
  const entries = Object.entries(series).filter(([, payload]) => payload && payload.points && payload.points.length);
  if (!entries.length) return "";
  return entries.map(([name, payload], index) => `
    <div class="chart-block">
      <div class="meta">${esc(name)} · ${esc(payload.total_points || payload.points.length)} points</div>
      ${renderChartCanvas(`emtSeriesChart${index}`, "line", payload)}
    </div>
  `).join("");
}

function drawCharts() {
  document.querySelectorAll("canvas[data-chart]").forEach((canvas) => {
    try {
      const payload = JSON.parse(canvas.dataset.chart || "{}");
      drawChart(canvas, payload.kind, payload.data || {});
    } catch (_error) {
      const context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
  });
}

// Store Chart.js instances for cleanup
const chartInstances = new Map();

function drawChart(canvas, kind, data) {
  // Destroy existing chart if any
  if (chartInstances.has(canvas.id)) {
    chartInstances.get(canvas.id).destroy();
    chartInstances.delete(canvas.id);
  }

  const points = (data.points || []).filter((point) => Number.isFinite(point.y));
  if (!points.length) return;

  const labels = points.map((point, index) => point.x !== undefined ? point.x : index);
  const values = points.map((point) => point.y);

  // Detect dark mode
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";

  // Chart colors based on theme
  const colors = {
    primary: isDark ? "#14b8a6" : "#116b68",
    primaryAlpha: isDark ? "rgba(20, 184, 166, 0.2)" : "rgba(17, 107, 104, 0.2)",
    grid: isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.05)",
    text: isDark ? "#e2e8f0" : "#334155",
    muted: isDark ? "#64748b" : "#64748b",
  };

  const ctx = canvas.getContext("2d");

  const config = {
    type: kind === "bar" ? "bar" : "line",
    data: {
      labels: labels,
      datasets: [{
        label: data.label || "数值",
        data: values,
        backgroundColor: kind === "bar" ? colors.primary : colors.primaryAlpha,
        borderColor: colors.primary,
        borderWidth: 2,
        pointRadius: kind === "bar" ? 0 : 3,
        pointHoverRadius: kind === "bar" ? 0 : 5,
        pointBackgroundColor: colors.primary,
        fill: kind === "line",
        tension: kind === "line" ? 0.1 : 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: isDark ? "#1e293b" : "#ffffff",
          titleColor: colors.text,
          bodyColor: colors.text,
          borderColor: isDark ? "#334155" : "#e2e8f0",
          borderWidth: 1,
          padding: 10,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return `数值: ${context.parsed.y?.toFixed(4) || context.parsed.y}`;
            }
          }
        },
      },
      scales: {
        x: {
          grid: {
            color: colors.grid,
            drawBorder: false,
          },
          ticks: {
            color: colors.muted,
            font: {
              size: 11,
            },
            maxRotation: 45,
            minRotation: 0,
          },
        },
        y: {
          grid: {
            color: colors.grid,
            drawBorder: false,
          },
          ticks: {
            color: colors.muted,
            font: {
              size: 11,
            },
            callback: function(value) {
              return value.toFixed(3);
            }
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
    },
  };

  // Create chart instance
  const chart = new Chart(ctx, config);
  chartInstances.set(canvas.id, chart);
}

// Redraw charts when theme changes
function redrawAllCharts() {
  document.querySelectorAll("canvas[data-chart]").forEach((canvas) => {
    try {
      const payload = JSON.parse(canvas.dataset.chart || "{}");
      drawChart(canvas, payload.kind, payload.data || {});
    } catch (_error) {
      // Ignore errors
    }
  });
}

function renderDataTable(rows) {
  if (!rows || rows.length === 0) return empty("暂无表格数据");
  const headers = Object.keys(rows[0]);
  return `
    <div class="data-table-wrap">
      <table class="data-table">
        <thead><tr>${headers.map((header) => `<th>${esc(header)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((row) => `<tr>${headers.map((header) => `<td>${esc(row[header])}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderCsvPreview(preview) {
  if (!preview || !preview.headers || preview.headers.length === 0) return "";
  return `
    <div class="data-table-wrap">
      <table class="data-table compact">
        <thead><tr>${preview.headers.map((header) => `<th>${esc(header)}</th>`).join("")}</tr></thead>
        <tbody>${preview.rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("")}</tbody>
      </table>
    </div>
  `;
}

async function resultAction(resultId, action) {
  try {
    const payload = await api(`/api/results/${resultId}/${action}`, { method: "POST", body: "{}" });
    showNotice(`${action === "report" ? "报告" : "归档"}已生成：${payload.path}`);
    await loadResultDetail(resultId);
  } catch (error) {
    showNotice(error.message, "error");
  }
}

function renderReports() {
  const headers = [
    { label: "结果名称", render: (result) => `<strong>${esc(result.name)}</strong>` },
    { label: "格式", render: (result) => `<span class="pill">${esc(result.format)}</span>` },
    { label: "Result ID", render: (result) => `<code>${esc(compactId(result.id))}</code>` },
    { label: "大小", render: (result) => esc(formatBytes(result.size_bytes || 0)) },
    { label: "操作", render: (result) => `
      <div class="inline-actions">
        <button class="button small report-action" data-result-id="${esc(result.id)}">生成报告</button>
        <button class="button small secondary archive-action" data-result-id="${esc(result.id)}">归档</button>
      </div>
    ` },
  ];
  $("reportList").innerHTML = dataTable(headers, (state.snapshot.results || []).map((result) => ({ item: result })), "暂无结果");
  document.querySelectorAll(".report-action").forEach((button) => button.addEventListener("click", () => resultAction(button.dataset.resultId, "report")));
  document.querySelectorAll(".archive-action").forEach((button) => button.addEventListener("click", () => resultAction(button.dataset.resultId, "archive")));
}

function renderServers() {
  $("serverList").innerHTML = serverTableRows(state.snapshot.servers || []);
}

async function renderAudit() {
  try {
    const payload = await api("/api/audit?limit=80");
    $("auditList").innerHTML = auditTableRows(payload.entries || []);
  } catch (error) {
    $("auditList").innerHTML = empty(error.message);
  }
}

function empty(message) {
  return `<div class="detail-empty">${esc(message)}</div>`;
}

function openTaskDialog(caseId) {
  const dialog = $("taskDialog");
  const form = $("taskForm");
  form.case_id.value = caseId;

  // Reset form to default state
  form.reset();
  form.case_id.value = caseId;

  // Show powerflow config by default
  showSimConfigForm("powerflow");

  // Load available channels for channel selector
  loadAvailableChannels(caseId);

  dialog.showModal();
}

function showSimConfigForm(type) {
  // Hide all config forms
  $("powerflowConfig").classList.add("hidden");
  $("emtConfig").classList.add("hidden");
  $("stabilityConfig").classList.add("hidden");

  // Show selected config form
  const configId = type + "Config";
  const configEl = $(configId);
  if (configEl) {
    configEl.classList.remove("hidden");
  }
}

// Channel selector state
let selectedChannels = new Set();
let availableChannelsList = [];

async function loadAvailableChannels(caseId) {
  try {
    const response = await api(`/api/cases/${caseId}/channels`);
    availableChannelsList = response.channels || [];
    renderChannelLists();
  } catch (error) {
    // Fallback: show empty channel list
    availableChannelsList = [];
    renderChannelLists();
  }
}

function renderChannelLists() {
  const availableList = $("availableChannelList");
  const selectedList = $("selectedChannelList");
  const searchQuery = ($("availableChannelSearch")?.value || "").toLowerCase();

  // Filter available channels
  const filteredAvailable = availableChannelsList.filter(
    (ch) => !selectedChannels.has(ch.id) && (!searchQuery || ch.name.toLowerCase().includes(searchQuery) || ch.id.toLowerCase().includes(searchQuery))
  );

  // Render available channels
  if (filteredAvailable.length === 0) {
    availableList.innerHTML = '<div class="channel-empty">无可用通道</div>';
  } else {
    availableList.innerHTML = filteredAvailable
      .map(
        (ch) => `
      <div class="channel-item" data-channel-id="${esc(ch.id)}" onclick="toggleChannelSelection('${esc(ch.id)}', 'available')">
        <input type="checkbox" ${ch.selected ? 'checked' : ''} onclick="event.stopPropagation()" onchange="toggleChannelSelection('${esc(ch.id)}', 'available')">
        <span>${esc(ch.name || ch.id)}</span>
      </div>
    `
      )
      .join("");
  }

  // Render selected channels
  const selectedArray = Array.from(selectedChannels);
  $("selectedChannelCount").textContent = selectedArray.length;

  if (selectedArray.length === 0) {
    selectedList.innerHTML = '<div class="channel-empty">暂无选择</div>';
  } else {
    selectedList.innerHTML = selectedArray
      .map(
        (id) => {
          const ch = availableChannelsList.find((c) => c.id === id) || { id, name: id };
          return `
        <div class="channel-item" data-channel-id="${esc(id)}" onclick="toggleChannelSelection('${esc(id)}', 'selected')">
          <input type="checkbox" checked onclick="event.stopPropagation()" onchange="toggleChannelSelection('${esc(id)}', 'selected')">
          <span>${esc(ch.name || ch.id)}</span>
        </div>
      `;
        }
      )
      .join("");
  }

  // Update hidden input with selected channels
  $("emtChannelsInput").value = selectedArray.join(",");
}

function toggleChannelSelection(channelId, list) {
  if (list === "available") {
    selectedChannels.add(channelId);
  } else {
    selectedChannels.delete(channelId);
  }
  renderChannelLists();
}

function addSelectedChannels() {
  const checkboxes = document.querySelectorAll('#availableChannelList input[type="checkbox"]:checked');
  checkboxes.forEach((cb) => {
    const item = cb.closest(".channel-item");
    if (item) {
      selectedChannels.add(item.dataset.channelId);
    }
  });
  renderChannelLists();
}

function removeSelectedChannels() {
  const checkboxes = document.querySelectorAll('#selectedChannelList input[type="checkbox"]:checked');
  checkboxes.forEach((cb) => {
    const item = cb.closest(".channel-item");
    if (item) {
      selectedChannels.delete(item.dataset.channelId);
    }
  });
  renderChannelLists();
}

function openEditCaseDialog(caseRow) {
  const form = $("editCaseForm");
  let notes = {};
  try {
    notes = JSON.parse(caseRow.description || "{}");
  } catch (_error) {
    notes = {};
  }
  form.case_id.value = caseRow.id;
  form.name.value = caseRow.name || "";
  form.rid.value = caseRow.rid || "";
  form.model_source.value = notes.model_source || "";
  form.tags.value = (caseRow.tags || []).join(",");
  form.description.value = caseDescriptionText(caseRow.description);
  $("editCaseDialog").showModal();
}

function openEditTaskDialog(task) {
  const form = $("editTaskForm");
  form.task_id.value = task.id;
  form.name.value = task.name || "";
  form.type.value = task.type || "powerflow";
  form.model_source.value = (task.config || {}).model_source || "";
  form.channels.value = taskChannels(task);
  form.config_json.value = JSON.stringify(task.config || {}, null, 2);
  $("editTaskDialog").showModal();
}

function setupEvents() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });
  document.querySelectorAll(".case-subtab").forEach((button) => {
    button.addEventListener("click", () => switchCaseTab(button.dataset.caseTab));
  });
  document.querySelectorAll(".result-subtab").forEach((button) => {
    button.addEventListener("click", () => switchResultTab(button.dataset.resultTab));
  });
  $("refreshBtn").addEventListener("click", refresh);
  $("healthBtn").addEventListener("click", async () => {
    const health = await api("/api/health");
    showNotice(`工作区正常：${health.summary.storage.total_mb} MB，index ${health.index_path}`);
    await refresh();
  });
  $("newCaseBtn").addEventListener("click", () => $("caseDialog").showModal());
  $("caseForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const rid = String(form.get("rid") || "");
    if (!rid.startsWith("model/") || rid.split("/").length < 3) {
      showNotice("CloudPSS RID 应类似 model/chenying/IEEE39", "error");
      return;
    }
    try {
      await api("/api/cases", {
        method: "POST",
        body: JSON.stringify(Object.fromEntries(form.entries())),
      });
      $("caseDialog").close();
      event.target.reset();
      await refresh();
      showNotice("Case 已创建");
    } catch (error) {
      showNotice(error.message, "error");
    }
  });
  $("editCaseForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const payload = Object.fromEntries(form.entries());
    const caseId = payload.case_id;
    delete payload.case_id;
    if (!String(payload.rid || "").startsWith("model/") || String(payload.rid || "").split("/").length < 3) {
      showNotice("CloudPSS RID 应类似 model/chenying/IEEE39", "error");
      return;
    }
    try {
      await api(`/api/cases/${caseId}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      $("editCaseDialog").close();
      await refresh();
      state.selectedCaseId = caseId;
      await loadCaseDetail(caseId);
      showNotice("Case 已更新");
    } catch (error) {
      showNotice(error.message, "error");
    }
  });
  $("taskForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const payload = Object.fromEntries(form.entries());
    try {
      await api("/api/tasks", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      $("taskDialog").close();
      event.target.reset();
      await refresh();
      if (state.selectedCaseId) await loadCaseDetail(state.selectedCaseId);
      showNotice("Task 已创建");
    } catch (error) {
      showNotice(error.message, "error");
    }
  });
  $("editTaskForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const payload = Object.fromEntries(form.entries());
    const taskId = payload.task_id;
    delete payload.task_id;
    try {
      payload.config = payload.config_json ? JSON.parse(payload.config_json) : {};
      delete payload.config_json;
      await api(`/api/tasks/${taskId}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      $("editTaskDialog").close();
      await refresh();
      if (state.selectedCaseId) await loadCaseDetail(state.selectedCaseId);
      showNotice("Task 配置已保存");
    } catch (error) {
      showNotice(error.message, "error");
    }
  });

  // 快速操作按钮
  $("quickNewCaseBtn")?.addEventListener("click", () => {
    $("caseDialog").showModal();
  });

  $("quickNewTaskBtn")?.addEventListener("click", () => {
    if (state.selectedCaseId) {
      openTaskDialog(state.selectedCaseId);
    } else if (state.snapshot?.cases?.length > 0) {
      openTaskDialog(state.snapshot.cases[0].id);
    } else {
      showNotice("请先创建一个 Case", "warning");
    }
  });

  $("quickRefreshBtn")?.addEventListener("click", refresh);

  // 指标卡片点击导航
  document.querySelectorAll(".metric-card[data-nav]").forEach((card) => {
    card.addEventListener("click", () => {
      const view = card.dataset.nav;
      if (view && titles[view]) {
        switchView(view);
      }
    });
  });

  // 仿真类型选择器
  document.querySelectorAll('input[name="sim_type"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      showSimConfigForm(radio.value);
    });
  });

  // 通道选择器
  $("addChannelBtn")?.addEventListener("click", addSelectedChannels);
  $("removeChannelBtn")?.addEventListener("click", removeSelectedChannels);
  $("availableChannelSearch")?.addEventListener("input", renderChannelLists);

  // 高级配置切换
  $("toggleAdvancedConfig")?.addEventListener("click", () => {
    const advanced = $("advancedConfig");
    advanced.classList.toggle("hidden");
    $("toggleAdvancedConfig").textContent = advanced.classList.contains("hidden") ? "高级配置" : "隐藏高级配置";
  });

  // Task filter buttons
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentTaskFilter = btn.dataset.filter;
      renderTasks();
    });
  });

  // Task detail dialog actions
  $("closeTaskDetailBtn")?.addEventListener("click", () => {
    $("taskDetailDialog").close();
  });

  $("cancelTaskBtn")?.addEventListener("click", () => {
    const taskId = $("taskDetailDialog").dataset.taskId;
    if (taskId) cancelTask(taskId);
  });

  $("rerunTaskBtn")?.addEventListener("click", () => {
    const taskId = $("taskDetailDialog").dataset.taskId;
    if (taskId) rerunTask(taskId);
  });

  $("cloneTaskBtn")?.addEventListener("click", () => {
    const taskId = $("taskDetailDialog").dataset.taskId;
    if (taskId) cloneTask(taskId);
  });

  $("viewResultBtn")?.addEventListener("click", () => {
    const taskId = $("taskDetailDialog").dataset.taskId;
    if (taskId) viewTaskResult(taskId);
  });

  $("refreshLogsBtn")?.addEventListener("click", async () => {
    const taskId = $("taskDetailDialog").dataset.taskId;
    if (taskId) {
      try {
        const response = await api(`/api/tasks/${taskId}/logs`);
        $("taskLogsContent").textContent = response.logs || "暂无日志";
      } catch (error) {
        $("taskLogsContent").textContent = "无法加载日志: " + error.message;
      }
    }
  });

  // Theme toggle button
  $("themeToggleBtn")?.addEventListener("click", () => {
    const newTheme = state.theme === "light" ? "dark" : "light";
    state.theme = newTheme;
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("cloudpss.portal.theme", newTheme);
    $("themeToggleBtn").textContent = newTheme === "light" ? "🌙" : "☀️";
    $("themeToggleBtn").title = newTheme === "light" ? "切换暗色主题" : "切换亮色主题";
    // Redraw charts with new theme colors
    redrawAllCharts();
  });

  // Set initial theme button state
  if ($("themeToggleBtn")) {
    $("themeToggleBtn").textContent = state.theme === "light" ? "🌙" : "☀️";
    $("themeToggleBtn").title = state.theme === "light" ? "切换暗色主题" : "切换亮色主题";
  }
}

// Keyboard shortcuts
document.addEventListener("keydown", (event) => {
  // Only handle shortcuts when not in an input/textarea
  if (event.target.matches("input, textarea, select, [contenteditable]")) {
    // Allow Escape to close dialogs even when in input
    if (event.key === "Escape") {
      const openDialog = document.querySelector("dialog[open]");
      if (openDialog) {
        event.preventDefault();
        openDialog.close();
        return;
      }
    }
    return;
  }

  const key = event.key.toLowerCase();
  const ctrl = event.ctrlKey || event.metaKey;
  const alt = event.altKey;

  // Ctrl/Cmd + R: Refresh
  if (ctrl && key === "r") {
    event.preventDefault();
    refresh();
    showNotice("已刷新", "info");
    return;
  }

  // Ctrl/Cmd + N: New Case
  if (ctrl && key === "n") {
    event.preventDefault();
    $("caseDialog")?.showModal();
    return;
  }

  // Ctrl/Cmd + T: New Task
  if (ctrl && key === "t") {
    event.preventDefault();
    if (state.selectedCaseId) {
      openTaskDialog(state.selectedCaseId);
    } else if (state.snapshot?.cases?.length > 0) {
      openTaskDialog(state.snapshot.cases[0].id);
    } else {
      showNotice("请先创建一个 Case", "warning");
    }
    return;
  }

  // Alt + 1-7: Switch views
  if (alt && key >= "1" && key <= "7") {
    event.preventDefault();
    const views = ["dashboard", "cases", "tasks", "results", "reports", "servers", "audit"];
    const index = parseInt(key, 10) - 1;
    if (views[index]) {
      switchView(views[index]);
    }
    return;
  }

  // Ctrl/Cmd + D: Toggle theme
  if (ctrl && key === "d") {
    event.preventDefault();
    $("themeToggleBtn")?.click();
    return;
  }

  // Ctrl/Cmd + /: Show help
  if (ctrl && key === "/") {
    event.preventDefault();
    showKeyboardShortcuts();
    return;
  }

  // Escape: Close dialogs
  if (key === "escape") {
    const openDialog = document.querySelector("dialog[open]");
    if (openDialog) {
      event.preventDefault();
      openDialog.close();
    }
    return;
  }

  // Ctrl/Cmd + S: Save (when editing model)
  if (ctrl && key === "s") {
    if (state.modelEdits && Object.keys(state.modelEdits).length > 0) {
      event.preventDefault();
      $("saveModelBtn")?.click();
    }
    return;
  }
});

// Show keyboard shortcuts help
function showKeyboardShortcuts() {
  const shortcuts = [
    { key: "Ctrl + R", desc: "刷新数据" },
    { key: "Ctrl + N", desc: "新建 Case" },
    { key: "Ctrl + T", desc: "新建任务" },
    { key: "Ctrl + D", desc: "切换主题" },
    { key: "Ctrl + S", desc: "保存模型修改" },
    { key: "Alt + 1~7", desc: "切换视图 (总览/算例/任务/结果/报告/服务/审计)" },
    { key: "Esc", desc: "关闭对话框" },
    { key: "Ctrl + /", desc: "显示快捷键帮助" },
  ];

  const content = shortcuts.map(s => `<div class="shortcut-item"><kbd>${esc(s.key)}</kbd> <span>${esc(s.desc)}</span></div>`).join("");

  const dialog = document.createElement("dialog");
  dialog.className = "shortcut-dialog";
  dialog.innerHTML = `
    <div class="dialog-header">
      <h3 class="dialog-title">键盘快捷键</h3>
      <button class="dialog-close" onclick="this.closest('dialog').close()">&times;</button>
    </div>
    <div class="dialog-body">
      ${content}
    </div>
    <div class="dialog-footer">
      <button class="button" onclick="this.closest('dialog').close()">关闭</button>
    </div>
  `;
  document.body.appendChild(dialog);
  dialog.showModal();
  dialog.addEventListener("close", () => dialog.remove());
}

setupEvents();
switchView("dashboard");
refresh().catch((error) => showNotice(error.message, "error"));
