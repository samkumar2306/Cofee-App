from app.extensions import db
from app.models.user import User


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def update_user():
    db.session.commit()


def create_user(user):

    db.session.add(user)

    return user