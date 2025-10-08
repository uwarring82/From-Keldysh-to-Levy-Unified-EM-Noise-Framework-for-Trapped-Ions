import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from unified_noise import ModelParams
from unified_noise.solver_me import MasterEquationSolver


def test_evolve_runs_and_shapes():
    p = ModelParams(
        m=6.64e-26,
        omega=2 * np.pi * 2e6,
        gamma=2 * np.pi * 5e3,
        kBT_eff=4.1e-21,
        lam=0.0,
        jump_law="gauss",
        jump_pars={"sigma_p": 1.0},
        nbar_bath=0.05,
    )
    N = 10
    solver = MasterEquationSolver(N=N, params=p)
    rho0 = np.zeros((N, N), dtype=complex)
    rho0[0, 0] = 1.0
    out = solver.evolve(rho0, [0.0, 1e-6, 2e-6])
    assert len(out) == 2
    for rho in out:
        assert rho.shape == (N, N)
        assert np.isclose(np.trace(rho), 1.0, atol=1e-10)
