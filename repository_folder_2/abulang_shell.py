"""
AbuLang Shell - Interactive REPL for AbuLang
Launch with: python -m abulang_shell
Or: import abulang_shell
"""

from abulang.repl import start_abulang_repl

if __name__ == "__main__":
    start_abulang_repl()

# Auto-start when imported
start_abulang_repl()
