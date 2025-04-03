from flask_cors import CORS
from controller.authenController import auth
from controller.faceScanController import scan

def init(app):
    CORS(app)
    app.register_blueprint(auth)
    app.register_blueprint(scan)
    # print("Blueprints registered:", app.url_map)