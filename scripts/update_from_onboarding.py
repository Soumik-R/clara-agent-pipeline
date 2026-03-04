import json
import os
from datetime import datetime, timezone
from scripts.generate_prompt import build_agent_spec
from utils.diff_engine import print_changes


# --------------------------------
# Step 1 — Helper Functions
# --------------------------------

def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# --------------------------------
# Step 2 — Extract Updates
# --------------------------------

def extract_updates_from_onboarding(transcript):

    import re
    updates = {}
    
    # Extract business hours dynamically
    hours_match = re.search(r"business hours are (.*?)(?:\.|\n)", transcript, re.IGNORECASE)
    if hours_match:
        hours_str = hours_match.group(1).lower()
        days = []
        if "monday to friday" in hours_str:
            days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        elif "monday to saturday" in hours_str:
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        elif "24/7" in hours_str or "24 hours" in hours_str:
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            
        start_time = "00:00"
        end_time = "23:59"
        
        time_match = re.search(r"from (\d+)\s*(am|pm)\s*to\s*(\d+)\s*(am|pm)", hours_str)
        if time_match:
            s_hr = int(time_match.group(1))
            if time_match.group(2) == "pm" and s_hr < 12: s_hr += 12
            start_time = f"{s_hr:02d}:00"
            
            e_hr = int(time_match.group(3))
            if time_match.group(4) == "pm" and e_hr < 12: e_hr += 12
            end_time = f"{e_hr:02d}:00"
            
        updates["business_hours"] = {
            "days": days,
            "start_time": start_time,
            "end_time": end_time,
            "timezone": "MST"
        }

    # Extract emergencies dynamically
    emerg_match = re.search(r"emergency calls include (.*?)(?:\.|\n)", transcript, re.IGNORECASE)
    if emerg_match:
        raw_list = emerg_match.group(1).replace(" and ", ", ")
        emergencies = [e.strip() for e in raw_list.split(",") if e.strip()]
        updates["emergency_definition"] = emergencies

    return updates


# --------------------------------
# Step 3 — Patch Memo
# --------------------------------

def patch_memo(old_memo, updates):

    new_memo = old_memo.copy()

    changes = []

    for key, value in updates.items():

        old_value = old_memo.get(key)

        if old_value != value:

            new_memo[key] = value

            changes.append({
                "field": key,
                "old_value": old_value,
                "new_value": value,
                "reason": "Updated during onboarding"
            })

    return new_memo, changes


# --------------------------------
# Step 4 — Main Execution
# --------------------------------

if __name__ == "__main__":
    import sys
    import os
    import glob
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "dataset/onboarding_calls/onboarding1.txt"
    file_name = os.path.basename(input_file).split('.')[0]
    
    # In a real system, you'd look up the account by an ID reference. 
    # Here, we know onboarding1 correlates to demo1. 
    # Let's read demo1 to see what company name we extracted, and use that slug
    
    num = file_name.replace("onboarding", "")
    demo_file = f"dataset/demo_calls/demo{num}.txt"
    
    # Just run a quick regex to grab the name if the demo file exists
    account_id = None
    if os.path.exists(demo_file):
        with open(demo_file, 'r') as f:
            transcript = f.read()
            import re
            
            company_name = f"Company Demo{num}"  # Fallback
            match = re.search(r"(?:from|with)\s+([A-Za-z0-9\s']+\b(?:Electric|HVAC|Plumbing|Roofing|Services|Solutions|Tech|IT)\b[A-Za-z0-9\s']*)[\.,\n]", transcript, re.IGNORECASE)
            if match:
                company_name = match.group(1).title().strip()
            else:
                match = re.search(r"(?:from|with)\s+([A-Z][a-zA-Z\s']+?)(?:\.|,|\n)", transcript)
                if match:
                    company_name = match.group(1).strip()
                    
            account_id = f"account_{company_name.lower().replace(' ', '_')}"
    
    if not account_id:
        print(f"Could not correlate {file_name} to an account. Skipping.")
        sys.exit(0)

    base_path = f"outputs/accounts/{account_id}"
    v1_path = f"{base_path}/v1/memo.json"

    if not os.path.exists(v1_path):
        print(f"Skipping {account_id} - v1 record not found.")
        sys.exit(0)
        
    with open(input_file, 'r') as f:
        onboarding_transcript = f.read()

    v1_memo = load_json(v1_path)
    updates = extract_updates_from_onboarding(onboarding_transcript)
    v2_memo, changes = patch_memo(v1_memo, updates)

    print_changes(changes)

    v2_dir = f"{base_path}/v2"
    os.makedirs(v2_dir, exist_ok=True)

    save_json(f"{v2_dir}/memo.json", v2_memo)

    agent_spec_v2 = build_agent_spec(v2_memo)
    agent_spec_v2["version"] = "v2"

    save_json(f"{v2_dir}/agent_spec.json", agent_spec_v2)

    changelog = {
        "account_id": account_id,
        "from_version": "v1",
        "to_version": "v2",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "changes": changes
    }

    save_json(f"{base_path}/changes.json", changelog)
    print("Onboarding update applied successfully.")