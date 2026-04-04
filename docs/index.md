---
hide:
  - navigation
  - toc
---

<div class="hero-section" markdown>

# Claude Code 源码解析红宝书

**基于 v2.1.88 双生逆向源码的设计思想深度解析**

*从高中生到架构师，一本书，三种读法，同一条路径*

<div class="hero-stats">
<div class="hero-stat">
<div class="number">1,884</div>
<div class="label">TypeScript 文件</div>
</div>
<div class="hero-stat">
<div class="number">512,664</div>
<div class="label">行源代码</div>
</div>
<div class="hero-stat">
<div class="number">54</div>
<div class="label">内置工具</div>
</div>
<div class="hero-stat">
<div class="number">88</div>
<div class="label">斜杠命令</div>
</div>
<div class="hero-stat">
<div class="number">89</div>
<div class="label">Feature Flag</div>
</div>
</div>

[开始阅读 :material-arrow-right:](guide.md){ .md-button .md-button--primary }
[第一编：欢迎来到源码的世界 :material-book-open-variant:](part1/index.md){ .md-button }

</div>

---

## 这本书讲什么

```mermaid
mindmap
  root((Claude Code<br/>源码解析))
    欢迎篇
      打开黑箱
      双生代码库
      全景地图
    启动篇
      启动链条
      多模式
      状态管理
      终端渲染
    引擎篇
      提示词装配
      Agent Loop
      流式响应
      Token经济
    工具篇
      54个工具
      Bash安全
      文件读写改
      Agent+Skill+MCP
    安全篇
      七层防御
      25道关卡
      沙箱隔离
    扩展篇
      MCP协议
      IDE桥接
      插件生态
    记忆篇
      四层记忆
      压缩系统
      实验功能
    协作篇
      多智能体
      团队蜂群
      编排引擎
    隐藏篇
      KAIROS
      Feature Flag
      彩蛋
    哲学篇
      设计模式
      性能工程
      恢复层真相
      竞品与未来
```

---

## 四条设计思想主线

!!! tip "主线一：不是聊天壳"
    Claude Code 不是套了个壳的 ChatGPT——它是一个**会调用工具的任务执行器**

!!! tip "主线二：铁三角"
    核心架构 = **上下文装配** + **Agent Loop** + **工具编排**

!!! tip "主线三：最难的不是生成"
    真正的工程挑战在于**权限、安全、压缩、恢复、一致性**

!!! tip "主线四：两套代码库"
    "能跑起来"不等于"官方原始设计"——严格区分**还原层**与**补全层**

---

## 全书结构一览

| 编 | 主题 | 章节 | 生活类比 |
|---|------|------|----------|
| 第一编 | [欢迎来到源码的世界](part1/index.md) | 1-4 | 拆开收音机 |
| 第二编 | [程序是怎么启动的](part2/index.md) | 5-8 | 汽车点火 |
| 第三编 | [AI 是怎么思考的](part3/index.md) | 9-13 | 厨师做菜 |
| 第四编 | [AI 的双手——工具系统](part4/index.md) | 14-19 | 电器插头标准 |
| 第五编 | [安全防线](part5/index.md) | 20-24 | 机场安检 |
| 第六编 | [连接世界](part6/index.md) | 25-28 | USB 接口 |
| 第七编 | [记忆与遗忘](part7/index.md) | 29-32 | 人的记忆系统 |
| 第八编 | [AI 团队](part8/index.md) | 33-35 | 蜜蜂分工 |
| 第九编 | [冰山之下](part9/index.md) | 36-38 | 隐藏关卡 |
| 第十编 | [站在巨人肩膀上](part10/index.md) | 39-42 | 武术心法 |

---

## 三种读法

=== "🌱 探索路径（初学者）"

    **推荐章节**：1 → 4 → 5 → 8 → 9 → 11 → 14 → 16 → 20 → 29 → 33 → 36 → 39 → 42

    每章只读**生活类比**和**核心问题**部分，跳过深水区。你会理解一个真实大型软件的设计思路。

=== "🔧 实战路径（开发者）"

    按编顺序通读，**选读深水区**。你会获得可复用的架构模式和 CLI 开发实战经验。

=== "🏗️ 架构路径（架构师）"

    先读**第3章**（证据边界）和**第41章**（恢复层真相），再按兴趣深入所有**深水区**。
