from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class GdkTableTests(unittest.TestCase):
    def test_macro_argument_spacing_preserves_all_rows(self):
        guid = '"01234567-89ab-cdef-0123-456789abcdef"'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir()
            generator = scripts / "gen_gdk_table.py"
            shutil.copyfile(Path(__file__).with_name(generator.name), generator)
            output = root / "crates/xcl/src/hle/xgameruntime/gdk_table.rs"
            output.parent.mkdir(parents=True)
            source = root / "input.txt"
            source.write_text(
                f"NAME(First, {guid}, {guid}, 3)\n"
                f"NAME( Second ,\t{guid},  {guid},4 )\n",
                encoding="utf-8",
            )
            subprocess.run([sys.executable, str(generator), str(source)], check=True, capture_output=True)
            generated = output.read_text(encoding="utf-8")
            self.assertIn('("First",', generated)
            self.assertIn('("Second",', generated)
