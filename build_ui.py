import os
import sys
import tempfile
from pathlib import Path

from calibre.build_forms import build_forms, find_forms

if len(sys.argv) < 2:
    print("Error: Missing target source directory argument.", file=sys.stderr)
    sys.exit(1)

#src_dir = Path(os.path.dirname(__file__), "calibre-plugin")
src_dir = Path(sys.argv[1]).resolve()

if not src_dir.exists():
    print(f"Error: Path does not exist: {src_dir}", file=sys.stderr)
    sys.exit(1)

print(f"Looking in path: {src_dir}")

with tempfile.TemporaryDirectory(suffix="robchio") as tmp_dir_str: # TODO: why use temp dir?
    tmp_dir = Path(tmp_dir_str)
    target_dir = Path(tmp_dir, "calibre", "gui2")
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(src_dir, target_dir, target_is_directory=True)
    print(f"Symlinked {src_dir} to {target_dir}")

    forms_to_build = find_forms(tmp_dir)
    print(f"Found forms: {forms_to_build}")

    build_forms(tmp_dir, summary=True, check_icons=False)