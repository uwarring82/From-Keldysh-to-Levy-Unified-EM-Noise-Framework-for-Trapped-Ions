import numpy as np


def trace(rho: np.ndarray) -> complex:
    return np.trace(rho)


def n_expectation(rho: np.ndarray, n_op: np.ndarray) -> float:
    return float(np.real(np.trace(rho @ n_op)))
