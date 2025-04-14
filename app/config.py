class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://devuser:devpassword@localhost:5432/meet_summarizer_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False