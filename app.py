from flask import Flask
from configs.setup import init, initDb

app = Flask(__name__)

initDb(app)
init(app)

if __name__ == "__main__":
    app.run(debug=True)