import pytest

import prompts


@pytest.mark.parametrize("kind,marker", [
    ("youtube", '"t": "MM:SS"'), ("video", '"t": "MM:SS"'),
    ("audio", '"speaker"'), ("image", '"where"'), ("document", '"page"'),
])
def test_each_kind_has_its_locator(kind, marker):
    p = prompts.ask_prompt(kind, "What is the level?")
    assert marker in p and p.rstrip().endswith("QUESTION: What is the level?")


def test_question_braces_do_not_break_formatting():
    assert "{x}" in prompts.ask_prompt("document", "what is {x}?")
