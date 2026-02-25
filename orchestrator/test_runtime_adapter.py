import tempfile
import unittest
from pathlib import Path

from orchestrator.runtime_adapter import (
    Invocation,
    ShellAdapter,
    resolve_runtime_adapter,
)


class RuntimeAdapterTests(unittest.TestCase):
    def test_unknown_adapter_falls_back_to_shell(self):
        adapter, warnings = resolve_runtime_adapter("does-not-exist")
        self.assertEqual(adapter.name, "shell")
        self.assertGreater(len(warnings), 0)

    def test_shell_adapter_non_strict_simulates_sdd_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            inv = Invocation(
                task_id="x",
                agent="sdd-ba",
                command="sdd-unknown-task --task_id=x",
                feature_path=Path(tmp),
                strict=False,
                timeout_seconds=30,
                env={},
            )
            result = ShellAdapter().invoke(inv)
            self.assertTrue(result.success)
            self.assertEqual(result.error_type, "NONE")

    def test_shell_adapter_runs_real_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            inv = Invocation(
                task_id="x",
                agent="sdd-ba",
                command="python3 -c \"open('ok.txt','w').write('ok')\"",
                feature_path=Path(tmp),
                strict=True,
                timeout_seconds=30,
                env={},
            )
            result = ShellAdapter().invoke(inv)
            self.assertTrue(result.success)
            self.assertTrue((Path(tmp) / "ok.txt").exists())


if __name__ == "__main__":
    unittest.main()
