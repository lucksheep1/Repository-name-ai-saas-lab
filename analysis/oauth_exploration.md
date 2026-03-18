# OAuth 认证探索

## 当前可用的认证

### GitHub
- PAT: 部分可用 (read:user, repo issues) ✓
- 权限不足: write:gist, repo, admin

## 需要认证的平台

### Reddit
- 认证方式: OAuth 2.0
- 需要: client_id, client_secret, redirect_uri
- 参考: https://www.reddit.com/dev/api

### Dev.to  
- 认证方式: API key
- 需要: 注册获取 API key
- 参考: https://developers.forem.com

### Hacker News
- 认证方式: 无 (只能手动)
- 限制: 无法 API 发布

## 下一步建议

1. 尝试注册 Reddit 开发者账号
2. 尝试注册 Dev.to API key
3. 或者接受现有约束，转向其他策略
