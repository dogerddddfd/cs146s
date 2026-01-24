# 第5周 — 使用 Warp 的代理式开发

使用 `week5/` 中的应用程序作为你的 playground。本周的任务与之前的作业类似，但强调 Warp 代理式开发环境和多代理工作流程。

## 了解 Warp
- Warp 代理式开发环境：[warp.dev](https://www.warp.dev/)
- [Warp 大学](https://www.warp.dev/university?slug=university)


## 探索 Starter 应用程序
最小化的全栈 starter 应用程序。
- 带有 SQLite（SQLAlchemy）的 FastAPI 后端
- 静态前端（无需 Node 工具链）
- 最小化测试（pytest）
- Pre-commit（black + ruff）
- 练习代理驱动工作流程的任务

使用此应用程序作为你的 playground，以试验你构建的 Warp 自动化工具。

### 结构

```
backend/                # FastAPI 应用
frontend/               # 由 FastAPI 提供服务的静态 UI
data/                   # SQLite 数据库 + 种子数据
docs/                   # 代理驱动工作流程的任务
```

### 快速开始

1) 激活你的 conda 环境。

```bash
conda activate cs146s
```

2)（可选）安装 pre-commit 钩子

```bash
pre-commit install
```

3) 运行应用程序（从 `week5/` 目录）

```bash
make run
```

4) 打开 `http://localhost:8000` 查看前端，打开 `http://localhost:8000/docs` 查看 API 文档。

5) 试用 starter 应用程序，了解其当前功能和特性。


### 测试
运行测试（从 `week5/` 目录）
```bash
make test
```

### 格式化/Linting
```bash
make format
make lint
```

## 第一部分：构建你的自动化工具（选择 2 个或更多）
从 `week5/docs/TASKS.md` 中选择任务来实现。你的实现必须以以下两种方式利用 Warp（详见下文）：

- A) 使用 Warp Drive 功能 — 如保存的提示词、规则或 MCP 服务器。
- B) 在 Warp 中纳入多代理工作流程。

将你的更改集中在 `week5/` 内的后端、前端、逻辑或测试上。
对于每个选定的任务，注意其难度级别。


### A) Warp Drive 保存的提示词、规则、MCP 服务器（必需：至少一个）
创建一个或多个可共享的 Warp Drive 提示词、规则或 MCP 服务器集成，专门针对此仓库。示例：
- 带覆盖率和不稳定测试重运行的测试运行器
- 文档同步：从 `/openapi.json` 生成/更新 `docs/API.md`，列出路由差异
- 重构工具：重命名模块，更新导入，运行 lint/测试
- 发布助手：更新版本，运行检查，准备更改日志片段
- 集成 Git MCP 服务器，让 Warp 自主与 Git 交互（创建分支、提交、PR 说明等）

>*提示：保持工作流程集中，传递参数，使其幂等，并在可能的情况下优先选择无头/非交互式步骤。*

### B) Warp 中的多代理工作流程（必需：至少一个）
运行多代理会话，其中不同 Warp 选项卡中的单独代理同时处理独立任务。
- 在不同的 Warp 选项卡中使用并发代理执行 `TASKS.md` 中的多个自包含任务。挑战：你能同时有多少个代理在工作？

>*提示：[git worktree](https://git-scm.com/docs/git-worktree) 可能有助于防止代理相互干扰。*


## 第二部分：使用你的自动化工具
现在你已经构建了 2+ 个自动化工具，让我们使用它们！在 `writeup.md` 的 "你如何使用自动化工具（它解决或加速了什么痛点）" 部分，描述你如何利用每个自动化工具来改进某些工作流程。

## 约束和范围
严格在 `week5/`（后端、前端、逻辑、测试）中工作。除非自动化工具明确需要，否则避免更改其他周的内容，并记录原因。


## 交付物
1) 两个或更多 Warp 自动化工具，可能包括：
   - Warp Drive 工作流程/规则（共享链接和/或导出的定义）和任何辅助脚本
   - 用于协调多个代理的任何补充提示词/剧本

2) `week5/` 下的 `writeup.md`，包括：
   - 每个自动化工具的设计，包括目标、输入/输出、步骤
   - 之前 vs 之后（即手动工作流程 vs 自动化工作流程）
   - 每个已完成任务使用的自主级别（什么代码权限，为什么，以及你如何监督）
   - （如适用）多代理说明：角色、协调策略以及并发的优势/风险/失败
   - 你如何使用自动化工具（它解决或加速了什么痛点）



## 提交说明
1. 确保你已将所有更改推送到远程仓库以进行评分。
2. **确保你已将 brentju 和 febielin 添加为作业仓库的协作者。**
2. 通过 Gradescope 提交。
