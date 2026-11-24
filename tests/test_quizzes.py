"""Quiz files in quizzes/ match the schema, and app.py renders and grades a page's quiz."""

import json
import re

import pytest
from streamlit.testing.v1 import AppTest

from common.quiz import QUIZ_DIR, QUIZ_DIR_ENV, validate_quiz
from tests.conftest import page_files, page_number

TIMEOUT = 60


def quiz_files():
    return sorted(QUIZ_DIR.glob("p*.json"))


def quiz_page_number(path):
    match = re.fullmatch(r"p(\d{2,})", path.stem)
    return int(match.group(1)) if match else None


@pytest.mark.parametrize("quiz_path", quiz_files(), ids=lambda p: p.stem)
def test_quiz_file_matches_schema(quiz_path):
    number = quiz_page_number(quiz_path)
    assert number is not None, f"{quiz_path.name}: expected pNN.json"
    data = json.loads(quiz_path.read_text(encoding="utf-8"))
    assert validate_quiz(data, number) == []
    assert any(page_number(p) == number for p in page_files()), f"no page file for {quiz_path.name}"


def test_every_page_has_a_quiz():
    missing = [p.name for p in page_files() if not (QUIZ_DIR / f"p{page_number(p):02d}.json").is_file()]
    assert not missing, f"pages without a quiz file: {missing}"


@pytest.mark.parametrize(
    "mutate, problem",
    [
        (lambda d: d.update(page=2), "'page'"),
        (lambda d: d["questions"].pop(), "'questions'"),
        (lambda d: d["questions"][0].update(answer=3), "'answer'"),
        (lambda d: d["questions"][0].update(answer=True), "'answer'"),
        (lambda d: d["questions"][0]["options"].append("A"), "unique"),
        (lambda d: d["questions"][0].update(options=["A", "B"]), "'options'"),
        (lambda d: d["questions"][0].update(explain=""), "'explain'"),
    ],
)
def test_validate_quiz_rejects_malformed(mutate, problem):
    data = fixture_quiz(1)
    assert validate_quiz(data, 1) == []
    mutate(data)
    assert any(problem in error for error in validate_quiz(data, 1))


def fixture_quiz(number):
    return {
        "page": number,
        "questions": [
            {"q": f"Question {i} with $x^{i}$?", "options": ["A", "B", "C"], "answer": i % 3, "explain": f"Because {i}."}
            for i in range(3)
        ],
    }


@pytest.fixture
def quiz_dir(tmp_path, monkeypatch):
    monkeypatch.setenv(QUIZ_DIR_ENV, str(tmp_path))
    return tmp_path


@pytest.fixture
def first_page():
    return page_files()[0]


def open_page(app_file, page):
    at = AppTest.from_file(str(app_file), default_timeout=TIMEOUT).run()
    at.switch_page(f"pages/{page.name}").run()
    assert not at.exception
    return at


def test_app_renders_and_grades_quiz(app_file, quiz_dir, first_page):
    number = page_number(first_page)
    prefix = f"quiz_p{number:02d}"
    (quiz_dir / f"p{number:02d}.json").write_text(json.dumps(fixture_quiz(number)), encoding="utf-8")

    at = open_page(app_file, first_page)
    assert any("Check your understanding" in h.value for h in at.subheader)
    radio = at.radio(key=f"{prefix}_q0")
    assert radio.value is None and radio.options == ["A", "B", "C"]

    # Two of three right (q0 answer 0, q1 answer 1; q2 left blank) -> 67 %, not passed.
    at.radio(key=f"{prefix}_q0").set_value(0)
    at.radio(key=f"{prefix}_q1").set_value(1)
    at.button(key=f"{prefix}_check").click().run()
    assert not at.exception
    assert len(at.success) >= 2 and any("No answer selected" in e.value for e in at.error)
    assert any("2 / 3" in w.value for w in at.warning)
    assert at.session_state["quiz_scores"][number] == pytest.approx(2 / 3)

    at.button(key=f"{prefix}_reset").click().run()
    assert at.radio(key=f"{prefix}_q0").value is None
    assert not any("Score" in w.value for w in at.warning)

    for i, answer in enumerate([0, 1, 2]):
        at.radio(key=f"{prefix}_q{i}").set_value(answer)
    at.button(key=f"{prefix}_check").click().run()
    assert any("3 / 3" in s.value and "passed" in s.value for s in at.success)
    assert at.session_state["quiz_scores"][number] == 1.0

    home = AppTest.from_file(str(app_file), default_timeout=TIMEOUT)
    home.session_state["quiz_scores"] = {number: 1.0}
    home.run()  # Home shows the passed quiz in its section progress
    assert not home.exception
    assert any("1 / 1 quizzes passed" in (p.proto.text or "") for p in home.get("progress"))


def test_missing_or_malformed_quiz_does_not_crash(app_file, quiz_dir, first_page):
    number = page_number(first_page)
    at = open_page(app_file, first_page)
    assert not any("Check your understanding" in h.value for h in at.subheader)

    (quiz_dir / f"p{number:02d}.json").write_text("{not json", encoding="utf-8")
    at = open_page(app_file, first_page)
    assert any("malformed quiz file" in c.value for c in at.caption)
