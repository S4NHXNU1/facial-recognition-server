from flask import Flask
from configs.setup import init

app = Flask(__name__)

init(app)

if __name__ == "__main__":
    app.run(debug=True)