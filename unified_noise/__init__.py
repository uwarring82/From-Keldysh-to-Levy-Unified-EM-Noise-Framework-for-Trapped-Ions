"""
unified_noise: numerical backends for the unified EM-noise framework.

Phase-1 focus: Backend 1 (Master-Equation / Wigner) scaffold.
"""

from .params import ModelParams  # re-export for convenience

__all__ = ["ModelParams"]
__version__ = "0.1.0"
