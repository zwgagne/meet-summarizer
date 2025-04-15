import os
from flask import Blueprint, request, jsonify, current_app
from app.database import db
from app.models.submission import Submission
from app.models.summary import Summary
from app.services.openai_service import summarize_text
from app.services.openai_parser import parse_openai_summary

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/analyse", methods=["POST"])
def analyse_submission():
    try:
        data = request.get_json()
        submission_id = data.get("id")

        submission = db.session.get(Submission, submission_id)
        if not submission:
            raise Exception("submission not found in db")

        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], submission.filename)

        if not os.path.exists(file_path):
            raise Exception(f"file not found: {file_path}")

        with open(file_path, "r") as f:
            content = f.read()

        result = summarize_text(content)
        parsed = parse_openai_summary(result)

        summary = Summary(
            submission_id=submission.id,
            title=parsed["title"],
            key_points=parsed["key_points"],
            action_items=parsed["action_items"],
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

    except Exception as e:
        submission.status = "error"
        db.session.commit()
        return jsonify({"error": str(e)}), 500