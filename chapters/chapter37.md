# 第37章：89个开关：Feature Flag的秘密

> **所属**：第九编 · 冰山之下——隐藏特性与前沿功能
>
> **关键源码**：feature() calls, bun:bundle config, GrowthBook

---

## 生活类比

一栋89个房间的大楼——有的开着灯正常使用，有的锁着门等待装修，有的是实验室限制进入。Feature Flag就是这些房间的开关。

## 这一章要回答的问题

**89个开关背后，Anthropic到底还在做什么？**

源码中散布着大量的feature()调用——每一个都是一道门。门开着就执行对应逻辑，门关着就走默认路径。这89个开关揭示了Claude Code的完整能力版图——包括你看得见的和看不见的。

---

## 37.1 Flag系统实现

### bun:bundle与DCE
- Feature Flag在编译时通过Bun的bundle特性处理
- DCE（Dead Code Elimination）在编译时移除未启用feature的代码路径
- 这意味着发布版本中某些代码路径物理上不存在——不是运行时判断，是编译时剔除

### feature()调用
- 代码中通过feature("FLAG_NAME")检查flag状态
- 返回值决定代码路径——true走新功能，false走旧路径或默认行为
- feature()的实现很轻量——通常是一次Map查找或常量返回

### 运行时vs编译时
- 编译时flag：在build阶段确定，发布后不可更改——用于彻底移除实验代码
- 运行时flag：通过GrowthBook等服务动态控制——用于灰度发布和AB测试
- 两种机制并存——安全敏感的用编译时，需要灵活控制的用运行时

## 37.2 核心Flag分类

### 模式类Flag
- **KAIROS**：自主行动模式——AI主动发现和执行任务
- **COORDINATOR_MODE**：编排器模式——多Agent协调的高级模式
- 模式类flag控制的是整个交互范式的切换

### 工具类Flag
- **WEB_BROWSER**：网页浏览工具——控制AI能否浏览网页
- **COMPUTER_USE**：计算机操控——控制AI能否操作鼠标键盘
- 工具类flag控制的是具体能力的开关

### 实验类Flag
- **TORCH**：可能与高级推理或模型切换相关的实验功能
- **ULTRAPLAN**：增强规划能力——可能是更强大的任务分解和规划
- 实验类flag通常在极小范围内测试——可能只有内部员工能触发

## 37.3 从Flag推测规划

### KAIROS→自主化方向
- KAIROS及相关flag暗示Anthropic在探索AI的自主行动能力
- 从被动响应到主动行动是一个根本性的范式转变
- 相关的安全flag（审计、确认、回滚）同步增长说明安全方面的重视

### VOICE→语音交互方向
- voice相关的flag和目录暗示语音交互是计划中的能力
- voiceKeyterms等子功能说明已经在处理语音识别的细节问题
- 语音+CLI的组合可能改变开发者与AI交互的方式

### ULTRAPLAN→增强规划与趋势分析
- ULTRAPLAN暗示更强大的任务规划能力——可能结合更长的推理链
- 结合COORDINATOR_MODE看，多Agent+强规划是一个清晰的发展方向
- 总体趋势：更自主、更多模态、更强协作——从工具向伙伴演进

---

## 深水区（架构师选读）

Dead Code Elimination的编译器原理——bun:bundle如何在编译时移除未启用feature的代码路径。DCE的核心原理是数据流分析：编译器分析每个代码分支是否可达，不可达的分支直接移除。当feature("KAIROS")被编译时替换为常量false时，if(false){ ... }中的整个代码块对编译器来说就是"死代码"。Bun的bundle在这方面做了特殊优化：它不仅移除直接的死代码块，还会追踪因此变得无引用的函数、类、模块——进行传递性的死代码消除。这就是为什么开源版本的编译产物中某些功能完全不存在——不是被隐藏了，是在编译阶段就被物理移除了。理解DCE对逆向分析至关重要：你看不到的代码不一定是被删除了，可能是被flag关闭后被DCE清理了。

---

## 本章小结

> **一句话**：89个Feature Flag通过编译时DCE和运行时GrowthBook两种机制控制Claude Code的完整能力版图——从中可以推测Anthropic在自主化、语音、增强规划等方向的战略布局。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/utils/features.ts | Feature Flag核心实现 | A |
| bun:bundle config | 编译时DCE配置 | A |
| src/services/growthbook/ | 运行时flag服务 | B |
| feature() 调用点（散布全项目） | 各feature的使用位置 | A |

### 逆向提醒

- ✅ RELIABLE: Feature Flag系统的实现机制和feature()调用模式
- ⚠️ CAUTION: 具体flag的开关状态可能每个版本都不同
- ❌ SHIM/STUB: 被DCE移除的代码路径在开源版中完全不可见
