import os
import subprocess
import sys

DEMO_FOLDER = "dataset/demo_calls"
ONBOARDING_FOLDER = "dataset/onboarding_calls"
ACCOUNTS_FOLDER = "outputs/accounts"

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_demo_pipeline():
    """Run demo extraction pipeline and return count of processed files."""
    print("\nRunning demo extraction pipeline...\n")
    
    count = 0
    for file in os.listdir(DEMO_FOLDER):

        if file.endswith(".txt"):

            print(f"Processing demo file: {file}")

            env = os.environ.copy()
            env['PYTHONPATH'] = PROJECT_ROOT

            subprocess.run([
                "python",
                "scripts/extract_demo_data.py",
                os.path.join(DEMO_FOLDER, file)
            ], env=env)
            
            count += 1
    
    return count


def run_onboarding_pipeline():
    """Run onboarding update pipeline and return count of processed files."""
    print("\nRunning onboarding update pipeline...\n")
    
    count = 0
    for file in os.listdir(ONBOARDING_FOLDER):

        if file.endswith(".txt"):

            print(f"Processing onboarding file: {file}")

            env = os.environ.copy()
            env['PYTHONPATH'] = PROJECT_ROOT

            subprocess.run([
                "python",
                "scripts/update_from_onboarding.py",
                os.path.join(ONBOARDING_FOLDER, file)
            ], env=env)
            
            count += 1
    
    return count


def count_accounts():
    """Count the number of accounts in the outputs folder."""
    if not os.path.exists(ACCOUNTS_FOLDER):
        return 0
    
    accounts = [d for d in os.listdir(ACCOUNTS_FOLDER) 
                if os.path.isdir(os.path.join(ACCOUNTS_FOLDER, d))]
    return len(accounts)


def count_agents():
    """Count total agent specs generated (v1 + v2)."""
    if not os.path.exists(ACCOUNTS_FOLDER):
        return 0
    
    total = 0
    for account in os.listdir(ACCOUNTS_FOLDER):
        account_path = os.path.join(ACCOUNTS_FOLDER, account)
        if os.path.isdir(account_path):
            # Check for v1 and v2 agent specs
            for version in ['v1', 'v2']:
                agent_spec_path = os.path.join(account_path, version, 'agent_spec.json')
                if os.path.exists(agent_spec_path):
                    total += 1
    
    return total


def display_dashboard(demo_count, onboarding_count, accounts_count, agents_count):
    """Display a summary dashboard."""
    print("\n")
    print("=" * 60)
    print(" " * 20 + "PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Demo Calls Processed:       {demo_count}")
    print(f"Onboarding Calls Processed: {onboarding_count}")
    print(f"Accounts Created:           {accounts_count}")
    print(f"Agent Specs Generated:      {agents_count}")
    print("=" * 60)
    print("\nTip: Run 'python scripts/view_diff.py' to view changes")
    print("=" * 60)
    print()


if __name__ == "__main__":

    demo_count = run_demo_pipeline()

    onboarding_count = run_onboarding_pipeline()

    accounts_count = count_accounts()
    agents_count = count_agents()

    display_dashboard(demo_count, onboarding_count, accounts_count, agents_count)