"""
Test script to verify AbuLang browser package imports work correctly
This can be run locally with Python to verify the package structure
"""

import sys
import os

# Add the parent directory to path to simulate Pyodide environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing AbuLang Browser Package Imports...")
    print("=" * 50)
    
    try:
        # Test basic import
        import abulang_browser
        print("✓ Successfully imported abulang_browser")
        print(f"  Version: {abulang_browser.__version__}")
        print(f"  Exports: {', '.join(abulang_browser.__all__)}")
        
        # Test individual imports
        from abulang_browser import AbuRunner
        print("✓ Successfully imported AbuRunner")
        
        from abulang_browser import AbuLang
        print("✓ Successfully imported AbuLang")
        
        from abulang_browser import GUIAliasManager
        print("✓ Successfully imported GUIAliasManager")
        
        from abulang_browser import run, reset, get_runner
        print("✓ Successfully imported utility functions (run, reset, get_runner)")
        
        print("\n" + "=" * 50)
        print("All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_runner_creation():
    """Test creating a runner instance"""
    print("\nTesting AbuRunner Creation...")
    print("=" * 50)
    
    try:
        from abulang_browser import AbuRunner
        
        runner = AbuRunner()
        print("✓ AbuRunner instance created")
        
        # Check attributes
        assert hasattr(runner, 'lang'), "Missing 'lang' attribute"
        print("✓ Runner has 'lang' attribute")
        
        assert hasattr(runner, 'gui_aliases'), "Missing 'gui_aliases' attribute"
        print("✓ Runner has 'gui_aliases' attribute")
        
        assert hasattr(runner, 'context'), "Missing 'context' attribute"
        print("✓ Runner has 'context' attribute")
        
        assert hasattr(runner, 'execute_line'), "Missing 'execute_line' method"
        print("✓ Runner has 'execute_line' method")
        
        assert hasattr(runner, 'run'), "Missing 'run' method"
        print("✓ Runner has 'run' method")
        
        # Check initial context
        print(f"✓ Initial context keys: {list(runner.context.keys())}")
        
        print("\n" + "=" * 50)
        print("Runner creation successful!")
        return True
        
    except Exception as e:
        print(f"\n✗ Runner creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_execution():
    """Test executing simple AbuLang code"""
    print("\nTesting Simple Code Execution...")
    print("=" * 50)
    
    try:
        from abulang_browser import AbuRunner
        import io
        import sys
        
        runner = AbuRunner()
        
        # Capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run simple code
        code = """
show "Hello from AbuLang!"
show 2 + 2
show 10 * 5
"""
        runner.run(code)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        print("✓ Code executed successfully")
        print("\nCaptured Output:")
        print("-" * 50)
        print(output)
        print("-" * 50)
        
        # Verify output contains expected values
        assert "Hello from AbuLang!" in output, "Missing expected output"
        assert "4" in output, "Missing math result"
        assert "50" in output, "Missing math result"
        
        print("\n" + "=" * 50)
        print("Code execution successful!")
        return True
        
    except Exception as e:
        print(f"\n✗ Code execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_variables():
    """Test variable assignment"""
    print("\nTesting Variable Assignment...")
    print("=" * 50)
    
    try:
        from abulang_browser import AbuRunner
        import io
        import sys
        
        runner = AbuRunner()
        
        # Capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Test variables
        code = """
x = 10
y = 20
z = x + y
show z
name = "AbuLang"
show name
"""
        runner.run(code)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        print("✓ Variable assignment works")
        print(f"✓ Variables in context: {[k for k in runner.context.keys() if not k.startswith('__')]}")
        print("\nCaptured Output:")
        print("-" * 50)
        print(output)
        print("-" * 50)
        
        # Verify variables are in context
        assert 'x' in runner.context, "Variable 'x' not in context"
        assert 'y' in runner.context, "Variable 'y' not in context"
        assert 'z' in runner.context, "Variable 'z' not in context"
        assert runner.context['z'] == 30, "Variable 'z' has wrong value"
        
        print("\n" + "=" * 50)
        print("Variable assignment successful!")
        return True
        
    except Exception as e:
        print(f"\n✗ Variable assignment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_library_import():
    """Test library import (libra)"""
    print("\nTesting Library Import (libra)...")
    print("=" * 50)
    
    try:
        from abulang_browser import AbuRunner
        import io
        import sys
        
        runner = AbuRunner()
        
        # Capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Test library import
        code = """
libra math
show math.pi
show math.sqrt(16)
"""
        runner.run(code)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        print("✓ Library import works")
        print("\nCaptured Output:")
        print("-" * 50)
        print(output)
        print("-" * 50)
        
        # Verify math is in context
        assert 'math' in runner.context, "Module 'math' not in context"
        
        print("\n" + "=" * 50)
        print("Library import successful!")
        return True
        
    except Exception as e:
        print(f"\n✗ Library import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("ABULANG BROWSER PACKAGE TEST SUITE")
    print("=" * 70 + "\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Runner Creation Test", test_runner_creation),
        ("Simple Execution Test", test_simple_execution),
        ("Variable Assignment Test", test_variables),
        ("Library Import Test", test_library_import),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
