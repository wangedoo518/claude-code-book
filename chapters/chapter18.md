# 第18章：搜索与上网：AI的眼睛

> **所属**：第四编 · AI的"双手"——工具系统
>
> **关键源码**：src/tools/GrepTool/, GlobTool/, WebSearchTool/, WebFetchTool/

---

## 生活类比

侦探的两件工具：放大镜（在已有证据中搜索）和情报网（从外界获取信息）。GrepTool和GlobTool是放大镜——在你项目的百万行代码中精准找到关键线索。WebSearch和WebFetch是情报网——到互联网上获取最新文档、API参考、错误解法。

## 这一章要回答的问题

**AI怎么在百万行代码中找bug？怎么查最新文档？**

搜索能力决定了AI的"视野"。内部搜索让AI理解你的代码库，外部搜索让AI突破知识截止日期的限制。没有搜索工具的AI是"近视"的——它只能看到上下文窗口里的内容。有了搜索，AI的视野从几千行扩展到整个项目甚至整个互联网。

---

## 18.1 GrepTool

### ripgrep封装
- GrepTool底层调用ripgrep（rg），不是Node.js原生的正则匹配
- ripgrep的速度是普通grep的数十倍——在大仓库中搜索毫秒级响应
- 封装层处理参数转换、输出格式化、错误处理

### 正则与多行
- 支持完整的正则表达式语法——`function\s+\w+`能匹配任意函数定义
- 多行模式（multiline）让模式可以跨越行边界——搜索跨行的代码结构
- 支持文件类型过滤（--type js）和glob模式过滤（*.tsx）

### 截断与限制
- 搜索结果默认限制前250条，防止海量结果撑爆上下文
- 支持offset分页——AI可以先看前250条，再看后面的
- 上下文行（-A/-B/-C参数）让AI看到匹配行周围的代码，理解语境

## 18.2 GlobTool

### 模式匹配
- GlobTool用文件名模式查找文件——`**/*.ts`找所有TypeScript文件
- 与GrepTool的区别：Glob找文件，Grep找内容
- 支持复杂模式如`src/**/*.{ts,tsx}`只在src目录下找TS和TSX文件

### 修改时间排序
- 搜索结果按修改时间排序——最近修改的文件排在前面
- 这对AI很有用：最近改过的文件往往与当前问题最相关
- AI可以先看最近修改的文件，快速定位问题

### 大仓库优化
- 自动忽略node_modules、.git等目录，避免搜索无关文件
- 尊重.gitignore规则——被版本控制忽略的文件也被搜索忽略
- 在百万文件的monorepo中依然保持快速响应

## 18.3 Web工具族

### WebSearch API
- WebSearch调用搜索API获取网页搜索结果
- 返回结果包含标题、摘要、URL——AI据此决定是否需要深入阅读
- 支持域名过滤：只搜特定网站，或排除特定网站

### WebFetch HTML转Markdown
- WebFetch获取网页内容，将HTML转换为Markdown格式
- 转换过程去除广告、导航栏等噪音，提取核心内容
- AI处理Markdown比HTML高效得多——结构清晰、token更少

### 15分钟缓存
- 同一URL在15分钟内的重复请求直接返回缓存结果
- 这避免了AI反复获取同一页面浪费时间和API调用
- 缓存是自清理的——过期自动失效，不需要手动管理

---

## 深水区（架构师选读）

ripgrep为什么快——Aho-Corasick算法、SIMD加速、与Node.js grep的性能差距。ripgrep的核心优势来自三个层面。算法层：使用Aho-Corasick自动机进行多模式匹配，一次遍历就能匹配多个模式。硬件层：利用SIMD（单指令多数据）指令集，一次CPU指令处理多个字节的比较。系统层：使用内存映射文件（mmap），避免了read系统调用的开销。相比之下，Node.js中用fs.readFile加正则匹配的方式在每个层面都慢一个数量级。在Claude Code的实际基准测试中，ripgrep搜索整个项目的速度比原生Node.js方案快50-100倍。

---

## 本章小结

> **一句话**：四个搜索工具让AI从"近视"变为"全视"——GrepTool用ripgrep在代码中闪电搜索，GlobTool按模式找文件，WebSearch和WebFetch让AI接入互联网获取实时信息。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/tools/GrepTool/GrepTool.ts | 代码内容搜索 | A |
| src/tools/GlobTool/GlobTool.ts | 文件模式匹配 | A |
| src/tools/WebSearchTool/WebSearchTool.ts | 网页搜索 | A |
| src/tools/WebFetchTool/WebFetchTool.ts | 网页内容获取 | A |

### 逆向提醒

- ✅ RELIABLE: GrepTool和GlobTool的参数接口和执行逻辑
- ⚠️ CAUTION: WebSearch的具体API提供方可能变化
- ❌ SHIM/STUB: WebFetch的HTML解析器细节可能随依赖更新变化
