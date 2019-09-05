from db import db


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    password = db.Column(db.String(60))
    access = db.Column(db.String(10))

    def __init__(self, email, password, access):
        self.email = email
        self.password = password
        self.access = access

    def json(self):
        return {"email": self.email, "password": self.password, "access": self.access}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
