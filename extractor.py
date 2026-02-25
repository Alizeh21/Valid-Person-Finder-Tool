import re
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

NAME_REGEX = re.compile(r"\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b")


def is_credible_source(url: str):
    allowed = [
        "linkedin.com",
        "wikipedia.org",
        "crunchbase.com",
        "forbes.com",
        "bloomberg.com",
        "reuters.com",
        "about.",
        "company",
        ".com"
    ]

    return any(a in url.lower() for a in allowed)


def fetch_page_text(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator=" ")
    except Exception:
        return ""


def extract_name_from_text(text: str):
    candidates = NAME_REGEX.findall(text)

    unique = []
    for c in candidates:
        full = f"{c[0]} {c[1]}"
        if full not in unique:
            unique.append(full)

    return unique


def score_candidate(text, company, designation, name):
    base = 0

    if company.lower() in text.lower():
        base += 0.4

    if designation.lower() in text.lower():
        base += 0.4

    name_score = fuzz.partial_ratio(name.lower(), text.lower())
    base += min(name_score / 100 * 0.2, 0.2)

    return round(min(base, 1.0), 2)