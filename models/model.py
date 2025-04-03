from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    face_embedding = db.Column(db.String(4000), nullable=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "password": self.password, "face_embedding": self.face_embedding}