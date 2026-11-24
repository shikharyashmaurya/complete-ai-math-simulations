"""Widget fuzz: every page survives each widget being pushed to its extremes.

For each page: a base run, then (each on a fresh AppTest) every slider at min/max, every
number_input at min/max/0, every selectbox/radio option, a click on every button and a flip of
every checkbox/toggle. Any uncaught exception in the page, or a harness error, fails the test.
"""

import pytest
from streamlit.testing.v1 import AppTest

TIMEOUT = 60
UNBOUNDED = 1e6  # stand-in extreme for a number_input without min/max


def _slider_mutations(base):
    for i, s in enumerate(base.slider):
        for which in ("min", "max"):
            def mutate(at, i=i, which=which):
                w = at.slider[i]
                w.set_value((w.min, w.max) if isinstance(w.value, tuple) else getattr(w, which))

            yield f"slider[{s.label[:30]}]={which}", mutate


def _number_input_mutations(base):
    for i, s in enumerate(base.number_input):
        low = s.min if s.min is not None else -UNBOUNDED
        high = s.max if s.max is not None else UNBOUNDED
        for val in dict.fromkeys((low, high, 0)):
            yield f"number_input[{s.label[:30]}]={val}", lambda at, i=i, val=val: at.number_input[i].set_value(val)


def _choice_mutations(base):
    for kind in ("selectbox", "radio"):
        for i, s in enumerate(getattr(base, kind)):
            for option in s.options:
                yield (
                    f"{kind}[{s.label[:25]}]={str(option)[:25]}",
                    lambda at, kind=kind, i=i, option=option: getattr(at, kind)[i].set_value(option),
                )


def _click_and_flip_mutations(base):
    for i, s in enumerate(base.button):
        yield f"button[{s.label[:30]}]", lambda at, i=i: at.button[i].click()
    for kind in ("checkbox", "toggle"):
        for i, s in enumerate(getattr(base, kind)):
            def mutate(at, kind=kind, i=i):
                w = getattr(at, kind)[i]
                w.set_value(not w.value)

            yield f"{kind}[{s.label[:30]}]", mutate


def mutations(base):
    yield from _slider_mutations(base)
    yield from _number_input_mutations(base)
    yield from _choice_mutations(base)
    yield from _click_and_flip_mutations(base)


@pytest.mark.slow
def test_page_widget_fuzz(page_path):
    base = AppTest.from_file(str(page_path), default_timeout=TIMEOUT).run()
    assert not base.exception, "base run: " + "; ".join(e.message for e in base.exception)

    errors = []
    for label, mutate in mutations(base):
        try:
            at = AppTest.from_file(str(page_path), default_timeout=TIMEOUT).run()
            mutate(at)
            at.run()
        except Exception as exc:  # a harness failure (e.g. widget vanished) is a failure too
            errors.append(f"{label}: harness {type(exc).__name__}: {exc}")
            continue
        errors.extend(f"{label}: {e.message}" for e in at.exception)

    assert not errors, "\n".join(dict.fromkeys(errors))
