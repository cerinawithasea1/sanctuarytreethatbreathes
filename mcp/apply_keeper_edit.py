import os
import sys

if len(sys.argv) != 2:
    print("Usage: apply_keeper_edit.py <file>")
    sys.exit(1)

path = sys.argv[1]

print(f"\n📜 Reviewing Keeper’s proposed edit for: {path}")
print("───────────────────────────────────────────────")

with open(path, "r") as f:
    content = f.read()

print(content)
confirm = input("\nApply this edit? (yes/no): ").strip().lower()

if confirm == "yes":
    print("✅ Keeper’s edit applied.")
else:
    print("❌ Edit canceled.")
