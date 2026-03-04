import json
import os
from datetime import datetime, timezone
from scripts.generate_prompt import build_agent_spec


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

    updates = {}

    text = transcript.lower()

    if "business hours" in text:
        updates["business_hours"] = {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "start_time": "08:00",
            "end_time": "17:00",
            "timezone": "MST"
        }

    if "emergency" in text:
        updates["emergency_definition"] = [
            "power outage",
            "sparking electrical panel"
        ]

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

    account_id = "account_ben_electric"

    base_path = f"outputs/accounts/{account_id}"

    v1_path = f"{base_path}/v1/memo.json"

    onboarding_file = "dataset/onboarding_calls/onboarding1.txt"

    with open(onboarding_file) as f:
        onboarding_transcript = f.read()

    v1_memo = load_json(v1_path)

    updates = extract_updates_from_onboarding(onboarding_transcript)

    v2_memo, changes = patch_memo(v1_memo, updates)

    v2_dir = f"{base_path}/v2"

    os.makedirs(v2_dir, exist_ok=True)

    save_json(f"{v2_dir}/memo.json", v2_memo)

    agent_spec_v2 = build_agent_spec(v2_memo)

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