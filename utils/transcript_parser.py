import re

def normalize_transcript(text):
    text = text.lower()
    text = text.replace("\n", " ")
    return text


def extract_company_name(text):
    match = re.search(r"company name is ([a-zA-Z\s]+)", text)
    if match:
        return match.group(1).strip()
    return None


def detect_services(text):
    services = []

    service_keywords = {
        "ev charger installation": ["ev charger", "electric vehicle charger"],
        "hot tub wiring": ["hot tub"],
        "panel upgrades": ["panel change", "panel upgrade"],
        "outlet replacement": ["outlet replacement"],
        "electrical troubleshooting": ["troubleshoot", "troubleshooting"],
        "aluminum wiring remediation": ["aluminum wiring"]
    }

    for service, keywords in service_keywords.items():
        for k in keywords:
            if k in text:
                services.append(service)
                break

    return list(set(services))