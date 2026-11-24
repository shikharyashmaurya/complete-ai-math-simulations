"""Every page, and the app entry point, renders without an uncaught exception."""

import pytest
from streamlit.testing.v1 import AppTest

TIMEOUT = 60
HOME_TITLE = "Complete AI Math Simulations"


def exception_messages(at):
    return "\n\n".join(f"{e.message}\n{''.join(e.stack_trace)}" for e in at.exception)


def test_page_renders(page_path):
    at = AppTest.from_file(str(page_path), default_timeout=TIMEOUT).run()
    assert not at.exception, exception_messages(at)


def test_home_renders(app_file):
    at = AppTest.from_file(str(app_file), default_timeout=TIMEOUT).run()
    assert not at.exception, exception_messages(at)
    assert any(HOME_TITLE in t.value for t in at.title)


@pytest.fixture(scope="module")
def app_test(app_file):
    at = AppTest.from_file(str(app_file), default_timeout=TIMEOUT).run()
    assert not at.exception, exception_messages(at)
    return at


def test_page_reachable_from_app(app_test, page_path):
    """The page is registered in app.py's st.navigation and runs when selected.

    AppTest.switch_page raises ValueError for a page that st.navigation did not register.
    """
    at = app_test.switch_page(f"pages/{page_path.name}").run()
    assert not at.exception, exception_messages(at)
    assert not any(HOME_TITLE in t.value for t in at.title), f"{page_path.name} rendered the Home page"
