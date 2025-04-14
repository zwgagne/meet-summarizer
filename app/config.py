import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://devuser:devpassword@localhost:5432/meet_summarizer_db" # might want to move in a .env file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")