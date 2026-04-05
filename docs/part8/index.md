---
icon: material/account-group
---

# 第八编：AI 团队

<div class="part-intro" markdown>

> *一个人能做很多事，但真正复杂的工程，往往靠分工协作。*
>
> Claude Code 的多智能体体系，不只是“多开几个窗口”，而是把 **子 Agent**、**worktree 隔离**、**团队消息**、**Coordinator 编排** 组合成了多种协作模式。

</div>

---

## 本编总览

```mermaid
flowchart LR
    subgraph 第八编["🐝 AI 团队"]
        direction TB
        C33["第33章<br/>为什么一个 AI 不够用<br/><i>三条组队路径</i>"]
        C34["第34章<br/>团队蜂群<br/><i>TeamCreate 与消息协作</i>"]
        C35["第35章<br/>指挥官模式<br/><i>Coordinator 编排</i>"]
    end

    C33 --> C34 --> C35
    C35 --> NEXT["第九编：冰山之下"]

    style 第八编 fill:#18324b,stroke:#64b5f6,color:#fff
    style C33 fill:#23415d,stroke:#ffd54f,color:#fff
    style C34 fill:#23415d,stroke:#4db6ac,color:#fff
    style C35 fill:#23415d,stroke:#ba68c8,color:#fff
```

---

## 本编三章速览

| 章 | 标题 | 核心问题 | 生活类比 |
|---|---|---|---|
| 33 | [为什么一个 AI 不够用](chapter33.md) | 子 Agent、worktree、远程隔离到底差在哪？ | 一个人搬家 vs 搬家公司 |
| 34 | [团队蜂群](chapter34.md) | 多个 Agent 怎样像团队一样协作？ | 蜜蜂分工 |
| 35 | [指挥官模式](chapter35.md) | 什么时候需要 Coordinator，而不是自由协作？ | 乐队指挥 |

!!! success "本编阅读目标"
    读完这一编，你会明白 Claude Code 的多智能体不是噱头，而是一套围绕隔离、协作、编排和恢复设计出来的工作体系。
