"""
AbuLang Browser Package
Browser-compatible version of AbuLang interpreter with I/O redirection

This package provides:
- BrowserIOAdapter: I/O redirection for browser environment
- Browser-compatible AbuRunner integration
"""

from .browser_io_adapter import (
    BrowserIOAdapter,
    create_browser_adapter,
    get_global_adapter,
    activate_browser_io,
    deactivate_browser_io,
    get_captured_output,
    clear_captured_output
)

__all__ = [
    'BrowserIOAdapter',
    'create_browser_adapter',
    'get_global_adapter',
    'activate_browser_io',
    'deactivate_browser_io',
    'get_captured_output',
    'clear_captured_output'
]

__version__ = '1.0.0'
