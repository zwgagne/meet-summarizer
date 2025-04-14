import os
from flask import Blueprint, request, jsonify
from app.database import db
from app.models.submission import Submission
from app.models.summary import Summary

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/analyse", methods=["POST"])
def analyse_submission():
    data = request.get_json()
    submission_id = data.get("id")

    if not submission_id:
        return jsonify({"error": "Missing submission ID"}), 400

    submission = Submission.query.get(submission_id)

    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    if submission.status == "done":
        return jsonify({"error": "Submission already processed"}), 400

    file_path = os.path.join("uploads", submission.filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    with open(file_path, "r") as f:
        content = f.read()

    # todo: call openai api
    summary = Summary(
        submission_id=submission.id,
        title="Mocked Summary",
        key_points=["Point 1", "Point 2"],
        action_items=["Action A", "Action B"],
        raw_response="Résumé simulé de contenu."
    )
    db.session.add(summary)

    submission.status = "done"
    db.session.commit()

    return jsonify({
        "status": "done",
        "summary": {
            "title": summary.title,
            "key_points": summary.key_points,
            "action_items": summary.action_items
        }
    }), 200