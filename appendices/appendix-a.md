# 附录A：逆向方法与证据分级

> 本书所有分析的方法论基础

---

## A.1 Source Map V3 规范

| 字段 | 含义 | 还原价值 |
|------|------|----------|
| version | 版本号(3) | 确认规范版本 |
| sources | 原始文件路径数组 | 还原目录结构 |
| sourcesContent | 原始文件内容数组 | 还原完整源码 |
| mappings | VLQ 编码的位置映射 | 行列对应关系 |
| names | 标识符名称数组 | 变量/函数名还原 |

## A.2 VLQ 编码与映射重建

- Base64 VLQ 的编解码流程
- 从编译产物行列 → 原始文件行列的映射
- 1,884 个文件路径的批量还原脚本

## A.3 可信度三级分级标准

| 等级 | 标记 | 定义 | 判定方法 |
|------|------|------|----------|
| **A级：确认原始** | ✅ | 两套代码库一致，且无 shim 标记 | sourcemap ∩ OpenClaudeCode 交集 |
| **B级：高度可信** | ⚠️ | 仅一套有，但代码风格一致无补全痕迹 | 风格分析 + 无 TODO/FIXME/shim 标记 |
| **C级：补全/推测** | ❌ | 明确标记为 shim/stub/fallback | shims/ 目录 或 空函数体 |

## A.4 七个已知 Shim 模块

| Shim | 原始功能 | 补全方式 |
|------|----------|----------|
| ant-computer-use-mcp | Computer Use 集成 | 功能降级 stub |
| ant-computer-use-swift | macOS 截图/TCC | 空实现 |
| ant-computer-use-input | 输入处理 | 空实现 |
| ant-claude-for-chrome-mcp | Chrome 扩展 | 功能降级 |
| color-diff-napi | 原生颜色差异 | JS 回退 |
| modifiers-napi | 键盘修饰键 | JS 回退 |
| url-handler-napi | URL 协议处理 | JS 回退 |
