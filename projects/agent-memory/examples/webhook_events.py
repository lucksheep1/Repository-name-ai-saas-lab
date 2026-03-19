"""
Memory Webhook Events
Webhook events from memory
"""
from agent_memory import Memory


class WebhookEvents:
    """Webhook events"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.webhooks = []
    
    def register(self, url: str, events: list):
        """Register webhook"""
        self.webhooks.append({"url": url, "events": events})
    
    def trigger(self, event: str, data: dict):
        """Trigger webhook"""
        for wh in self.webhooks:
            if event in wh["events"]:
                print(f"Would send to {wh['url']}: {event}")
    
    def on_add(self, mem_id: str):
        """On add trigger"""
        self.trigger("memory.add", {"id": mem_id})
    
    def on_delete(self, mem_id: str):
        """On delete trigger"""
        self.trigger("memory.delete", {"id": mem_id})


def demo():
    """Demo webhooks"""
    memory = Memory(storage="json", path="./webhook_demo2.json")
    hooks = WebhookEvents(memory)
    
    hooks.register("http://example.com/hook", ["memory.add"])
    hooks.on_add("test")
    
    print("Webhook triggered")


if __name__ == "__main__":
    demo()
