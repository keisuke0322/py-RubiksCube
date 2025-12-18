# ルービックキューブシミュレーター
"""
ルービックキューブをシミュレートするPythonアプリケーション
"""

from .cube import Cube
from .solver import Solver

__version__ = "1.0.0"
__all__ = ["Cube", "Solver"]
