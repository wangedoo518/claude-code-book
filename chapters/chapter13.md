# 第13章：Token经济学：每个字都有价格

> **所属**：第三编 · AI是怎么"思考"的
>
> **关键源码**：src/services/tokenEstimation/, src/services/api/claude.ts

---

## 生活类比

手机流量套餐——你的月流量有上限，视频比文字更耗流量，用完就要额外付费。LLM的token就像流量：每个字都有价格，上下文窗口就是你的"套餐额度"。

## 这一章要回答的问题

**怎么在有限的"流量"里完成更多任务？prompt caching怎么省70-90%成本？**

每次API调用都有真金白银的成本——输入token和输出token分别计费。一个复杂任务可能触发十几次API调用，每次都带着越来越长的消息历史。如果不管理token预算，成本会快速飙升。理解token经济学，是构建可持续AI产品的关键。

---

## 13.1 Token估算服务

### 不同内容类型的估算
- 纯文本：大约1 token ≈ 4个英文字符或1.5个中文字符
- 代码：变量名、缩进、符号导致每行消耗更多token
- JSON/Schema：结构性字符（大括号、引号、冒号）占了大量token

### 图片token特殊计算
- 图片不是按文件大小计费，而是按分辨率
- 一张1024x1024的图片约消耗数百到上千token
- Claude Code在发送图片前会估算token消耗，避免意外成本

### 精度vs性能
- 精确计算token需要调用tokenizer——这本身有计算成本
- Claude Code使用启发式估算：对大多数场景足够准确，且几乎不耗时
- 在关键决策点（如是否截断历史）使用精确计算，日常统计用估算

## 13.2 Prompt Caching策略

### Cache Breakpoint
- 将system prompt分成多个段，在段之间插入cache breakpoint标记
- API服务器检测到前缀与之前请求匹配时，复用已缓存的计算结果
- breakpoint的位置决定了缓存粒度——越靠前的内容越适合做缓存

### 缓存命中 = 70-90%成本削减
- 被缓存的token按大幅折扣计费
- system prompt通常占总输入token的很大比例——缓存它带来巨大节省
- 多轮对话中，前几轮的消息历史也可能被缓存

### 失效条件
- 任何一个字符的变化都会导致该位置之后的缓存失效
- 因此动态内容（如时间戳、文件修改时间）要放在prompt末尾
- 静态内容（安全规则、工具Schema）放在开头，最大化缓存命中

## 13.3 成本追踪与预算

### 实时统计
- 每次API调用后记录输入token、输出token、缓存命中token
- 累计统计当前会话的总成本
- 用户可以随时查看已消耗的token和估算费用

### 输入输出分类计费
- 输入token（你发给AI的）和输出token（AI回复的）价格不同
- 输出token通常比输入token贵3-5倍
- 工具调用的结果作为输入token计费，AI生成的工具参数作为输出token计费

### 用户端成本显示与预算警告
- 在终端UI中显示当前会话的token消耗和估算成本
- 接近预算上限时发出警告
- 超出预算时可以选择继续（付费）或停止

---

## 深水区（架构师选读）

上下文预算分配是一个资源分配优化问题。200K token的上下文窗口看似巨大，但需要在四个竞争者之间分配：system prompt（安全规则、工具Schema，通常10-20K）、历史消息（随对话增长，可能占据100K+）、工具结果（一次文件读取可能就是几K）、最新轮次的生成空间（需要为AI的输出预留足够空间）。当总量接近上限时，需要动态调整：压缩历史消息、截断过长的工具结果、甚至减少注入的工具Schema。这个动态预算分配算法是保证长对话不崩溃的关键。

---

## 本章小结

> **一句话**：Token是AI的"货币"——Claude Code通过估算服务控制消耗、通过prompt caching削减70-90%成本、通过实时追踪让用户掌握开支。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/services/tokenEstimation/ | Token估算服务 | A |
| src/services/api/claude.ts | API调用与计费 | A |
| src/constants/prompts.ts | Cache breakpoint位置 | A |
| src/services/cost.ts | 成本追踪与显示 | B |

### 逆向提醒

- ✅ RELIABLE: Token估算的整体机制和prompt caching策略
- ⚠️ CAUTION: 具体的token价格和缓存折扣率随Anthropic定价调整
- ❌ SHIM/STUB: 成本追踪UI的部分实现可能来自OpenClaudeCode补全
