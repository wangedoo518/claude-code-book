# 第30章：AI的笔记本：CLAUDE.md与记忆目录

> **所属**：第七编 · 记忆与遗忘——上下文的艺术
>
> **关键源码**：src/utils/memdir/memdir.ts, CLAUDE.md loading, src/services/extractMemories/, src/services/autoDream/

---

## 生活类比

学生的学习系统：教科书(CLAUDE.md)→笔记本(MEMORY.md)→错题集(typed memory)→学习助手自动整理(DreamTask)。

## 这一章要回答的问题

**CLAUDE.md、MEMORY.md、Magic Doc、DreamTask——这么多"笔记"各管什么？**

一个学生不会把所有知识写在同一个本子上。教科书是系统化的基础知识，笔记本是自己的理解，错题集是需要反复强化的薄弱点。Claude Code的记忆系统也做了类似的分工——每种"笔记"有不同的格式、不同的更新频率、不同的用途。

---

## 30.1 memdir.ts与MEMORY.md

### 目录结构
- memdir（memory directory）是记忆文件的组织方式——不是一个大文件，而是一组结构化的目录
- ~/.claude/memory/下按主题、项目、类型分类存放
- 每个记忆文件都是独立的Markdown文件，方便人类阅读和编辑

### 索引文件与Frontmatter
- MEMORY.md充当记忆目录的索引文件，汇总各条记忆的概要
- 每条记忆文件使用YAML frontmatter标记元数据：类型、创建时间、来源、过期时间
- frontmatter让程序可以快速扫描记忆属性，无需解析全文

### 四种记忆类型
- **user**：用户偏好和习惯——"我喜欢用单引号"、"项目用pnpm不用npm"
- **feedback**：用户对AI行为的反馈——"不要自动加分号"、"commit message用英文"
- **project**：项目特定的知识——架构决策、关键路径、常见坑点
- **reference**：参考资料和文档片段——API用法、配置模板、代码样例

## 30.2 Typed Memory

### 结构化存储
- 与自由文本不同，Typed Memory有明确的Schema定义
- 每条记忆有类型标签、置信度评分、关联标签
- 结构化使得记忆可以被程序精确检索，而不只是全文搜索

### 可检索与可过期
- 通过类型和标签快速定位相关记忆——"找到所有关于测试框架的记忆"
- 过期时间让短期有效的信息自动退场——"这个API的临时workaround三个月后清除"
- 去重机制避免同一条信息被反复记录——基于语义相似度判断

### 为什么比随手塞文本更稳
- 自由文本的记忆容易堆积成难以维护的"垃圾堆"
- 有Schema约束的记忆可以自动校验、自动清理、自动合并
- Typed Memory是"有纪律的记忆"——写入有规范，存储有结构，过期有机制

## 30.3 Magic Doc与DreamTask

### AI自动更新文档
- Magic Doc是AI主动更新项目文档的能力——发现代码变化时自动修改对应文档
- 不是简单的文件监听，而是基于语义理解判断"这次代码改动是否影响了文档描述"
- 更新结果需要经过可信度评估，低置信度的更新会标记为"待审核"

### 后台记忆整理
- DreamTask是一个后台运行的记忆整理任务——像人在睡眠中整理白天的记忆
- 它分析会话中的对话，提取值得长期保留的信息写入记忆目录
- 整理过程包括：去重、归类、摘要、建立关联

### extractMemories服务
- extractMemories是DreamTask的核心引擎——从对话历史中提取结构化记忆
- 它识别用户的偏好表达、纠正反馈、知识传授等模式
- 提取的记忆经过格式化后写入memdir，成为持久化的知识

---

## 深水区（架构师选读）

DreamTask的自主性——后台记忆整理是如何触发的，以及如何避免删除有用知识。DreamTask的触发条件包括：会话结束时、空闲时间超过阈值时、记忆条目数量超过阈值时。但自主整理面临一个核心挑战：如何判断一条记忆"不再有用"？删除过激会丢失关键知识，不删除则记忆膨胀。当前的策略是多信号融合——最近访问时间、引用频率、用户显式标记、语义与其他记忆的重叠度。被判定为"可能过时"的记忆不会直接删除，而是降级到低优先级区域，在上下文紧张时最后被加载。

---

## 本章小结

> **一句话**：CLAUDE.md是教科书、MEMORY.md是笔记本、Typed Memory是结构化错题集、DreamTask是自动整理助手——各司其职，共同构成AI的知识管理系统。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/utils/memdir/memdir.ts | 记忆目录管理核心 | A |
| src/services/extractMemories/ | 记忆提取引擎 | B |
| src/services/autoDream/ | DreamTask后台整理 | B |
| CLAUDE.md | 项目级记忆载体 | A |

### 逆向提醒

- ✅ RELIABLE: memdir目录结构和MEMORY.md格式规范
- ⚠️ CAUTION: DreamTask的触发条件和整理策略可能随版本调整
- ❌ SHIM/STUB: extractMemories的部分NLP逻辑在开源版中可能被降级为简单规则
