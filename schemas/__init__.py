# Used in TinyDB and JSON schemas


class UserSchema:
    '''
    Dados de identificação do usuário para login
    '''

    def __init__(
        self,
        id: int | None,
        username: str | None,
        password: str | None,
        created_at: str | None,
        last_login: str | None,
        real_name: str | None,
        email: str | None,
    ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.last_login = last_login
        self.real_name = real_name
        self.email = email
