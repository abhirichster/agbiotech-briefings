"""Kept for compatibility: renders all briefings and the index. Use scripts/render.py."""
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).with_name("render.py")), run_name="__main__")
