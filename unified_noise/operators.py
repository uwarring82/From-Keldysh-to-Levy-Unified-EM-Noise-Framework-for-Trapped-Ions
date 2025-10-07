import numpy as np


def harmonic_ops(N: int, omega: float):
    """
    Return number operator n, creation a†, annihilation a, and H = ħω(n+1/2).
    NOTE: placeholder; replace with sparse implementations in the next step.
    """
    n = np.diag(np.arange(N))
    a = np.zeros((N, N), dtype=complex)
    for k in range(1, N):
        a[k - 1, k] = np.sqrt(k)
    adag = a.conj().T
    hbar = 1.054_571_817e-34
    H = hbar * omega * (n + 0.5 * np.eye(N))
    return n, a, adag, H


def jump_superoperator_stub(N: int):
    """
    Placeholder for the Poisson/Lévy kick superoperator.
    Returns a callable matvec (y ↦ L_jump @ y) that currently does nothing.
    """

    def matvec(y):
        # No-op for now; to be implemented:
        # average over U_{Δp} ρ U_{Δp}† minus ρ, weighted by ν(Δp).
        return np.zeros_like(y)

    return matvec
