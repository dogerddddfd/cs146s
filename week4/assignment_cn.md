# 第4周 — 真实环境中的自主编码代理

> ***我们建议在开始前阅读整个文档。***

本周，你的任务是在这个仓库的上下文中构建至少 **2个自动化工具**，使用以下 **Claude Code** 功能的任意组合：

- 自定义斜杠命令（签入 `.claude/commands/*.md`）

- 用于仓库或上下文指导的 `CLAUDE.md` 文件

- Claude 子代理（协同工作的角色专业化代理）

- 集成到 Claude Code 中的 MCP 服务器

你的自动化工具应该有意义地改进开发者工作流程——例如，通过简化测试、文档、重构或数据相关任务。然后，你将使用你创建的自动化工具来扩展 `week4/` 中的 starter 应用程序。

## 了解 Claude Code
为了更深入地了解 Claude Code 并探索你的自动化选项，请阅读以下两个资源：

1. **Claude Code 最佳实践：** [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **子代理概述：** [docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 探索 Starter 应用程序
最小化的全栈 starter 应用程序，设计为 **"开发者的命令中心"**。
- 带有 SQLite（SQLAlchemy）的 FastAPI 后端
- 静态前端（无需 Node 工具链）
- 最小化测试（pytest）
- Pre-commit（black + ruff）
- 练习代理驱动工作流程的任务

使用此应用程序作为你的 playground，以试验你构建的 Claude 自动化工具。

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

3) 运行应用程序（从 `week4/` 目录）

```bash
make run
```

4) 打开 `http://localhost:8000` 查看前端，打开 `http://localhost:8000/docs` 查看 API 文档。

5) 试用 starter 应用程序，了解其当前功能和特性。


### 测试
运行测试（从 `week4/` 目录）
```bash
make test
```

### 格式化/ linting
```bash
make format
make lint
```

## 第一部分：构建你的自动化工具（选择 2 个或更多）
现在你已经熟悉了 starter 应用程序，下一步是构建自动化工具来增强或扩展它。以下是你可以选择的几个自动化选项。你可以跨类别混合搭配。

在构建自动化工具时，请在 `writeup.md` 文件中记录你的更改。暂时保留 "你如何使用自动化工具来增强 starter 应用程序" 部分为空 - 你将在作业的第二部分返回此部分。

### A) Claude 自定义斜杠命令
斜杠命令是用于重复工作流程的功能，允许你在 `.claude/commands/` 内的 Markdown 文件中创建可重用的工作流程。Claude 通过 `/` 暴露这些命令。


- 示例 1：带覆盖率的测试运行器
  - 名称：`tests.md`
  - 意图：运行 `pytest -q backend/tests --maxfail=1 -x`，如果通过，则运行覆盖率测试。
  - 输入：可选标记或路径。
  - 输出：总结失败并建议下一步。
- 示例 2：文档同步
  - 名称：`docs-sync.md`
  - 意图：读取 `/openapi.json`，更新 `docs/API.md`，并列出路由差异。
  - 输出：类似差异的摘要和待办事项。
- 示例 3：重构工具
  - 名称：`refactor-module.md`
  - 意图：重命名模块（例如，`services/extract.py` → `services/parser.py`），更新导入，运行 lint/测试。
  - 输出：修改文件的清单和验证步骤。

>*提示：保持命令专注，使用 `$ARGUMENTS`，并优先考虑幂等步骤。考虑允许列出安全工具并使用无头模式以提高可重复性。*

### B) `CLAUDE.md` 指导文件
`CLAUDE.md` 文件在开始对话时会自动读取，允许你提供特定于仓库的指令、上下文或指导，以影响 Claude 的行为。在仓库根目录（以及可选的 `week4/` 子文件夹）中创建 `CLAUDE.md` 来指导 Claude 的行为。

- 示例 1：代码导航和入口点
  - 包括：如何运行应用程序，路由所在位置（`backend/app/routers`），测试所在位置，数据库如何种子化。
- 示例 2：样式和安全护栏
  - 包括：工具期望（black/ruff），可以运行的安全命令，应避免的命令，以及 lint/测试门控。
- 示例 3：工作流程片段
  - 包括："当被要求添加端点时，首先编写失败的测试，然后实现，然后运行 pre-commit。"

> *提示：像提示词一样迭代 `CLAUDE.md`，保持简洁和可操作，并记录你期望 Claude 使用的自定义工具/脚本。*

### C) 子代理（角色专业化）

子代理是专门的 AI 助手，配置为处理特定任务，具有自己的系统提示、工具和上下文。设计两个或更多协作代理，每个负责单个工作流程中的不同步骤。

- 示例 1：TestAgent + CodeAgent
  - 流程：TestAgent 为更改编写/更新测试 → CodeAgent 实现代码以通过测试 → TestAgent 验证。
- 示例 2：DocsAgent + CodeAgent
  - 流程：CodeAgent 添加新的 API 路由 → DocsAgent 更新 `API.md` 和 `TASKS.md` 并检查与 `/openapi.json` 的差异。
- 示例 3：DBAgent + RefactorAgent
  - 流程：DBAgent 提出 schema 更改（调整 `data/seed.sql`）→ RefactorAgent 更新模型/模式/路由并修复 lints。

>*提示：使用清单/草稿本，在角色之间重置上下文（`/clear`），并为独立任务并行运行代理。*

## 第二部分：使用你的自动化工具
现在你已经构建了 2+ 个自动化工具，让我们使用它们！在 `writeup.md` 中的 "你如何使用自动化工具来增强 starter 应用程序" 部分，描述你如何利用每个自动化工具来改进或扩展应用程序的功能。

例如，如果你实现了自定义斜杠命令 `/generate-test-cases`，请解释你如何使用它来与 starter 应用程序交互和测试。


## 交付物
1) 两个或更多自动化工具，可能包括：
   - `.claude/commands/*.md` 中的斜杠命令
   - `CLAUDE.md` 文件
   - 子代理提示/配置（清晰记录，如有文件/脚本）

2) `week4/` 下的 `writeup.md`，包括：
  - 设计灵感（例如，引用最佳实践和/或子代理文档）
  - 每个自动化工具的设计，包括目标、输入/输出、步骤
  - 如何运行它（确切命令）、预期输出以及回滚/安全注意事项
  - 之前 vs 之后（即手动工作流程 vs 自动化工作流程）
  - 你如何使用自动化工具来增强 starter 应用程序



## 提交说明
1. 确保你已将所有更改推送到远程仓库以进行评分。
2. **确保你已将 brentju 和 febielin 添加为作业仓库的协作者。**
2. 通过 Gradescope 提交。
