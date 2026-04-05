---
icon: material/trophy-outline
---

# 第十编：站在巨人肩膀上

<div class="part-intro" markdown>

> *前面九编是在拆机器，这一编开始总结“这台机器为什么这样设计”。*
>
> 我们会从全局视角回看 Claude Code：提炼跨系统的设计模式，理解它为什么能在 CLI 里跑得又快又稳，分清还原层与补全层的边界，并最终把它放回更大的 AI 编程路线图里。

</div>

---

## 本编总览

```mermaid
flowchart LR
    subgraph 第十编["🏆 站在巨人肩膀上"]
        direction TB
        C39["第39章<br/>设计模式<br/><i>带走的架构智慧</i>"]
        C40["第40章<br/>性能工程<br/><i>速度的艺术</i>"]
        C41["第41章<br/>恢复层真相<br/><i>原貌与补全的边界</i>"]
        C42["第42章<br/>竞品与未来<br/><i>Claude Code 的路线坐标</i>"]
    end

    C39 --> C40 --> C41 --> C42
    C42 --> END["全书结束"]

    style 第十编 fill:#18324b,stroke:#64b5f6,color:#fff
    style C39 fill:#23415d,stroke:#ffd54f,color:#fff
    style C40 fill:#23415d,stroke:#4db6ac,color:#fff
    style C41 fill:#23415d,stroke:#ff8a65,color:#fff
    style C42 fill:#23415d,stroke:#ba68c8,color:#fff
```

---

## 本编四章速览

| 章 | 标题 | 核心问题 | 生活类比 |
|---|---|---|---|
| 39 | [设计模式](chapter39.md) | 读完大规模源码，哪些通用工程心法最值得带走？ | 武术心法 |
| 40 | [性能工程](chapter40.md) | 这么大的系统为什么还能做出秒启 CLI？ | F1 赛车调校 |
| 41 | [恢复层真相](chapter41.md) | 哪些是官方原貌，哪些是逆向补全？ | 修复古画 |
| 42 | [竞品与未来](chapter42.md) | Claude Code 代表了哪种路线，下一步会走向哪里？ | 路线图与地图坐标 |

!!! success "本编阅读目标"
    读完这一编，你不只会“看懂 Claude Code”，还会更清楚哪些设计值得复用、哪些结论需要谨慎，以及这套系统在更大 AI 编程版图中的位置。
