#!/usr/bin/env python
"""Test random module import"""

from Module.runner import AbuRunner

runner = AbuRunner()

# Test 1: Import random
print("Test 1: Importing random...")
runner.execute_line("libra random")

# Test 2: Create list
print("\nTest 2: Creating list...")
runner.execute_line('mylist is ["hi", "hello", "greetings"]')

# Test 3: Use random.choice
print("\nTest 3: Using random.choice...")
runner.execute_line("show random.choice(mylist)")

print("\nDone!")
