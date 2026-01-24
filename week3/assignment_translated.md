# 第 3 周 — 构建自定义 MCP 服务器

设计并实现一个模型上下文协议 (MCP) 服务器，该服务器包装一个真实的外部 API。你可以：
- **本地**运行（STDIO 传输）并与 MCP 客户端（如 Claude Desktop）集成。
- 或者**远程**运行（HTTP 传输）并从模型代理或客户端调用它。这更难但可获得额外学分。

如果添加与 MCP 授权规范一致的身份验证（API 密钥或 OAuth2），可获得加分。

## 学习目标
- 理解核心 MCP 功能：工具、资源、提示。
- 实现带有类型化参数和健壮错误处理的工具定义。
- 遵循日志记录和传输最佳实践（STDIO 服务器不使用 stdout）。
- 可选地为 HTTP 传输实现授权流程。

## 要求
1. 选择一个外部 API 并记录你将使用哪些端点。示例：天气、GitHub issues、Notion 页面、电影/电视数据库、日历、任务管理器、金融/加密货币、旅行、体育统计。
2. 公开至少两个 MCP 工具
3. 实现基本的弹性：
   - 对 HTTP 失败、超时和空结果进行优雅错误处理。
   - 遵守 API 速率限制（例如，简单退避或面向用户的警告）。
4. 打包和文档：
   - 提供清晰的设置说明、环境变量和运行命令。
   - 包含示例调用流程（在客户端中输入/点击什么来触发工具）。
5. 选择一种部署模式：
   - 本地：STDIO 服务器，可从你的机器运行，并可被 Claude Desktop 或 Cursor 等 AI IDE 发现。
   - 远程：可通过网络访问的 HTTP 服务器，可被 MCP 感知客户端或代理运行时调用。如果部署并可访问，可获得额外学分。
6. （可选）奖励：身份验证
   - 通过环境变量和客户端配置提供 API 密钥支持；或
   - 用于 HTTP 传输的 OAuth2 风格 bearer 令牌，验证令牌受众，且绝不将令牌传递给上游 API。

## 交付物
- `week3/` 目录下的源代码（建议：`week3/server/`，带有清晰的入口点，如 `main.py` 或 `app.py`）。
- `week3/README.md`，包含：
  - 前提条件、环境设置和运行说明（本地和/或远程）。
  - 如何配置 MCP 客户端（本地使用的 Claude Desktop 示例）或远程代理运行时。
  - 工具参考：名称、参数、示例输入/输出和预期行为。

## 评分标准（共 90 分）
- 功能（35）：实现 2+ 工具，正确的 API 集成，有意义的输出。
- 可靠性（20）：输入验证、错误处理、日志记录、速率限制感知。
- 开发者体验（20）：清晰的设置/文档，易于本地运行；合理的文件夹结构。
- 代码质量（15）：可读的代码，描述性名称，最小复杂性，适用的类型提示。
- 额外学分（10）：
  - +5 远程 HTTP MCP 服务器，可被代理/客户端（如 OpenAI/Claude SDK）调用。
  - +5 正确实现身份验证（API 密钥或带有受众验证的 OAuth2）。

## 有用的参考资料
- MCP 服务器快速入门：[modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)。
*注意：你不能提交这个确切的示例。*
- MCP 授权（HTTP）：[modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- Cloudflare 上的远程 MCP（代理）：[developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)。在部署前，使用 modelcontextprotocol 检查工具在本地调试你的服务器。
- https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel 如果你选择进行远程 MCP 部署，Vercel 是一个很好的选择，它提供免费套餐。
