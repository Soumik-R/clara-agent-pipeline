import json
import os

from utils.supabase_client import save_account_version

# -------------------------------
# STEP 1: Generate System Prompt
# -------------------------------

def generate_prompt(memo):

    company = memo.get("company_name", "the company")
    services = memo.get("services_supported", [])

    services_text = ", ".join(services) if services else "general electrical services"

    prompt = f"""
You are the AI call assistant for {company}.

Your job is to help callers, collect required information, and route calls correctly.

Supported services include: {services_text}

BUSINESS HOURS FLOW:
1. Greet the caller professionally.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Determine if the request is service, emergency, or general inquiry.
5. Transfer call to the correct team if necessary.
6. If transfer fails, apologize and inform the caller someone will follow up.
7. Ask if the caller needs anything else.
8. Close the call politely.

AFTER HOURS FLOW:
1. Greet the caller.
2. Ask purpose of the call.
3. Determine if this is an emergency.
4. If emergency:
   - Immediately collect name, phone number, and address.
   - Attempt transfer to emergency contact.
5. If transfer fails:
   - Apologize and assure quick follow-up.
6. If non-emergency:
   - Collect details and schedule follow-up during business hours.
7. Ask if they need anything else.
8. Close the call politely.

RULES:
- Do not ask unnecessary questions.
- Only collect information needed for routing and dispatch.
- Never mention internal tools or system processes.
"""

    return prompt


# -------------------------------
# STEP 2: Build Agent Spec
# -------------------------------

def build_agent_spec(memo):

    prompt = generate_prompt(memo)

    agent_spec = {
        "agent_name": f"{memo.get('company_name', 'Company')} Voice Assistant",
        "voice_style": "professional and calm",
        "system_prompt": prompt,
        "key_variables": {
            "company_name": memo.get("company_name", ""),
            "services_supported": memo.get("services_supported", []),
            "business_hours": memo.get("business_hours", {}),
            "office_address": memo.get("office_address", "")
        },
        "call_transfer_protocol": "Transfer caller to appropriate team after collecting name and phone number.",
        "transfer_fail_protocol": "Apologize and inform caller that the team will follow up shortly.",
        "tool_invocation_placeholders": [],
        "version": "v1"
    }

    return agent_spec


# -------------------------------
# STEP 3: Run Script
# -------------------------------

if __name__ == "__main__":

    memo_path = "outputs/accounts/account_ben_electric/v1/memo.json"

    with open(memo_path) as f:
        memo = json.load(f)

    agent_spec = build_agent_spec(memo)

    output_dir = "outputs/accounts/account_ben_electric/v1"

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "agent_spec.json")

    with open(output_path, "w") as f:
        json.dump(agent_spec, f, indent=2)

    print("Agent spec generated successfully.")