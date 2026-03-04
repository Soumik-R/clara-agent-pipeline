import os
import subprocess
import sys

DEMO_FOLDER = "dataset/demo_calls"
ONBOARDING_FOLDER = "dataset/onboarding_calls"

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_demo_pipeline():
    print("\nRunning demo extraction pipeline...\n")

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


def run_onboarding_pipeline():
    print("\nRunning onboarding update pipeline...\n")

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


if __name__ == "__main__":

    run_demo_pipeline()

    run_onboarding_pipeline()

    print("\nPipeline completed for all accounts.")