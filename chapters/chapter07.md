# 第7章：程序的"记忆"：状态管理的艺术

> **所属**：第二编 · 程序是怎么启动的
>
> **关键源码**：src/state/store.ts, src/state/AppState.tsx, src/state/AppStateStore.tsx

---

## 生活类比

你的大脑有一个"工作记忆"——正在想的事情、刚看到的画面。容量有限，但随时可用。程序也需要这样一个"工作台"来放当前状态。

## 这一章要回答的问题

**Redux太重、全局变量太乱——Claude Code用什么管状态？为什么自己写？**

状态管理是前端开发的核心难题之一。Redux功能强大但模板代码多，全局变量简单但无法追踪变化。Claude Code选择了第三条路——自己实现一个轻量级的Zustand-like状态库。这个选择背后的思考，值得每个工程师学习。

---

## 7.1 createStore设计

### Zustand-like但更轻
- Claude Code没有用任何第三方状态管理库——自己写了一个
- 核心思想与Zustand相同：一个store就是一个可订阅的状态容器
- 但去掉了middleware、devtools等"大型项目"功能，只保留最核心的部分

### subscribe：监听变化
- 组件通过subscribe注册回调，状态变化时自动通知
- 支持selector：只关心状态的一部分，减少不必要的更新通知

### getState/setState：读写分离
- getState返回当前状态的快照——只读的，不能直接修改
- setState接受一个更新函数，返回新状态——旧状态不变，新状态替代
- 三个API就够了：subscribe、getState、setState——简洁到极致

## 7.2 DeepImmutable：不可变的艺术

### 状态一旦创建就不能改
- `DeepImmutable<T>`将对象的所有属性递归设为readonly
- 不只是第一层——嵌套对象、数组元素、Map的值都不可变

### 只能创建新的
- 要更新状态？不能改旧的，只能创建一个新对象
- `setState(old => ({ ...old, count: old.count + 1 }))` 是唯一的方式

### 并发安全与类型保护
- 不可变状态天然线程安全——没有人能在你读取时偷偷改掉它
- TypeScript编译器会阻止任何试图修改readonly属性的代码
- Bug在编译时就被发现，而不是在运行时随机崩溃

## 7.3 87个Hooks与Context

### useCanUseTool / useToolPermission
- 每个Hook封装了一个特定的状态查询逻辑
- `useCanUseTool`检查某个工具是否在当前上下文中可用
- `useToolPermission`查询用户是否授予了特定工具的执行权限

### Context拆分
- 不是一个巨大的Context包含所有状态
- 按职责拆分：AppStateContext、ToolContext、ThemeContext等
- 每个Context只包含相关状态，减少不必要的组件重渲染

### 性能优化
- Selector模式：组件只订阅自己需要的状态片段
- 浅比较：只有selector返回值真正变化时才触发重渲染
- 87个Hooks看似多，但每个都精确控制了自己的更新边界

---

## 深水区（架构师选读）

React的渲染优化核心在于"避免不必要的重渲染"。Claude Code的Selector模式与React.memo配合，实现了精确的更新控制。当store状态变化时，每个组件的selector被调用——如果返回值与上次相同（浅比较），组件就不会重渲染。这在终端UI中尤其重要：终端的刷新率有限，频繁重渲染不仅浪费CPU，还会导致可见的闪烁。理解这种"最小化渲染"的设计思想，对任何React项目都有借鉴意义。

---

## 本章小结

> **一句话**：Claude Code用自研的createStore实现轻量级状态管理，DeepImmutable保证不可变性，87个Hooks和Context拆分提供精确的状态订阅与更新控制。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/state/store.ts | createStore核心实现 | A |
| src/state/AppState.tsx | 应用状态定义 | A |
| src/state/AppStateStore.tsx | 应用状态Store | A |
| src/hooks/ | 87个自定义Hooks | A |

### 逆向提醒

- ✅ RELIABLE: createStore的API设计和DeepImmutable类型定义
- ⚠️ CAUTION: 具体的Hook数量（87个）基于Source Map统计，可能随版本增减
- ❌ SHIM/STUB: 部分Context Provider的初始值可能被OpenClaudeCode简化
