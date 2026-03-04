import json
import uuid
from utils.transcript_parser import normalize_transcript, detect_services


def generate_account_id(company_name):
    if company_name:
        slug = company_name.lower().replace(" ", "_")
        return f"account_{slug}"
    return f"account_{uuid.uuid4().hex[:6]}"


def extract_account_memo(transcript):

    text = normalize_transcript(transcript)

    services = detect_services(text)

    memo = {
        "account_id": generate_account_id("ben_electric"),
        "company_name": "Ben Electric",
        "industry": "Electrical Services",
        "business_hours": {
            "days": [],
            "start_time": "",
            "end_time": "",
            "timezone": ""
        },
        "office_address": "",
        "services_supported": services,
        "emergency_definition": [],
        "emergency_routing_rules": {},
        "non_emergency_routing_rules": {},
        "call_transfer_rules": {},
        "integration_constraints": [],
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "Initial demo extraction"
    }

    return memo


if __name__ == "__main__":

    with open("dataset/demo_calls/demo1.txt") as f:
        transcript = f.read()

    memo = extract_account_memo(transcript)

    with open("outputs/accounts/account_ben_electric/v1/memo.json", "w") as f:
        json.dump(memo, f, indent=2)