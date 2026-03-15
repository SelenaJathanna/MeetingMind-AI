import json
import re

def extract_insights(text: str):

    insights = {
        "meeting_summary": {
            "title": "AI Detected Meeting",
            "participants": []
        },
        "decisions": [],
        "action_items": [],
        "deadlines": [],
        "open_issues": [],
        "responsibility_map": {},
        "intelligence_score": {
            "score": 50,
            "flags": []
        },
        "errors": []
    }

    lines = text.split("\n")

    for line in lines:

        # detect decisions
        if "decided" in line.lower() or "agreed" in line.lower():
            insights["decisions"].append(line.strip())

        # detect action items
        if "will" in line.lower() or "needs to" in line.lower():
            insights["action_items"].append({
                "assignee": "Unknown",
                "task": line.strip()
            })

        # detect deadlines
        date_match = re.search(r"\b\d{1,2}\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", line)
        if date_match:
            insights["deadlines"].append({
                "description": line.strip()
            })

        # detect issues
        if "issue" in line.lower() or "problem" in line.lower():
            insights["open_issues"].append(line.strip())

    # simple score
    score = (
        len(insights["decisions"]) * 10 +
        len(insights["action_items"]) * 10 +
        len(insights["deadlines"]) * 5
    )

    insights["intelligence_score"]["score"] = min(score, 100)

    return insights


def insights_to_json(data):
    return json.dumps(data, indent=2)