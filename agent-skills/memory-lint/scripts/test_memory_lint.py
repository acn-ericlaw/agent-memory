import unittest
import importlib.util
from pathlib import Path
import sys

# Load memory-lint.py dynamically since it has a hyphen in the name
script_path = Path(__file__).parent / "memory-lint.py"
spec = importlib.util.spec_from_file_location("memory_lint", str(script_path))
memory_lint = importlib.util.module_from_spec(spec)
sys.modules["memory_lint"] = memory_lint
spec.loader.exec_module(memory_lint)

class TestMemoryLint(unittest.TestCase):
    def test_pinned_open_threads_flat(self):
        text = """
- [ ] Parent task
  <!-- id: t1 -->
- [x] Done task
  <!-- id: t2 -->
"""
        self.assertEqual(memory_lint.pinned_open_threads(text), {"t1"})

    def test_pinned_open_threads_nested(self):
        # Nested list inside an open thread
        text = """
- [ ] Parent task
  - Subtask 1
  - Subtask 2
  <!-- id: t3 -->
"""
        self.assertEqual(memory_lint.pinned_open_threads(text), {"t3"})

    def test_pinned_open_threads_nested_open(self):
        text = """
- [ ] Parent task
  - [ ] Nested open
    <!-- id: t4 -->
"""
        self.assertEqual(memory_lint.pinned_open_threads(text), {"t4"})

    def test_pinned_open_threads_sibling_reset(self):
        text = """
- [ ] Parent task
  <!-- id: t5 -->
- Regular bullet that should reset
  <!-- id: t6 -->
"""
        self.assertEqual(memory_lint.pinned_open_threads(text), {"t5"})

    def test_pinned_open_threads_mixed(self):
        text = """
- [ ] Open task 1
  - Subtask
  <!-- id: mix-1 -->
- [x] Done task
  <!-- id: mix-2 -->
- [ ] Open task 2
  <!-- id: mix-3 -->
- Regular sub-bullet
  <!-- id: mix-4 -->
"""
        self.assertEqual(memory_lint.pinned_open_threads(text), {"mix-1", "mix-3"})

if __name__ == "__main__":
    unittest.main()
