---
name: crpcg-sdd-initialize
description: 初始化 CRPCG 项目标准结构。当用户需要为项目设置 AI 辅助开发环境时使用此 skill，从公司仓库拉取规则文件、mcp 配置、参考文档等，创建标准目录结构。触发词："Harness目录初始化"、"目录初始化"、"初始化"。
---

# CRPCG 项目初始化

从公司仓库 `http://gitea.crpcg.com/common-components/ai-coding-sdd.git` 拉取标准配置并创建项目结构。

## 工作流

```
   ┌───────────┐      ┌───────────┐      ┌───────────┐      ┌───────────┐
   │ 1.检查项目 │ ───> │ 2.克隆仓库 │ ───> │3.创建目录 │ ───> │4.选择类型 │
   │   环境    │      │           │      │   结构   │      │ 并复制配置│
   └─────┬─────┘      └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
         │                  │                  │                  │
         ▼                  ▼                  │                  ▼
    已有配置           克隆失败              │             ┌──────────┐
    提示用户           提示用户              │             │ 选择项目 │
                      手动下载              │             │   类型   │
                                            │             └────┬─────┘
                                            │                  │
                                            │                  ▼
                                            │         确定规则和引用文件
                                            │                  │
                                            │                  ▼
                                            │             检查文件冲突
                                            │                  │
                                            │                  ▼
                                            │             处理冲突策略
                                            │                  │
                                            └──────────────────┘
                                                               │
                                                               ▼
                                                        ┌───────────┐
                                                        │5.清理临时 │
                                                        │   文件    │
                                                        └─────┬─────┘
                                                              │
                                                              ▼
                                                       删除临时克隆目录
```

### 步骤1：检查项目环境

在执行初始化前，必须先检查项目当前状态。

1. **确认当前工作目录** — 通过命令获取当前目录，确认是否为项目根目录：

   **⚠️ Windows 路径格式处理：**

   在将路径传递给 `ask_user_question` 工具前，必须对 Windows 路径进行格式转换，避免反斜杠导致 JSON 解析异常：

   - **问题**：路径 `D:\code\test\new` 中的 `\t` 会被 JSON 解析为制表符，`\n` 会被解析为换行符
   - **解决**：将反斜杠替换为正斜杠，如 `D:/code/test/new`

   **PowerShell 转换命令：**
   ```powershell
   # 获取路径并转换为正斜杠格式
   (Get-Location).Path.Replace('\', '/')
   ```

   **执行后：** 将格式化后的路径与用户预期的项目根目录进行比对，若不一致则使用 `ask_user_question` 确认是否继续。

2. **确认项目根目录** — 检查是否存在 `.git` 目录或确认用户指定的项目根目录

3. **检查已有配置** — 扫描以下目录和文件是否已存在（⚠️ 注意：`glob_path` 工具对以 `.` 开头的目录检测有问题，必须使用 `run_command` 执行 `Test-Path` 或 `Get-ChildItem -Force` 检测）：
   - `.comate/` 目录
   - `.comate/mcp.json` 文件
   - `docs/` 目录
   - `AGENTS.md` 文件
   - `sdd.md` 文件

### 步骤2：克隆仓库

从公司仓库克隆标准配置到临时目录。

1. **创建临时目录** — 在系统临时目录下创建 `ai-coding-sdd-{timestamp}` 目录
2. **执行克隆** — 运行 `git clone http://gitea.crpcg.com/common-components/ai-coding-sdd.git <临时目录>`
3. **处理克隆失败** — 若克隆失败，提示用户：
   - 检查网络连接
   - 确认是否有访问权限
   - 提供手动下载地址：`http://gitea.crpcg.com/common-components/ai-coding-sdd`

### 步骤3：创建目录结构

创建标准的项目目录结构。

```
.comate/
├── rules/          # 规则文件，供 Comate 自动加载（用户根据需要保留）
├── references/     # 部门引用参考文档
├── skills/         # Skill 文件，供 Comate 自动加载
├── agents/         # Sub-agents 目录，供 Comate 自动加载
├── scripts/        # 脚本文件，供规则、技能、sub-agent 等调用
├── templates/      # 模板文件
└── mcp/            # MCP资源及配置文件

docs/               # 项目知识库目录（长期资产）
├── references/     # 存放供引用的参考文档
    └── tech-assets/# 技术资产目录

└── requirements/   # 原始需求文档存放处
    └── 编号-标题/   # 例如：1221287-supply-order-void

```

**创建规则：**
- 不覆盖已有目录
- 仅创建不存在的目录
- 目录创建后记录创建清单

### 步骤4：选择项目类型并复制配置文件

