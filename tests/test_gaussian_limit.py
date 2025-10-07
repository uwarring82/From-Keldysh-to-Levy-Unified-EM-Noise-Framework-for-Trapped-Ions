import numpy as np
import pytest

from unified_noise import ModelParams
from unified_noise.analytics import trace
from unified_noise.solver_me import MasterEquationSolver


def test_smoke_stub_evolve_raises():
    # Minimal parameters (values here are placeholders)
    p = ModelParams(
        m=6.64e-26,  # 40 amu
        omega=2 * np.pi * 2e6,  # 2 MHz
        gamma=2 * np.pi * 5e3,  # 5 kHz
        kBT_eff=4.1e-21,  # room temp ~ kB*T
        lam=0.0,  # no jumps in smoke test
        jump_law="gauss",
        jump_pars={"sigma_p": 1.0},
        nbar_bath=0.05,
    )
    N = 10
    solver = MasterEquationSolver(N=N, params=p)
    # vacuum state ρ0 = |0><0|
    rho0 = np.zeros((N, N), dtype=complex)
    rho0[0, 0] = 1.0
    assert abs(trace(rho0) - 1.0) < 1e-12

    # For now, evolve should raise NotImplementedError (placeholder milestone)
    with pytest.raises(NotImplementedError):
        solver.evolve(rho0, t_grid=[0.0, 1e-6])
