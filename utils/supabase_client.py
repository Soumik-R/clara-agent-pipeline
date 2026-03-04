import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_account_version(account_id, version, memo, agent_spec):

    data = {
        "account_id": account_id,
        "version": version,
        "memo_json": memo,
        "agent_spec_json": agent_spec
    }

    response = supabase.table("account_versions").insert(data).execute()

    return response


def save_change_log(account_id, from_version, to_version, changes):

    data = {
        "account_id": account_id,
        "from_version": from_version,
        "to_version": to_version,
        "changes_json": changes
    }

    response = supabase.table("change_logs").insert(data).execute()

    return response