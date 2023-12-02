import os
from flask import Flask, session
from datetime import timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from couple_ways.routes import pages
from flask_uploads import configure_uploads
from couple_ways.utils.functions import photos

load_dotenv(".env")

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "5B2A8DB6FB704A5A90E09E2DF2EE056F45E741CCD005644389D276C29A94F69D"
    )
    app.config["UPLOADED_PHOTOS_DEST"] = "./couple_ways/static/uploads"

    configure_uploads(app, photos)

    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    app.register_blueprint(pages)

    @app.before_request
    def set_default_theme():
        # Check if the "theme" key is not already in the session
        if "theme" not in session:
            session["theme"] = "dark"

    return app

