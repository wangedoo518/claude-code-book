---
hide:
  - navigation
  - toc
---

<section class="cover-page">
  <div class="cover-shell">
    <div class="cover-art-panel">
      <div class="cover-art-ring"></div>
      <img
        class="cover-book-icon"
        src="assets/images/warwolf-book-icon.png"
        alt="Warwolf book icon"
      />
      <div class="cover-art-badge">WARWOLF EDITION</div>
    </div>

    <div class="cover-copy">
      <p class="cover-kicker">WARWOLF TEAM · OPEN SOURCE READING PROJECT</p>
      <h1>Claude Code 源码解析红宝书</h1>
      <p class="cover-subtitle">基于 v2.1.88 双生逆向源码的设计思想深度解析</p>

      <blockquote class="cover-slogan">
        开源、免费，只为培养下一代中国开源战狼
        <span>--- 来自 中国开源战狼团队</span>
      </blockquote>

      <div class="cover-metrics">
        <span>42 章正文</span>
        <span>5 个附录</span>
        <span>54 个工具</span>
        <span>88 个命令</span>
        <span>89 个 Feature Flag</span>
      </div>

      <div class="cover-actions">
        <a class="landing-button landing-button--primary" href="guide/">开始阅读</a>
        <a class="landing-button" href="https://github.com/wangedoo518/claude-code-book/releases/latest" target="_blank" rel="noopener">下载 PDF</a>
        <a class="landing-button" href="https://github.com/wangedoo518/claude-code-book/releases/latest" target="_blank" rel="noopener">下载 EPUB</a>
        <a class="landing-button" href="https://github.com/wangedoo518/claude-code-book" target="_blank" rel="noopener">源码</a>
      </div>

      <p class="cover-note">PDF / EPUB 将在 GitHub Releases 页面持续更新，源码入口直达仓库主页。</p>
    </div>
  </div>
</section>

<section class="community-page">
  <div class="community-shell">
    <div class="community-copy">
      <p class="community-kicker">第二页 / 一起聊下一代技术</p>
      <h2>一群热爱技术的小伙伴一起探讨下一个时代最新技术进展</h2>
      <p class="community-lead">
        从 Claude Code、AI Agent、MCP 与插件生态，到源码逆向、自动化工作流和工程实践，我们把“看懂”变成“能一起做出来”。
      </p>

      <div class="community-points">
        <div class="community-point">
          <strong>讨论方向</strong>
          <span>源码拆解、AI 工程化、开源协作、下一代工具链</span>
        </div>
        <div class="community-point">
          <strong>交流方式</strong>
          <span>问题互答、资料共享、项目实战、路线讨论</span>
        </div>
        <div class="community-point">
          <strong>适合谁</strong>
          <span>想认真理解 AI 编程助手的人，和愿意一起做开源的人</span>
        </div>
      </div>
    </div>

    <div class="community-poster">
      <img src="assets/images/community-group.jpg" alt="Claude Code 源码交流群二维码" />
      <p>扫码加入交流群。若二维码过期，我们会在仓库中更新最新版本。</p>
    </div>
  </div>
</section>

## 快速入口

<div class="quick-entry-grid">
  <a class="quick-entry-card" href="part1/">
    <span>01</span>
    <strong>欢迎来到源码的世界</strong>
    <em>先建立地图，再进入正文章节</em>
  </a>
  <a class="quick-entry-card" href="guide/">
    <span>GUIDE</span>
    <strong>三种读法与推荐路径</strong>
    <em>按你的背景选择最顺手的阅读路线</em>
  </a>
  <a class="quick-entry-card" href="appendices/">
    <span>APPX</span>
    <strong>附录与速查资料</strong>
    <em>工具、命令、Feature Flag 和证据分级</em>
  </a>
</div>

## 四条设计思想主线

<div class="idea-grid">
  <div class="idea-card">
    <h3>不是聊天壳</h3>
    <p>Claude Code 不是套了个壳的聊天应用，而是一个会调用工具的任务执行器。</p>
  </div>
  <div class="idea-card">
    <h3>核心铁三角</h3>
    <p>理解这套系统，关键是上下文装配、Agent Loop 和工具编排这三根主梁。</p>
  </div>
  <div class="idea-card">
    <h3>最难的是约束</h3>
    <p>真正的工程挑战不只是生成代码，而是权限、安全、压缩、恢复和一致性。</p>
  </div>
  <div class="idea-card">
    <h3>必须分清两套代码库</h3>
    <p>能跑起来不等于官方原始设计。阅读时要持续区分还原层和补全层。</p>
  </div>
</div>
