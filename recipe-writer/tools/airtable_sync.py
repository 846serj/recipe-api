import requests
import json
import os

# Use environment variables instead of config file
RECIPES_JSON = os.environ.get("RECIPES_JSON", "data/recipes.json")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appa4SaUbDRFYM42O")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME", "Molly's View")

HEADERS = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

def fetch_airtable_records():
    """
    Fetch all records from Airtable and save them locally as JSON.
    Returns the list of recipe records.
    """
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    all_records = []
    offset = None

    print("Fetching records from Airtable...")
    
    while True:
        params = {}
        if offset:
            params["offset"] = offset
            
        try:
            resp = requests.get(url, headers=HEADERS, params=params)
            resp.raise_for_status()  # Raise an exception for bad status codes
            data = resp.json()
            
            for rec in data.get("records", []):
                fields = rec["fields"]
                
                # Handle image field - Airtable stores images as URL strings
                image_url = fields.get("Image Link", "")
                
                all_records.append({
                    "title": fields.get("Title", ""),
                    "description": fields.get("Description", ""),
                    "category": fields.get("Category", ""),
                    "tags": fields.get("Tags", []),
                    "url": fields.get("URL", ""),
                    "image_url": image_url
                })
            
            offset = data.get("offset")
            if not offset:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Airtable: {e}")
            raise

    print(f"Fetched {len(all_records)} records from Airtable")

    # Save locally as JSON
    with open(RECIPES_JSON, "w") as f:
        json.dump(all_records, f, indent=2)

    print(f"Saved recipes to {RECIPES_JSON}")
    return all_records

def sync_and_get_recipes():
    """
    Convenience function to fetch latest recipes from Airtable.
    This is the main function other modules should use.
    """
    return fetch_airtable_records()
