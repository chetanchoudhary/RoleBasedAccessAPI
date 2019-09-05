from db import db


class SensorModel(db.Model):

    __tablename__ = "sensors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    value = db.Column(db.Float(precision=2))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def json(self):
        return {"name": self.name, "value": self.value}

    @classmethod
    def find_by_name(cls, name):

        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
