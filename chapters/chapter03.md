# 第3章：双生代码库：我们到底在看什么

> **所属**：第一编 · 欢迎来到源码的世界
>
> **关键源码**：cli.js.map (59.8MB), sourcemap root, OpenClaudeCode root

---

## 生活类比

考古学家挖出一座古城，发现了两份拼图。一份是原始碎片直接粘回去的（sourcemap），另一份是有人补上缺失部分后重建的（OpenClaudeCode）。两份都有价值，但要分清哪些是原始的、哪些是后来补的。

## 这一章要回答的问题

**一份59.8MB的文件泄露了整个源码——但"看到的"都可信吗？**

源码逆向不像正常阅读开源项目——你看到的每一行代码都需要评估其可信度。理解两套代码库的来源和差异，是后续所有分析的基础。没有这个判断力，你可能会把补全代码当成原始设计来学习。

---

## 3.1 Source Map泄露事件

### npm包中的意外
- Claude Code作为npm包发布时，cli.js.map被意外包含在内
- 这个59.8MB的Source Map文件包含了几乎完整的源码信息

### Source Map V3格式
- Source Map是浏览器调试的标准技术，用于将压缩代码映射回原始源码
- V3版本使用VLQ编码压缩映射数据，`sourcesContent`字段直接嵌入源文件内容

### 1884个文件的还原
- 通过解析Source Map的`sources`和`sourcesContent`字段，可还原出1884个原始文件
- 文件路径、目录结构、甚至注释都被完整保留——这就是本书的主要分析对象

## 3.2 两套代码库的关系

### sourcemap还原层：1884个文件
- 直接从cli.js.map中提取，每个文件都有明确的原始路径
- 这是最可信的数据源——未经第三方修改的原始代码

### OpenClaudeCode补全层：1989个文件
- 社区项目OpenClaudeCode在sourcemap基础上增加了105个文件
- 补全了类型声明、缺失的接口定义和部分stub实现

### 7个shim文件
- OpenClaudeCode引入了7个shim文件来填补运行时缺失
- 这些shim是社区推测实现，不是Anthropic的原始代码
- 例如：某些内部API的模拟实现、缺失模块的替代品

## 3.3 可信度分级

### A级：确认原始
- 直接从Source Map的sourcesContent中提取的文件
- 与cli.js中的实际执行代码有映射关系可验证
- 本书分析的核心依据

### B级：高度可信
- 路径存在于Source Map中但sourcesContent为空的文件
- 通过上下文和依赖关系可以推断其内容的合理性

### C级：补全推测
- OpenClaudeCode独有的文件，不在原始Source Map中
- 可能是正确的补全，也可能与真实实现有偏差
- 本书会明确标注，避免误导读者

---

## 深水区（架构师选读）

Source Map V3的核心是`mappings`字段——一串用分号和逗号分隔的VLQ编码字符串。每个分号代表生成文件的一行，每个逗号分隔的段(segment)包含4-5个VLQ编码数字：生成列、源文件索引、源行、源列、可选的名称索引。VLQ(Variable-Length Quantity)编码将整数压缩为Base64字符，使得59.8MB的映射数据能高效存储1884个文件的完整位置信息。理解这个格式，就能写出自己的Source Map解析器。

---

## 本章小结

> **一句话**：Claude Code的源码来自Source Map泄露（1884文件）和社区补全（OpenClaudeCode），读源码时必须区分A/B/C三级可信度。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| cli.js.map | 59.8MB Source Map文件 | A |
| sourcemap root (1884 files) | 原始还原代码 | A |
| OpenClaudeCode root (1989 files) | 社区补全代码 | B/C |
| 7 shim files | 运行时填补 | C |

### 逆向提醒

- ✅ RELIABLE: sourcesContent中直接提取的1884个文件内容
- ⚠️ CAUTION: OpenClaudeCode新增的105个文件需要交叉验证
- ❌ SHIM/STUB: 7个shim文件为社区推测实现，可能与真实代码不同
