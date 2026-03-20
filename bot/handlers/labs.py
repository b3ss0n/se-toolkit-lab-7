from services.lms_api import LMSAPIClient
from config import LMS_API_URL, LMS_API_KEY


def handle_labs(user_input: str = "") -> str:
    """Handle /labs command."""
    try:
        client = LMSAPIClient(LMS_API_URL, LMS_API_KEY)
        items = client.get_items()
        if not items or not isinstance(items, list):
            return "No labs available."

        labs = {}
        for item in items:
            if isinstance(item, dict):
                lab_id = item.get("lab_id", item.get("lab", "unknown"))
                lab_name = item.get("lab_name", item.get("lab_name", lab_id))
                if lab_id and lab_id not in labs:
                    labs[lab_id] = lab_name

        if not labs:
            return "No labs found."

        result = "Available labs:"
        for lab_id, lab_name in sorted(labs.items()):
            result += f"\n- {lab_id} — {lab_name}"
        return result
    except ConnectionError as e:
        return f"Backend error: {e}"
    except Exception as e:
        return f"Backend error: {type(e).__name__}: {e}"
