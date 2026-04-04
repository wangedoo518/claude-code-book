# 附录E��sourcemap vs OpenClaudeCode 差异矩阵

> 逐模块对比两套逆向代码库的差异

---

## 差异总览

| 维度 | claude-code-sourcemap | OpenClaudeCode |
|------|----------------------|----------------|
| 文件总数 | 1,884 | 1,989 (+105) |
| 可运行性 | 不可直接运行 | 可通过 bun run dev 运行 |
| Shim 层 | 无 | 7 个原生模块 shim |
| Vendor 目录 | 无 | 有(4个原生源码) |
| 构建配置 | 无 | 完整 package.json + tsconfig |
| 技能内容 | 占位文件 | 真实内容还原 |
| 原生绑定 | 引用但不存在 | shim 替代 |

## 关键模块差异

| 模块 | sourcemap 状态 | OpenClaudeCode 状态 | 可信度 |
|------|---------------|--------------------|----|
| src/entrypoints/ | ✅ 完整 | ✅ 完整 + bootstrap 适配 | A |
| src/main.tsx | ✅ 完整 | ✅ 完整 | A |
| src/query.ts | ✅ 完整 | ✅ 完整 | A |
| src/QueryEngine.ts | ✅ 完整 | ✅ 完整 | A |
| src/Tool.ts | ✅ 完整 | ✅ 完整 | A |
| src/tools/ | ✅ 完整 | �� 完��� | A |
| src/commands/ | ��� 完��� | ✅ 完整 | A |
| src/services/api/ | ✅ 完整 | ✅ 完整 | A |
| src/services/mcp/ | ✅ 完整 | ✅ 完整 + auth 适配 | A |
| src/bridge/ | ✅ 完整 | ✅ 完整 | A |
| src/ink/ | ✅ 完整 | ✅ 完整 | A |
| src/state/ | ✅ 完整 | ✅ ���整 | A |
| src/coordinator/ | ✅ 完整 | ✅ 完整 | A |
| src/assistant/ | ✅ 完整 | ✅ 完整 | A |
| src/skills/bundled/ | ⚠️ 占位 | ✅ 内容还原 | B |
| src/voice/ | ✅ 完整 | ✅ 完整 | A |
| shims/ | 不存在 | ❌ 补全层 | C |
| vendor/ | 不存在 | ❌ 补全层 | C |
| 原生模块引用 | 引用存在 | shim 替代 | C |

## 差异产生的原因

1. **+105 文件**：主要来自 shims/(7) + vendor/(4) + 构建配置 + 技能内容还原
2. **Shim 层**：原生 Rust/Swift 模块无法从 Source Map 获取，OpenClaudeCode 用 JS/TS 回退
3. **技能内容**：Source Map 中技能文件为空占位，OpenClaudeCode 从其他渠道还原

## 阅读建议

- **理解架构设计**：优先参考 sourcemap（更接近原貌）
- **验证运行行为**：使用 OpenClaudeCode（可实际运行）
- **涉及 shim 模块**：明确标注为"补全层"，不代表官方实现
