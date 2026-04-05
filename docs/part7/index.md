---
icon: material/brain
---

# 第七编：记忆与遗忘

<div class="part-intro" markdown>

> *一个好助手，不只是“现在听得懂你”，还要“过几天还能接上你的上下文”。*
>
> Claude Code 的记忆系统不是一个大缓存，而是多层结构：**会话内上下文**、**项目级指令**、**持久化记忆目录**、**团队共享记忆**，再加上一整套压缩和实验机制来控制体积与新鲜度。

</div>

---

## 本编总览

```mermaid
flowchart LR
    subgraph 第七编["🧠 记忆与遗忘"]
        direction TB
        C29["第29章<br/>四层记忆<br/><i>Claude Code 怎么记住你</i>"]
        C30["第30章<br/>AI 的笔记本<br/><i>CLAUDE.md 与 MEMORY.md</i>"]
        C31["第31章<br/>压缩系统<br/><i>上下文装不下怎么办</i>"]
        C32["第32章<br/>实验区<br/><i>哪些功能还在试验</i>"]
    end

    C29 --> C30 --> C31 --> C32
    C32 --> NEXT["第八编：AI 团队"]

    style 第七编 fill:#18324b,stroke:#64b5f6,color:#fff
    style C29 fill:#23415d,stroke:#ffd54f,color:#fff
    style C30 fill:#23415d,stroke:#4db6ac,color:#fff
    style C31 fill:#23415d,stroke:#ff8a65,color:#fff
    style C32 fill:#23415d,stroke:#ba68c8,color:#fff
```

---

## 本编四章速览

| 章 | 标题 | 核心问题 | 生活类比 |
|---|---|---|---|
| 29 | [四层记忆](chapter29.md) | 关掉终端之后，Claude Code 还记得什么？ | 人的记忆分层 |
| 30 | [AI 的笔记本](chapter30.md) | CLAUDE.md、MEMORY.md、DreamTask 各自负责什么？ | 教科书、笔记本、错题集 |
| 31 | [压缩系统](chapter31.md) | 上下文快满了，怎么瘦身又不丢重点？ | 塞满的行李箱 |
| 32 | [实验区](chapter32.md) | 哪些代码已经上线，哪些还只是概念车？ | 车展上的概念车 |

---

## 你会在这一编看到什么

```mermaid
flowchart TD
    A["用户与项目信息"] --> B["CLAUDE.md / 规则文件"]
    A --> C["Auto Memory / Team Memory"]
    B --> D["QueryEngine 注入上下文"]
    C --> D
    D --> E["上下文增长"]
    E --> F["Compact / Snip / Context Collapse"]

    style D fill:#e3f2fd,stroke:#1e88e5,color:#000
    style F fill:#ede7f6,stroke:#7e57c2,color:#000
```

!!! success "本编阅读目标"
    读完这一编，你会明白 Claude Code 的“记忆”不是魔法，而是一套文件化、可注入、可压缩、可同步、也会过期的工程系统。
