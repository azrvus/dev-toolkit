from dev_toolkit.transforms import capitalize_words, normalize_spaces, to_snake_case


def test_normalize_spaces():
    assert normalize_spaces("  hello   world  ") == "hello world"


def test_capitalize_words():
    assert capitalize_words("hello world from python") == "Hello World From Python"


def test_to_snake_case():
    assert to_snake_case("AValidVariableName") == "a_valid_variable_name"
    assert to_snake_case("camelCaseString") == "camel_case_string"
