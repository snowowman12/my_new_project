from pydantic import BaseModel, Field, field_validator


class Post(BaseModel):
    # Используем Field для валидации параметров (минимум 2-3 на модель)

    id: int = Field(gt=0, description="ID поста должен быть больше 0")
    user_id: int = Field(
        alias="userId", gt=0, description="ID пользователя должен быть больше 0"
    )
    title: str = Field(
        min_length=1, max_length=200, description="Заголовок от 1 до 200 символов"
    )
    body: str = Field(min_length=1, description="Текст поста не может быть пустым")

    # Кастомный field_validator (требование критериев приемки)
    @field_validator("title")
    @classmethod
    def title_must_not_be_only_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Заголовок не должен состоять только из пробелов")
        return v

    userId: int
    id: int
    title: str
    body: str

class User(BaseModel):
    id: int = Field(gt=0, description="ID пользователя должен быть больше 0")
    name: str = Field(
        min_length=2, description="Имя должно содержать минимум 2 символа"
    )
    username: str = Field(min_length=3, description="Никнейм должен быть от 3 символов")
    email: str = Field(min_length=5, description="Email слишком короткий")

    # Кастомный field_validator (требование критериев приемки)
    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email должен содержать символ @")
        return v
