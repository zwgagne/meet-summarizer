import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.database import db
from app.models.submission import Submission

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "empty request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    filename = secure_filename(file.filename)
    file_ext = filename.rsplit(".", 1)[-1].lower()
    file_type = "audio" if file_ext in ["mp3", "wav"] else "text"

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    submission = Submission(filename=filename, file_type=file_type)
    db.session.add(submission)
    db.session.commit()

    return jsonify({"id": submission.id, "status": submission.status}), 201


@upload_bp.route("/results/<submission_id>", methods=["GET"])
def get_results(submission_id):
    submission = db.session.get(Submission, submission_id)

    if not submission:
        return jsonify({"error": "submission not found"}), 404

    response = {
        "id": submission.id,
        "filename": submission.filename,
        "file_type": submission.file_type,
        "status": submission.status,
    }

    if submission.summary:
        response["summary"] = {
            "title": submission.summary.title,
            "key_points": submission.summary.key_points,
            "action_items": submission.summary.action_items,
        }

    return jsonify(response), 200