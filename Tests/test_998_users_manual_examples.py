"""
Executes every ` ```python ` code block in `docs/USERS_MANUAL.md` under
a clean namespace and asserts each one runs without raising.

Companion to `Tests/test_999_readme_examples.py`; see that file for the
older, near-identical pattern applied to `README.md`.

Landed by `docs/plans/PL-01_C_and_D_Standards_Update.md` Phase 1.
"""
import os
import re
from contextlib import redirect_stdout
from io import StringIO

import pytest


class TestActualUsersManualExamples:
    """
    Tests that execute the actual Python code blocks from docs/USERS_MANUAL.md.
    """

    @pytest.fixture
    def manual_content(self):
        """Read the docs/USERS_MANUAL.md file content."""
        manual_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "USERS_MANUAL.md",
        )
        with open(manual_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_python_code_blocks(self, manual_content):
        """Extract and test all Python code blocks from docs/USERS_MANUAL.md."""
        # Match fenced code blocks that start with ```python and end with ```.
        # Non-`python` fences (bash, powershell, plain ```) are ignored so that
        # shell recipes and grammar snippets do not enter the test.
        code_block_pattern = r"```python\s+(.*?)\s+```"
        code_blocks = re.findall(code_block_pattern, manual_content, re.DOTALL)

        assert len(code_blocks) > 0, "No Python code blocks found in USERS_MANUAL.md"

        for i, code_block in enumerate(code_blocks):
            print(f"\nTesting USERS_MANUAL code block #{i + 1}:")

            # Clean namespace per block — no cross-block state leakage.
            namespace = {}

            stdout = StringIO()
            try:
                with redirect_stdout(stdout):
                    exec(code_block, namespace)

                output = stdout.getvalue()
                if output:
                    print(f"Output from code block #{i + 1}:\n{output}")

                assert True

            except Exception as e:
                print(f"Code block #{i + 1} failed with error: {type(e).__name__}: {e}")
                print(f"Code block content:\n{code_block}")
                raise
        return
