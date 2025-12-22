import requests

HEADERS = {
    "User-Agent": "ADK-Agent-Test/0.1 (contact: you@example.com)"
}

def wikipedia_full_text(query: str):
    api = "https://en.wikipedia.org/w/api.php"

    # 1) Search
    r = requests.get(
        api,
        headers=HEADERS,
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 1,
            "format": "json",
        },
        timeout=10,
    )
    r.raise_for_status()

    search_results = r.json()["query"]["search"]
    if not search_results:
        raise ValueError(f"No Wikipedia results for {query!r}")

    pageid = search_results[0]["pageid"]

    # 2) Fetch full plaintext content
    r = requests.get(
        api,
        headers=HEADERS,
        params={
            "action": "query",
            "pageids": pageid,
            "prop": "extracts",
            "explaintext": 1,
            "redirects": 1,
            "format": "json",
        },
        timeout=10,
    )
    r.raise_for_status()

    page = next(iter(r.json()["query"]["pages"].values()))
    return page["title"], page["extract"]
