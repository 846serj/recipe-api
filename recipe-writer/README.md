# Recipe Writer - RAG Pipeline

A modular RAG (Retrieval-Augmented Generation) pipeline for recipe content creation using OpenAI embeddings and FAISS vector search, with **Airtable integration** as the source of truth.

## Features

- **Airtable Integration**: Automatic sync from Airtable as source of truth
- **Modular Architecture**: Clean separation of concerns with dedicated tool modules
- **Scalable**: Handles 10k+ recipes with batch embedding generation
- **Flexible**: Easy to swap LLMs or vector stores
- **WordPress Ready**: Built-in HTML output generation
- **Filtered Search**: Search by category and tags
- **Real-time Updates**: Fetch latest data from Airtable on demand

## Project Structure

```
recipe-writer/
│
├── data/
│   ├── recipes.json                    # Input recipe data
│   ├── recipes_with_embeddings.json    # Recipes with generated embeddings
│   └── recipes.index                   # FAISS vector index
│
├── tools/
│   ├── __init__.py
│   ├── airtable_sync.py                # Airtable API integration
│   ├── embeddings.py                   # OpenAI embedding generation
│   ├── vector_store.py                 # FAISS index management
│   ├── retrieval.py                    # Recipe search functionality
│   ├── generator.py                    # LLM-based content generation
│   └── html_formatter.py               # HTML output generation
│
├── scripts/
│   ├── sync_from_airtable.py           # Complete Airtable sync workflow
│   ├── build_embeddings.py             # Generate embeddings for recipes
│   ├── build_faiss_index.py            # Build FAISS vector index
│   └── run_query.py                    # Example query script
│
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
└── README.md
```

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   Edit `config.py` and set your API keys:
   ```python
   OPENAI_API_KEY = "your-openai-api-key-here"
   AIRTABLE_API_KEY = "your-airtable-api-key-here"
   AIRTABLE_BASE_ID = "your-airtable-base-id"
   AIRTABLE_TABLE_NAME = "Recipes"  # or your table name
   ```

3. **Set up Airtable**:
   Create an Airtable base with a "Recipes" table containing these fields:
   - **Title** (Single line text)
   - **Description** (Long text)
   - **Category** (Single select: Summer, Fall, Winter, Spring)
   - **Tags** (Multiple select: grill, seafood, healthy, etc.)
   - **URL** (URL field)

## Usage

### Option A: Complete Airtable Sync (Recommended)
```bash
python scripts/sync_from_airtable.py
```

### Option B: Step-by-Step Process
```bash
# 1. Sync from Airtable and generate embeddings
python scripts/build_embeddings.py

# 2. Build FAISS index
python scripts/build_faiss_index.py

# 3. Run queries
python scripts/run_query.py
```

### Option C: Fresh Data Query
```bash
# Fetch latest from Airtable before querying
python scripts/run_query.py --fresh
```

## Configuration

Key settings in `config.py`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `AIRTABLE_API_KEY`: Your Airtable API key
- `AIRTABLE_BASE_ID`: Your Airtable base ID
- `AIRTABLE_TABLE_NAME`: Your Airtable table name (default: "Recipes")
- `EMBEDDING_MODEL`: OpenAI embedding model (default: "text-embedding-3-small")
- `LLM_MODEL`: OpenAI chat model (default: "gpt-4-turbo")
- `TOP_K`: Number of top results to retrieve (default: 10)
- `BATCH_SIZE`: Batch size for embedding generation (default: 100)

## API Reference

### Tools

#### `airtable_sync.py`
- `fetch_airtable_records()`: Fetch all records from Airtable and save locally
- `sync_and_get_recipes()`: Convenience function to get latest recipes

#### `embeddings.py`
- `generate_embeddings(recipes)`: Generate embeddings for recipe list
- `save_embeddings(recipes, path)`: Save recipes with embeddings to JSON
- `load_embeddings(path)`: Load recipes with embeddings from JSON

#### `vector_store.py`
- `build_faiss_index(recipes)`: Build FAISS index from recipes
- `load_faiss_index()`: Load existing FAISS index
- `get_id_to_recipe(recipes)`: Create ID to recipe mapping

#### `retrieval.py`
- `search_recipes(query, index, id_to_recipe, category, tags, k)`: Search recipes with filters

#### `generator.py`
- `generate_summary(recipes_list)`: Generate LLM summary of recipes

#### `html_formatter.py`
- `generate_html(recipes_list)`: Generate HTML output for recipes

## Example Usage

### Basic Usage with Airtable
```python
from tools import airtable_sync, embeddings, vector_store, retrieval, generator, html_formatter

# Sync from Airtable
recipes = airtable_sync.fetch_airtable_records()

# Generate embeddings and build index
recipes_with_embeddings = embeddings.generate_embeddings(recipes)
index = vector_store.build_faiss_index(recipes_with_embeddings)
id_to_recipe = vector_store.get_id_to_recipe(recipes_with_embeddings)

# Search
results = retrieval.search_recipes(
    "summer grilling recipes", 
    index, 
    id_to_recipe, 
    category="Summer", 
    tags=["grill"]
)

# Generate content
summary = generator.generate_summary(results)
html = html_formatter.generate_html(results)
```

### Using Existing Data
```python
from tools import embeddings, vector_store, retrieval, generator, html_formatter

# Load existing data
recipes = embeddings.load_embeddings()
index = vector_store.load_faiss_index()
id_to_recipe = vector_store.get_id_to_recipe(recipes)

# Search and generate
results = retrieval.search_recipes("summer recipes", index, id_to_recipe)
summary = generator.generate_summary(results)
```

## Performance

- **Embedding Generation**: ~100 recipes per minute (with rate limiting)
- **Search Speed**: Sub-second retrieval for 10k+ recipes
- **Memory Usage**: ~50MB for 10k recipes with embeddings

## License

MIT License
