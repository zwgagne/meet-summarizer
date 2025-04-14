import os
from flask import Blueprint, request, jsonify
from app.database import db
from app.models.submission import Submission
from app.models.summary import Summary
from app.services.openai_service import summarize_text

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/analyse", methods=["POST"])
def analyse_submission():
    data = request.get_json()
    submission_id = data.get("id")

    if not submission_id:
        return jsonify({"error": "missing submission id"}), 400

    submission = Submission.query.get(submission_id)

    if not submission:
        return jsonify({"error": "submission not found"}), 404

    if submission.status == "done":
        return jsonify({"error": "submission already processed"}), 400

    file_path = os.path.join("uploads", submission.filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "file not found"}), 404

    with open(file_path, "r") as f:
        content = f.read()

    try:
        result = summarize_text(content)
    except Exception as e:
        submission.status = "error"
        db.session.commit()
        return jsonify({"error": str(e)}), 500

    summary = Summary(
        submission_id=submission.id,
        title="(to extract)",  # todo: replace with actual title extraction
        key_points=[],
        action_items=[],
        raw_response=result
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