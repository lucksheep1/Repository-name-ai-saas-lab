#!/usr/bin/env python3
"""
Agent Memory - Summary
======================
Quick summary of all examples.

This file documents all the examples available in agent-memory.
"""

# Complete list of examples (50 total)

EXAMPLES = {
    # Core
    "quickstart_minimal.py": "Minimal 3-line demo",
    "demo_30s.py": "30-second demo",
    "quickstart.py": "Quick start guide",
    "integration_demo.py": "Complete integration demo",
    
    # Storage Backends
    "fts_demo.py": "Full-text search demo",
    
    # Advanced Features
    "langchain_example.py": "LangChain integration",
    "multi_agent_example.py": "Multi-agent sharing",
    "memory_mixer.py": "Combine multiple memory sources",
    "event_driver.py": "Event-driven memory",
    "cached_memory.py": "Cached memory layer",
    "plugin_system.py": "Plugin architecture",
    "priority_queue.py": "Priority queue semantics",
    "batch_ops.py": "Batch operations",
    "analytics.py": "Memory analytics",
    "compression.py": "Memory compression",
    "scheduler.py": "Scheduled cleanup",
    "notifications.py": "Notification system",
    "cloud_sync.py": "Cloud sync",
    "versioning.py": "Version control",
    "encryption.py": "Encryption",
    "multiuser.py": "Multi-user support",
    "tag_manager.py": "Advanced tag management",
    "triggers.py": "Automation triggers",
    "backup_manager.py": "Backup and restore",
    
    # API & Web
    "web_api.py": "FastAPI web server",
    "web_dashboard.py": "Web dashboard",
    "api_auth.py": "API with authentication",
    "mobile_api.py": "Mobile-optimized API",
    "graphql_api.py": "GraphQL API",
    "cli.py": "Command-line interface",
    "cli_interactive.py": "Interactive CLI",
    "rest_client.py": "REST client library",
    "webhook.py": "Webhook handler",
    "lambda_function.py": "AWS Lambda handler",
    
    # Bot Integrations
    "discord_bot.py": "Discord bot",
    "slack_bot.py": "Slack bot",
    "telegram_bot.py": "Telegram bot",
    
    # LLM Integrations
    "chatgpt_integration.py": "ChatGPT/GPT-4",
    "claude_integration.py": "Anthropic Claude",
    "azure_openai.py": "Azure OpenAI",
    "vertex_agent.py": "Google Vertex AI",
    "openai_assistant.py": "OpenAI Assistant",
    "langchain_adapter.py": "LangChain adapter",
    
    # Use Cases
    "logger.py": "Structured logging",
    "task_tracker.py": "Task tracking",
    "conversation.py": "Conversation context",
    "user_preferences.py": "User preferences",
    "knowledge_base.py": "Knowledge base",
    
    # Export/Import
    "export_formats.py": "Export to CSV/XML/HTML",
    
    # Docker
    "Dockerfile.api": "Docker container",
    "DOCKER.md": "Docker guide",
}

def print_summary():
    """Print summary."""
    print("=" * 60)
    print("🤖 Agent Memory - Examples Summary")
    print("=" * 60)
    print(f"\nTotal: {len(EXAMPLES)} examples\n")
    
    # Group by category
    categories = {
        "Core": ["quickstart_minimal.py", "demo_30s.py", "quickstart.py", "integration_demo.py"],
        "Storage": ["fts_demo.py"],
        "Advanced": ["langchain_example.py", "multi_agent_example.py", "memory_mixer.py", 
                    "event_driver.py", "cached_memory.py", "plugin_system.py", "priority_queue.py",
                    "batch_ops.py", "analytics.py", "compression.py", "scheduler.py",
                    "notifications.py", "cloud_sync.py", "versioning.py", "encryption.py",
                    "multiuser.py", "tag_manager.py", "triggers.py", "backup_manager.py"],
        "API & Web": ["web_api.py", "web_dashboard.py", "api_auth.py", "mobile_api.py",
                      "graphql_api.py", "cli.py", "cli_interactive.py", "rest_client.py",
                      "webhook.py", "lambda_function.py"],
        "Bots": ["discord_bot.py", "slack_bot.py", "telegram_bot.py"],
        "LLM": ["chatgpt_integration.py", "claude_integration.py", "azure_openai.py",
                "vertex_agent.py", "openai_assistant.py", "langchain_adapter.py"],
        "Use Cases": ["logger.py", "task_tracker.py", "conversation.py", 
                      "user_preferences.py", "knowledge_base.py"],
        "Export": ["export_formats.py"],
        "Docker": ["Dockerfile.api", "DOCKER.md"],
    }
    
    for cat, files in categories.items():
        print(f"\n{cat} ({len(files)}):")
        for f in files:
            desc = EXAMPLES.get(f, "")
            print(f"  - {f}: {desc}")


if __name__ == "__main__":
    print_summary()
