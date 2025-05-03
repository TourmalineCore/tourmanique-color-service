from domain.data_access_layer.db import db


class Color(db.Model):
    __tablename__ = 'color'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    photo_id = db.Column(db.Integer, nullable=False)
    red = db.Column(db.Integer, nullable=False)
    green = db.Column(db.Integer, nullable=False)
    blue = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Color {self.id!r} photo_id: {self.photo_id!r} red:{self.red!r} green:{self.green!r} blue:{self.blue!r}>'