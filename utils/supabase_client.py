from supabase import create_client

SUPABASE_URL = "https://grqlyniakbqhqmeldciu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdycWx5bmlha2JxaHFtZWxkY2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI2MTQxMTIsImV4cCI6MjA4ODE5MDExMn0.o4rorrZ1v3lkopTXFokbX4RPlQWzi7rLI_6jm76InF8"

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