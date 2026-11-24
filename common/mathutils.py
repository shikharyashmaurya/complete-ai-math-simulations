"""Numerically stable activation helpers and number formatting shared by several pages."""

import numpy as np


def sigmoid(z):
    """Logistic function 1 / (1 + e^-z) that never overflows, for any sign of z (no clipping)."""
    z = np.asarray(z, dtype=float)
    e = np.exp(-np.abs(z))  # in (0, 1], so neither branch can overflow
    out = np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))
    return out[()]  # NumPy scalar for scalar input, array otherwise


def softmax(z, axis=-1):
    """Softmax along ``axis``; subtracting the max first keeps exp() from overflowing."""
    z = np.asarray(z, dtype=float)
    exps = np.exp(z - np.max(z, axis=axis, keepdims=True))
    return exps / np.sum(exps, axis=axis, keepdims=True)


def fmt_num(x, prec=2):
    return f"{x + 0.0:.{prec}f}"  # + 0.0 turns -0.0 into 0.0


def fmt_factor(x, prec=2):
    """Number for a product term, negatives in parentheses: 2.00 × (-3.00)."""
    text = fmt_num(x, prec)
    return f"({text})" if x < 0 else text


def fmt_signed(x, prec=2):
    """'+ 1.50' or '- 1.50', for writing sums like 'a + b' without '+ -1.50'."""
    return f"- {fmt_num(abs(x), prec)}" if x < 0 else f"+ {fmt_num(x, prec)}"


def close_enough(a, b, rtol=1e-05, atol=1e-08):
    """np.isclose with its default tolerances; plain bool for scalar inputs."""
    result = np.isclose(a, b, rtol=rtol, atol=atol)
    return bool(result) if np.ndim(result) == 0 else result
