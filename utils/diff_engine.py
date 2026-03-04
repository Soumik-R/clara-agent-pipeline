"""
Diff Engine - Utilities for comparing and displaying changes
"""

import json


def print_changes(changes):
    """
    Print changes in a readable format.
    
    Args:
        changes: List of change dictionaries with 'field', 'old_value', 'new_value'
    """
    
    print("\nChanges detected:\n")

    for change in changes:

        field = change["field"]
        old_value = change["old_value"]
        new_value = change["new_value"]

        print(f"{field}")
        print(f"  old: {old_value}")
        print(f"  new: {new_value}\n")
