import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from couple_ways.routes import pages

load_dotenv(".env")

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "5B2A8DB6FB704A5A90E09E2DF2EE056F45E741CCD005644389D276C29A94F69D"
    )

    app.db = MongoClient(app.config["MONGODB_URI"])

    app.register_blueprint(pages)
    return app
