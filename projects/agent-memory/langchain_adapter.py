#!/usr/bin/env python3
"""
LangChain Memory Adapter for agent-memory
==========================================
Use agent-memory as a drop-in replacement for LangChain memory.

Usage:
    from agent_memory import LangChainMemory
    
    memory = LangChainMemory(
        storage="sqlite",
        path="./memory.db",
        return_messages=True
    )
    
    # Use with LCEL
    chain = prompt | llm | StrOutputParser()
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        memory,
        input_messages_key="question",
        history_messages_key="chat_history"
    )

NOTE: Requires langchain-core. Install with: pip install langchain-core
"""

# Check if LangChain is available
try:
    from langchain_core.memory import BaseMemory
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
    from langchain_core.runnables import RunnableConfig
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    # Stub classes for when LangChain is not installed
    class BaseMemory:
        memory_key = "chat_history"
        return_messages = True
    class BaseMessage:
        def __init__(self, content):
            self.content = content
    class HumanMessage(BaseMessage):
        pass
    class AIMessage(BaseMessage):
        pass
    class RunnableConfig:
        pass

import json
from typing import List, Dict, Any, Optional

from agent_memory import Memory


if HAS_LANGCHAIN:
    class LangChainMemory(BaseMemory):
        """
        LangChain-compatible memory using agent-memory backend.
        
        Implements BaseMemory interface for seamless LangChain integration.
        """
        
        memory_key: str = "chat_history"
        
        def __init__(
            self,
            storage: str = "json",
            path: str = "./memory.json",
            memory_key: str = "chat_history",
            return_messages: bool = True,
            ttl_days: Optional[int] = None,
            **kwargs
        ):
            """Initialize LangChain memory adapter."""
            super().__init__(memory_key=memory_key, return_messages=return_messages)
            self._memory = Memory(storage=storage, path=path, ttl_days=ttl_days)
            self.return_messages = return_messages
        
        @property
        def memory_variables(self) -> List[str]:
            """Return memory variables."""
            return [self.memory_key]
        
        def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            """Load memory variables for context."""
            # Get recent memories as chat history
            recent = self._memory.get_recent(limit=10)
            
            if self.return_messages:
                messages = []
                for mem in recent:
                    # Heuristic: if it looks like user input, use HumanMessage
                    # Otherwise assume AI response
                    if mem.get("metadata", {}).get("role") == "user":
                        messages.append(HumanMessage(content=mem["text"]))
                    else:
                        messages.append(AIMessage(content=mem["text"]))
                return {self.memory_key: messages}
            else:
                # Return as string format
                history = "\n".join([f"{mem['text']}" for mem in recent])
                return {self.memory_key: history}
        
        def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
            """Save context to memory."""
            # Extract input (user message)
            input_text = ""
            if "question" in inputs:
                input_text = inputs["question"]
            elif "input" in inputs:
                input_text = inputs["input"]
            elif self.memory_key in inputs:
                input_text = str(inputs[self.memory_key])
            
            # Extract output (AI response)
            output_text = ""
            if "text" in outputs:
                output_text = outputs["text"]
            elif "output" in outputs:
                output_text = outputs["output"]
            elif "answer" in outputs:
                output_text = outputs["answer"]
            
            # Save to agent-memory
            if input_text:
                self._memory.add(
                    input_text,
                    metadata={"role": "user", "source": "langchain"}
                )
            if output_text:
                self._memory.add(
                    output_text,
                    metadata={"role": "ai", "source": "langchain"}
                )
        
        def clear(self) -> None:
            """Clear memory."""
            self._memory.clear()


def get_chat_memory(
    storage: str = "json",
    path: str = "./memory.json",
    **kwargs
):
    """Convenience function to get LangChain-compatible memory."""
    return LangChainMemory(storage=storage, path=path, **kwargs)


# Example usage
if __name__ == "__main__":
    if HAS_LANGCHAIN:
        # Quick demo
        memory = LangChainMemory(
            storage="json",
            path="/tmp/lc_demo.json",
            return_messages=True
        )
        
        # Simulate conversation
        memory.save_context(
            {"question": "My name is Bob"},
            {"text": "Nice to meet you, Bob!"}
        )
        
        memory.save_context(
            {"question": "What's my name?"},
            {"text": "Your name is Bob!"}
        )
        
        # Load context
        context = memory.load_memory_variables({})
        print("Chat History:")
        for msg in context.get("chat_history", []):
            print(f"  {type(msg).__name__}: {msg.content}")
        
        print("\n✅ LangChain adapter working!")
    else:
        # Basic demo without LangChain
        print("⚠️ LangChain not installed. Running basic demo...")
        memory = Memory(storage="json", path="/tmp/lc_demo.json")
        
        memory.add("User: My name is Bob", metadata={"role": "user"})
        memory.add("AI: Nice to meet you, Bob!", metadata={"role": "ai"})
        memory.add("User: What's my name?", metadata={"role": "user"})
        memory.add("AI: Your name is Bob!", metadata={"role": "ai"})
        
        context = memory.get_context(max_tokens=500)
        print("\nContext:")
        print(context)
        print("\n✅ Basic demo complete!")
else:
    # Stub when LangChain not available
    LangChainMemory = None
    get_chat_memory = None
    
    # Still run demo with basic memory
    if __name__ == "__main__":
        print("⚠️ LangChain not installed. Running basic demo...")
        memory = Memory(storage="json", path="/tmp/lc_demo.json")
        
        memory.add("User: My name is Bob", metadata={"role": "user"})
        memory.add("AI: Nice to meet you, Bob!", metadata={"role": "ai"})
        memory.add("User: What's my name?", metadata={"role": "user"})
        memory.add("AI: Your name is Bob!", metadata={"role": "ai"})
        
        context = memory.get_context(max_tokens=500)
        print("\nContext:")
        print(context)
        print("\n✅ Basic demo complete!")
