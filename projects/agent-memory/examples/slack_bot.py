#!/usr/bin/env python3
"""
Agent Memory - Slack Bot Example
=================================
Use agent-memory with a Slack bot for persistent conversation memory.

Requirements:
    pip install slack-sdk flask

Usage:
    python slack_bot.py
    # Set up Slack app with Event Subscriptions and Bot Token
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory

# Check for slack-sdk
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    HAS_SLACK = True
except ImportError:
    HAS_SLACK = False
    print("⚠️ slack-sdk not installed. Install with: pip install slack-sdk")
    print("Running in demo mode...")


# Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "xoxb-...")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "your_secret")
MEMORY_PATH = "./slack_memory.db"
MAX_CONTEXT_LENGTH = 1500


def create_memory():
    """Create memory instance with SQLite backend."""
    return Memory(storage="sqlite", path=MEMORY_PATH, ttl_days=30)


if HAS_SLACK:
    # Slack client setup
    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    memory = create_memory()
    
    def handle_message(event, client):
        """Handle incoming Slack message."""
        user = event.get("user")
        channel = event.get("channel")
        text = event.get("text", "")
        ts = event.get("ts")
        
        # Skip bot messages
        if not user or user.startswith("B"):
            return
        
        # Save user message
        memory.add(
            f"User {user}: {text}",
            metadata={"role": "user", "channel": channel, "ts": ts}
        )
        
        # Check for mentions
        if client.auth["user_id"] in text:
            # Get context
            context = memory.get_context(max_tokens=MAX_CONTEXT_LENGTH)
            
            # Simple response (replace with your LLM)
            response = f"I remember: {context[:500]}"
            
            # Post response
            try:
                client.chat_postMessage(
                    channel=channel,
                    thread_ts=ts,
                    text=response
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")
            
            # Save bot response
            memory.add(
                f"Bot: {response}",
                metadata={"role": "bot", "thread": ts}
            )
    
    def handle_command(command, ack, say):
        """Handle slash commands."""
        ack()
        
        if command == "/remember":
            # Already handled by middleware
            pass
        elif command == "/recall":
            say("Use /remember to save, I'll recall automatically!")
        elif command == "/history":
            recent = memory.get_recent(limit=10)
            if recent:
                say("Recent:\n" + "\n".join([r["text"][:100] for r in recent]))
            else:
                say("No memories yet.")
    
    def run():
        """Run the Slack bot (requires Flask for events)."""
        from flask import Flask, request, Response
        import hmac
        import hashlib
        
        app = Flask(__name__)
        
        @app.route("/slack/events", methods=["POST"])
        def slack_events():
            # Verify signature
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            signature = request.headers.get("X-Slack-Signature")
            
            # For demo, skip verification
            # In production, verify with hmac.compare_digest
            
            payload = request.get_data()
            event_data = request.get_json()
            
            # Handle URL verification
            if event_data.get("type") == "url_verification":
                return Response(event_data.get("challenge"), mimetype="text/plain")
            
            # Handle events
            if event_data.get("type") == "event_callback":
                event = event_data.get("event", {})
                if event.get("type") == "message":
                    handle_message(event, slack_client)
            
            return Response(), 200
        
        print("Starting Slack bot server...")
        app.run(host="0.0.0.0", port=3000)


# Demo mode without Slack
if __name__ == "__main__":
    if HAS_SLACK and SLACK_BOT_TOKEN != "xoxb-...":
        run()
    else:
        # Demo mode
        print("\n" + "=" * 50)
        print("💬 Slack Bot Demo (without Slack)")
        print("=" * 50)
        
        memory = create_memory()
        
        # Simulate conversation
        print("\n1. Simulating Slack conversation...")
        memory.add("User U123: Hey, can you remember my meeting at 3pm?", metadata={"role": "user", "channel": "C001"})
        memory.add("Bot: Sure! I'll remember your 3pm meeting.", metadata={"role": "bot"})
        memory.add("User U123: Thanks! It's with @alice about the project.", metadata={"role": "user", "channel": "C001"})
        memory.add("User U456: What's on my calendar?", metadata={"role": "user", "channel": "C002"})
        
        # Test search
        print("\n2. Testing search...")
        results = memory.search("meeting")
        print(f"   Search 'meeting': {len(results)} results")
        
        # Test context
        print("\n3. Getting context...")
        context = memory.get_context(max_tokens=500)
        print(f"   Context: {context[:200]}...")
        
        # Test timeline
        print("\n4. Getting timeline...")
        timeline = memory.get_timeline(limit=5)
        print(f"   Timeline entries: {len(timeline)}")
        
        print("\n" + "=" * 50)
        print("✅ Slack bot example complete!")
        print("=" * 50)
        print("\nTo run real bot:")
        print("  1. Create Slack app at api.slack.com")
        print("  2. Add Bot Token and Signing Secret to env:")
        print("     export SLACK_BOT_TOKEN='xoxb-...'")
        print("     export SLACK_SIGNING_SECRET='...'")
        print("  3. Enable Event Subscriptions")
        print("  4. Run: python slack_bot.py")
