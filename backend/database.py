from flask_pymongo import PyMongo
from pymongo import TEXT

mongo = PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = " "
    mongo.init_app(app)
    with app.app_context():
        mongo.db.documents.create_index([("content", TEXT)])
        print("Database initialized and text index created")

def get_db():
    return mongo.db
