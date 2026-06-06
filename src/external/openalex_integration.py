import requests


def search_openalex(query, num=10):
    """Search OpenAlex works and return simplified result objects."""
    if not query:
        return []

    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": num,
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        title = item.get("title")
        publication_date = item.get("publication_date")
        year = None
        if publication_date:
            year = publication_date.split("-")[0]
        authors = []
        for author in item.get("authorships", []):
            if author.get("author", {}).get("display_name"):
                authors.append(author["author"]["display_name"])
        results.append({
            "title": title,
            "authors": ", ".join(authors),
            "year": year,
            "link": item.get("id"),
            "snippet": item.get("abstract_inverted_index") and "Abstract available" or item.get("display_name"),
            "source": item.get("primary_source", {}).get("display_name"),
        })
    return results
