# @author alyssa

class User:

    def __init__(self,
                 username: str,
                 id: str,
                 is_authenticated: bool = False,
                 is_active: bool = False,
                 is_anonymous: bool = False):

        self.username = username
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous

    def become_authenticated(self) -> None:
        self.is_authenticated = True

    def set_activation(self, status: bool) -> None:
        self.is_active = bool

    def set_identification(self, id: str) -> None:
        self.id = id

    def get_id(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return f'User: {self.username}, is authenticated: {self.is_authenticated}'
