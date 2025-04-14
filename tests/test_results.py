import pytest
from app import create_app
from app.database import db
from app.models.submission import Submission

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["UPLOAD_FOLDER"] = "/tmp/uploads"

    with app.app_context():
        db.create_all()

    return app.test_client()

def test_get_results_existing_submission(client):
    with client.application.app_context():
        submission = Submission(filename="blob.txt", file_type="text", status="pending")
        db.session.add(submission)
        db.session.commit()
        sub_id = submission.id 

    response = client.get(f"/results/{sub_id}")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["id"] == sub_id
    assert json_data["filename"] == "blob.txt"
    assert json_data["file_type"] == "text"
    assert json_data["status"] == "pending"

def test_get_results_not_found(client):
    response = client.get("/results/invalid-id")
    assert response.status_code == 404
    assert response.get_json()["error"] == "submission not found"