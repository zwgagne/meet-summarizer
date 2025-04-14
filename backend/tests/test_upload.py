import io
import pytest
from app import create_app
from app.database import db

@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["UPLOAD_FOLDER"] = "/tmp/uploads"

    with app.app_context():
        db.create_all()

    return app.test_client()

def test_upload_text_file(client):
    data = {
        "file": (io.BytesIO(b"hello world, blblbl"), "blob.txt")
    }

    response = client.post("/upload", content_type="multipart/form-data", data=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert "id" in json_data
    assert json_data["status"] == "pending"