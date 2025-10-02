#!/usr/bin/env python3
"""
Recipe API Server
A dedicated Python API for recipe article generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
openai_client = OpenAI(api_key=openai_api_key)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "message": "Recipe API server is running!",
        "version": "1.0.0"
    }), 200

@app.route('/recipe-query', methods=['POST'])
def recipe_query():
    """Handle recipe queries and generate articles"""
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"error": "Query is required"}), 400

        print(f"Processing recipe query: {query}")

        # Generate professional recipe article
        prompt = f"""Write a professional article about "{query}". 

Create a compelling article with:
- An engaging introduction
- 3-5 recipe sections with descriptions  
- Cooking tips
- A conclusion

Format the response as HTML with proper headings and paragraphs.
"""
        
        response = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        article_content = response.choices[0].message.content or ''

        return jsonify({
            "success": True,
            "html": article_content,
            "summary": "Recipe article generated successfully"
        }), 200

    except Exception as e:
        print(f"Error generating recipe article: {e}")
        return jsonify({
            "error": "Failed to generate recipe content", 
            "details": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
