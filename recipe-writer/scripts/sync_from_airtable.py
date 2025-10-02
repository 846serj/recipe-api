#!/usr/bin/env python3
"""
Complete workflow script to sync from Airtable and rebuild everything.
Usage: python scripts/sync_from_airtable.py
"""

import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import airtable_sync, embeddings, vector_store
from config import *

def main():
    print("=== Airtable Sync Workflow ===")
    
    # Step 1: Fetch latest recipes from Airtable
    print("\n1. Fetching latest recipes from Airtable...")
    recipes = airtable_sync.fetch_airtable_records()
    
    # Step 2: Generate embeddings
    print("\n2. Generating embeddings...")
    recipes_with_embeddings = embeddings.generate_embeddings(recipes)
    embeddings.save_embeddings(recipes_with_embeddings)
    
    # Step 3: Build FAISS index
    print("\n3. Building FAISS index...")
    index = vector_store.build_faiss_index(recipes_with_embeddings)
    
    print(f"\n✅ Complete! Index contains {index.ntotal} vectors")
    print("You can now run queries with: python scripts/run_query.py")

if __name__ == "__main__":
    main()
