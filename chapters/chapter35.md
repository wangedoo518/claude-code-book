# 第35章：指挥官模式：编排引擎

> **所属**：第八编 · AI团队——多智能体协作
>
> **关键源码**：src/coordinator/, feature gate COORDINATOR_MODE

---

## 生活类比

乐队指挥——不演奏任何乐器，但让小提琴、大提琴、长笛在恰当的时刻一起响起。Coordinator就是AI团队的"指挥"。

## 这一章要回答的问题

**什么时候需要"指挥官"而不是"自由协作"？**

前两章介绍的多智能体方式——无论是子进程还是Team——都是"扁平协作"：成员各自认领任务，相对独立地工作。但当任务之间有复杂的依赖关系时，就需要一个"指挥官"来编排执行顺序、管理资源冲突、确保全局最优。

---

## 35.1 Coordinator目录

### 核心类
- coordinator/目录包含编排引擎的核心实现
- 主要组件：CoordinatorEngine（主引擎）、TaskDAG（任务依赖图）、Scheduler（调度器）
- Coordinator不执行具体任务——它只负责"指挥"其他Agent去执行

### 任务DAG
- DAG（有向无环图）描述任务之间的依赖关系
- 节点是任务，边是依赖——"先完成A和B，才能开始C"
- 没有环保证了任务图的可执行性——不会出现死锁

### 并发控制
- DAG中没有依赖关系的任务可以并行执行
- 并发度受限于可用的Agent数量和系统资源
- Coordinator动态调整并发度——当某个Agent完成任务后立即分配下一个可执行任务

## 35.2 Channel通信

### 抽象定义
- Channel是Agent之间通信的抽象层——不关心底层传输方式
- 每个Channel有唯一ID、发送方、接收方和消息类型约束
- Channel可以一对一，也可以一对多

### 消息路由
- Coordinator充当消息路由中心——所有跨Agent通信经过它
- 路由规则基于Channel定义——消息只会到达正确的接收方
- 路由中心模式让Coordinator能监控所有通信，发现异常及时干预

### 同步vs异步与背压
- 大部分通信是异步的——发送方不等待接收方处理完
- 少数关键通信是同步的——比如需要对方确认的审批流程
- 背压机制防止快速发送方淹没慢速接收方——消息队列有容量上限

## 35.3 Feature Gate

### COORDINATOR_MODE
- Coordinator系统目前由COORDINATOR_MODE Feature Gate保护
- 这意味着它不是对所有用户默认启用的——需要特定条件触发
- Gate的存在说明这是一个正在成熟但尚未完全稳定的能力

### 相关Flag
- COORDINATOR_MODE不是孤立的——它关联着一组Feature Flag
- 相关flag控制Coordinator的子功能：任务超时、自动重试、失败回滚等
- 这些flag的组合决定了Coordinator的具体行为配置

### 未来方向
- 从flag的命名和注释可以推测Coordinator的发展方向
- 更智能的任务拆解（自动将大任务分解为DAG）
- 更丰富的Agent角色（专门的reviewer、tester、documenter）

---

## 深水区（架构师选读）

任务依赖图的拓扑排序——DAG在多智能体任务分配中的应用。Coordinator的核心调度算法基于DAG的拓扑排序：找出所有入度为0的节点（没有前置依赖的任务），分配给空闲Agent执行。当一个任务完成时，减少所有后继节点的入度，新产生的入度为0的节点加入就绪队列。这就是经典的Kahn算法在多智能体场景下的应用。但实际实现比教科书版本更复杂：任务可能有优先级权重（关键路径上的任务优先）、Agent可能有能力差异（某些Agent更适合某类任务）、任务可能动态增加（执行中发现新的子任务）。这些扩展让简单的拓扑排序变成了一个在线调度优化问题。

---

## 本章小结

> **一句话**：Coordinator是多智能体的"指挥官"——通过任务DAG管理依赖、通过Channel路由通信、通过并发控制最大化效率——目前由Feature Gate保护，正在走向成熟。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/coordinator/ | 编排引擎核心目录 | B |
| src/coordinator/TaskDAG.ts | 任务依赖图 | B |
| src/coordinator/Channel.ts | Agent间通信通道 | B |
| src/utils/features.ts | Feature Gate (COORDINATOR_MODE) | A |

### 逆向提醒

- ✅ RELIABLE: Coordinator目录的存在和Feature Gate保护
- ⚠️ CAUTION: DAG调度和Channel通信的具体实现可能处于快速迭代中
- ❌ SHIM/STUB: Coordinator的部分高级功能（自动任务拆解等）可能只有接口定义
