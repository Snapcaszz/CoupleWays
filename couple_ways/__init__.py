import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from couple_ways.routes import pages
from flask_uploads import UploadSet, configure_uploads, IMAGES

load_dotenv(".env")

photos = UploadSet("photos", IMAGES)

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "5B2A8DB6FB704A5A90E09E2DF2EE056F45E741CCD005644389D276C29A94F69D"
    )
    app.config["UPLOADED_PHOTOS_DEST"] = "uploads"
    configure_uploads(app, photos)

    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    app.register_blueprint(pages)
    return app
