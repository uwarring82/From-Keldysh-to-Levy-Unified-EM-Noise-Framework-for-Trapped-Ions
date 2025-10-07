from typing import Callable, Iterable

import numpy as np

from .operators import harmonic_ops, jump_superoperator_stub
from .params import ModelParams


class MasterEquationSolver:
    """
    Backend 1 (stub): Assembles a matrix-free Liouvillian and evolves ρ(t).
    Next PR will replace placeholders with:
      - sparse Kronecker actions for H, D[a], D[a†]
      - kick superoperator built from characteristic function of jump law
      - Krylov expm_multiply propagation
    """

    def __init__(self, N: int, params: ModelParams):
        self.N = int(N)
        self.params = params
        # Build basic ops (placeholders for now)
        self.n, self.a, self.adag, self.H = harmonic_ops(self.N, params.omega)
        self._L_H = self._liouvillian_commutator(self.H)
        self._L_jump = jump_superoperator_stub(self.N)

    @staticmethod
    def _liouvillian_commutator(H) -> Callable[[np.ndarray], np.ndarray]:
        """
        Return matrix-free action of -i(I⊗H - Hᵀ⊗I) on vec(ρ).
        NOTE: placeholder uses dense arrays; will be swapped for sparse matvec.
        """
        identity = np.eye(H.shape[0], dtype=complex)
        L = -1j * (np.kron(identity, H) - np.kron(H.T, identity))

        def matvec(y: np.ndarray) -> np.ndarray:
            return L @ y

        return matvec

    def liouvillian(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        Full Liouvillian matvec y ↦ L@y.
        Currently includes only Hamiltonian term; jump is zero-op placeholder.
        """

        def L(y: np.ndarray) -> np.ndarray:
            return self._L_H(y) + self._L_jump(y)

        return L

    def evolve(self, rho0: np.ndarray, t_grid: Iterable[float]):
        """
        Validate shapes and deliberately raise NotImplementedError to mark
        the next milestone (Krylov expm_multiply integration).
        """
        N = self.N
        rho0 = np.asarray(rho0, dtype=complex)
        assert rho0.shape == (N, N), "rho0 must be NxN"
        t_grid = np.asarray(list(t_grid), dtype=float)
        assert np.all(np.diff(t_grid) >= 0), "t_grid must be non-decreasing"
        # Next PR: loop over dt and apply expm_multiply(dt * L, vec(rho)).
        raise NotImplementedError("Time propagation not yet implemented (next step).")
