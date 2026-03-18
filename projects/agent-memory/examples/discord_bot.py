#!/usr/bin/env python3
"""
Agent Memory - Discord Bot Example
===================================
Use agent-memory with a Discord bot for persistent conversation memory.

Requirements:
    pip install discord.py

Usage:
    python discord_bot.py
    # Then mention the bot in a server
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory

# Check for discord.py
try:
    import discord
    from discord.ext import commands
    HAS_DISCORD = True
except ImportError:
    HAS_DISCORD = False
    print("⚠️ discord.py not installed. Install with: pip install discord.py")
    print("Running in demo mode...")
    HAS_DISCORD = False


# Configuration
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_TOKEN_HERE")
MEMORY_PATH = "./discord_memory.db"
MAX_CONTEXT_LENGTH = 1500


def create_memory():
    """Create memory instance with SQLite backend."""
    return Memory(storage="sqlite", path=MEMORY_PATH, ttl_days=30)


if HAS_DISCORD:
    # Discord bot setup
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    memory = create_memory()
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot logged in as {bot.user}")
        print(f"�_memory stored at: {MEMORY_PATH}")
    
    @bot.event
    async def on_message(message):
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Check if bot is mentioned
        if bot.user.mentioned_in(message):
            user_message = message.content.replace(f"<@!{bot.user.id}>", "").strip()
            
            # Save user message
            memory.add(
                f"User {message.author.name}: {user_message}",
                metadata={"role": "user", "channel": str(message.channel.id)}
            )
            
            # Get context for response
            context = memory.get_context(max_tokens=MAX_CONTEXT_LENGTH)
            
            # Simple response (replace with your LLM integration)
            response = f"Hello {message.author.name}! I remember: {context[:500]}"
            
            # Save bot response
            memory.add(
                f"Bot: {response}",
                metadata={"role": "bot"}
            )
            
            await message.reply(response[:2000])
        
        await bot.process_commands(message)
    
    @bot.command(name="remember")
    async def remember(ctx, *, text):
        """Save a memory with optional tags."""
        memory.add(
            f"{ctx.author.name}: {text}",
            metadata={"role": "user", "command": "remember"}
        )
        await ctx.reply(f"✅ Remembered: {text}")
    
    @bot.command(name="recall")
    async def recall(ctx, *, query):
        """Search memories."""
        results = memory.search(query)
        if results:
            await ctx.reply("Found:\n" + "\n".join([r["text"][:100] for r in results[:5]]))
        else:
            await ctx.reply("Nothing found.")
    
    @bot.command(name="history")
    async def history(ctx):
        """Get conversation history."""
        recent = memory.get_recent(limit=10)
        if recent:
            await ctx.reply("Recent:\n" + "\n".join([r["text"][:100] for r in recent]))
        else:
            await ctx.reply("No memories yet.")
    
    def run():
        """Run the bot."""
        print("Starting Discord bot with agent-memory...")
        bot.run(BOT_TOKEN)


# Demo mode without Discord
if __name__ == "__main__":
    if HAS_DISCORD:
        run()
    else:
        # Demo mode
        print("\n" + "=" * 50)
        print("🎭 Discord Bot Demo (without Discord)")
        print("=" * 50)
        
        memory = create_memory()
        
        # Simulate conversation
        print("\n1. Simulating conversation...")
        memory.add("User Alice: I love coding in Python", metadata={"role": "user"})
        memory.add("Bot: That's great Alice!", metadata={"role": "bot"})
        memory.add("User Bob: What's my name?", metadata={"role": "user"})
        memory.add("Bot: Your name is Bob!", metadata={"role": "bot"})
        memory.add("User Alice: My favorite color is blue", metadata={"role": "user"})
        
        # Test commands
        print("\n2. Testing !recall command...")
        results = memory.search("Python")
        print(f"   Search 'Python': {len(results)} results")
        
        print("\n3. Testing !history command...")
        recent = memory.get_recent(limit=5)
        print(f"   Recent memories: {len(recent)}")
        
        print("\n4. Testing !remember command...")
        memory.add("User: Important note", metadata={"role": "user", "command": "remember"})
        print("   Memory saved!")
        
        # Get full context
        print("\n5. Full context:")
        context = memory.get_context(max_tokens=500)
        print(context)
        
        print("\n" + "=" * 50)
        print("✅ Discord bot example complete!")
        print("=" * 50)
        print("\nTo run real bot:")
        print("  1. Install discord.py: pip install discord.py")
        print("  2. Set DISCORD_BOT_TOKEN env var")
        print("  3. Run: python discord_bot.py")
