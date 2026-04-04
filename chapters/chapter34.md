# 第34章：团队蜂群：AI组队的架构

> **所属**：第八编 · AI团队——多智能体协作
>
> **关键源码**：src/tools/TeamCreateTool/, src/tools/SendMessageTool/, src/services/teamMemorySync/

---

## 生活类比

蜜蜂的分工协作——侦察蜂(Explore Agent)负责找花、采蜜蜂(general Agent)负责干活、守卫蜂(security)负责安全。AI团队也有类似的角色分工。

## 这一章要回答的问题

**AI也能组团队？"团队"到底意味着什么？**

在上一章我们看到了三种"组队"路径。但"组队"只是手段，真正的问题是：这些Agent如何像一个真正的团队那样运作——有创建、有分工、有协作、有解散？TeamCreate系统给出了完整的答案。

---

## 34.1 Team生命周期

### 配置结构
- Team的配置存储在~/.claude/teams/{team-name}/config.json
- 配置包含团队名称、描述、成员列表（name、agentId、agentType）
- 每个团队同时有一个任务列表目录~/.claude/tasks/{team-name}/

### 成员注册
- 团队创建后通过Agent工具派生成员，每个成员有唯一名称
- 成员注册到config.json的members数组中
- 成员类型决定其能力范围——只读Agent只能搜索，全能Agent可以编辑文件

### 创建→执行→关闭
- **创建阶段**：TeamCreateTool初始化配置和任务目录，定义团队目标
- **执行阶段**：成员认领任务、并行工作、通过消息协调、标记完成
- **关闭阶段**：所有任务完成后，主Agent发送shutdown_request，成员优雅退出

## 34.2 任务分配与Mailbox

### 认领机制
- 任务创建后处于"待认领"状态，任何空闲成员都可以认领
- 认领通过TaskUpdate设置owner字段——先到先得
- 优先认领ID较小的任务——早期任务往往为后续任务建立上下文

### 消息投递
- SendMessageTool实现成员间的消息传递
- 消息投递到目标成员的Mailbox——如果成员正忙，消息排队等待
- 消息在成员空闲时自动投递——不需要轮询

### 广播vs定向与idle通知
- 定向消息发送给指定成员，广播消息发送给所有成员（开销较大）
- 成员每个轮次结束后自动进入idle状态并发送通知
- idle不代表完成——只是等待下一条消息，可以随时被唤醒

## 34.3 团队记忆同步

### teamMemorySync服务
- 团队成员需要共享某些知识——比如项目的编码规范、已发现的问题列表
- teamMemorySync在成员之间同步这些共享记忆
- 同步是增量的——只传递新增或修改的记忆条目

### 共享知识
- 团队级的CLAUDE.md是所有成员的共享知识基础
- 运行时发现的知识（如"这个API有bug"）通过同步服务共享
- 共享知识让后加入的成员也能获得先行者的发现

### 冲突解决
- 当两个成员同时更新同一条记忆时，需要冲突解决
- 当前策略是"最后写入胜"——简单但可能丢失信息
- 未来可能引入更智能的合并策略——基于语义理解合并冲突内容

---

## 深水区（架构师选读）

Mailbox通信模型——与Actor模型的异同，以及在分布式智能体中的扩展可能。Claude Code的Mailbox与Erlang/Akka的Actor模型有明显的相似性：每个Agent有独立的消息队列，通过异步消息通信，不共享状态。但也有关键区别：Actor模型中Actor是轻量级的（可以有数百万个），而AI Agent是重量级的（每个需要一个API连接和独立上下文）。Actor模型的监督树（supervisor tree）在Claude Code中对应Team Lead的角色——负责监控成员状态、处理异常、重新分配失败的任务。如果将来多智能体系统需要跨机器扩展，Mailbox模型天然适合分布式化——消息队列可以替换为消息中间件，Agent可以分布在不同节点上。

---

## 本章小结

> **一句话**：AI团队有完整的生命周期——创建、成员注册、任务认领、Mailbox消息协调、记忆同步、优雅关闭——像一个真正的蜂群各司其职又协同工作。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/tools/TeamCreateTool/ | 团队创建工具 | A |
| src/tools/SendMessageTool/ | 消息发送工具 | A |
| src/services/teamMemorySync/ | 团队记忆同步 | B |
| ~/.claude/teams/ | 团队配置存储 | A |

### 逆向提醒

- ✅ RELIABLE: Team生命周期和Mailbox消息投递机制
- ⚠️ CAUTION: teamMemorySync的同步策略和冲突解决可能演进
- ❌ SHIM/STUB: 部分高级冲突解决逻辑可能在开源版中降级为简单覆写
