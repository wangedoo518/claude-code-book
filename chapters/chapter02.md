# 第2章：你需要知道的背景知识

> **所属**：第一编 · 欢迎来到源码的世界
>
> **关键源码**：package.json, tsconfig.json

---

## 生活类比

学开车之前，你至少要知道方向盘、油门、刹车在哪。读源码也一样——先认识几个核心"零件"就够了。

## 这一章要回答的问题

**TypeScript、React、CLI是什么？为什么Claude Code选这些技术？**

技术选型不是随意的。Claude Code选择TypeScript而非Python，选择React而非直接打印字符，选择Bun而非Node.js——每个选择都有工程上的理由。了解这些背景，才能看懂后面的源码。

---

## 2.1 TypeScript：带类型的JavaScript

### 为什么类型重要
- JavaScript是动态类型语言——变量可以随时变成任何类型，灵活但危险
- 在16万行的大项目中，没有类型就像在黑暗中走钢丝——你不知道哪一步会踩空

### 给大型项目的保护
- TypeScript在编译阶段就能发现类型错误，不用等到运行时崩溃
- 自动补全、跳转定义、重构——IDE的这些能力全靠类型信息驱动

### 简单示例
- `function add(a: number, b: number): number` 比 `function add(a, b)` 多了什么？多了确定性
- 当AI返回的JSON缺少字段时，TypeScript能在编译时告诉你，而不是在用户面前崩溃

## 2.2 React与Ink：终端里的"前端"

### 组件思维
- 把UI拆成独立、可复用的组件——按钮是组件、对话框是组件、消息列表也是组件
- 每个组件只关心自己的状态和渲染逻辑，互不干扰

### 声明式UI
- 告诉React"我要什么样子"，而不是"一步步怎么画"
- 状态变了→UI自动更新，不需要手动操作DOM（或终端字符）

### 为什么CLI也用React
- 终端UI同样需要布局、事件处理、状态管理——这些React都已经解决了
- Ink框架让React组件渲染到终端，`<Box>` 替代 `<div>`，`<Text>` 替代 `<span>`

## 2.3 Bun与CLI工具链

### Bun是什么
- Bun是一个JavaScript运行时，和Node.js做同样的事，但更快
- 它内置了打包器、测试运行器、包管理器——一个工具替代了整个工具链

### 为什么不用Node.js
- 启动速度：Bun的冷启动比Node.js快数倍，对CLI工具来说这是关键体验
- 打包能力：Bun能把整个项目打包成单个文件（cli.js），简化分发

### Zod校验的角色
- Zod是运行时类型校验库——TypeScript管编译时，Zod管运行时
- AI返回的JSON是否符合预期？用户输入的参数是否合法？都靠Zod来把关
- 在Claude Code中，每个工具的输入Schema都用Zod定义，同时生成JSON Schema给AI阅读

---

## 深水区（架构师选读）

TypeScript的类型体操在Claude Code中有不少高级应用。`DeepImmutable<T>`类型递归地将对象的所有层级设为只读——不只是第一层属性，而是嵌套对象、数组元素都不可变。泛型工具类型如`Tool<Input, Output, Progress>`在54个工具定义中保证了类型安全。这些高级类型不是炫技，而是在大型项目中防止整类Bug的工程手段。

---

## 本章小结

> **一句话**：TypeScript提供类型安全，React+Ink实现终端UI，Bun加速启动与打包，Zod守卫运行时——这四个"零件"是理解Claude Code源码的前置知识。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| package.json | 依赖声明与脚本 | A |
| tsconfig.json | TypeScript编译配置 | A |
| src/ink/ | 自研Ink框架 | A |
| src/types/ | 全局类型定义 | A |

### 逆向提醒

- ✅ RELIABLE: package.json中的依赖版本和脚本定义
- ⚠️ CAUTION: tsconfig.json的部分编译选项可能与发布配置不同
- ❌ SHIM/STUB: 无（本章为背景知识章节）