从克隆的仓库复制标准配置到项目目录。

**4.1 选择项目类型（强制执行）**

⚠️ **重要**：不管当前目录内容如何，**每次执行此 skill 时必须由用户选择项目类型**。即使检测到项目已有配置文件，也不能跳过此步骤，必须使用 `ask_user_question` 工具让用户确认。

使用 `ask_user_question` 工具询问用户项目类型：

| 项目类型 | 说明 |
|---------|------|
| 后端项目 | Java/Spring Boot 等后端服务 |
| Vue项目 | Vue + TypeScript 前端项目 |
| React项目 | React + TypeScript 前端项目 |
| ReactNative项目 | React Native 移动端项目 |
| Uniapp项目 | Uniapp 跨端项目 |

根据用户选择，确定要复制的规则文件、引用文件和技术模板：

| 项目类型 | 规则文件 | 引用文件 | technical.md 模板 |
|---------|---------|---------|-------------------|
| 后端项目 | git-workflow.mdr, lang-java.mdr, lang-sql.mdr, quality.mdr, security.mdr | crpcg-application-log-spec.md, crpcg-idempotent-spec.md, crpcg-integration-log-spec.md | templates/technical.md |
| Vue项目 | lang-vue-typescript.mdr, git-workflow.mdr, quality.mdr, security.mdr | crpcg-rc-vue-spec.md | templates/technical-frontend.md |
| React项目 | lang-react-typescript.mdr, git-workflow.mdr, quality.mdr, security.mdr | 无 | templates/technical-frontend.md |
| ReactNative项目 | lang-react-typescript.mdr, git-workflow.mdr, quality.mdr, security.mdr | crpcg-rc-rn-spec.md | templates/technical-frontend.md |
| Uniapp项目 | lang-vue-typescript.mdr, git-workflow.mdr, quality.mdr, security.mdr | 无 | templates/technical-frontend.md |

**4.2 确认冲突处理策略**

根据步骤1的检查结果，对已存在的配置项确认处理策略。使用 `ask_user_question` 工具让用户选择：

| 配置项 | 可选策略 |
|-------|---------|
| `.comate/` 目录下的文件 | 跳过 / 覆盖 |
| `mcp.json` 文件 | 跳过 / 覆盖 / 合并 |
| `docs/` 目录下的文件 | 跳过 / 覆盖 |
| `AGENTS.md` 文件 | 跳过 / 覆盖 |
| `sdd.md` 文件 | 跳过 / 覆盖 |

**⚠️ 重要：策略是文件级别的，不是目录级别**

**策略说明：**
- **跳过**：目标位置已存在同名文件则跳过该文件，不存在则复制
- **覆盖**：目标位置已存在同名文件则替换，不存在则直接复制
- **合并**：仅适用于 `mcp.json`，合并 `mcpServers` 配置（见下方 mcp.json 合并逻辑）

**文件级别处理示例：**

假设项目 `.comate/rules/` 目录已有：`custom-rule.mdr`、`quality.mdr`

仓库 `.comate/rules/` 目录有：`quality.mdr`、`lang-java.mdr`

| 策略 | 处理结果 |
|------|---------|
| 跳过 | `custom-rule.mdr` 保留，`quality.mdr` 保留（同名跳过），`lang-java.mdr` 复制（不存在则复制） |
| 覆盖 | `custom-rule.mdr` 保留，`quality.mdr` 替换（同名覆盖），`lang-java.mdr` 复制（不存在则复制） |

**⚠️ 特别说明：**
- 用户自定义的文件永远不会被删除（仓库中不存在的文件保留，如 `custom-rule.mdr`）
- 策略只影响仓库中要复制的文件与项目中已存在文件的冲突处理
- 只有同名文件才会触发策略判断

**4.3 前置检查：配置 .gitignore**

在复制配置文件前，检查并配置 `.gitignore`：
1. **确认 .git 存在** — 步骤1已检查项目根目录是否存在 `.git` 目录
2. **检查 .gitignore** — 若 `.git` 存在，检查项目根目录是否存在 `.gitignore` 文件
3. **追加忽略规则** — 若 `.gitignore` 不存在，创建该文件；若已存在，检查是否包含 `.comate/` 忽略规则，若未包含则追加以下内容：
   ```gitignore
   ### comate ###
   .comate/
   ```

**4.4 复制文件清单：**

