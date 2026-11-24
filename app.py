"""Entry point: groups every lesson in pages/ into curriculum sections."""

import re
import unicodedata
from pathlib import Path

import streamlit as st

from common.quiz import PASS_FRACTION, is_passed, load_quiz, read_quiz, render_quiz

st.set_page_config(page_title="Complete AI Math Simulations", layout="wide")

PAGES_DIR = Path(__file__).parent / "pages"

# (section name, icon, page numbers). Pages are listed by number inside a section,
# so later additions (e.g. 76-78) appear after the original block (1-18).
SECTIONS = [
    ("Vectors & Matrices", "🧭", {*range(1, 19), 76, 77, 78}),
    ("Functions", "⚙️", {*range(19, 23)}),
    ("Probability & Statistics", "🎲", {*range(23, 44), 84, 85, 86, 87, 88}),
    ("Calculus", "📈", {*range(44, 50), 79, 80, 81, 82, 83}),
    ("Optimization", "⛰️", {*range(50, 57), 90, 91, 92}),
    ("Information Theory", "📡", {*range(57, 61), 89}),
    ("Eigenvectors & PCA", "🔍", {*range(61, 64)}),
    ("Neural Networks & ML", "🧠", {*range(64, 76), *range(93, 99)}),
]
OTHER_SECTION = ("More Lessons", "📘")


def slugify(text):
    """Return a lowercase ASCII slug safe to use in a URL path."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def discover_lessons():
    """Yield (number, title, path) for every numbered page, sorted by number."""
    lessons = []
    for path in PAGES_DIR.glob("*.py"):
        match = re.match(r"^(\d+)\s*(.+)$", path.stem)
        if match:
            lessons.append((int(match.group(1)), match.group(2).strip(), path))
    return sorted(lessons)


def section_for(number):
    for name, icon, numbers in SECTIONS:
        if number in numbers:
            return name, icon
    return OTHER_SECTION


# url_path -> page number for every lesson, filled by build_sections().
PAGE_NUMBERS = {}
# section name -> page numbers in that section, filled by build_sections().
SECTION_NUMBERS = {}


def build_sections():
    """Map section name -> (icon, list of st.Page) in curriculum order."""
    grouped = {name: (icon, []) for name, icon, _ in SECTIONS}
    for number, title, path in discover_lessons():
        name, icon = section_for(number)
        grouped.setdefault(name, (icon, []))
        url_path = f"p{number:02d}-{slugify(title)}"
        grouped[name][1].append(
            st.Page(
                f"pages/{path.name}",
                title=f"{number:02d} · {title}",
                icon=icon,
                url_path=url_path,
            )
        )
        PAGE_NUMBERS[url_path] = number
        SECTION_NUMBERS.setdefault(name, []).append(number)
    return {name: value for name, value in grouped.items() if value[1]}


LESSON_SECTIONS = build_sections()


def quiz_progress(numbers):
    """(passed, total) quizzes among the given page numbers; only pages with a valid quiz count."""
    with_quiz = [n for n in numbers if load_quiz(n) is not None]
    return sum(is_passed(n) for n in with_quiz), len(with_quiz)


def show_progress(passed, total, label):
    if total:
        st.progress(passed / total, text=f"{label}: {passed} / {total} quizzes passed")
    else:
        st.caption(f"{label}: no quizzes yet")


def home():
    st.title("🧮 Complete AI Math Simulations")
    st.markdown(
        "Interactive simulations that build the mathematics behind AI and machine "
        "learning one idea at a time — from vectors and probability to gradients, "
        "information theory and neural networks."
    )

    st.subheader("How to use")
    st.markdown(
        "- Work through the lessons **in order**: each page builds on the ones before it.\n"
        "- Use the **sidebar** to jump to any lesson; lessons are grouped by topic.\n"
        "- Move the **sliders and controls** on each page and watch the plots respond.\n"
        "- Come back to this page any time for the curriculum map below."
    )

    st.subheader("Curriculum map")
    total = sum(len(pages) for _, pages in LESSON_SECTIONS.values())
    st.caption(
        f"{total} lessons in {len(LESSON_SECTIONS)} sections. Each lesson ends with a short quiz; "
        f"a quiz counts as passed at {PASS_FRACTION:.0%} or better. Progress is kept for this "
        "browser session only and resets when you close or reload the app."
    )
    columns = st.columns(2)
    for index, (name, (icon, pages)) in enumerate(LESSON_SECTIONS.items()):
        with columns[index % 2]:
            with st.expander(f"{icon} {name} ({len(pages)} lessons)", expanded=index < 2):
                show_progress(*quiz_progress(SECTION_NUMBERS[name]), "Progress")
                for page in pages:
                    st.page_link(page)


home_page = st.Page(home, title="Home", icon="🏠", default=True)
navigation = {"Start": [home_page]}
navigation.update({name: pages for name, (_, pages) in LESSON_SECTIONS.items()})

pg = st.navigation(navigation)
pg.run()

current_number = PAGE_NUMBERS.get(pg.url_path)  # None on Home
if current_number is not None:
    if any(read_quiz(current_number)):  # a quiz, or an error caption for a malformed file
        st.divider()
    render_quiz(current_number)

with st.sidebar:
    show_progress(*quiz_progress(PAGE_NUMBERS.values()), "🧠 Overall")
