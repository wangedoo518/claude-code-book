# 第23章：沙箱与拦截：操作系统级别的保护

> **所属**：第五编 · 安全防线
>
> **关键源码**：src/utils/hooks/, sandbox modules

---

## 生活类比

化学实验室的生物安全柜——即使你操作失误，危险物质也被隔离在柜子里不会泄漏到外面。应用层的安全检查就像实验员自己的操作规范，而沙箱就像安全柜——即使规范全部失效，物理隔离仍然保护你。

## 这一章要回答的问题

**应用层检查不够，操作系统还能做什么？**

25道安全关卡全部运行在应用层——如果应用本身被绕过了呢？操作系统级别的沙箱提供了最后一道物理防线：即使攻击者控制了Claude Code进程，沙箱仍能限制它的能力范围。这就是"纵深防御"中最深的那一层。

---

## 23.1 沙箱机制

### macOS sandbox-exec
- macOS提供sandbox-exec命令，可以用配置文件限制进程行为
- Claude Code使用沙箱限制子进程的文件系统访问——只能读写工作目录
- 网络访问也可以被限制——防止命令向外部发送敏感数据

### Linux namespace
- Linux的namespace机制提供进程级别的资源隔离
- PID namespace让子进程看不到宿主机的其他进程
- Mount namespace限制文件系统挂载点，防止访问宿主机目录
- Network namespace可以完全隔离网络——子进程无法联网

### Docker协作
- 当Claude Code在Docker容器内运行时，容器本身就是一层沙箱
- 容器的文件系统隔离、网络隔离、资源限制天然提供安全保障
- Claude Code检测Docker环境后会调整自身的安全策略——部分检查可以放松

## 23.2 Hook拦截链

### PreToolUse Hook
- 在任何工具执行前触发——可以审查参数、修改参数或阻止执行
- 返回值决定操作命运：approve放行、deny拒绝、modify修改后放行
- 企业可以注册自定义的PreToolUse Hook实现公司级安全策略

### PostToolUse Hook
- 在工具执行完成后触发——可以审计执行结果、记录日志
- 可以检测异常结果——比如命令输出中是否包含敏感信息
- PostToolUse Hook不能撤销已执行的操作，但可以触发告警

### 配置方式
- Hook在settings.json中配置——支持项目级和全局级
- 每个Hook是一个可执行命令——Claude Code调用它并传入工具调用信息
- Hook命令的退出码决定允许或拒绝，stdout可以包含修改后的参数

## 23.3 策略回退

### 拒绝追踪
- 系统记录每次工具调用被拒绝的情况——包括被谁拒绝、什么原因
- 拒绝记录帮助AI"学习"当前会话的安全边界
- 反复尝试被拒绝的操作会触发更严格的限制

### 连续拒绝降级
- 当同类操作被连续拒绝超过阈值，AI的行为模式自动降级
- 降级意味着AI转向更保守的策略——给建议而非直接操作
- 这防止AI陷入"尝试→拒绝→换种方式尝试→再拒绝"的循环

### Hook失败处理
- 如果Hook命令本身执行失败（崩溃、超时），默认策略是deny
- "失败即拒绝"而非"失败即放行"——安全默认值
- Hook的超时时间有限制，防止Hook成为性能瓶颈

---

## 深水区（架构师选读）

macOS sandbox-exec vs Linux namespace的安全模型对比与防御深度分析。两种机制的设计哲学不同：sandbox-exec基于"profile"模式，用声明式规则描述进程可以做什么；Linux namespace基于"隔离"模式，让进程认为自己在独立的系统中。sandbox-exec的粒度更细——可以精确到允许读取哪些路径、允许哪些系统调用；namespace的隔离更彻底——进程完全看不到宿主机的资源。在实际防御深度上，sandbox-exec更适合细粒度的权限控制（允许读/etc/hosts但禁止写），namespace更适合粗粒度的完全隔离（看不到/etc）。Claude Code根据平台选择合适的机制，并尽量利用两者的优势。

---

## 本章小结

> **一句话**：沙箱是应用层安全的最后保险——macOS sandbox-exec和Linux namespace在操作系统层面限制进程能力，Hook拦截链让安全策略可扩展可定制，策略回退确保安全失败时的正确降级。

### 关键源码索引

| 文件 | 职责 | 可信度 |
|------|------|--------|
| src/utils/sandbox.ts | 沙箱配置与初始化 | B |
| src/utils/hooks/preToolUse.ts | 工具执行前Hook | A |
| src/utils/hooks/postToolUse.ts | 工具执行后Hook | A |
| src/utils/hooks/config.ts | Hook配置加载 | A |

### 逆向提醒

- ✅ RELIABLE: Hook拦截链的触发时机和配置方式
- ⚠️ CAUTION: 沙箱profile的具体规则可能因系统版本而异
- ❌ SHIM/STUB: Linux namespace的完整实现可能在容器环境中有差异
