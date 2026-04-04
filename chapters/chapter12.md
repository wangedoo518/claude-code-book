# 第12章：流式响应：为什么回复一个字一个字蹦出来

> **所属**：第三编 · AI是怎么"思考"的
>
> **关键源码**：src/services/api/client.ts, streaming handlers

---

## 生活类比

水龙头vs水桶——你口渴时是等人用水桶打满水送来，还是直接拧开水龙头就喝？流式响应就是"水龙头"：AI边想边说，你边看边理解。

## 这一章要回答的问题

**如果等AI全部生成完再显示，用户要等多久？体验有多差？**

一个复杂问题的回答可能需要10-30秒才能生成完毕。如果让用户盯着空白屏幕等30秒，大多数人会以为程序卡了。流式响应把等待变成了阅读——第一个字在1-2秒内就出现，用户的感知延迟从30秒变成了2秒。

---

## 12.1 SSE事件结构

### message_start
- 标记一条新消息的开始，包含消息元信息（模型、角色、token估算等）
- 这是流的第一个事件，收到它意味着API已经开始处理请求

### content_block_delta
- 消息内容的增量片段——可能是几个字符的文本，也可能是JSON参数的碎片
- delta事件是流式响应的主体，占所有事件的绝大多数
- 每个delta都有一个index，指示它属于哪个content block

### message_stop与事件流示例
- 标记整条消息生成完毕
- 完整事件流示例：message_start → content_block_start → 多个delta → content_block_stop → message_stop
- 一条消息可能包含多个content block（文本块 + 工具调用块）

## 12.2 StreamingToolExecutor

### 工具参数的流式JSON解析
- 工具调用的参数以JSON格式传输，但JSON是分段到达的
- `{"file": "/sr` ... `c/main.tsx", "co` ... `ntent": "hello"}`
- 需要一个增量JSON解析器来处理不完整的JSON片段

### 部分响应处理
- 文本内容可以逐字渲染——每收到一个delta就更新UI
- 工具参数不能逐字执行——必须等完整JSON拼接完毕才能开始执行工具
- 但可以提前展示"正在准备执行XXX工具"的提示

### 渲染节流
- 不是每收到一个字符就刷新一次终端——那会导致性能问题
- 使用requestAnimationFrame式的节流：收集一批delta后统一渲染
- 在流畅感和性能之间找到平衡点

## 12.3 Thinking Block处理

### Extended Thinking
- Claude的"思考过程"以thinking content block的形式返回
- 这些思考内容展示了AI的推理过程——为什么选择这个工具、为什么这样修改

### Thinking与Text交替
- 一条消息中可能出现thinking→text→thinking→text的交替模式
- AI先思考一部分、输出一部分结果、再思考下一步
- 需要正确处理这种交替结构，不能打乱顺序

### Thinking的显示策略
- 默认折叠：用户主要关心结果，不是推理过程
- 可展开查看：好奇的用户可以展开看AI在想什么
- 在终端中用特殊样式（如淡灰色或斜体）与正式回复区分

---

## 深水区（架构师选读）

流式JSON解析是一个有趣的技术挑战。标准JSON解析器要求输入是完整的——`JSON.parse('{"a": 1')` 会直接报错。但在流式场景中，你需要在JSON不完整时就提取已有信息。Claude Code的增量解析器维护一个状态机，跟踪当前解析位置（是在字符串内、对象内还是数组内），在收到新的delta后从断点继续解析。对于中断恢复，如果网络断开又重连，需要从最后一个成功处理的事件继续，而不是从头开始——这要求客户端维护精确的事件序号追踪。

---

## 本章小结

> **一句话**：流式响应通过SSE事件将AI的生成过程实时传输到终端，StreamingToolExecutor处理不完整的JSON碎片，Thinking Block让用户可以窥见AI的推理过程。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/services/api/client.ts | API客户端与SSE处理 | A |
| src/services/api/streaming.ts | 流式事件解析 | A |
| src/tools/StreamingToolExecutor.ts | 流式工具执行 | A |
| src/components/ThinkingBlock.tsx | Thinking UI渲染 | B |

### 逆向提醒

- ✅ RELIABLE: SSE事件结构和流式处理的整体架构
- ⚠️ CAUTION: 增量JSON解析器的具体实现可能有多种版本
- ❌ SHIM/STUB: 部分渲染节流参数可能使用OpenClaudeCode的默认值
