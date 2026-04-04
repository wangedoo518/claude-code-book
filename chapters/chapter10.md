# 第10章：会话引擎：不只是聊天那么简单

> **所属**：第三编 · AI是怎么"思考"的
>
> **关键源码**：src/QueryEngine.ts (1295 lines, 46KB)

---

## 生活类比

下棋时，你不只是走一步棋——你需要一个"棋盘引擎"来记录局面、判断合法走法、追踪历史。QueryEngine就是Claude Code的"棋盘引擎"。

## 这一章要回答的问题

**直接调API不行吗？为什么还要抽出一个"引擎"？**

直接调用Claude API当然可以得到回复，但生产级的AI助手需要处理远比"一问一答"更复杂的场景：多轮对话的消息管理、工具调用的注册与分发、中断与恢复、SDK与REPL的统一接口。QueryEngine把这些复杂性封装在一个地方，让上层代码只需要关心"发问题、收答案"。

---

## 10.1 会话对象模型

### QueryContext
- 每次会话的完整上下文：消息历史、注册的工具、system prompt、配置参数
- QueryContext是只读的——创建后不修改，新的轮次创建新的Context

### 消息历史
- 按时间序列存储所有消息：用户输入、AI回复、工具调用结果
- 每条消息有角色（user/assistant/tool）、内容、时间戳
- 历史消息随对话增长，token预算管理决定何时截断

### 状态机：idle → running → paused → completed
- **idle**：等待用户输入，引擎空闲
- **running**：正在处理请求，Agent Loop执行中
- **paused**：等待用户确认（如工具执行权限），暂停Agent Loop
- **completed**：当前请求处理完毕，可以接受新输入

## 10.2 Turn生命周期

### Turn的定义
- 一个Turn = 用户的一次输入触发的完整处理过程
- 一个Turn可能包含多次API调用（因为工具调用触发循环）

### 单次输入触发多轮次示例
- 用户说"修复这个Bug"
- AI分析代码（第1次API调用）→ 决定读文件（工具调用）→ 继续分析（第2次API调用）→ 决定修改文件（工具调用）→ 报告结果（第3次API调用）
- 一个用户Turn，但包含了3次API调用和2次工具执行

### 轮次间状态传递
- 工具执行的结果作为新消息追加到历史中
- 下一次API调用能看到之前的所有工具结果
- 状态在Turn内部流转，Turn结束后持久化到会话历史

## 10.3 Headless与REPL共核

### SDK模式复用同一引擎
- SDK模式（headless）和REPL模式使用同一个QueryEngine
- 区别只在上层：REPL有UI层，SDK没有——但引擎逻辑完全共享

### API客户端封装
- QueryEngine不直接调用HTTP——通过ApiClient抽象层通信
- ApiClient处理认证、重试、限流、错误恢复等网络层面的复杂性

### 工具注册统一
- 无论哪种模式，工具的注册和执行路径都相同
- 54个工具通过统一接口注册到引擎中，引擎在Agent Loop中按需调用

---

## 深水区（架构师选读）

QueryEngine的四种状态转换不是随意的——它们构成了一个有限状态机，每个转换都有明确的前置条件和触发事件。idle→running的唯一触发是用户输入到达；running→paused的触发是遇到需要确认的操作；paused→running的触发是用户确认；running→completed的触发是Agent Loop正常退出。异常路径更加复杂：API超时、token耗尽、用户强制中断——每种异常都需要将状态安全地转换回idle，同时保存已有的会话历史不丢失。

---

## 本章小结

> **一句话**：QueryEngine是Claude Code的会话引擎，封装了消息管理、状态机控制、工具注册和API通信，让REPL和SDK模式共享同一套核心逻辑。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/QueryEngine.ts | 会话引擎（1295行） | A |
| src/types/query.ts | 查询相关类型定义 | A |
| src/services/api/client.ts | API客户端封装 | A |
| src/state/AppStateStore.tsx | 会话状态持久化 | A |

### 逆向提醒

- ✅ RELIABLE: QueryEngine的核心API和状态机设计
- ⚠️ CAUTION: 状态转换的异常处理路径可能有未覆盖的边界情况
- ❌ SHIM/STUB: 部分SDK模式的入口封装可能来自OpenClaudeCode推测
