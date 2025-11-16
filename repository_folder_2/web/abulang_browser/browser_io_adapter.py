"""
BrowserIOAdapter - I/O redirection adapter for AbuLang in browser environment
Replaces Python's print() and input() with browser-based output capture and input dialog

Task 11: Create BrowserIOAdapter for I/O redirection
Requirements: 5.1, 5.2, 5.3, 5.4
"""

import sys
import io
import builtins


class BrowserIOAdapter:
    """
    Adapter class that redirects Python I/O operations to browser interface
    
    This adapter:
    - Replaces print() with output capture that sends to browser results panel
    - Replaces input() with async input dialog that prompts user in browser
    - Maintains compatibility with AbuLang's show and ask commands
    """
    
    def __init__(self):
        """Initialize the BrowserIOAdapter"""
        self.output_buffer = []
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.original_input = builtins.input
        self.is_active = False
        
    def activate(self):
        """
        Activate the I/O adapter
        Redirects stdout, stderr, and input to browser interface
        """
        if self.is_active:
            return
            
        # Create output capture stream
        self.output_stream = BrowserOutputStream(self.output_buffer)
        
        # Redirect stdout and stderr
        sys.stdout = self.output_stream
        sys.stderr = self.output_stream
        
        # Replace input function with browser input
        # Note: The actual browser input function will be injected by JavaScript
        # This is just a placeholder that will be overridden
        builtins.input = self._browser_input_placeholder
        
        self.is_active = True
        
    def deactivate(self):
        """
        Deactivate the I/O adapter
        Restores original stdout, stderr, and input
        """
        if not self.is_active:
            return
            
        # Restore original streams
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        builtins.input = self.original_input
        
        self.is_active = False
        
    def get_output(self):
        """
        Get captured output as a string
        
        Returns:
            str: All captured output joined together
        """
        return ''.join(self.output_buffer)
        
    def clear_output(self):
        """Clear the output buffer"""
        self.output_buffer.clear()
        
    def _browser_input_placeholder(self, prompt=''):
        """
        Placeholder for browser input function
        This will be replaced by JavaScript with an async function
        
        Args:
            prompt (str): The prompt to display to the user
            
        Returns:
            str: User input (when overridden by JavaScript)
        """
        raise RuntimeError(
            "Browser input not properly initialized. "
            "This function should be overridden by JavaScript."
        )


class BrowserOutputStream(io.StringIO):
    """
    Custom output stream that captures output to a buffer
    Compatible with Python's stdout/stderr interface
    """
    
    def __init__(self, buffer):
        """
        Initialize the output stream
        
        Args:
            buffer (list): List to append output lines to
        """
        super().__init__()
        self.buffer = buffer
        
    def write(self, text):
        """
        Write text to the output buffer
        
        Args:
            text (str): Text to write
            
        Returns:
            int: Number of characters written
        """
        if text:
            self.buffer.append(text)
        return len(text)
        
    def flush(self):
        """Flush the stream (no-op for browser)"""
        pass


def create_browser_adapter():
    """
    Factory function to create and return a BrowserIOAdapter instance
    
    Returns:
        BrowserIOAdapter: A new adapter instance
    """
    return BrowserIOAdapter()


# Global adapter instance for easy access
_global_adapter = None


def get_global_adapter():
    """
    Get or create the global BrowserIOAdapter instance
    
    Returns:
        BrowserIOAdapter: The global adapter instance
    """
    global _global_adapter
    if _global_adapter is None:
        _global_adapter = create_browser_adapter()
    return _global_adapter


def activate_browser_io():
    """
    Convenience function to activate browser I/O redirection
    Uses the global adapter instance
    """
    adapter = get_global_adapter()
    adapter.activate()


def deactivate_browser_io():
    """
    Convenience function to deactivate browser I/O redirection
    Uses the global adapter instance
    """
    adapter = get_global_adapter()
    adapter.deactivate()


def get_captured_output():
    """
    Convenience function to get captured output
    Uses the global adapter instance
    
    Returns:
        str: All captured output
    """
    adapter = get_global_adapter()
    return adapter.get_output()


def clear_captured_output():
    """
    Convenience function to clear captured output
    Uses the global adapter instance
    """
    adapter = get_global_adapter()
    adapter.clear_output()
