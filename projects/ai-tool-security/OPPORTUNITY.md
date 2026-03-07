# Opportunity & Evidence

## 项目: AI Tool Security Scanner

### Evidence Quality: 9/10

### 可追溯来源 (3+)

1. **Clinejection 事件** (核心证据)
   - GitHub Issue Title 攻击 4000+ 台开发者机器
   - 来源: 安全事件披露 (2026-03)
   - 影响: npm postinstall 脚本恶意利用

2. **npm 安全问题**
   - 恶意 postinstall/preinstall 脚本检测
   - typosquatting, dependency confusion
   - 来源: npm 官方安全报告, Snyk, Socket.dev

3. **GitHub Actions 安全**
   - Cache poisoning (Attacking the cache: from SSRF to global RCE)
   - 权限过宽 (GITHUB_TOKEN, OIDC)
   - 外部 action 依赖风险
   - 来源: 先知社区, GitHub Security Lab

4. **AI Coding Tools 流行**
   - Cursor, Cline, GitHub Copilot 安全风险
   - Prompt injection via issues/PRs/comments
   - 来源: Product Hunt Trending, GitHub Trending

5. **Terraform/K8s 配置安全**
   - IaC 安全扫描需求上升
   - 来源: Open Policy Agent, Checkov issues
