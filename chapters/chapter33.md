# 第33章：为什么一个AI不够用

> **所属**：第八编 · AI团队——多智能体协作
>
> **关键源码**：src/tools/AgentTool/, src/utils/swarm/, src/coordinator/

---

## 生活类比

一个人搬家vs请搬家公司——有些活一个人干太慢，需要分工协作。AI也是：一个Agent搞不定的复杂任务，就"组团"。

## 这一章要回答的问题

**子进程、Worktree、Coordinator——三种"组队"方式有什么区别？**

你让Claude Code重构一个大项目：改架构、更新测试、修改文档——一个Agent按顺序做要几个小时。如果能让三个Agent各负责一块，并行工作呢？Claude Code提供了三种"组队"路径，各有取舍。

---

## 33.1 路径一：子进程

### AgentTool派生
- AgentTool是最基础的多智能体方式——主Agent派生一个子Agent
- 子Agent运行在独立的子进程中，有自己的上下文和工具集
- 主Agent通过AgentTool的调用接口与子Agent通信

### 上下文隔离
- 子Agent不共享主Agent的完整上下文——只接收到主Agent传递的任务描述
- 这种隔离是有意为之：防止子Agent被无关信息干扰，聚焦于分配的子任务
- 子Agent有自己的工具集，可以限制为只读或特定工具子集

### 结果回传
- 子Agent完成任务后将结果以文本形式返回给主Agent
- 主Agent收到结果后继续自己的推理循环——子Agent的生命周期结束
- 适用场景：独立的搜索任务、文件分析、方案探索——不需要持续协作的子任务

## 33.2 路径二：Worktree隔离

### Git Worktree
- 利用Git的worktree特性为每个Agent创建独立的工作目录
- 每个Agent在自己的worktree中操作文件——互不干扰
- 避免了多Agent同时修改同一文件导致的冲突

### 独立文件系统
- 每个worktree是项目仓库的一个独立检出——拥有完整的文件系统视图
- Agent可以自由创建、修改、删除文件，不影响其他Agent的工作
- 这比子进程模式更重——需要磁盘空间和Git操作的开销

### 变更合并
- 各Agent完成工作后，通过Git的合并机制整合变更
- 冲突由主Agent或用户解决——与正常的Git协作流程一致
- 适用场景：需要大规模并行文件修改的任务——重构、批量迁移、多模块开发

## 33.3 路径三：Coordinator

### coordinator/目录
- coordinator/是一个独立的协调层——不同于AgentTool的简单派生
- 它管理多个Agent的生命周期、任务分配、通信路由
- 目前由COORDINATOR_MODE Feature Gate控制，尚在逐步开放

### Channel通信
- Agent之间通过Channel发送消息——而不是简单的结果回传
- Channel支持双向通信——Agent可以请求协助、报告进度、同步状态
- 这使得Agent之间可以动态协作，而不只是"分配-完成-回传"

### 任务依赖图
- Coordinator维护一个任务依赖图——哪些任务可以并行、哪些必须串行
- 当一个任务完成时，自动解锁依赖它的下游任务
- 这是最复杂但也最强大的协作模式——适合有复杂依赖关系的大型任务

---

## 深水区（架构师选读）

三种路径的性能与成本对比——启动时间、token消耗、通信开销的量化分析。子进程路径启动最快（毫秒级），但每个子Agent需要独立的API调用，token消耗与Agent数量成正比。Worktree路径启动较慢（秒级，需要Git checkout），磁盘开销显著，但文件操作性能与单Agent相同。Coordinator路径启动最慢（需要建立通信Channel和依赖图），但在复杂任务上的总完成时间最短——因为任务调度更智能。一个经验法则：子任务少于3个用子进程，3-10个独立文件修改任务用Worktree，超过10个有依赖关系的任务用Coordinator。

---

## 本章小结

> **一句话**：Claude Code提供三种多智能体路径——子进程（轻量、一次性）、Worktree（文件隔离、Git合并）、Coordinator（完整编排、Channel通信）——从简单到复杂覆盖不同的协作场景。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/tools/AgentTool/ | 子Agent派生工具 | A |
| src/utils/swarm/ | 多智能体基础设施 | B |
| src/coordinator/ | 协调器核心目录 | B |
| src/utils/worktree.ts | Git Worktree管理 | A |

### 逆向提醒

- ✅ RELIABLE: AgentTool的子进程派生和结果回传机制
- ⚠️ CAUTION: Coordinator的完整实现可能随Feature Gate状态变化
- ❌ SHIM/STUB: coordinator/中的部分Channel实现可能为占位代码
