# 阅读指南

## 每章的阅读地图

本书每一章都遵循相同的结构，方便不同水平的读者各取所需：

```mermaid
flowchart TD
    A["🎯 生活类比<br/><i>一个人人能懂的比喻</i>"] --> B["❓ 核心问题<br/><i>激发好奇心的真实场景</i>"]
    B --> C["🔍 源码拆解<br/><i>关键文件 → 核心函数 → 数据流</i>"]
    C --> D["⚖️ 设计取舍<br/><i>为什么这样做而不那样做</i>"]
    D --> E["🔭 深水区<br/><i>架构师选读的高级话题</i>"]
    E --> F["📝 本章小结<br/><i>结论 + 源码索引 + 逆向提醒</i>"]

    style A fill:#fff8e1,stroke:#f9a825,color:#000
    style B fill:#e3f2fd,stroke:#1565c0,color:#000
    style C fill:#f3e5f5,stroke:#7b1fa2,color:#000
    style D fill:#e8f5e9,stroke:#2e7d32,color:#000
    style E fill:#e0f7fa,stroke:#00838f,color:#000
    style F fill:#fce4ec,stroke:#c62828,color:#000
```

!!! tip "所有人都读"
    **生活类比** + **核心问题** —— 建立直觉，激发好奇心

!!! info "有基础的读者继续"
    **源码拆解** + **设计取舍** —— 理解"怎么做"和"为什么"

!!! abstract "架构师选读"
    **深水区** —— 高级话题、边界情况、竞品对比

---

## 特殊标记说明

本书使用以下标记帮助你快速定位内容：

### 可信度等级

每个源码引用都标注可信度：

| 等级 | 标记 | 含义 |
|------|------|------|
| **A级** | <span class="reliability-a">A</span> | 确认原始 — Source Map 直接还原 |
| **B级** | <span class="reliability-b">B</span> | 高度可信 — 主体原始，少量补全 |
| **C级** | <span class="reliability-c">C</span> | 补全推测 — shim/stub/fallback |

### 逆向提醒

每章末尾的逆向提醒用三个图标区分：

- ✅ **RELIABLE**：可以放心引用的分析
- ⚠️ **CAUTION**：需要注意版本差异或可能的变化
- ❌ **SHIM/STUB**：来自补全层，不代表官方实现

---

## 技术准备

阅读本书不需要成为 TypeScript 专家，但以下基础知识会帮助你更好地理解：

```mermaid
graph LR
    A[JavaScript 基础] --> B[TypeScript 类型]
    A --> C[React 组件概念]
    B --> D[读懂源码]
    C --> D
    E[命令行使用] --> D
    F[Git 基础] --> D

    style D fill:#7c4dff,stroke:#7c4dff,color:#fff
```

**第2章**会为你补充必要的背景知识，即使你目前只熟悉其中一两项也没关系。
