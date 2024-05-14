from routes import *
from flask import Flask
from models import calculate_carbon_footprint
from utils import *

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)
