import faiss
import numpy as np
from config import *

def build_faiss_index(recipes):
    dimension = len(recipes[0]["embedding"])
    index = faiss.IndexFlatL2(dimension)
    vectors = np.array([r["embedding"] for r in recipes]).astype("float32")
    index.add(vectors)
    faiss.write_index(index, FAISS_INDEX_FILE)
    return index

def load_faiss_index():
    return faiss.read_index(FAISS_INDEX_FILE)

def get_id_to_recipe(recipes):
    return {i: r for i, r in enumerate(recipes)}
