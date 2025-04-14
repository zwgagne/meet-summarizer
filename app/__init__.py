from flask import Flask
from .config import Config
from .database import db
from .routes.upload import upload_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(upload_bp)

    return app