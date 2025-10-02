#!/usr/bin/env python3
"""
Script to build FAISS index from recipes with embeddings.
Usage: python scripts/build_faiss_index.py
"""

import json
import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import vector_store, embeddings
from config import *

def main():
    print("Loading recipes with embeddings...")
    recipes = embeddings.load_embeddings()
    
    print(f"Found {len(recipes)} recipes with embeddings")
    print("Building FAISS index...")
    
    # Build FAISS index
    index = vector_store.build_faiss_index(recipes)
    
    print(f"FAISS index saved to {FAISS_INDEX_FILE}")
    print(f"Index contains {index.ntotal} vectors")

if __name__ == "__main__":
    main()
