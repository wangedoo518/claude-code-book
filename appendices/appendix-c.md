# 附录C：88 个命令速查手册

> 每个斜杠命令的名称、功能说明、参数、可见性速查

---

## 会话管理

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /resume | 恢复历史会话 | 公开 |
| /session | 会话管理 | 公开 |
| /teleport | 跳转到特定会话状态 | 公开 |
| /remote-env | 远程环境连接 | 公开 |
| /compact | 手动压缩上下文 | 公开 |
| /clear | 清除会话 | 公开 |
| /context | 查看当前上下文 | 公开 |

## 代码操作

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /commit | Git 提交 | 公开 |
| /branch | 分支管理 | 公开 |
| /diff | 查看变更差异 | 公开 |
| /files | 列出相关文件 | 公开 |
| /rename | 重命名操作 | 公开 |
| /review | 代码审查 | 公开 |

## 配置管理

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /config | 配置管理 | 公开 |
| /keybindings | 快捷键配置 | 公开 |
| /theme | 主题切换 | 公开 |
| /permissions | 权限管理 | 公开 |
| /model | 模型选择 | 公开 |

## 智能体与任务

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /agents | 智能体管理 | 公开 |
| /tasks | 任务管理 | 公开 |
| /skills | 技能管理 | 公开 |
| /plugin | 插件管理 | 公开 |
| /install | 安装插件/扩展 | 公开 |
| /plan | 进入计划模式 | 公开 |

## 工具与调试

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /help | 帮助信息 | 公开 |
| /doctor | 健康检查 | 公开 |
| /cost | 成本统计 | 公开 |
| /usage | 使用统计 | 公开 |
| /memory | 记忆管理 | 公开 |
| /summary | 会话摘要 | 公开 |
| /context-viz | 上下文可视化 | 公开 |
| /insights | 项目洞察 | 公开 |

## 认证授权

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /login | 登录 | 公开 |
| /logout | 登出 | 公开 |
| /install-github-app | 安装 GitHub App | 公开 |
| /install-slack-app | 安装 Slack App | 公开 |
| /add-dir | 添加工作目录 | 公开 |

## 高级功能

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /voice | 语音模式 | Feature Gated |
| /bridge | Bridge 连接 | Feature Gated |
| /proactive | 主动模式 | Feature Gated |
| /fast | 快速模式切换 | 公开 |

## 隐藏命令

| 命令 | 功能 | 可见性 |
|------|------|--------|
| /buddy | 虚拟宠物 | 隐藏 |
| /agent-platform | 智能体平台 | ant-only |
| /context-viz | 上下文可视化 | 隐藏 |
| /daemon | 守护进程管理 | 隐藏 |
| /export | 会话导出 | 隐藏 |
| /feedback | 反馈 | 隐藏 |
| /trust | 信任设置 | 隐藏 |

---

*注：Feature Gated = 需要特定 Feature Flag 启用；ant-only = 仅 Anthropic 内部可用*
*完整列表基于 commands.ts 注册表，部分命令在不同版本中可能变化*
