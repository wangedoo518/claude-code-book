---
tags:
  - 附录
  - 命令
---

# 附录C：88 个命令速查手册

本地可见的命令目录统计为 **87 个**，再加上运行时合并进来的动态命令、技能命令或隐藏入口，构成了书中所说的“88 个命令级入口”。

---

## C.1 命令分组思路

| 类别 | 示例 |
|---|---|
| 环境与登录 | `login` `logout` `oauth-refresh` `privacy-settings` |
| 项目与上下文 | `add-dir` `context` `memory` `model` `config` |
| 任务与协作 | `plan` `tasks` `review` `share` `plugin` `skills` |
| 系统与诊断 | `doctor` `heapdump` `stats` `usage` `debug-tool-call` |
| 隐藏与实验 | `ctx_viz` `break-cache` `voice` `desktop` `mobile` |

---

## C.2 目录级命令清单

```text
add-dir
agents
agents-platform
ant-trace
autofix-pr
backfill-sessions
branch
break-cache
bridge
btw
bughunter
chrome
clear
color
compact
config
context
copy
cost
ctx_viz
debug-tool-call
desktop
diff
doctor
effort
env
exit
export
extra-usage
fast
feedback
files
good-claude
heapdump
help
hooks
ide
install-github-app
install-slack-app
issue
keybindings
login
logout
mcp
memory
mobile
mock-limits
model
oauth-refresh
onboarding
output-style
passes
perf-issue
permissions
plan
plugin
pr_comments
privacy-settings
rate-limit-options
release-notes
reload-plugins
remote-env
remote-setup
rename
reset-limits
resume
review
rewind
sandbox-toggle
session
share
skills
stats
status
stickers
summary
tag
tasks
teleport
terminalSetup
theme
thinkback
thinkback-play
upgrade
usage
vim
voice
```

---

## C.3 命令系统阅读入口

| 想看什么 | 入口文件 |
|---|---|
| 命令合并总入口 | `src/commands.ts` |
| 某个命令实现 | `src/commands/<name>/` |
| 技能命令如何进来 | `src/skills/loadSkillsDir.ts` |
| MCP 命令如何进来 | `src/commands.ts` 中 `getMcpSkillCommands` |

---

## C.4 使用这一附录的方法

- 想找某个 `/命令` 背后的目录，就先在上面按名字定位。
- 若目录有但界面没出现，优先检查 gate、可见性过滤和当前模式。
- 若命令来自技能或 MCP，可能不会在静态目录列表里占一席之地。

!!! success "附录C结论"
    Claude Code 的命令系统不是固定菜单，而是“内置命令 + 技能命令 + 插件命令 + MCP 命令”的合并空间。目录列表只是静态入口，真正运行时的命令空间会更动态。
