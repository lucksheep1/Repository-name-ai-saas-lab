# Feature Request: TTL + Encryption Support

## Status: Planned for v3.1

## Background
Based on LangChain community feedback, users need:

1. **TTL Support** - Automatic data expiration
2. **Encrypted Storage** - Sensitive data protection

## Requirements

### TTL (Time-To-Live)
- Add `ttl` parameter to Memory configuration
- Support automatic data expiration
- Configurable per-memory or global TTL

### Encryption
- Add encrypted storage backend
- Support Fernet/AES encryption
- Protect sensitive API keys and credentials

## Use Cases
- Short-term session data needs automatic cleanup
- Sensitive API keys need encrypted storage

## Priority
- High: TTL Support (most requested)
- Medium: Encryption Support

---
*Created by AI SaaS Lab - 2026-03-20*
