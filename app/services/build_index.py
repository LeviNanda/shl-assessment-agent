import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DATA_PATH = Path("app/data/catalog.json")
INDEX_PATH = Path("app/data/faiss.index")
META_PATH = Path("app/data/metadata.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"


def load_catalog():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_documents(products):
    docs = []

    for product in products:
        text = f"""
        Name: {product.get('name', '')}
        Description: {product.get('description', '')}
        Raw Text: {product.get('raw_text', '')}
        """

        docs.append(text)

    return docs


def build_faiss_index():

    print("Loading catalog...")
    products = load_catalog()

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Preparing documents...")
    docs = prepare_documents(products)

    print("Generating embeddings...")
    embeddings = model.encode(
        docs,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    print("Building FAISS index...")
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("Saving FAISS index...")
    faiss.write_index(index, str(INDEX_PATH))

    print("Saving metadata...")
    with open(META_PATH, "wb") as f:
        pickle.dump(products, f)

    print(f"Indexed {len(products)} SHL assessments")


if __name__ == "__main__":
    build_faiss_index()