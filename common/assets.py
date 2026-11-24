"""Load self-contained HTML labs from assets/labs."""
from pathlib import Path
from string import Template

LABS_DIR = Path(__file__).resolve().parents[1] / "assets" / "labs"


def load_lab(name: str, **values) -> str:
    """Return assets/labs/<name>.html; substitute $placeholders from values (string.Template, $$ = literal $)."""
    text = (LABS_DIR / f"{name}.html").read_text(encoding="utf-8")
    return Template(text).substitute(**values) if values else text
