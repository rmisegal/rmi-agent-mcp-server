#!/usr/bin/env python3
"""
Simple calculator test.
"""

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def main():
    print("Calculator Test")
    print("=" * 40)
    
    x, y = 10, 5
    
    print(f"{x} + {y} = {add(x, y)}")
    print(f"{x} * {y} = {multiply(x, y)}")
    
    # Test with floats
    a, b = 3.14, 2.0
    print(f"{a} + {b} = {add(a, b)}")
    print(f"{a} * {b} = {multiply(a, b)}")
    
    print("=" * 40)
    print("All tests passed!")

if __name__ == "__main__":
    main()