| 仓库路径 | 项目路径 | 说明 |
|---------|---------|------|
| `rules/*.mdr` | `.comate/rules/` | 规则文件，根据项目类型选择性复制（见步骤4.1配置表） |
| `references/` | `.comate/references/` | 部门引用参考文档，根据项目类型选择性复制（见步骤4.1配置表） |
| `skills/` | `.comate/skills/` | Skill 文件，供 Comate 自动加载 |
| `agents/` | `.comate/agents/` | Sub-agents 目录，供 Comate 自动加载 |
| `scripts/`| `.comate/scripts/`| 存放脚本文件 |
| `templates/`| `.comate/templates/`| 存放模板文件 |
| `mcp/`（不含 mcp.json） | `.comate/mcp/` | MCP 资源文件（如 d2c-mcp 等），不含 mcp.json |
| `mcp/mcp.json` | `.comate/mcp.json` | MCP 配置文件，需特殊处理（见下方 mcp.json 处理逻辑） |
| `templates/business.md` | `docs/business.md` | 业务知识模板，记录当前工程的业务知识 |
| `templates/technical.md` 或 `templates/technical-frontend.md` | `docs/technical.md` | 技术知识模板，根据项目类型自动选择（见步骤4.1配置表） |
| `AGENTS.md` | `AGENTS.md` | Agent 配置规范，AI 进入仓库的地图 |
| `sdd.md` | `sdd.md` | sdd.md |

**规则文件与引用文件复制：**

仅复制步骤4.1中根据项目类型确定的规则文件和引用文件。

**technical.md 模板选择：**

根据用户在步骤4.1中选择的项目类型，自动选择对应的模板：
- 后端项目：使用 `templates/technical.md`
- Vue项目 / React项目 / ReactNative项目 / Uniapp项目：使用 `templates/technical-frontend.md`

**mcp.json 合并逻辑：**

当用户选择 `mcp.json` 策略为"合并"时，执行以下逻辑：

1. **检查目标文件** — 确认 `.comate/mcp.json` 已存在（步骤1已检测）
2. **读取配置** — 读取仓库中的 `mcp/mcp.json` 和目标 `.comate/mcp.json`
3. **合并 mcpServers** — 执行配置合并：
   - 以目标文件为基础
   - 将仓库配置中的 `mcpServers` 项合并到目标文件
   - 相同 key 的配置项，保留目标文件中的原有配置（不覆盖）
   - 新增的 key，追加到目标文件中
4. **校验格式** — 合并后必须校验 JSON 格式是否正确：
   - 使用 `python -c "import json; json.load(open('.comate/mcp.json'))"` 校验
   - 若格式错误，回滚合并操作并提示用户手动处理
5. **记录合并结果** — 在输出结果中明确列出：
   - 新增的 MCP Server 配置项名称
   - 保留的已有配置项名称
   - 最终 mcp.json 的完整内容概览（服务器数量等）

**复制规则：**
- 根据用户在"确认各部分处理策略"中选择的策略执行对应操作
- 根据用户选择的项目类型，仅复制对应的规则文件和引用文件
- 当生成新的 docs/technical.md 文件时，由用户选择从 templates/technical.md 或由 templates/technical-frontend.md 生成
- 仓库中不存在但目录结构需要的目录，创建空目录
- 复制后记录复制清单

### 步骤5：清理临时文件

删除临时克隆目录，释放磁盘空间。

1. **删除临时目录** — 删除步骤2中创建的临时目录及其所有内容
2. **记录清理状态** — 告知用户临时文件已清理
3. **输出初始化结果** — 列出已创建的目录和已复制的文件
4. **强调 mcp.json 合并结果** — 若执行了 mcp.json 合并，单独输出：
   ```
   📋 MCP 配置合并结果：
   - 新增服务：[列出新增的 mcpServers key]
   - 保留服务：[列出已有的 mcpServers key]
   - 配置文件：.comate/mcp.json
   - 服务总数：X 个
   ```

## Restrictions

⛔ **严禁自主代替用户做决定**  在Skill 执行过程中，凡需要向用户询问确认的事项，均不得代替用户做出决定，必须明确获得用户反馈后方可继续执行

⛔ **强制要求** 冲突处理策略是文件级别的，不是目录级别。用户自定义的文件（仓库中不存在的文件）永远不会被删除。

**绝不：**
- 绝不删除整个目录（即使选择"覆盖"策略）
- 绝不删除用户自定义的文件（仓库中不存在的文件）
- 绝不在未确认的情况下覆盖已有文件
- 绝不跳过环境检查直接执行初始化
- 绝不保留临时克隆目录不清理
- 绝不复制与项目类型无关的规则和引用文件

**始终：**
- 先检查项目环境再执行初始化
- 让用户选择项目类型，根据类型选择规则和引用文件
- 以文件为单位处理冲突（同名文件按策略处理，不同名文件直接复制）
- 克隆仓库到临时目录，完成后清理
- 输出完整的创建目录和已复制文件
