"""Small 2-D linear-algebra helpers for the transformation pages (14, 17, 18)."""

import numpy as np


def rotation_matrix(theta_deg):
    t = np.deg2rad(theta_deg)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]], dtype=float)


def unit_square():
    """Closed outline of the unit square (first vertex repeated at the end)."""
    return np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)


def transform_points(M, points):
    """Apply M to every row (x, y) of an (n, 2+) point array; extra columns are ignored."""
    return (M @ np.asarray(points)[:, :2].T).T


def det2(M):
    return float(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])
