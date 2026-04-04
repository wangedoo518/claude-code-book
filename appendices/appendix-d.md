# 附录D：89 个 Feature Flag 完整清单

> 每个 Feature Flag 的名称、用途、关联模块、类型分类

---

## 模式类 Flag

| Flag 名称 | 用途 | 关联模块 | 类型 |
|-----------|------|----------|------|
| KAIROS | 自主助理模式 | src/assistant/ | 编译时 |
| COORDINATOR_MODE | 多智能体编排 | src/coordinator/ | 编译时 |
| BRIDGE_MODE | IDE 集成模式 | src/bridge/ | 编译时 |
| DAEMON | 后台守护进程 | 守护进程模块 | 编译时 |
| KAIROS_BRIEF | KAIROS 简要模式 | src/assistant/ | 编译时 |
| PROACTIVE | 主动模式 | 主动触发模块 | 编译时 |

## 工具类 Flag

| Flag 名称 | 用途 | 关联模块 | 类型 |
|-----------|------|----------|------|
| WEB_BROWSER_TOOL | 浏览器控制工具 | src/tools/WebBrowserTool/ | 编译时 |
| TERMINAL_PANEL | 终端面板捕获 | 终端模块 | 编译时 |
| CHICAGO_MCP | Computer Use MCP | shims/ant-computer-use-mcp/ | 编译时 |
| AGENT_TRIGGERS | 远程触发器 | src/tools/RemoteTriggerTool/ | 编译时 |

## 交互类 Flag

| Flag 名称 | 用途 | 关联模块 | 类型 |
|-----------|------|----------|------|
| VOICE_MODE | 语音交互 | src/voice/ | 编译时 |
| WORKFLOW_SCRIPTS | 工作流自动化 | 工作流模块 | 编译时 |

## 实验类 Flag

| Flag 名称 | 用途 | 关联模块 | 类型 |
|-----------|------|----------|------|
| ABLATION_BASELINE | 消融实验基线 | 实验模块 | 编译时 |
| TORCH | 实验性推理增强 | 推理模块 | 编译时 |
| ULTRAPLAN | 增强计划模式 | 计划模块 | 编译时 |

## 运行时 Flag（GrowthBook）

| Flag 名称 | 用途 | 类型 |
|-----------|------|------|
| 各种 A/B 测试 flag | 功能实验 | 运行时 |
| 各种 rollout flag | 灰度发布 | 运行时 |

---

*注：编译时 Flag 通过 bun:bundle 在编译阶段消除死代码*
*运行时 Flag 通过 GrowthBook 平台动态控制*
*完整清单基于源码中所有 feature() 调用点的统计*
*部分 Flag 名称可能为内部代号，确切含义基于关联模块推断*
