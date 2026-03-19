"""
Memory Pagination
Paginate memory results
"""
from agent_memory import Memory


class PagedMemory:
    """Paged memory"""
    
    def __init__(self, memory: Memory, page_size: int = 10):
        self.memory = memory
        self.page_size = page_size
    
    def get_page(self, page: int = 1):
        """Get page"""
        offset = (page - 1) * self.page_size
        all_mem = self.memory.get_all()
        
        total = len(all_mem)
        pages = (total + self.page_size - 1) // self.page_size
        
        mems = all_mem[offset:offset + self.page_size]
        
        return {
            "page": page,
            "page_size": self.page_size,
            "total": total,
            "pages": pages,
            "data": mems
        }
    
    def iterate(self):
        """Iterate pages"""
        page = 1
        
        while True:
            result = self.get_page(page)
            
            if not result["data"]:
                break
            
            yield result
            
            if page >= result["pages"]:
                break
            
            page += 1


def demo():
    """Demo pagination"""
    memory = Memory(storage="json", path="./page_demo.json")
    paged = PagedMemory(memory, page_size=3)
    
    for i in range(10):
        memory.add(f"Memory {i}")
    
    result = paged.get_page(2)
    print(f"Page 2: {len(result['data'])} items")
    
    import os
    if os.path.exists("./page_demo.json"):
        os.remove("./page_demo.json")


if __name__ == "__main__":
    demo()
