import json
import time
import os
from openai import OpenAI

# Use environment variables instead of config file
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "100"))

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_embeddings(recipes):
    """Generate embeddings for all recipes in batches."""
    if "embedding" in recipes[0]:
        return recipes  # already embedded

    for i in range(0, len(recipes), BATCH_SIZE):
        batch = recipes[i:i+BATCH_SIZE]
        texts = [
            r["title"] + " " + r["description"] + " " + " ".join(r.get("tags", []))
            for r in batch
        ]
        resp = client.embeddings.create(input=texts, model=EMBEDDING_MODEL)
        for j, r in enumerate(batch):
            r["embedding"] = resp.data[j].embedding
        print(f"Processed batch {i}-{i+len(batch)}")
        time.sleep(1)  # avoid rate limits
    return recipes

def save_embeddings(recipes, path=EMBEDDINGS_JSON):
    with open(path, "w") as f:
        json.dump(recipes, f)

def load_embeddings(path=EMBEDDINGS_JSON):
    with open(path) as f:
        return json.load(f)
