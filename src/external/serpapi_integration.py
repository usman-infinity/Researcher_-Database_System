from serpapi import GoogleSearch

def search_serpapi(query, api_key, num=10):
    """Search Google Scholar via SerpAPI and return simplified results list.

    Each result will be a dict with keys: title, authors, year, link, snippet
    """
    if not api_key:
        raise RuntimeError("SERPAPI_KEY not configured")

    params = {
        "engine": "google_scholar",
        "q": query,
        "num": num,
        "api_key": api_key,
    }
    search = GoogleSearch(params)
    res = search.get_dict()

    results = []
    for item in res.get("organic_results", []):
        r = {
            "title": item.get("title"),
            "authors": item.get("publication_info", {}).get("summary") or item.get("publication_info", {}).get("authors"),
            "year": item.get("publication_info", {}).get("year"),
            "link": item.get("link") or item.get("serpapi_link"),
            "snippet": item.get("snippet"),
        }
        results.append(r)
    return results
