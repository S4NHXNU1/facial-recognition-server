from flask_cors import CORS
from controller.authenController import auth
from controller.faceScanController import scan
from models.model import db, User
import os

def initDb(app):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__)) + "/utils"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

def init(app):
    CORS(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(scan)

    with app.app_context():
        db.create_all()
    # print("Blueprints registered:", app.url_map)