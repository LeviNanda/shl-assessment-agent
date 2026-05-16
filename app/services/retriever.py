import pickle
from pathlib import Path
from typing import List, Dict

import faiss
from sentence_transformers import SentenceTransformer

from app.services.context_extractor import extract_context


INDEX_PATH = Path("app/data/faiss.index")
META_PATH = Path("app/data/metadata.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_index = None
_products = None


def load_retriever():
    global _model, _index, _products

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    if _index is None:
        _index = faiss.read_index(str(INDEX_PATH))

    if _products is None:
        with open(META_PATH, "rb") as f:
            _products = pickle.load(f)


def keyword_score(query: str, product: Dict) -> float:
    context = extract_context(query)

    product_text = (
        product.get("name", "") + " " +
        product.get("description", "") + " " +
        product.get("raw_text", "")
    ).lower()

    score = 0.0

    for role in context["roles"]:
        if role in product_text:
            score += 2

    for skill in context["technical_skills"]:
        if skill in product_text:
            score += 3

    for skill in context["soft_skills"]:
        if skill in product_text:
            score += 2

    if context["personality_required"]:
        if any(term in product_text for term in ["opq", "personality", "behavior", "behaviour"]):
            score += 5

    if context["cognitive_required"]:
        if any(term in product_text for term in ["cognitive", "reasoning", "aptitude", "ability", "gsa"]):
            score += 5

    return score


def search_catalog(query: str, top_k: int = 10) -> List[Dict]:
    load_retriever()

    query_embedding = _model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = _index.search(query_embedding, min(top_k * 4, len(_products)))

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        product = _products[idx]

        semantic_score = 1 / (1 + float(distance))
        lexical_score = keyword_score(query, product)

        final_score = (0.6 * semantic_score) + (0.4 * lexical_score)

        item = dict(product)
        item["score"] = final_score
        results.append(item)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:top_k]