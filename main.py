from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from search import build_queries, duckduckgo_search
from extractor import (
    fetch_page_text,
    extract_name_from_text,
    score_candidate,
    is_credible_source
)
from db import results_collection

app = FastAPI(title="Valid Person Finder")


class PersonRequest(BaseModel):
    company: str
    designation: str


@app.post("/find-person")
def find_person(req: PersonRequest):

    queries = build_queries(req.company, req.designation)

    search_results = duckduckgo_search(queries)

    best_match = None
    best_score = 0

    for r in search_results:

        url = r["url"]
        snippet = r["snippet"] or ""

        if not is_credible_source(url):
            continue

        text = fetch_page_text(url)

        combined_text = snippet + " " + text

        names = extract_name_from_text(combined_text)

        for name in names:
            score = score_candidate(
                combined_text,
                req.company,
                req.designation,
                name
            )

            if score > best_score:
                best_score = score
                best_match = {
                    "full_name": name,
                    "source_url": url,
                    "confidence": score
                }

        time.sleep(0.8)   # rate limiting

    if not best_match:
        return {
            "status": "no_result",
            "message": "No valid person found"
        }

    first, last = best_match["full_name"].split(" ", 1)

    result = {
        "first_name": first,
        "last_name": last,
        "current_title": req.designation,
        "company": req.company,
        "source_url": best_match["source_url"],
        "confidence_score": best_match["confidence"]
    }

    results_collection.insert_one(result)

    return result