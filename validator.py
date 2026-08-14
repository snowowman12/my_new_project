MIN_PASSWORD_LENGTH = 8


def is_valid_password(password: str) -> bool:
    """
    Пароль валиден, если:
    - длина >= MIN_PASSWORD_LENGTH
    - есть хотя бы одна цифра
    - есть хотя бы одна заглавная буква
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    return True
