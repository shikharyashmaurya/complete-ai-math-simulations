"""Static checks on the page sources: syntax, banned patterns, file names and widget keys."""

import ast
import re
import warnings
from collections import defaultdict

import pytest

BANNED_PATTERNS = [
    "use_container_width",  # deprecated: use width="stretch"
    "components.html(",  # embed labs with st.iframe
    "fonts.googleapis",  # no external fonts
    "file:///",  # local paths do not work once deployed
    "np.random.seed(",  # use a seeded Generator kept in session state
]

# Widget / session-state keys that are deliberately not page-prefixed: {"<page file name>": {"key", ...}}.
KEY_PREFIX_ALLOWLIST = {}


def page_number(path):
    match = re.match(r"\d+", path.name)
    return int(match.group()) if match else None


def page_prefix(path):
    return f"p{page_number(path):02d}_"


def test_app_compiles_without_syntax_warnings(app_file):
    with warnings.catch_warnings():
        warnings.simplefilter("error", SyntaxWarning)
        compile(app_file.read_text(encoding="utf-8"), str(app_file), "exec")


def test_page_compiles_without_syntax_warnings(page_path):
    """Invalid escape sequences (e.g. "\\sigma" outside a raw string) are SyntaxWarnings."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", SyntaxWarning)
        compile(page_path.read_text(encoding="utf-8"), str(page_path), "exec")


@pytest.mark.parametrize("pattern", BANNED_PATTERNS)
def test_no_banned_patterns(all_pages, app_file, pattern):
    offenders = [p.name for p in [app_file, *all_pages] if pattern in p.read_text(encoding="utf-8")]
    assert not offenders, f"{pattern!r} found in: {offenders}"


def test_page_file_names_have_no_stray_whitespace(all_pages):
    offenders = [p.name for p in all_pages if p.stem != p.stem.strip()]
    assert not offenders


def test_page_file_names_have_number_prefix(all_pages):
    offenders = [p.name for p in all_pages if page_number(p) is None]
    assert not offenders


def test_page_numbers_are_unique(all_pages):
    by_number = defaultdict(list)
    for p in all_pages:
        by_number[page_number(p)].append(p.name)
    duplicates = {n: names for n, names in by_number.items() if len(names) > 1}
    assert not duplicates


def _literal_keys(tree):
    """(line, key) for every string-literal widget key or session_state key in the module.

    For f-strings only the leading literal part is checked (e.g. f"p15_i_{n}" -> "p15_i_").
    """

    def literal(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr) and node.values and isinstance(node.values[0], ast.Constant):
            return node.values[0].value
        return None

    def is_session_state(node):
        return ast.unparse(node).endswith("session_state")

    for node in ast.walk(tree):
        candidate = None
        if isinstance(node, ast.keyword) and node.arg == "key":
            candidate = node.value
        elif isinstance(node, ast.Subscript) and is_session_state(node.value):
            candidate = node.slice
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"get", "setdefault", "pop"}
            and is_session_state(node.func.value)
            and node.args
        ):
            candidate = node.args[0]
        elif (
            isinstance(node, ast.Compare)
            and isinstance(node.ops[0], (ast.In, ast.NotIn))
            and is_session_state(node.comparators[0])
        ):
            candidate = node.left
        key = literal(candidate) if candidate is not None else None
        if key is not None:
            yield candidate.lineno, key


def test_keys_are_page_prefixed(page_path):
    """Widget and session_state keys start with the page's own prefix (pNN_) so pages never collide."""
    prefix = page_prefix(page_path)
    allowed = KEY_PREFIX_ALLOWLIST.get(page_path.name, set())
    tree = ast.parse(page_path.read_text(encoding="utf-8"))
    offenders = [
        f"line {line}: {key!r}" for line, key in _literal_keys(tree) if not key.startswith(prefix) and key not in allowed
    ]
    assert not offenders, f"keys without the {prefix!r} prefix: {offenders}"


def _string_arg_calls(tree, func_names):
    """(line, function name, first argument) for every call to one of func_names (bare or attribute call).

    The first argument is the string literal, or None when it is not a literal.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else None
        if name in func_names:
            arg = node.args[0]
            value = arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else None
            yield node.lineno, name, value


def test_load_lab_targets_exist(page_path, repo_root):
    """Every load_lab("name") call refers to an existing assets/labs/name.html file."""
    labs_dir = repo_root / "assets" / "labs"
    tree = ast.parse(page_path.read_text(encoding="utf-8"))
    offenders = [
        f"line {line}: {name!r}"
        for line, _, name in _string_arg_calls(tree, {"load_lab"})
        if name is None or not (labs_dir / f"{name}.html").is_file()
    ]
    assert not offenders, f"load_lab calls without a matching assets/labs/*.html file: {offenders}"


def test_page_link_targets_exist(page_path, repo_root):
    """Every (safe_)page_link("pages/<file>.py", ...) points at an existing page file.

    safe_page_link silently degrades to a caption for unknown pages, so a typo would otherwise go unnoticed.
    """
    tree = ast.parse(page_path.read_text(encoding="utf-8"))
    offenders = [
        f"line {line}: {target!r}"
        for line, _, target in _string_arg_calls(tree, {"page_link", "safe_page_link"})
        if target is None or not (target.startswith("pages/") and (repo_root / target).is_file())
    ]
    assert not offenders, f"page links to missing pages: {offenders}"
