from app.database import db
import uuid
from datetime import datetime

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)