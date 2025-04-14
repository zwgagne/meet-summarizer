from app import create_app
from app.database import db
from app.models.submission import Submission

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ database initialized 🪼")