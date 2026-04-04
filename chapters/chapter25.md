# 第25章：MCP协议：AI时代的USB接口

> **所属**：第六编 · 连接世界
>
> **关键源码**：src/services/mcp/(25 files), src/tools/MCPTool/

---

## 生活类比

USB让所有设备——键盘、鼠标、U盘、手机——用同一种接口连电脑。MCP让所有外部工具用同一种协议连AI。在USB之前，每个设备有自己的接口（PS/2、串口、并口）；在MCP之前，每个AI工具有自己的集成方式。统一接口降低了接入成本，释放了生态潜力。

## 这一章要回答的问题

**已经有54个内置工具了，为什么还要接"外部能力"？**

54个内置工具覆盖了通用的编程场景，但世界上的工具和服务远不止这些。数据库管理、项目管理、设计工具、CI/CD平台——每个团队有自己的工具链。MCP协议让Claude Code变成一个开放的AI平台，任何服务都能通过标准协议接入。

---

## 25.1 协议核心

### 设计理念
- MCP（Model Context Protocol）是Anthropic推出的开放协议
- 核心理念：AI不需要内置所有能力，只需要一种标准方式接入外部能力
- 类似于浏览器不需要内置所有网站，只需要HTTP协议

### Client-Server架构
- Claude Code是MCP Client——发起请求、调用工具、获取资源
- 外部服务是MCP Server——暴露工具、提供资源、响应请求
- 一个Client可以连接多个Server，一个Server可以服务多个Client

### 三大原语
- Tools：Server暴露的可执行操作——类似内置工具，但由外部实现
- Resources：Server提供的数据资源——文件、数据库记录、API响应
- Prompts：Server定义的提示词模板——预置的对话起点或指令

## 25.2 七种传输统一

### Stdio传输
- 最简单的传输方式——通过标准输入输出与本地进程通信
- 适合本地运行的MCP Server——启动一个进程，通过stdin/stdout交换消息
- 零网络开销，延迟最低，但只能连接本地服务

### SSE与HTTP传输
- SSE（Server-Sent Events）支持服务端推送——适合需要实时通知的场景
- HTTP传输用标准的请求-响应模式——最广泛支持，兼容性最好
- 两者都支持远程连接——MCP Server可以运行在云端

### WebSocket/Docker/npx/Proxy
- WebSocket提供全双工通信——双向实时消息
- Docker传输自动在容器中启动MCP Server——隔离且可复现
- npx传输通过npm包启动Server——一行命令接入新能力
- Proxy传输通过中间代理连接——适合企业网络环境

## 25.3 能力发现与异常

### 工具发现
- Client连接Server后首先调用tools/list获取可用工具列表
- Server返回每个工具的名称、描述、输入Schema
- Claude Code将这些工具转换为内部格式，注入工具池

### 资源获取
- Client通过resources/list发现可用资源
- 资源可以是文件、数据记录、配置项等结构化数据
- AI可以决定是否需要读取某个资源来完成当前任务

### 心跳重连与降级处理
- Client定期发送心跳检测Server是否在线
- Server断开时自动尝试重连——临时网络波动不影响使用
- 重连失败后优雅降级——从工具池中移除该Server的工具，告知AI

---

## 深水区（架构师选读）

MCP的生态博弈——开放协议vs闭源生态，Anthropic的标准化策略与行业采纳现状。Anthropic将MCP作为开放协议发布，任何人都可以实现MCP Server。这是一个生态策略：如果MCP成为行业标准，Claude就自动获得最大的工具生态。但开放协议面临"标准之战"的风险——OpenAI、Google等竞争对手可能推出自己的协议。目前MCP的采纳在快速增长，主要得益于协议设计的简洁性和Claude Code的大量用户基数。长期来看，MCP能否成为"AI工具的USB"取决于它能否像USB一样做到真正的即插即用和广泛兼容。

---

## 本章小结

> **一句话**：MCP协议通过Client-Server架构、三大原语（Tools/Resources/Prompts）、七种传输方式，让Claude Code从封闭的CLI工具变为开放的AI平台——任何服务都能通过标准协议接入。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/services/mcp/client.ts | MCP客户端核心 | A |
| src/services/mcp/transport/ | 七种传输实现 | A |
| src/tools/MCPTool/MCPTool.ts | MCP工具代理 | A |
| src/services/mcp/discovery.ts | 能力发现与管理 | B |

### 逆向提醒

- ✅ RELIABLE: MCP协议的核心消息格式和Client实现
- ⚠️ CAUTION: MCP协议仍在演进中，部分原语可能新增或调整
- ❌ SHIM/STUB: 某些传输方式（如Proxy）在开源版中可能未完整实现
