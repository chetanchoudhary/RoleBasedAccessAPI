from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(email, password):
    user = UserModel.find_by_email(email)
    if user and safe_str_cmp(user.password, password):

        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
