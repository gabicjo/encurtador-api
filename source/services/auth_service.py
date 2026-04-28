from source.models.users_model import User, BANCO_PATH
from source import error_handler


def register(username: str, password: str) -> User:
    """Registra novo usuário."""
    if not username or not password:
        raise error_handler.CodigoInvalido("Username e password são obrigatórios")
    
    existing = User.get_by_username(username)
    if existing:
        raise error_handler.CodigoInvalido("Usuário já existe")
    
    return User.create(username, password)


def authenticate(username: str, password: str) -> User | None:
    """Autentica usuário. Retorna User se válido, None caso contrário."""
    user = User.get_by_username(username)
    if user and user.verify_password(password):
        return user
    return None