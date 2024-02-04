from pydantic import BaseModel, Field, SecretStr


class UserRegister(BaseModel):
    user_login: str = Field(min_length=2, max_length=40)
    user_pass: SecretStr = Field(min_length=6)
    first_name: str = Field(min_length=2, max_length=40)
    last_name: str = Field(min_length=2, max_length=40)
