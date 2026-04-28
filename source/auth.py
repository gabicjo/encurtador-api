import sqlite3
from flask_login import LoginManager
from source.models.users_model import User, BANCO_PATH

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    return User.get_by_id(int(user_id))