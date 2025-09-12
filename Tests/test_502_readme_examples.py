import pytest
import re
import os
from io import StringIO
from contextlib import redirect_stdout

class TestActualReadmeExamples:
    """
    Tests that execute the actual code blocks from README.md
    """   
    @pytest.fixture
    def readme_content(self):
        """Read the README.md file content"""
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_python_code_blocks(self, readme_content):
        """Extract and test all Python code blocks from README.md"""
        # Regular expression to find Python code blocks in markdown
        # Matches code blocks that start with ```python and end with ```
        code_block_pattern = r'```python\s+(.*?)\s+```'
        code_blocks = re.findall(code_block_pattern, readme_content, re.DOTALL)
        
        # Make sure we found some code blocks
        assert len(code_blocks) > 0, "No Python code blocks found in README.md"
        
        # Execute each code block
        for i, code_block in enumerate(code_blocks):
            print(f"\nTesting README code block #{i+1}:")
            
            # Create a clean namespace for each code block
            namespace = {}
            
            # Redirect stdout to capture any print statements
            stdout = StringIO()
            try:
                with redirect_stdout(stdout):
                    # Execute the code block with exec()
                    exec(code_block, namespace)
                
                # Print captured output for debugging
                output = stdout.getvalue()
                if output:
                    print(f"Output from code block #{i+1}:\n{output}")
                
                # Test passed if we got here without exceptions
                assert True
                
            except Exception as e:
                print(f"Code block #{i+1} failed with error: {type(e).__name__}: {e}")
                print(f"Code block content:\n{code_block}")
                raise  # Re-raise the exception to fail the test