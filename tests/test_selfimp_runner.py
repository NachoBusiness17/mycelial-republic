"""tests/test_selfimp_runner.py -- Test suite for Autonomous Ring 4 Build Runner."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.selfimp_runner import (
    execute_selfimp_task,
    extract_component_target,
    get_open_tasks,
    load_queue,
)
from tools.quasilocal_boundary_gate import audit_file_content


class TestSelfimpRunner(unittest.TestCase):
    """Test suite for autonomous Ring 4 build runner."""

    def test_extract_component_target(self):
        """Verify extraction of component identifiers from task descriptions."""
        self.assertEqual(
            extract_component_target("Implement boundary flux harness for m021 components"),
            "m021",
        )
        self.assertEqual(
            extract_component_target("Automate verification for m1496 components: wire gate"),
            "m1496",
        )
        self.assertEqual(
            extract_component_target("Fix SI-02 headless subprocess flags"),
            "SI-02",
        )
        self.assertIsNone(extract_component_target("General cleanup task with no component"))

    def test_execute_selfimp_task_structure(self):
        """Verify execution generates clean receipt without forbidden tokens."""
        mock_item = {
            "id": "imp_test_001",
            "task": "Implement automated boundary flux verification harness for m021 components",
        }
        ok, note, receipt = execute_selfimp_task(mock_item)
        self.assertTrue(ok)
        self.assertIn("imp_test_001", note)
        self.assertIn("# selfimp imp_test_001 receipt", receipt)
        self.assertNotIn("\u2014", receipt)
        self.assertNotIn("\u2013", receipt)

    def test_queue_inspection(self):
        """Verify queue loading operates without crashing."""
        all_tasks = load_queue()
        self.assertIsInstance(all_tasks, list)
        open_tasks = get_open_tasks()
        self.assertIsInstance(open_tasks, list)
        self.assertLessEqual(len(open_tasks), len(all_tasks))


def test_standalone():
    """Standalone test runner for pytest-style discovery."""
    t = TestSelfimpRunner()
    t.test_extract_component_target()
    t.test_execute_selfimp_task_structure()
    t.test_queue_inspection()


if __name__ == "__main__":
    unittest.main()
