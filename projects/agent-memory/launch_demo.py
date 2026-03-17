#!/usr/bin/env python3
"""
Agent Memory - One-Click Launch Demo
=====================================
Run this script to:
1. Check agent-memory installation
2. Run a live demo
3. Open feedback link in your browser

Usage: python3 launch_demo.py
"""

import sys
import os
import webbrowser
import subprocess

def main():
    print("=" * 60)
    print("⚡ Agent Memory - One-Click Launch")
    print("=" * 60)
    
    # Step 1: Check if agent-memory is available
    print("\n[1/3] Checking agent-memory installation...")
    try:
        import agent_memory
        print("✅ agent-memory is installed")
    except ImportError:
        print("❌ agent-memory not found")
        print("   Note: pip not available in this environment")
        print("   Install manually: pip install agent-memory")
    
    # Step 2: Run demo using local module
    print("\n[2/3] Running demo...")
    try:
        sys.path.insert(0, ".")
        from agent_memory import Memory
        
        demo_path = "/tmp/agent_memory_launch.json"
        if os.path.exists(demo_path):
            os.remove(demo_path)
        
        memory = Memory(storage="json", path=demo_path)
        memory.add("User prefers dark mode")
        memory.add("User is building AI agents")
        memory.add("User needs simple memory management")
        
        print("\n" + "="*50)
        print("CONTEXT FOR YOUR AGENT:")
        print("="*50)
        print(memory.get_context(max_tokens=500))
        print("="*50)
        print("✅ Demo ran successfully")
    except Exception as e:
        print(f"⚠️  Demo error: {e}")
    
    # Step 3: Show feedback link
    print("\n[3/3] Feedback Link:")
    feedback_url = "https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues"
    print(f"   {feedback_url}")
    
    print("\n" + "=" * 60)
    print("📢 FEEDBACK QUESTIONS:")
    print("=" * 60)
    print("1. Is LangChain memory too heavy for you?")
    print("2. Do you need agent memory right now?")
    print("3. Would you try a demo if it took 30 seconds?")
    print("=" * 60)
    print("\n🎉 Thanks for trying Agent Memory!")

if __name__ == "__main__":
    main()
