"""Basic usage example for govsearch."""
from src.core import Govsearch

def main():
    instance = Govsearch(config={"verbose": True})

    print("=== govsearch Example ===\n")

    # Run primary operation
    result = instance.analyze(input="example data", mode="demo")
    print(f"Result: {result}")

    # Run multiple operations
    ops = ["analyze", "evaluate", "score]
    for op in ops:
        r = getattr(instance, op)(source="example")
        print(f"  {op}: {"✓" if r.get("ok") else "✗"}")

    # Check stats
    print(f"\nStats: {instance.get_stats()}")

if __name__ == "__main__":
    main()
