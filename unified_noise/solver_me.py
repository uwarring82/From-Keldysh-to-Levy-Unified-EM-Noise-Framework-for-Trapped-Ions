from __future__ import annotations

import numpy as np
from typing import Callable, Iterable, List, Optional
from scipy.sparse.linalg import LinearOperator, expm_multiply

from .params import ModelParams


def _ladder_ops(N: int):
    """Return (n_op, a, adag) in the truncated Fock basis (dense for now)."""
    n = np.diag(np.arange(N, dtype=float))
    a = np.zeros((N, N), dtype=complex)
    for k in range(1, N):
        a[k - 1, k] = np.sqrt(k)
    adag = a.conj().T
    return n, a, adag


class MasterEquationSolver:
    """
    Matrix-free master-equation solver for one harmonic mode:
      dρ/dt = -i/ħ [H, ρ] + κ[(n̄+1) D[a] + n̄ D[a†]] + (optional) L_jump[ρ]
    with D[L]ρ = LρL† - 1/2 {L†L, ρ}.
    """

    def __init__(self, N: int, params: ModelParams):
        self.N = int(N)
        self.p = params

        # Map params → solver rates
        self.hbar = 1.054_571_817e-34
        self.omega = float(self.p.omega)
        self.kappa = float(getattr(self.p, "gamma", 0.0))
        self.nbar = float(getattr(self.p, "nbar_bath", 0.0))

        # Operators
        self.n_op, self.a, self.adag = _ladder_ops(self.N)
        self.H = self.hbar * self.omega * (self.n_op + 0.5 * np.eye(self.N))

        # Composites
        self._adag_a = self.adag @ self.a   # a† a
        self._a_adag = self.a @ self.adag   # a a†

        # Optional jump term: callable(y_vec) -> y_vec
        self._L_jump_matvec: Optional[Callable[[np.ndarray], np.ndarray]] = None
        self._L_jump_rmatvec: Optional[Callable[[np.ndarray], np.ndarray]] = None

        # Build Liouvillian LinearOperator
        self._L = self._build_liouvillian()

    # --- Public API ---

    def liouvillian(self) -> LinearOperator:
        return self._L

    def set_jump_matvec(self, matvec_callable, rmatvec_callable=None) -> None:
        """Install custom jump superoperator acting on vec(ρ).

        Parameters
        ----------
        matvec_callable : callable
            Function implementing y ↦ L_jump@y.
        rmatvec_callable : callable, optional
            Function implementing y ↦ L_jump†@y. Required for Krylov propagation.
        """
        if matvec_callable is None:
            self._L_jump_matvec = None
            self._L_jump_rmatvec = None
        else:
            if rmatvec_callable is None:
                raise ValueError("set_jump_matvec requires both matvec and rmatvec callables")
            self._L_jump_matvec = matvec_callable
            self._L_jump_rmatvec = rmatvec_callable
        self._L = self._build_liouvillian()  # refresh closure

    def evolve(self, rho0: np.ndarray, t_grid: Iterable[float]) -> List[np.ndarray]:
        """
        Piecewise-constant propagation using expm_multiply over each Δt.
        Returns: [ρ(t1), ρ(t2), ..., ρ(t_end)] (no ρ(t0) duplicate).
        """
        N = self.N
        rho0 = np.asarray(rho0, dtype=complex)
        if rho0.shape != (N, N):
            raise ValueError(f"rho0 must be shape ({N}, {N})")

        t = np.asarray(list(t_grid), dtype=float)
        if np.any(np.diff(t) < 0):
            raise ValueError("t_grid must be non-decreasing")

        y = self._vec(rho0)
        out: List[np.ndarray] = []
        for dt in np.diff(t):
            if dt == 0.0:
                out.append(self._unvec(y))
                continue
            y = expm_multiply(self._L, y, start=0.0, stop=dt, num=2)[-1]
            rho = self._unvec(y)
            # tiny renormalization guard
            tr = np.trace(rho)
            if abs(tr - 1.0) > 1e-12:
                rho = rho / tr
                y = self._vec(rho)
            out.append(rho)
        return out

    # --- Internals ---

    def _build_liouvillian(self) -> LinearOperator:
        """
        Build a matrix-free LinearOperator for 𝓛 acting on vec(ρ):
          𝓛 = 𝓛_H + 𝓛_G + (optional) 𝓛_jump
        """
        N = self.N
        hbar = self.hbar
        H = self.H
        a, adag = self.a, self.adag
        adag_a, a_adag = self._adag_a, self._a_adag
        kappa, nbar = self.kappa, self.nbar
        have_bath = kappa != 0.0
        L_jump = self._L_jump_matvec  # may be None
        L_jump_adj = self._L_jump_rmatvec

        def matvec(y: np.ndarray) -> np.ndarray:
            rho = self._unvec(y)

            # Hamiltonian commutator: -i/ħ (Hρ - ρH)
            L_rho = (-1j / hbar) * (H @ rho - rho @ H)

            # Gaussian bath (Lindblads)
            if have_bath:
                # D[a]ρ
                a_rho = a @ rho
                D_a = a_rho @ adag - 0.5 * (adag_a @ rho + rho @ adag_a)
                # D[a†]ρ
                adag_rho = adag @ rho
                D_adag = adag_rho @ a - 0.5 * (a_adag @ rho + rho @ a_adag)
                L_rho += kappa * ((nbar + 1.0) * D_a + nbar * D_adag)

            # Optional jump term (already defined on vec)
            if L_jump is not None:
                L_rho += self._unvec(L_jump(self._vec(rho)))

            return self._vec(L_rho)

        def rmatvec(y: np.ndarray) -> np.ndarray:
            sigma = self._unvec(y)

            # Adjoint of Hamiltonian commutator: +i/ħ [H, σ]
            Ld_sigma = (1j / hbar) * (H @ sigma - sigma @ H)

            if have_bath:
                # D[a]†σ
                adag_sigma = adag @ sigma
                D_a_dag = adag_sigma @ a - 0.5 * (adag_a @ sigma + sigma @ adag_a)
                # D[a†]†σ
                a_sigma = a @ sigma
                D_adag_dag = a_sigma @ adag - 0.5 * (a_adag @ sigma + sigma @ a_adag)
                Ld_sigma += kappa * ((nbar + 1.0) * D_a_dag + nbar * D_adag_dag)

            if L_jump_adj is not None:
                Ld_sigma += self._unvec(L_jump_adj(self._vec(sigma)))

            return self._vec(Ld_sigma)

        dim = N * N
        return LinearOperator((dim, dim), matvec=matvec, rmatvec=rmatvec, dtype=complex)

    # vec/unvec (column-major for Kronecker-style consistency)
    def _vec(self, rho: np.ndarray) -> np.ndarray:
        return np.asarray(rho, dtype=complex, order="F").reshape(-1, order="F")

    def _unvec(self, y: np.ndarray) -> np.ndarray:
        return np.asarray(y, dtype=complex).reshape((self.N, self.N), order="F")
