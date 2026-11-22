import shutil
import os
from pathlib import Path


source = Path(__file__).resolve().parent / "entry.png"
output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
output_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, output_dir / "entry.png")
