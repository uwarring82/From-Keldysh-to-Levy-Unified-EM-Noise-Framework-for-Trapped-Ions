from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ModelParams:
    """
    Minimal model parameters for Phase-1 (Backend 1).

    m: ion mass [kg]
    omega: trap frequency [rad/s]
    gamma: damping rate [1/s]
    kBT_eff: effective bath temperature [J] (maps to Gaussian diffusion)
    lam: Poisson jump rate [1/s]
    jump_law: 'gauss' | 'laplace' | 'stable' | 'table' | 'langevin' (future use)
    jump_pars: dict of jump-law parameters
    nbar_bath: optional Lindblad mapping for quantum baths
    """

    m: float
    omega: float
    gamma: float
    kBT_eff: float
    lam: float
    jump_law: str
    jump_pars: Dict[str, float]
    nbar_bath: float = 0.0
