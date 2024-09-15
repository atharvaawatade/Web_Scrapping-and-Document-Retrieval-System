from database import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    request_count = db.Column(db.Integer, default=0)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)