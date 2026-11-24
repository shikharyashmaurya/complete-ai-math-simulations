"""End-of-page quizzes loaded from quizzes/pNN.json and rendered below each lesson by app.py.

Quiz file schema (UTF-8 JSON)::

    {"page": 24, "questions": [
        {"q": "Markdown question ($LaTeX$ allowed)", "options": ["A", "B", "C"], "answer": 1,
         "explain": "Why option B is right."}
    ]}

3-4 questions, 3-4 unique options each, ``answer`` is the 0-based index of the correct option.
Scores live in ``st.session_state["quiz_scores"]`` (page number -> best fraction correct), so
progress is per browser session and resets when the session ends.
"""

import json
import os
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
QUIZ_DIR = ROOT / "quizzes"
# Overrides QUIZ_DIR when set (used by the tests to point at fixture quizzes).
QUIZ_DIR_ENV = "AI_MATH_QUIZ_DIR"

MIN_QUESTIONS, MAX_QUESTIONS = 3, 4
MIN_OPTIONS, MAX_OPTIONS = 3, 4
PASS_FRACTION = 0.75
SCORES_KEY = "quiz_scores"


def quiz_dir():
    return Path(os.environ.get(QUIZ_DIR_ENV) or QUIZ_DIR)


def quiz_path(page_number):
    return quiz_dir() / f"p{page_number:02d}.json"


def validate_quiz(data, page_number):
    """Return a list of schema problems (empty when the quiz is valid)."""
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]
    errors = []
    if data.get("page") != page_number:
        errors.append(f"'page' is {data.get('page')!r}, expected {page_number}")
    questions = data.get("questions")
    if not isinstance(questions, list) or not MIN_QUESTIONS <= len(questions) <= MAX_QUESTIONS:
        return [*errors, f"'questions' must be a list of {MIN_QUESTIONS}-{MAX_QUESTIONS} items"]
    for i, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            errors.append(f"question {i}: must be an object")
            continue
        for field in ("q", "explain"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"question {i}: '{field}' must be a non-empty string")
        options = item.get("options")
        if (
            not isinstance(options, list)
            or not MIN_OPTIONS <= len(options) <= MAX_OPTIONS
            or not all(isinstance(o, str) and o.strip() for o in options)
        ):
            errors.append(f"question {i}: 'options' must be {MIN_OPTIONS}-{MAX_OPTIONS} non-empty strings")
            continue
        if len({o.strip() for o in options}) != len(options):
            errors.append(f"question {i}: options must be unique")
        answer = item.get("answer")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 0 <= answer < len(options):
            errors.append(f"question {i}: 'answer' must be an index into 'options'")
    return errors


def read_quiz(page_number):
    """Return (quiz, error): (None, None) when there is no quiz file, (None, message) when it is malformed."""
    path = quiz_path(page_number)
    if not path.is_file():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"{path.name}: {exc}"
    errors = validate_quiz(data, page_number)
    if errors:
        return None, f"{path.name}: " + "; ".join(errors)
    return data, None


def load_quiz(page_number):
    """The validated quiz for a page, or None when it is missing or malformed."""
    return read_quiz(page_number)[0]


def best_scores():
    return st.session_state.setdefault(SCORES_KEY, {})


def is_passed(page_number):
    return best_scores().get(page_number, 0.0) >= PASS_FRACTION


def _keys(page_number, count):
    prefix = f"quiz_p{page_number:02d}"
    return prefix, [f"{prefix}_q{i}" for i in range(count)]


def _grade(page_number, quiz):
    prefix, keys = _keys(page_number, len(quiz["questions"]))
    correct = sum(st.session_state.get(k) == q["answer"] for k, q in zip(keys, quiz["questions"]))
    fraction = correct / len(keys)
    st.session_state[f"{prefix}_result"] = correct
    scores = best_scores()
    scores[page_number] = max(scores.get(page_number, 0.0), fraction)


def _reset(page_number, count):
    prefix, keys = _keys(page_number, count)
    for key in [*keys, f"{prefix}_result"]:
        st.session_state.pop(key, None)


def render_quiz(page_number):
    """Show the page's quiz (if it has a valid one) in a bordered box with grading and a reset."""
    quiz, error = read_quiz(page_number)
    if error:
        st.caption(f"⚠️ Quiz unavailable — malformed quiz file ({error})")
        return
    if quiz is None:
        return
    questions = quiz["questions"]
    prefix, keys = _keys(page_number, len(questions))
    result = st.session_state.get(f"{prefix}_result")

    with st.container(border=True):
        st.subheader("🧠 Check your understanding")
        with st.form(f"{prefix}_form", border=False):
            for i, (key, item) in enumerate(zip(keys, questions), start=1):
                st.markdown(f"**Q{i}.** {item['q']}")
                options = item["options"]
                st.radio(
                    f"Q{i}",
                    range(len(options)),
                    index=None,
                    format_func=lambda j, options=options: options[j],
                    key=key,
                    label_visibility="collapsed",
                )
                if result is not None:
                    chosen = st.session_state.get(key)
                    if chosen == item["answer"]:
                        st.success(f"✅ Correct. {item['explain']}")
                    else:
                        lead = "No answer selected." if chosen is None else "Not quite."
                        st.error(f"❌ {lead} Correct answer: {options[item['answer']]}  \n{item['explain']}")
            st.form_submit_button(
                "Check answers", type="primary", key=f"{prefix}_check", on_click=_grade, args=(page_number, quiz)
            )

        if result is not None:
            total = len(questions)
            best = best_scores().get(page_number, 0.0)
            message = f"Score: **{result} / {total}** · best this session: {best:.0%}"
            if result / total >= PASS_FRACTION:
                st.success(f"🎉 {message} — passed!")
            else:
                st.warning(f"{message} — {PASS_FRACTION:.0%} needed to pass. Review the page and try again.")
            st.button("🔄 Try again", key=f"{prefix}_reset", on_click=_reset, args=(page_number, total))
