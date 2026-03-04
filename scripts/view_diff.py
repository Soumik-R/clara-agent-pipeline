"""
Diff Viewer - Shows changes between v1 and v2 agent configurations
"""

import json
import os
import sys


def load_json(path):
    """Load JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def format_value(value):
    """Format value for display."""
    if isinstance(value, list):
        if not value:
            return '[]'
        return '[' + ', '.join(f'"{v}"' for v in value) + ']'
    elif isinstance(value, dict):
        if not value:
            return '{}'
        return json.dumps(value, indent=2)
    elif value == "":
        return '""'
    else:
        return str(value)


def display_diff(account_id, base_path="outputs/accounts"):
    """Display the differences between v1 and v2."""
    
    changes_file = f"{base_path}/{account_id}/changes.json"
    
    if not os.path.exists(changes_file):
        print(f"No changes found for {account_id}")
        return
    
    changes_data = load_json(changes_file)
    
    print("=" * 70)
    print(f"DIFF VIEWER: {account_id}")
    print("=" * 70)
    print(f"From Version: {changes_data.get('from_version', 'N/A')}")
    print(f"To Version:   {changes_data.get('to_version', 'N/A')}")
    print(f"Timestamp:    {changes_data.get('timestamp', 'N/A')}")
    print("=" * 70)
    print()
    
    changes = changes_data.get('changes', [])
    
    if not changes:
        print("No changes detected.")
        return
    
    for i, change in enumerate(changes, 1):
        field = change.get('field', 'unknown')
        old_value = change.get('old_value')
        new_value = change.get('new_value')
        reason = change.get('reason', 'N/A')
        
        print(f"Change #{i}: {field}")
        print("-" * 70)
        print(f"Old Value: {format_value(old_value)}")
        print(f"New Value: {format_value(new_value)}")
        print(f"Reason:    {reason}")
        print()
    
    print("=" * 70)


def display_all_diffs(base_path="outputs/accounts"):
    """Display diffs for all accounts."""
    
    if not os.path.exists(base_path):
        print("No accounts found.")
        return
    
    accounts = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    if not accounts:
        print("No accounts found.")
        return
    
    for account_id in accounts:
        display_diff(account_id, base_path)
        print()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        # Display specific account
        account_id = sys.argv[1]
        display_diff(account_id)
    else:
        # Display all accounts
        display_all_diffs()
