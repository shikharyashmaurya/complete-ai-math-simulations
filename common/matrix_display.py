"""HTML matrix/vector cards and cell-by-cell reveal helpers for the matrix pages (11–18)."""

from html import escape

import numpy as np

# Card (outer box) styles used by the pages.
CARD_THEMES = {
    "lab": "padding:12px;border:1px solid #475569;border-radius:12px;background:rgba(148,163,184,0.08);",
    "slate": "padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;",
}
MISSING_CSS = "opacity:0.6;font-style:italic;"


def format_entry(value, precision):
    """Fixed-point text for one entry. NaN means "not solved yet" and is shown as '?'."""
    if np.isnan(value):
        return "?"
    return f"{value + 0.0:.{precision}f}"  # + 0.0 turns -0.0 into 0.0


def _highlight_css(highlighted, color, cell_style):
    if cell_style == "fill":
        # Explicit colours on every cell; dark text keeps bright fills readable in light and dark themes.
        bg, fg = (color, "#0f172a") if highlighted else ("transparent", "inherit")
        return f"background:{bg};color:{fg};"
    if cell_style == "bold":
        if highlighted:
            return f"background:{color};color:#0b1020;font-weight:700;"
        return "background:transparent;"
    if cell_style == "plain":
        return ""
    raise ValueError(f"unknown cell_style {cell_style!r}")


def matrix_html(
    matrix,
    title,
    highlight=None,
    color="#38bdf8",
    *,
    precision=2,
    font_size=18,
    cell_padding="7px 10px",
    min_width=42,
    theme="slate",
    cell_style="bold",
    title_color=None,
    text_color=None,
    margin_bottom=None,
):
    """HTML card with a title and a bordered table of the entries of a 2-D array.

    highlight: iterable of (row, col) cells painted with ``color``.
    cell_style: "fill" (highlight = fill + dark text, other cells get explicit transparent/inherit),
        "bold" (highlight = fill + bold dark text) or "plain" (no per-cell colours, highlight ignored).
    NaN entries render as an italic, faded "?" (a cell that is not solved yet).
    """
    matrix = np.asarray(matrix, dtype=float)
    rows, cols = matrix.shape
    highlight = set(highlight or ())
    card = CARD_THEMES[theme] + (f"margin-bottom:{margin_bottom};" if margin_bottom else "")
    h4 = "margin:0 0 8px 0;" + (f"color:{title_color};" if title_color else "")
    table = f"border-collapse:collapse;font-size:{font_size}px;" + (f"color:{text_color};" if text_color else "")
    # The indentation is removed by st.markdown's dedent; every line keeps at least 4 leading spaces.
    html = (
        f'\n    <div style="{card}">\n'
        f'      <h4 style="{h4}">{escape(title)}</h4>\n'
        f'      <table style="{table}">\n    '
    )
    for i in range(rows):
        html += "<tr>"
        for j in range(cols):
            text = format_entry(matrix[i, j], precision)
            extra = MISSING_CSS if text == "?" else ""
            css = _highlight_css((i, j) in highlight, color, cell_style)
            html += (
                f"<td style='border:1px solid #475569;padding:{cell_padding};text-align:center;"
                f"min-width:{min_width}px;{css}{extra}'>{text}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


def vector_html(vector, title, highlight=None, color="#38bdf8", **style):
    """Like matrix_html for a column vector; highlight is an iterable of entry indices."""
    column = np.asarray(vector, dtype=float).reshape(-1, 1)
    return matrix_html(column, title, [(i, 0) for i in (highlight or ())], color, **style)


def row_major_cells(step, rows, cols):
    """The first ``step`` cells of a rows x cols grid in reading order (row by row)."""
    return [divmod(idx, cols) for idx in range(min(step, rows * cols))]


def partial_matrix(full, cells):
    """Copy of ``full`` where only ``cells`` are filled in and every other entry is NaN ("?")."""
    partial = np.full_like(full, np.nan, dtype=float)
    for r, c in cells:
        partial[r, c] = full[r, c]
    return partial
