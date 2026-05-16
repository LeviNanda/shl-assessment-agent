from app.services.retriever import search_catalog


def compare_assessments(query: str) -> str:
    results = search_catalog(query, top_k=2)

    if len(results) < 2:
        return "I could not find enough matching SHL assessments in the catalog to compare."

    a = results[0]
    b = results[1]

    return (
        "Here is a grounded comparison based only on the SHL catalog:\n\n"
        f"1. {a.get('name')}\n"
        f"URL: {a.get('url')}\n\n"
        f"2. {b.get('name')}\n"
        f"URL: {b.get('url')}\n\n"
        "Choose the assessment that better matches the hiring requirement."
    )