from duckduckgo_search import DDGS

DESIGNATION_ALIASES = {
    "ceo": ["CEO", "Chief Executive Officer"],
    "cto": ["CTO", "Chief Technology Officer"],
    "cfo": ["CFO", "Chief Financial Officer"],
    "coo": ["COO", "Chief Operating Officer"],
}

def build_queries(company: str, designation: str):
    d = designation.lower()

    aliases = DESIGNATION_ALIASES.get(d, [designation])

    queries = []

    for a in aliases:
        queries.append(f"{company} {a}")
        queries.append(f"{company} {a} site:linkedin.com")
        queries.append(f"{company} {a} official website")

    return list(dict.fromkeys(queries))


def duckduckgo_search(queries, max_results=5):
    results = []

    with DDGS() as ddgs:
        for q in queries:
            try:
                for r in ddgs.text(q, max_results=max_results):
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body", "")
                    })
            except Exception:
                continue

    return results