from app.database import db
import uuid

# each sumary is associated with a submission 1:1
class Summary(db.Model):
    __tablename__ = "summaries"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    submission_id = db.Column(db.String, db.ForeignKey("submissions.id"), nullable=False, unique=True)

    title = db.Column(db.String, nullable=True)
    key_points = db.Column(db.JSON, nullable=True)
    action_items = db.Column(db.JSON, nullable=True)
    raw_response = db.Column(db.Text, nullable=True)

    # mirror relationship back to Submission
    # ensures bidirectional access between submission and summary
    submission = db.relationship("Submission", back_populates="summary")