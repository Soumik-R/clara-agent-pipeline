import re

texts = [
    "Hi, this is Ben from Ben Electric.",
    "Hello, this is Sarah from CoolAir HVAC.",
    "Hi, I'm Mike from Mike's Precision Plumbing.",
    "This is John with Apex Roofing Solutions.",
    "Hello, it's David from TechFix IT Services."
]

for t in texts:
    match = re.search(r"(?:from|with)\s+([A-Za-z0-9\s']+\b(?:Electric|HVAC|Plumbing|Roofing|Services|Solutions|Tech|IT)\b[A-Za-z0-9\s']*)[\.,\n]", t, re.IGNORECASE)
    if match:
        print(f"MATCH: {match.group(1).title().strip()}")
    else:
        print(f"FAIL: {t}")
