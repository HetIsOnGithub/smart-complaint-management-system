import json

from django.conf import settings
from google import genai


client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
]


def clean_json(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):]

    elif text.startswith("```"):
        text = text[len("```"):]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_complaint_details(description):
    prompt = f"""
You are an AI Complaint Classification Assistant.

Analyze the complaint.

Return ONLY valid JSON.

Categories:
- Technical
- Electrical
- Network
- Maintenance
- Cleanliness
- Security
- Academic
- Administrative
- Other

Priorities:
- Low
- Medium
- High

JSON Format:

{{
    "title": "",
    "category": "",
    "priority": ""
}}

Complaint:

{description}
"""

    last_error = None

    for model_name in MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            text = clean_json(response.text)

            data = json.loads(text)

            title = data.get("title", "General Complaint").strip()

            category = data.get("category", "Other").strip()

            priority = data.get("priority", "Medium").strip()

            valid_categories = {
                "Technical",
                "Electrical",
                "Network",
                "Maintenance",
                "Cleanliness",
                "Security",
                "Academic",
                "Administrative",
                "Other",
            }

            valid_priorities = {
                "Low",
                "Medium",
                "High",
            }

            if category not in valid_categories:
                category = "Other"

            if priority not in valid_priorities:
                priority = "Medium"

            return {
                "title": title,
                "category": category,
                "priority": priority,
            }

        except Exception as e:
            print(f"{model_name}: {e}")
            last_error = e

    print("Gemini Error:", last_error)

    return {
        "title": "General Complaint",
        "category": "Other",
        "priority": "Medium",
    }