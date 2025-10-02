from openai import OpenAI
import numpy as np
import faiss
from config import *

client = OpenAI(api_key=OPENAI_API_KEY)

def search_recipes(query, index, id_to_recipe, category=None, tags=None, k=TOP_K):
    # If no filters specified, search all recipes
    if not category and not tags:
        # Use the main index directly for better performance
        query_embedding = client.embeddings.create(input=query, model=EMBEDDING_MODEL).data[0].embedding
        query_vector = np.array([query_embedding]).astype("float32")
        distances, top_indices = index.search(query_vector, k)
        return [id_to_recipe[i] for i in top_indices[0]]
    
    # Filter indices based on category and tags
    filtered_indices = []
    for i, r in id_to_recipe.items():
        recipe_category = r.get("category", "").lower()
        recipe_tags = [tag.lower() for tag in r.get("tags", [])]
        
        # Check category filter (handle comma-separated categories)
        category_match = True
        if category:
            category_lower = category.lower()
            category_match = category_lower in recipe_category
        
        # Check tags filter
        tags_match = True
        if tags:
            tags_lower = [tag.lower() for tag in tags]
            tags_match = any(tag in recipe_tags for tag in tags_lower)
        
        if category_match and tags_match:
            filtered_indices.append(i)
    
    if not filtered_indices:
        return []

    # Create temporary index with filtered vectors
    filtered_vectors = np.array([id_to_recipe[i]["embedding"] for i in filtered_indices]).astype("float32")
    temp_index = faiss.IndexFlatL2(len(filtered_vectors[0]))
    temp_index.add(filtered_vectors)

    query_embedding = client.embeddings.create(input=query, model=EMBEDDING_MODEL).data[0].embedding
    query_vector = np.array([query_embedding]).astype("float32")

    distances, top_indices = temp_index.search(query_vector, min(k, len(filtered_indices)))
    return [id_to_recipe[filtered_indices[i]] for i in top_indices[0]]
