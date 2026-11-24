"""Unit tests for the shared helpers in common/."""

import warnings

import numpy as np
import pytest

from common.linalg2d import det2
from common.mathutils import close_enough, fmt_signed, sigmoid, softmax
from common.matrix_display import MISSING_CSS, matrix_html, partial_matrix, row_major_cells


@pytest.fixture
def no_warnings():
    with warnings.catch_warnings(), np.errstate(over="raise", invalid="raise", divide="raise"):
        warnings.simplefilter("error")
        yield


class TestSigmoid:
    def test_extremes_do_not_overflow(self, no_warnings):
        out = sigmoid(np.array([-1000.0, 1000.0]))
        assert out[0] == pytest.approx(0.0, abs=1e-300)
        assert out[1] == 1.0
        assert np.all(np.isfinite(out))

    def test_scalar_extremes(self, no_warnings):
        assert sigmoid(-1000) == pytest.approx(0.0, abs=1e-300)
        assert sigmoid(1000) == 1.0
        assert sigmoid(0) == 0.5

    def test_symmetry(self):
        z = np.linspace(-30, 30, 61)
        np.testing.assert_allclose(sigmoid(-z), 1.0 - sigmoid(z), atol=1e-15)


class TestSoftmax:
    def test_sums_to_one_along_axis(self):
        z = np.array([[1.0, 2.0, 3.0], [-5.0, 0.0, 5.0]])
        np.testing.assert_allclose(softmax(z, axis=1).sum(axis=1), 1.0)
        np.testing.assert_allclose(softmax(z, axis=0).sum(axis=0), 1.0)

    def test_shift_invariant_with_large_logits(self, no_warnings):
        z = np.array([1.0, 2.0, 3.0])
        np.testing.assert_allclose(softmax(z + 1000.0), softmax(z))
        np.testing.assert_allclose(softmax(z - 1000.0), softmax(z))


class TestFormatting:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [(-1.5, "- 1.50"), (2.0, "+ 2.00"), (0.0, "+ 0.00"), (-0.0, "+ 0.00"), (-0.001, "- 0.00")],
    )
    def test_fmt_signed(self, value, expected):
        assert fmt_signed(value) == expected

    def test_fmt_signed_precision(self):
        assert fmt_signed(-3.14159, prec=3) == "- 3.142"


class TestCloseEnough:
    def test_scalar_returns_bool(self):
        assert close_enough(0.1 + 0.2, 0.3) is True
        assert close_enough(1.0, 1.1) is False

    def test_array_is_elementwise(self):
        np.testing.assert_array_equal(close_enough(np.array([1.0, 2.0]), np.array([1.0, 2.5])), [True, False])


class TestMatrixDisplay:
    def test_title_is_html_escaped(self):
        html = matrix_html(np.eye(2), "<b>A & B</b>")
        assert "<b>A & B</b>" in html
        assert "<b>A" not in html

    def test_nan_cells_render_as_question_mark(self):
        full = np.array([[1.0, 2.0], [3.0, 4.0]])
        partial = partial_matrix(full, row_major_cells(3, 2, 2))
        html = matrix_html(partial, "Result")
        assert html.count(">?</td>") == 1
        assert html.count(MISSING_CSS) == 1
        assert ">3.00</td>" in html and ">4.00</td>" not in html

    def test_row_major_cells_caps_at_grid_size(self):
        assert row_major_cells(3, 2, 2) == [(0, 0), (0, 1), (1, 0)]
        assert len(row_major_cells(10, 2, 2)) == 4


class TestDet2:
    @pytest.mark.parametrize(
        ("matrix", "expected"),
        [([[1, 0], [0, 1]], 1.0), ([[2, 1], [1, 3]], 5.0), ([[1, 2], [2, 4]], 0.0), ([[0, 1], [1, 0]], -1.0)],
    )
    def test_det2(self, matrix, expected):
        result = det2(np.array(matrix, dtype=float))
        assert isinstance(result, float)
        assert result == pytest.approx(expected)
