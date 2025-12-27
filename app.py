from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VALID_STATUSES = [
    "interested",
    "not_interested",
    "callback",
    "voicemail",
    "no_answer",
    "wrong_number"
]

@app.route("/")
def home():
    return render_template("index.html")


def has_conflict(status, notes):
    notes = notes.lower()
    if status == "interested" and "not interested" in notes:
        return True
    if status == "not_interested" and "interested" in notes:
        return True
    return False


@app.route("/ai-summary", methods=["POST"])
def ai_summary():
    data = request.json or {}
    call_status = data.get("call_status")
    call_notes = data.get("call_notes", "").strip()

    if call_status not in VALID_STATUSES:
        return jsonify({"error": "Invalid call status"}), 400

    if not call_notes:
        return jsonify({"error": "Call notes are required"}), 400

    conflict = has_conflict(call_status, call_notes)
    conflict_note = (
        "\n⚠ Note: The original notes conflicted with the selected outcome."
        if conflict else ""
    )

    summaries = {
        "interested": f"""Call Outcome: Interested
Summary:
The prospect showed interest during the call.{conflict_note}
Next step: Share program details and assist with the application process.""",

        "not_interested": f"""Call Outcome: Not Interested
Summary:
The prospect was marked as not interested based on the final outcome.{conflict_note}
Next step: No follow-up unless initiated by the prospect.""",

        "callback": f"""Call Outcome: Call Back
Summary:
The prospect requested a follow-up call.
Next step: Schedule the callback at the requested time.""",

        "voicemail": f"""Call Outcome: Voicemail
Summary:
The call reached voicemail.
Next step: Attempt a follow-up call or send a brief message.""",

        "no_answer": f"""Call Outcome: No Answer
Summary:
The call was unanswered.
Next step: Retry the call at a different time.""",

        "wrong_number": f"""Call Outcome: Wrong Number
Summary:
The dialed number was incorrect.
Next step: Verify and update contact details."""
    }

    return jsonify({"summary": summaries[call_status]})


if __name__ == "__main__":
    app.run(debug=True)
