import os
import pytest
from unittest.mock import patch
from app import create_app
from app.database import db
from app.models.submission import Submission
from app.models.summary import Summary

UPLOAD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["UPLOAD_FOLDER"] = UPLOAD_PATH

    with app.app_context():
        db.create_all()

    return app.test_client()

def test_analyse_text_submission(client):
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    file_path = os.path.join(UPLOAD_PATH, "blob.txt")
    with open(file_path, "w") as f:
        f.write("this is a file to analyse and summarize")

    with client.application.app_context():
        submission = Submission(filename="blob.txt", file_type="text", status="pending")
        db.session.add(submission)
        db.session.commit()
        submission_id = submission.id

    # openai mock
    with patch("app.routes.analyse.summarize_text") as mock_summarize:
        mock_summarize.return_value = """Title: weekly blob sync

        Key Points:
        - Blob griotte is super happy
        - Blob coco is not happy

        Action Items:
        - Schedule a blob party
        - Send a blob to the blob team
        """

        response = client.post("/api/analyse", json={"id": submission_id})
        json_data = response.get_json()

        assert response.status_code == 200
        assert json_data["status"] == "done"
        assert "summary" in json_data

        summary_data = json_data["summary"]
        assert summary_data["title"] == "weekly blob sync"
        assert summary_data["key_points"] == [
            "Blob griotte is super happy",
            "Blob coco is not happy"
        ]
        assert summary_data["action_items"] == [
            "Schedule a blob party",
            "Send a blob to the blob team"
        ]

        with client.application.app_context():
            updated = db.session.get(Submission, submission_id)
            assert updated.status == "done"
            assert updated.summary is not None
            assert updated.summary.raw_response == mock_summarize.return_value