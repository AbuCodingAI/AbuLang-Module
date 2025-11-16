// AbuLang Web Playground - Main Application

// Define AbuLang syntax highlighting mode for CodeMirror
CodeMirror.defineMode("abulang", function () {
    // AbuLang keywords and builtins
    const keywords = {
        'show': true,
        'ask': true,
        'libra': true,
        'def': true,
        'if': true,
        'else': true,
        'elif': true,
        'while': true,
        'for': true,
        'in': true,
        'return': true,
        'break': true,
        'continue': true,
        'pass': true,
        'and': true,
        'or': true,
        'not': true,
        'is': true,
        'True': true,
        'False': true,
        'None': true
    };

    const builtins = {
        'len': true,
        'range': true,
        'print': true,
        'input': true,
        'int': true,
        'float': true,
        'str': true,
        'list': true,
        'dict': true,
        'set': true,
        'tuple': true
    };

    return {
        startState: function () {
            return {
                inString: false,
                stringDelim: null
            };
        },
        token: function (stream, state) {
            // Handle comments
            if (stream.match(/^#.*/)) {
                return "abulang-comment";
            }

            // Handle strings
            if (state.inString) {
                if (stream.match(state.stringDelim)) {
                    state.inString = false;
                    state.stringDelim = null;
                    return "abulang-string";
                }
                stream.next();
                return "abulang-string";
            }

            if (stream.match(/^["']/) || stream.match(/^"""|^'''/)) {
                state.inString = true;
                state.stringDelim = stream.current();
                return "abulang-string";
            }

            // Handle numbers
            if (stream.match(/^[0-9]+\.?[0-9]*/)) {
                return "abulang-number";
            }

            // Handle operators
            if (stream.match(/^[+\-*/%=<>!&|]/)) {
                return "abulang-operator";
            }

            // Handle words (keywords, builtins, identifiers)
            if (stream.match(/^[a-zA-Z_]\w*/)) {
                const word = stream.current();
                if (keywords.hasOwnProperty(word)) {
                    return "abulang-keyword";
                }
                if (builtins.hasOwnProperty(word)) {
                    return "abulang-builtin";
                }
                return null;
            }

            // Skip other characters
            stream.next();
            return null;
        }
    };
});

/**
 * PyodideManager - Handles Pyodide runtime initialization and management
 * Implements lazy loading: Pyodide is only loaded on first code execution
 */
class PyodideManager {
    constructor() {
        this.pyodide = null;
        this.isInitialized = false;
        this.isLoading = false;
        this.loadingPromise = null;
        this.onLoadingStateChange = null;
        this.onMessage = null;
    }

    /**
     * Initialize Pyodide from CDN with lazy loading
     * Returns the same promise if already loading to prevent duplicate loads
     */
    async initialize() {
        // If already initialized, return immediately
        if (this.isInitialized && this.pyodide) {
            return this.pyodide;
        }

        // If currently loading, return the existing promise
        if (this.isLoading && this.loadingPromise) {
            return this.loadingPromise;
        }

        // Start loading
        this.isLoading = true;
        this.notifyLoadingState(true);
        this.notifyMessage('Loading Python runtime (Pyodide)...', 'info');

        this.loadingPromise = this._loadPyodide();

        try {
            this.pyodide = await this.loadingPromise;
            this.isInitialized = true;
            this.notifyMessage('Python runtime loaded successfully!', 'success');
            return this.pyodide;
        } catch (error) {
            this.isInitialized = false;
            this.pyodide = null;
            this.handleLoadingError(error);
            throw error;
        } finally {
            this.isLoading = false;
            this.loadingPromise = null;
            this.notifyLoadingState(false);
        }
    }

    /**
     * Internal method to load Pyodide from CDN
     */
    async _loadPyodide() {
        try {
            // Check if loadPyodide function is available
            if (typeof loadPyodide === 'undefined') {
                throw new Error('Pyodide script not loaded. Please check your internet connection.');
            }

            // Load Pyodide with configuration
            const pyodide = await loadPyodide({
                indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
                fullStdLib: false // Don't load full stdlib to improve load time
            });

            return pyodide;
        } catch (error) {
            // Re-throw with more context
            if (error.message.includes('fetch')) {
                throw new Error('Network error: Unable to download Pyodide. Please check your internet connection.');
            } else if (error.message.includes('WebAssembly')) {
                throw new Error('WebAssembly not supported. Please use a modern browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+).');
            } else {
                throw new Error(`Failed to load Pyodide: ${error.message}`);
            }
        }
    }

    /**
     * Handle Pyodide loading errors with user-friendly messages
     */
    handleLoadingError(error) {
        let userMessage = 'Failed to load Python runtime.';
        let suggestions = [];

        if (error.message.includes('internet connection') || error.message.includes('Network')) {
            userMessage = 'Unable to load Python runtime due to network issues.';
            suggestions = [
                'Check your internet connection',
                'Try refreshing the page',
                'Check if you can access cdn.jsdelivr.net'
            ];
        } else if (error.message.includes('WebAssembly')) {
            userMessage = 'Your browser does not support WebAssembly.';
            suggestions = [
                'Update your browser to the latest version',
                'Use Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+'
            ];
        } else if (error.message.includes('timeout')) {
            userMessage = 'Loading Python runtime timed out.';
            suggestions = [
                'Check your internet speed',
                'Try refreshing the page',
                'Try again later'
            ];
        } else {
            userMessage = `Failed to load Python runtime: ${error.message}`;
            suggestions = [
                'Try refreshing the page',
                'Check browser console for details'
            ];
        }

        // Format error message with suggestions
        const fullMessage = `${userMessage}\n\nSuggestions:\n${suggestions.map(s => `• ${s}`).join('\n')}`;
        this.notifyMessage(fullMessage, 'error');
    }

    /**
     * Get the initialized Pyodide instance
     */
    getPyodide() {
        if (!this.isInitialized || !this.pyodide) {
            throw new Error('Pyodide not initialized. Call initialize() first.');
        }
        return this.pyodide;
    }

    /**
     * Check if Pyodide is initialized
     */
    isReady() {
        return this.isInitialized && this.pyodide !== null;
    }

    /**
     * Reset the manager (for testing or error recovery)
     */
    reset() {
        this.pyodide = null;
        this.isInitialized = false;
        this.isLoading = false;
        this.loadingPromise = null;
    }

    /**
     * Notify loading state change
     */
    notifyLoadingState(isLoading) {
        if (this.onLoadingStateChange) {
            this.onLoadingStateChange(isLoading);
        }
    }

    /**
     * Notify message
     */
    notifyMessage(message, type = 'info') {
        if (this.onMessage) {
            this.onMessage(message, type);
        }
    }

    /**
     * Set callback for loading state changes
     */
    setLoadingStateCallback(callback) {
        this.onLoadingStateChange = callback;
    }

    /**
     * Set callback for messages
     */
    setMessageCallback(callback) {
        this.onMessage = callback;
    }
}

/**
 * OutputCapture - Captures Python stdout for display in the web UI
 * Intercepts print statements and redirects them to a buffer
 */
class OutputCapture {
    constructor() {
        this.buffer = [];
        this.isCapturing = false;
        this.pyodide = null;
    }

    /**
     * Initialize the output capture with a Pyodide instance
     * @param {Object} pyodide - The Pyodide runtime instance
     */
    initialize(pyodide) {
        this.pyodide = pyodide;
    }

    /**
     * Start capturing stdout
     * Redirects Python's sys.stdout to capture buffer
     */
    startCapture() {
        if (!this.pyodide) {
            throw new Error('OutputCapture not initialized. Call initialize() with Pyodide instance first.');
        }

        this.isCapturing = true;
        this.buffer = [];

        // Set up Python code to redirect stdout
        this.pyodide.runPython(`
import sys
import io

class OutputCapture:
    def __init__(self):
        self.buffer = []
    
    def write(self, text):
        if text and text.strip():
            self.buffer.append(text)
    
    def flush(self):
        pass
    
    def get_output(self):
        return ''.join(self.buffer)
    
    def clear(self):
        self.buffer = []

# Create global output capture instance
_output_capture = OutputCapture()
sys.stdout = _output_capture
sys.stderr = _output_capture
        `);
    }

    /**
     * Stop capturing stdout
     * Restores Python's original stdout
     */
    stopCapture() {
        if (!this.pyodide || !this.isCapturing) {
            return;
        }

        try {
            // Restore original stdout/stderr
            this.pyodide.runPython(`
import sys
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
            `);
        } catch (error) {
            console.error('Error stopping output capture:', error);
        }

        this.isCapturing = false;
    }

    /**
     * Get the captured output as formatted text
     * @returns {string} The captured output
     */
    getOutput() {
        if (!this.pyodide) {
            return '';
        }

        try {
            // Retrieve output from Python
            const output = this.pyodide.runPython('_output_capture.get_output()');
            return output || '';
        } catch (error) {
            console.error('Error retrieving output:', error);
            return '';
        }
    }

    /**
     * Clear the output buffer
     */
    clearOutput() {
        this.buffer = [];

        if (this.pyodide && this.isCapturing) {
            try {
                this.pyodide.runPython('_output_capture.clear()');
            } catch (error) {
                console.error('Error clearing output buffer:', error);
            }
        }
    }

    /**
     * Check if currently capturing
     * @returns {boolean} True if capturing is active
     */
    isActive() {
        return this.isCapturing;
    }

    /**
     * Reset the capture state
     */
    reset() {
        this.stopCapture();
        this.buffer = [];
        this.pyodide = null;
    }
}

/**
 * InputManager - Manages input dialog for user input (ask command)
 * Implements promise-based input handling for async code execution
 */
class InputManager {
    constructor() {
        this.inputDialog = null;
        this.inputPrompt = null;
        this.inputField = null;
        this.inputSubmitBtn = null;
        this.inputCancelBtn = null;
        this.currentResolve = null;
        this.currentReject = null;
        this.isWaitingForInput = false;
    }

    /**
     * Initialize the InputManager with DOM elements
     * @param {Object} elements - Object containing DOM element references
     */
    initialize(elements) {
        this.inputDialog = elements.inputDialog;
        this.inputPrompt = elements.inputPrompt;
        this.inputField = elements.inputField;
        this.inputSubmitBtn = elements.inputSubmitBtn;
        this.inputCancelBtn = elements.inputCancelBtn;

        // Attach event listeners
        this.attachEventListeners();
    }

    /**
     * Attach event listeners to input dialog elements
     */
    attachEventListeners() {
        // Submit button click
        this.inputSubmitBtn.addEventListener('click', () => this.submitInput());

        // Cancel button click
        this.inputCancelBtn.addEventListener('click', () => this.cancelInput());

        // Enter key to submit
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.submitInput();
            }
        });

        // Escape key to cancel
        this.inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                e.preventDefault();
                this.cancelInput();
            }
        });

        // Click outside modal to cancel (optional)
        this.inputDialog.addEventListener('click', (e) => {
            if (e.target === this.inputDialog) {
                this.cancelInput();
            }
        });
    }

    /**
     * Show input dialog and wait for user input
     * Returns a promise that resolves with the user's input
     * @param {string} prompt - The prompt text to display
     * @returns {Promise<string>} Promise that resolves with user input
     */
    showInputDialog(prompt = 'Enter value:') {
        return new Promise((resolve, reject) => {
            // Check if already waiting for input
            if (this.isWaitingForInput) {
                reject(new Error('Input dialog already open'));
                return;
            }

            // Set up promise handlers
            this.currentResolve = resolve;
            this.currentReject = reject;
            this.isWaitingForInput = true;

            // Update prompt text
            this.inputPrompt.textContent = prompt;

            // Clear previous input
            this.inputField.value = '';

            // Show dialog
            this.inputDialog.classList.remove('hidden');

            // Focus on input field
            this.inputField.focus();
        });
    }

    /**
     * Submit the input value and resolve the promise
     */
    submitInput() {
        if (!this.isWaitingForInput || !this.currentResolve) {
            return;
        }

        // Get input value
        const value = this.inputField.value;

        // Hide dialog
        this.hideDialog();

        // Resolve promise with input value
        this.currentResolve(value);

        // Clean up
        this.cleanup();
    }

    /**
     * Cancel the input and reject the promise
     */
    cancelInput() {
        if (!this.isWaitingForInput || !this.currentReject) {
            return;
        }

        // Hide dialog
        this.hideDialog();

        // Reject promise with cancellation error
        this.currentReject(new Error('Input cancelled by user'));

        // Clean up
        this.cleanup();
    }

    /**
     * Hide the input dialog
     */
    hideDialog() {
        this.inputDialog.classList.add('hidden');
    }

    /**
     * Clean up after input is submitted or cancelled
     */
    cleanup() {
        this.currentResolve = null;
        this.currentReject = null;
        this.isWaitingForInput = false;
        this.inputField.value = '';
    }

    /**
     * Check if currently waiting for input
     * @returns {boolean} True if waiting for input
     */
    isActive() {
        return this.isWaitingForInput;
    }

    /**
     * Get the current input value (without submitting)
     * @returns {string} Current input field value
     */
    getCurrentValue() {
        return this.inputField.value;
    }

    /**
     * Reset the input manager state
     */
    reset() {
        if (this.isWaitingForInput && this.currentReject) {
            this.currentReject(new Error('Input manager reset'));
        }
        this.hideDialog();
        this.cleanup();
    }
}

// RuntimeBridge is now loaded from lib/runtime-bridge.js

class AbuLangPlayground {
    constructor() {
        this.pyodideManager = new PyodideManager();
        this.outputCapture = new OutputCapture();
        this.inputManager = new InputManager();
        this.errorFormatter = new ErrorFormatter();
        this.runtimeBridge = null; // Will be initialized after UI setup
        this.isExecuting = false;
        this.editor = null;
        this.initializeUI();
        this.setupPyodideCallbacks();
        this.initializeRuntimeBridge();
    }

    setupPyodideCallbacks() {
        // Set up callbacks for PyodideManager
        this.pyodideManager.setLoadingStateCallback((isLoading) => {
            this.showLoading(isLoading);
        });

        this.pyodideManager.setMessageCallback((message, type) => {
            this.displayOutput(message + '\n', type);
        });
    }

    initializeRuntimeBridge() {
        // Create RuntimeBridge instance with all dependencies
        this.runtimeBridge = new RuntimeBridge(
            this.pyodideManager,
            this.outputCapture,
            this.inputManager,
            this.errorFormatter
        );
    }

    initializeUI() {
        // Get DOM elements
        this.codeEditorContainer = document.getElementById('code-editor');
        this.resultsPanel = document.getElementById('results-panel');
        this.runBtn = document.getElementById('run-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.clearOutputBtn = document.getElementById('clear-output-btn');
        this.helpBtn = document.getElementById('help-btn');
        this.examplesDropdown = document.getElementById('examples-dropdown');
        this.loadingIndicator = document.getElementById('loading-indicator');

        // Initialize InputManager with DOM elements
        this.inputManager.initialize({
            inputDialog: document.getElementById('input-dialog'),
            inputPrompt: document.getElementById('input-prompt'),
            inputField: document.getElementById('input-field'),
            inputSubmitBtn: document.getElementById('input-submit-btn'),
            inputCancelBtn: document.getElementById('input-cancel-btn')
        });

        // Initialize CodeMirror editor
        this.initializeCodeMirror();

        // Attach event listeners
        this.attachEventListeners();

        // Set default code
        this.setDefaultCode();
    }

    initializeCodeMirror() {
        // Create CodeMirror instance
        this.editor = CodeMirror(this.codeEditorContainer, {
            mode: 'abulang',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            smartIndent: true,
            lineWrapping: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            extraKeys: {
                "Tab": function (cm) {
                    if (cm.somethingSelected()) {
                        cm.indentSelection("add");
                    } else {
                        cm.replaceSelection("    ", "end");
                    }
                },
                "Shift-Tab": function (cm) {
                    cm.indentSelection("subtract");
                }
            }
        });
    }

    attachEventListeners() {
        this.runBtn.addEventListener('click', () => this.runCode());
        this.clearBtn.addEventListener('click', () => this.clearEditor());
        this.downloadBtn.addEventListener('click', () => this.downloadCode());
        this.clearOutputBtn.addEventListener('click', () => this.clearOutput());
        this.helpBtn.addEventListener('click', () => this.showHelp());
        this.examplesDropdown.addEventListener('change', (e) => this.loadExample(e.target.value));

        // Test input dialog button (for Task 7 demonstration)
        const testInputBtn = document.getElementById('test-input-btn');
        if (testInputBtn) {
            testInputBtn.addEventListener('click', () => this.testInputDialog());
        }

        // Note: InputManager handles its own event listeners
    }

    setDefaultCode() {
        this.editor.setValue(`# Welcome to AbuLang Web Playground!
# Try running this example:

show "Hello from AbuLang!"
show "This is running in your browser!"

# Variables and expressions
x = 10
y = 20
show "x + y = " + str(x + y)

# Test the input dialog:
# Uncomment the lines below to test input functionality
# name = ask "What is your name?"
# show "Hello, " + name + "!"`);
    }

    async runCode() {
        if (this.isExecuting) return;

        const code = this.editor.getValue().trim();
        if (!code) {
            this.displayOutput('No code to execute.\n', 'error');
            return;
        }

        this.isExecuting = true;
        this.runBtn.disabled = true;
        this.runBtn.textContent = 'Running...';
        this.clearOutput();

        try {
            // Execute code using RuntimeBridge
            this.displayOutput('Executing AbuLang code...\n', 'info');

            const result = await this.runtimeBridge.executeCode(code);

            if (result.success) {
                // Display captured output
                if (result.output) {
                    this.displayOutput(result.output, 'normal');
                }
                this.displayOutput('\n✓ Execution completed successfully.\n', 'success');
            } else {
                // Display any output that was captured before error
                if (result.output) {
                    this.displayOutput(result.output, 'normal');
                    this.displayOutput('\n', 'normal');
                }

                // Display error information with enhanced formatting
                this.displayError(result.error);
            }

        } catch (error) {
            // Handle unexpected errors
            this.displayOutput(`✗ Unexpected error: ${error.message}\n`, 'error');
            console.error('Execution error:', error);
        } finally {
            this.isExecuting = false;
            this.runBtn.disabled = false;
            this.runBtn.textContent = 'Run Code';
        }
    }

    clearEditor() {
        this.editor.setValue('');
        this.editor.focus();
    }

    clearOutput() {
        this.resultsPanel.innerHTML = '';
    }

    downloadCode() {
        const code = this.editor.getValue();
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        a.href = url;
        a.download = `abulang-code-${timestamp}.abu`;
        a.click();
        URL.revokeObjectURL(url);
    }

    loadExample(exampleName) {
        if (!exampleName) return;

        // Placeholder for loading examples
        // This will be implemented in Phase 4
        this.displayOutput('Example loading not yet implemented.\n', 'info');
        this.examplesDropdown.value = '';
    }

    showHelp() {
        window.open('https://github.com/yourusername/abulang', '_blank');
    }

    displayOutput(text, type = 'normal') {
        const line = document.createElement('div');
        line.className = `output-line`;

        // Add type-specific classes
        if (type === 'error') {
            line.classList.add('error-line');
        } else if (type === 'success') {
            line.classList.add('success-line');
        } else if (type === 'info') {
            line.classList.add('info-line');
        }

        line.textContent = text;
        this.resultsPanel.appendChild(line);
        this.resultsPanel.scrollTop = this.resultsPanel.scrollHeight;
    }

    /**
     * Display formatted error with color coding and structure
     * @param {Object} error - Formatted error object from ErrorFormatter
     */
    displayError(error) {
        // Create error container
        const errorContainer = document.createElement('div');
        errorContainer.className = 'error-container';

        // Add syntax/runtime error class for color coding
        if (error.isSyntaxError) {
            errorContainer.classList.add('syntax-error');
        } else {
            errorContainer.classList.add('runtime-error');
        }

        // Error header
        const errorHeader = document.createElement('div');
        errorHeader.className = 'error-header';
        errorHeader.innerHTML = `<span class="error-icon">✗</span> <span class="error-type">${error.type}</span>: <span class="error-message">${this.escapeHtml(error.message)}</span>`;
        errorContainer.appendChild(errorHeader);

        // Line number if available
        if (error.lineNumber) {
            const lineInfo = document.createElement('div');
            lineInfo.className = 'error-line-info';
            lineInfo.textContent = `   at line ${error.lineNumber}`;
            errorContainer.appendChild(lineInfo);
        }

        // Description
        if (error.description) {
            const description = document.createElement('div');
            description.className = 'error-description';
            description.textContent = error.description;
            errorContainer.appendChild(description);
        }

        // Suggestions
        if (error.suggestions && error.suggestions.length > 0) {
            const suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'error-suggestions';

            const suggestionsHeader = document.createElement('div');
            suggestionsHeader.className = 'suggestions-header';
            suggestionsHeader.textContent = 'Suggestions:';
            suggestionsContainer.appendChild(suggestionsHeader);

            const suggestionsList = document.createElement('ul');
            suggestionsList.className = 'suggestions-list';
            error.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
            suggestionsContainer.appendChild(suggestionsList);

            errorContainer.appendChild(suggestionsContainer);
        }

        this.resultsPanel.appendChild(errorContainer);
        this.resultsPanel.scrollTop = this.resultsPanel.scrollHeight;
    }

    /**
     * Escape HTML special characters
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showLoading(show) {
        if (show) {
            this.loadingIndicator.classList.remove('hidden');
        } else {
            this.loadingIndicator.classList.add('hidden');
        }
    }

    /**
     * Test the InputManager functionality (Task 7 demonstration)
     */
    async testInputDialog() {
        this.clearOutput();
        this.displayOutput('Testing InputManager (Task 7)...\n\n', 'info');

        try {
            // Test 1: Basic input
            this.displayOutput('Test 1: Basic input dialog\n', 'info');
            const name = await this.inputManager.showInputDialog('What is your name?');
            this.displayOutput(`✓ Received input: "${name}"\n\n`, 'success');

            // Test 2: Sequential inputs
            this.displayOutput('Test 2: Sequential inputs\n', 'info');
            const age = await this.inputManager.showInputDialog('What is your age?');
            this.displayOutput(`✓ Received age: "${age}"\n\n`, 'success');

            const city = await this.inputManager.showInputDialog('What city are you from?');
            this.displayOutput(`✓ Received city: "${city}"\n\n`, 'success');

            // Summary
            this.displayOutput('=== Test Summary ===\n', 'info');
            this.displayOutput(`Name: ${name}\n`, 'normal');
            this.displayOutput(`Age: ${age}\n`, 'normal');
            this.displayOutput(`City: ${city}\n\n`, 'normal');
            this.displayOutput('✓ All tests passed! InputManager is working correctly.\n', 'success');

        } catch (error) {
            this.displayOutput(`✗ Test cancelled or error: ${error.message}\n`, 'error');
        }
    }
}

// Initialize the playground when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.playground = new AbuLangPlayground();
});
