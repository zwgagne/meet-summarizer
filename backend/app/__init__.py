from flask import Flask
from .config import Config
from .database import db
from .routes.upload import upload_bp
from .routes.analyse import analyse_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(analyse_bp, url_prefix="/api")

    return app