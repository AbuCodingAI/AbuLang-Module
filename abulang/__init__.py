"""
AbuLang - A friendly, Pythonic programming language for beginners and creative coders
"""

from essentials.python.runner import AbuRunner

__version__ = "3.0.0"
__author__ = "Abu"
__license__ = "MIT"

# Create default runner instance
_runner = AbuRunner()

def run(code: str):
    """
    Run AbuLang code
    
    Args:
        code (str): AbuLang code to execute
    
    Example:
        >>> from abulang import run
        >>> run('show "Hello, World!"')
        Hello, World!
    """
    _runner.run(code)

def run_file(filename: str):
    """
    Run an AbuLang file
    
    Args:
        filename (str): Path to .abu file
    
    Example:
        >>> from abulang import run_file
        >>> run_file("myprogram.abu")
    """
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    run(code)

# Exports
__all__ = [
    'run',
    'run_file',
    'AbuRunner',
]
