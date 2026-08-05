"""
Makes `import doda` work from tests/ without needing `pip install -e .`.
Adds src/ to the path once, automatically, for every test run.
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))
