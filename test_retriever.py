from app.services.retriever import search_catalog

query = "Hiring a mid-level Java developer with coding and communication skills"

results = search_catalog(query, top_k=5)

for i, item in enumerate(results, start=1):
    print(f"\n{i}. {item['name']}")
    print(item["url"])
    print("Score:", round(item["score"], 4))