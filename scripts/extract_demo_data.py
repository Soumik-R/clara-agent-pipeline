import json
import uuid
from utils.transcript_parser import normalize_transcript, detect_services


def generate_account_id(company_name):
    if company_name:
        slug = company_name.lower().replace(" ", "_")
        return f"account_{slug}"
    return f"account_{uuid.uuid4().hex[:6]}"


def extract_account_memo(transcript, company_name):

    text = normalize_transcript(transcript)
    services = detect_services(text)
    
    slug = generate_account_id(company_name)

    memo = {
        "account_id": slug,
        "company_name": company_name,
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

    return memo, slug

if __name__ == "__main__":
    import sys
    import os
    import re
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "dataset/demo_calls/demo1.txt"
    file_name = os.path.basename(input_file).split('.')[0]
    
    with open(input_file, 'r') as f:
        transcript = f.read()

    # Try to extract company name from transcript (e.g. "Hi, this is Ben from Ben Electric")
    company_name = f"Company Demo{num}" if 'num' in locals() else f"Company {file_name.capitalize()}" # Fallback
    
    # regex matches: "from X [Electric|HVAC...]" up to the first punctuation
    match = re.search(r"(?:from|with)\s+([A-Za-z0-9\s']+\b(?:Electric|HVAC|Plumbing|Roofing|Services|Solutions|Tech|IT)\b[A-Za-z0-9\s']*)[\.,\n]", transcript, re.IGNORECASE)
    if match:
        company_name = match.group(1).title().strip()
    else:
        # Fallback 2: "from X"
        match = re.search(r"(?:from|with)\s+([A-Z][a-zA-Z\s']+?)(?:\.|,|\n)", transcript)
        if match:
             company_name = match.group(1).strip()

    memo, slug = extract_account_memo(transcript, company_name)
    
    os.makedirs(f"outputs/accounts/{slug}/v1", exist_ok=True)
    with open(f"outputs/accounts/{slug}/v1/memo.json", "w") as f:
        json.dump(memo, f, indent=2)