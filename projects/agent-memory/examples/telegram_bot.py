#!/usr/bin/env python3
"""
Agent Memory - Telegram Bot Example
===================================
Use agent-memory with a Telegram bot for persistent conversation memory.

Requirements:
    pip install python-telegram-bot

Usage:
    python telegram_bot.py
    # Start a chat with your bot
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory

# Check for telegram
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False
    print("⚠️ python-telegram-bot not installed. Install with: pip install python-telegram-bot")
    print("Running in demo mode...")


# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN_HERE")
MEMORY_PATH = "./telegram_memory.db"
MAX_CONTEXT_LENGTH = 1000


def create_memory():
    """Create memory instance with SQLite backend."""
    return Memory(storage="sqlite", path=MEMORY_PATH, ttl_days=30)


if HAS_TELEGRAM:
    # Telegram bot setup
    memory = create_memory()
    
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "🤖 Hi! I'm your memory bot.\n\n"
            "I'll remember things you tell me!\n"
            "Commands:\n"
            "/remember <text> - Save something to memory\n"
            "/recall <query> - Search memories\n"
            "/history - Recent memories\n"
            "/export - Export all memories"
        )
    
    async def remember_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remember command."""
        user = update.effective_user
        text = " ".join(context.args)
        
        if not text:
            await update.message.reply_text("Usage: /remember <text to remember>")
            return
        
        memory.add(
            f"User {user.name}: {text}",
            metadata={"role": "user", "user_id": user.id}
        )
        
        await update.message.reply_text(f"✅ Remembered: {text}")
    
    async def recall_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /recall command."""
        query = " ".join(context.args)
        
        if not query:
            await update.message.reply_text("Usage: /recall <search query>")
            return
        
        results = memory.search(query)
        
        if results:
            response = "Found:\n\n" + "\n".join([
                f"• {r['text'][:100]}" for r in results[:5]
            ])
        else:
            response = "Nothing found 😕"
        
        await update.message.reply_text(response)
    
    async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command."""
        recent = memory.get_recent(limit=10)
        
        if recent:
            response = "Recent memories:\n\n" + "\n".join([
                f"• {r['text'][:100]}" for r in recent
            ])
        else:
            response = "No memories yet!"
        
        await update.message.reply_text(response)
    
    async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /export command."""
        export_path = f"/tmp/telegram_export_{update.effective_user.id}.json"
        memory.export(export_path)
        
        await update.message.reply_text("📦 Here's your memory export:")
        await update.message.reply_document(document=open(export_path, "rb"))
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages."""
        user = update.effective_user
        text = update.message.text
        
        # Save user message
        memory.add(
            f"User {user.name}: {text}",
            metadata={"role": "user", "user_id": user.id}
        )
        
        # Check if mentioned or replied to bot
        if update.message.reply_to_message:
            if update.message.reply_to_message.from_user.is_bot:
                # Get context
                context_text = memory.get_context(max_tokens=MAX_CONTEXT_LENGTH)
                
                # Simple response
                response = f"I remember: {context_text[:300]}..."
                
                await update.message.reply_text(response)
                
                # Save bot response
                memory.add(
                    f"Bot: {response}",
                    metadata={"role": "bot"}
                )
    
    def run():
        """Run the Telegram bot."""
        import asyncio
        
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("remember", remember_command))
        app.add_handler(CommandHandler("recall", recall_command))
        app.add_handler(CommandHandler("history", history_command))
        app.add_handler(CommandHandler("export", export_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Starting Telegram bot...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)


# Demo mode without Telegram
if __name__ == "__main__":
    if HAS_TELEGRAM and TELEGRAM_BOT_TOKEN != "YOUR_TOKEN_HERE":
        run()
    else:
        # Demo mode
        print("\n" + "=" * 50)
        print("📱 Telegram Bot Demo (without Telegram)")
        print("=" * 50)
        
        memory = create_memory()
        
        # Simulate conversation
        print("\n1. Simulating Telegram conversation...")
        memory.add("User Alice: Remind me to call mom", metadata={"role": "user"})
        memory.add("Bot: ✅ I'll remind you!", metadata={"role": "bot"})
        memory.add("User Alice: It's about her birthday", metadata={"role": "user"})
        memory.add("User Bob: What's the weather?", metadata={"role": "user"})
        
        # Test commands
        print("\n2. Testing /recall command...")
        results = memory.search("mom")
        print(f"   Search 'mom': {len(results)} results")
        
        print("\n3. Testing /history command...")
        recent = memory.get_recent(limit=5)
        print(f"   Recent: {len(recent)} memories")
        
        # Get context
        print("\n4. Getting context...")
        context = memory.get_context(max_tokens=500)
        print(f"   Context: {context[:200]}...")
        
        print("\n" + "=" * 50)
        print("✅ Telegram bot example complete!")
        print("=" * 50)
        print("\nTo run real bot:")
        print("  1. Get bot token from @BotFather on Telegram")
        print("  2. Set token: export TELEGRAM_BOT_TOKEN='...'")
        print("  3. Run: python telegram_bot.py")
