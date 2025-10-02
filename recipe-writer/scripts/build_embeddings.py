#!/usr/bin/env python3
"""
Script to build embeddings for recipes from Airtable.
Usage: python scripts/build_embeddings.py
"""

import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import airtable_sync, embeddings
from config import *

def main():
    print("Fetching latest recipes from Airtable...")
    recipes = airtable_sync.fetch_airtable_records()
    
    print(f"Found {len(recipes)} recipes")
    print("Generating embeddings...")
    
    # Generate embeddings
    recipes_with_embeddings = embeddings.generate_embeddings(recipes)
    
    # Save embeddings
    embeddings.save_embeddings(recipes_with_embeddings)
    
    print(f"Embeddings saved to {EMBEDDINGS_JSON}")

if __name__ == "__main__":
    main()
