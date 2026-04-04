# 第24章：配置与认证：谁能用、怎么管

> **所属**：第五编 · 安全防线
>
> **关键源码**：src/utils/config.ts, src/utils/settings/, src/services/oauth/, src/utils/auth.ts

---

## 生活类比

公司的门禁系统：员工卡（OAuth）→刷卡机（keychain）→权限分级（settings）→管理员后台（MDM）。门禁系统不只是"能不能进门"这么简单——它管理谁是谁、谁能去哪、配置从哪来、出了事怎么查。Claude Code的配置与认证系统就是这样一套企业级门禁。

## 这一章要回答的问题

**配置散在5个地方、认证散在3个协议——怎么管？**

全局配置、项目配置、命令行参数、MDM策略、Feature Flag——配置来源太多，优先级怎么定？OAuth、keychain、JWT——认证协议太多，怎么串联？这一章理清这两团"麻线"，让你看到背后的统一逻辑。

---

## 24.1 Settings分层

### 五层配置源
- 全局级：`~/.claude/settings.json`，对所有项目生效
- 项目级：`.claude/settings.json`，只对当前项目生效
- 命令行参数：启动时通过flag覆盖特定配置
- Managed settings：企业管理员通过MDM推送的强制配置
- Feature Flag：GrowthBook等平台下发的运行时配置

### MDM企业管理
- 大型企业需要统一管理所有开发者的Claude Code配置
- MDM（Mobile Device Management）可以推送配置文件到每台机器
- MDM配置优先级最高——即使开发者本地修改了settings.json，MDM配置也会覆盖

### 合并算法
- 从低优先级到高优先级依次叠加：全局→项目→命令行→MDM
- 同名配置高优先级覆盖低优先级，不同名配置合并保留
- 数组类型配置（如权限规则列表）通过concat合并而非替换

## 24.2 Migrations与GrowthBook

### 版本间配置迁移
- 不同版本的Claude Code配置格式可能变化——字段重命名、结构调整
- Migration系统在启动时检查配置版本号，自动执行迁移脚本
- 迁移是幂等的——多次执行结果相同，不会重复处理

### Feature Flag运行时
- GrowthBook SDK在Claude Code启动时拉取最新的Feature Flag配置
- Flag控制功能开关：新工具是否启用、新UI是否展示、实验性功能是否开放
- Flag还用于灰度发布——按用户ID或组织维度逐步放量

### 灰度发布实践
- 新功能先对1%用户开放，观察错误率和用户反馈
- 如果一切正常，逐步提升到10%、50%、100%
- 出现问题可以秒级回滚——修改Flag值即刻生效，不需要发版

## 24.3 认证串联

### OAuth PKCE流程
- 用户首次使用Claude Code时通过OAuth PKCE流程认证
- PKCE防止授权码被拦截——没有client secret在客户端暴露
- 认证成功后获取access token和refresh token

### Keychain预取
- 认证令牌存储在操作系统的keychain中（macOS Keychain/Linux Secret Service）
- 启动时自动从keychain预取令牌，实现免登录体验
- 令牌过期时自动使用refresh token刷新，对用户完全透明

### Bridge JWT与MCP鉴权
- IDE桥接场景使用JWT令牌——IDE扩展和Claude Code CLI之间的身份互认
- MCP服务器可能有自己的认证要求——MCPTool代理这些认证流程
- 认证信息不在日志中明文出现——安全审计的基本要求

---

## 深水区（架构师选读）

企业级安全特性——MDM集成、远程策略推送、审计日志、合规检查的实现路径。大型企业在采用AI编程工具时面临独特的合规挑战：代码是否可能泄露到外部？AI的操作是否可审计？安全策略能否统一管理？Claude Code通过MDM集成实现策略的集中管理——安全团队可以限制AI能访问的文件类型、能执行的命令类别、能连接的MCP服务器。审计日志记录每次工具调用的完整上下文——谁在什么时间让AI执行了什么操作。合规检查可以在PreToolUse Hook中实现——每次操作前检查是否符合公司的安全政策。这些特性让Claude Code从个人工具升级为企业级平台。

---

## 本章小结

> **一句话**：五层配置源通过优先级合并形成最终配置，三种认证协议通过串联实现无缝体验——配置管理和身份认证是Claude Code从个人工具走向企业平台的基础设施。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/utils/config.ts | 配置加载与合并 | A |
| src/utils/settings/index.ts | Settings分层管理 | A |
| src/services/oauth/oauthClient.ts | OAuth PKCE实现 | A |
| src/utils/auth.ts | 认证令牌管理 | A |

### 逆向提醒

- ✅ RELIABLE: Settings合并算法和OAuth认证流程
- ⚠️ CAUTION: MDM配置格式可能因企业部署方式不同而有差异
- ❌ SHIM/STUB: 企业审计日志接口在开源版中可能是空实现
