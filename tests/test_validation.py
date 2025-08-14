import pytest
from core.validation import normalize_name, parse_age, parse_date_br

def test_normalize_name_ok():
    assert normalize_name("  Olga ") == "Olga"

def test_normalize_name_vazio():
    with pytest.raises(ValueError):
        normalize_name("   ")

@pytest.mark.parametrize("raw,expected", [("0", 0), ("18", 18), (" 42 ", 42)])
def test_parse_age_ok(raw, expected):
    assert parse_age(raw) == expected

@pytest.mark.parametrize("raw", ["", "x", "-1"])
def test_parse_age_invalido(raw):
    with pytest.raises(ValueError):
        parse_age(raw)

def test_parse_date_br_ok():
    assert parse_date_br("01/09/2025") == "2025-09-01"

def test_parse_date_br_invalida():
    with pytest.raises(ValueError):
        parse_date_br("2025/09/01")
