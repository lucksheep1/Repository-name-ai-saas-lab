"""
Memory Benchmark
Performance testing utilities for memory operations
"""
from agent_memory import Memory
import time
from typing import Callable


def benchmark(func: Callable, iterations: int = 100) -> dict:
    """Benchmark a function"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # ms
    
    return {
        "iterations": iterations,
        "total_ms": sum(times),
        "avg_ms": sum(times) / len(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "p95_ms": sorted(times)[int(len(times) * 0.95)],
    }


def run_benchmarks():
    """Run all benchmarks"""
    results = {}
    
    # Benchmark: JSON storage
    print("=== Memory Benchmark ===\n")
    
    mem = Memory(storage="json", path="./bench_json.json")
    
    # Benchmark: Add
    def add_op():
        mem.add(f"Benchmark test {time.time()}")
    
    results["add_json"] = benchmark(add_op, 100)
    print(f"Add (JSON): {results['add_json']['avg_ms']:.2f}ms avg")
    
    # Benchmark: Search
    mem.add("Searchable benchmark content")
    
    def search_op():
        mem.search("benchmark")
    
    results["search_json"] = benchmark(search_op, 50)
    print(f"Search (JSON): {results['search_json']['avg_ms']:.2f}ms avg")
    
    # Benchmark: Get all
    def get_all_op():
        mem.get_all()
    
    results["get_all_json"] = benchmark(get_all_op, 50)
    print(f"Get All (JSON): {results['get_all_json']['avg_ms']:.2f}ms avg")
    
    print("\n--- SQLite ---")
    
    mem_sqlite = Memory(storage="sqlite", path="./bench_sqlite.db")
    
    def add_sqlite():
        mem_sqlite.add(f"Benchmark test {time.time()}")
    
    results["add_sqlite"] = benchmark(add_sqlite, 100)
    print(f"Add (SQLite): {results['add_sqlite']['avg_ms']:.2f}ms avg")
    
    mem_sqlite.add("Searchable benchmark content")
    
    def search_sqlite():
        mem_sqlite.search("benchmark")
    
    results["search_sqlite"] = benchmark(search_sqlite, 50)
    print(f"Search (SQLite): {results['search_sqlite']['avg_ms']:.2f}ms avg")
    
    print("\n=== Summary ===")
    print(f"JSON: Add={results['add_json']['avg_ms']:.1f}ms, Search={results['search_json']['avg_ms']:.1f}ms")
    print(f"SQLite: Add={results['add_sqlite']['avg_ms']:.1f}ms, Search={results['search_sqlite']['avg_ms']:.1f}ms")
    
    # Cleanup
    import os
    for f in ["./bench_json.json", "./bench_sqlite.db"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    run_benchmarks()
