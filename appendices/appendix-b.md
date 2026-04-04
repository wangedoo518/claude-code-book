# 附录B：54 个工具速查手册

> 每个工具的名称、用途、输入参数、权限要求、并发安全性速查

---

## 文件操作类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| FileReadTool | 读取文件内容 | Yes | Yes | Allow |
| FileWriteTool | 创建/重写文件 | No | No | Ask |
| FileEditTool | 精确编辑文件 | No | No | Ask |
| NotebookEditTool | 编辑 Jupyter Notebook | No | No | Ask |

## 执行类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| BashTool | 执行 Shell 命令 | No | 视命令 | Ask |
| PowerShellTool | 执行 PowerShell | No | 视命令 | Ask |
| REPLTool | Node.js REPL | No | No | Ask |

## 搜索类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| GrepTool | 内容搜索(ripgrep) | Yes | Yes | Allow |
| GlobTool | 文件模式匹配 | Yes | Yes | Allow |
| ToolSearchTool | 搜索可用工具 | Yes | Yes | Allow |

## Web 类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| WebSearchTool | 互联网搜索 | Yes | Yes | Allow |
| WebFetchTool | 获取网页内容 | Yes | Yes | Allow |
| WebBrowserTool | 浏览器控制(MCP) | No | No | Ask |

## AI/智能体类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| AgentTool | 派生子智能体 | No | Yes | Allow |
| SkillTool | 调用技能 | No | No | Ask |
| RemoteTriggerTool | 远程触发器 | No | No | Ask |

## 任务管理类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| TaskCreateTool | 创建后台任务 | No | Yes | Allow |
| TaskUpdateTool | 更新任务状态 | No | No | Allow |
| TaskListTool | 列出任务 | Yes | Yes | Allow |
| TaskGetTool | 获取任务详情 | Yes | Yes | Allow |
| TaskOutputTool | 获取任务输出 | Yes | Yes | Allow |
| TaskStopTool | 终止任务 | No | No | Allow |
| TodoWriteTool | 写入 Todo 列表 | No | No | Allow |

## 团队协作类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| TeamCreateTool | 创建智能体团队 | No | No | Allow |
| TeamDeleteTool | 删除团队 | No | No | Allow |
| SendMessageTool | 智能体间消息 | No | Yes | Allow |

## 计划模式类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| EnterPlanModeTool | 进入计划模式 | No | No | Allow |
| ExitPlanModeTool | 退出计划模式 | No | No | Allow |
| VerifyPlanExecutionTool | 验证计划执行 | Yes | Yes | Allow |

## 工作树类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| EnterWorktreeTool | 进入 Git Worktree | No | No | Ask |
| ExitWorktreeTool | 退出 Worktree | No | No | Allow |

## MCP 类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| MCPTool | MCP 工具代理 | 视工具 | 视工具 | Ask |
| ReadMcpResourceTool | 读取 MCP 资源 | Yes | Yes | Allow |
| ListMcpResourcesTool | 列出 MCP 资源 | Yes | Yes | Allow |
| McpAuthTool | MCP 认证 | No | No | Ask |

## 交互类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| AskUserQuestionTool | 向用户提问 | Yes | No | Allow |
| ReviewArtifactTool | 审查产物 | Yes | Yes | Allow |

## 配置/系统类

| 工具名 | 用途 | 只读 | 并发安全 | 权限级别 |
|--------|------|------|----------|----------|
| ConfigTool | 配置管理 | No | No | Allow |
| SleepTool | 延时等待 | Yes | Yes | Allow |
| MonitorTool | 系统监控 | Yes | Yes | Allow |
| BriefTool | 摘要生成 | Yes | Yes | Allow |
| ScheduleCronTool | 定时调度 | No | No | Allow |
| SyntheticOutputTool | 合成输出 | Yes | Yes | Allow |
| LSPTool | 语言服务器协议 | Yes | Yes | Allow |

---

*注：权限级别 Allow=自动允许，Ask=需用户确认，Deny=默认拒绝*
*并发安全性基于源码中 isConcurrencySafe 方法的返回值*
