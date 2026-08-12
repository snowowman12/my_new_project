import pytest
from validator import is_valid_password, MIN_PASSWORD_LENGTH

# Константы вместо магических чисел/строк
SHORT_PASSWORD = "Ab1"
NO_DIGIT_PASSWORD = "Password"
NO_UPPERCASE_PASSWORD = "password1"
VALID_PASSWORD = "Password1"
EMPTY_PASSWORD = ""


@pytest.mark.smoke
@pytest.mark.parametrize(
    "password, expected_result",
    [
        (SHORT_PASSWORD, False),
        (NO_DIGIT_PASSWORD, False),
        (NO_UPPERCASE_PASSWORD, False),
        (VALID_PASSWORD, True),
        (EMPTY_PASSWORD, False),
    ],
    ids=[
        "too_short_password",
        "missing_digit",
        "missing_uppercase",
        "valid_password",
        "empty_password",
    ],
)
def test_is_valid_password(password, expected_result):
    assert is_valid_password(password) == expected_result
