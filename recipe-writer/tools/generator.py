from openai import OpenAI
import re
import os

# Use environment variables instead of config file
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4-turbo")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_cuisine(query):
    """Extract cuisine type from query"""
    cuisine_keywords = {
        'italian': ['italian', 'italy'],
        'mexican': ['mexican', 'mexico'],
        'chinese': ['chinese', 'china'],
        'indian': ['indian', 'india'],
        'french': ['french', 'france'],
        'thai': ['thai', 'thailand'],
        'japanese': ['japanese', 'japan'],
        'mediterranean': ['mediterranean'],
        'american': ['american', 'usa'],
        'spanish': ['spanish', 'spain']
    }
    
    query_lower = query.lower()
    for cuisine, keywords in cuisine_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            return cuisine
    return 'international'

def extract_number(query):
    """Extract number from query"""
    numbers = re.findall(r'\d+', query)
    return int(numbers[0]) if numbers else len(recipes_list)

def generate_professional_article(query, recipes_list):
    """Generate a professional article using template-based approach"""
    cuisine = extract_cuisine(query)
    number = extract_number(query)
    
    # Generate each section
    intro = generate_intro(query, cuisine, number)
    recipe_sections = generate_recipe_sections(recipes_list, cuisine)
    cooking_tips = generate_cooking_tips(cuisine)
    conclusion = generate_conclusion(query, cuisine, number)
    
    # Combine all sections
    article_content = f"{intro}\n\n{recipe_sections}\n\n{cooking_tips}\n\n{conclusion}"
    return article_content

def generate_intro(query, cuisine, number):
    """Generate compelling introduction"""
    prompt = f"""
Write a compelling 2-3 paragraph introduction for an article titled "{query}".

Create anticipation and set the scene for {cuisine} cuisine. Mention what makes {cuisine} food special and what readers will discover in this collection of {number} recipes.

Write in an engaging, warm tone that makes readers excited to cook these dishes.

Format the response as HTML paragraphs using <p> tags.
"""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content
    
    # Ensure it's wrapped in HTML if not already
    if not content.strip().startswith('<'):
        content = content.replace('\n\n', '</p><p>')
        content = f"<p>{content}</p>"
    
    return f"<h1>{query}</h1>\n{content}"

def generate_recipe_sections(recipes_list, cuisine):
    """Generate engaging sections for each recipe"""
    sections = []
    
    for recipe in recipes_list:
        prompt = f"""
Write an engaging 2 paragraph section about this {cuisine} recipe:

Title: {recipe['title']}
Description: {recipe['description']}

Include:
- Why this recipe is special
- Cooking tips or techniques
- Cultural context or flavor notes
- What makes it authentic {cuisine}

Write in engaging food-blog style, keep it profesional and new york times style, no buzzwords.

Format the response as HTML paragraphs using <p> tags.
"""
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Ensure it's wrapped in HTML if not already
        if not content.strip().startswith('<'):
            content = content.replace('\n\n', '</p><p>')
            content = f"<p>{content}</p>"
        
        # Add image if available (with fallback placeholder)
        image_html = ""
        if recipe.get('image_url'):
            image_html = f'<img src="{recipe["image_url"]}" alt="{recipe["title"]}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 16px 0;" />\n'
        else:
            # Fallback: Add a placeholder div that can be styled or replaced
            image_html = f'<div class="recipe-image-placeholder" style="width: 100%; max-width: 600px; height: 300px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 8px; margin: 16px 0; display: flex; align-items: center; justify-content: center; color: #666; font-style: italic;">Image: {recipe["title"]}</div>\n'
        
        sections.append(f"<h2>{recipe['title']}</h2>\n{image_html}{content}\n<p><a href='{recipe['url']}'>View Recipe</a></p>")
    
    return "\n\n".join(sections)

def generate_cooking_tips(cuisine):
    """Generate general cooking tips for the cuisine"""
    prompt = f"""
Write 1-2 paragraphs of general cooking tips for {cuisine} cuisine.

Focus on:
- Essential techniques
- Key ingredients
- Common mistakes to avoid
- Pro tips for authentic flavor

Write in a helpful, encouraging tone that builds confidence in home cooks.

Format the response as HTML paragraphs using <p> tags.
"""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    content = response.choices[0].message.content
    
    # Ensure it's wrapped in HTML if not already
    if not content.strip().startswith('<'):
        content = content.replace('\n\n', '</p><p>')
        content = f"<p>{content}</p>"
    
    return f"<h2>Cooking Tips for {cuisine.title()} Cuisine</h2>\n{content}"

def generate_conclusion(query, cuisine, number):
    """Generate compelling conclusion"""
    prompt = f"""
Write a compelling conclusion paragraph for an article about {query}.

Tie everything together and encourage readers to try these {cuisine} recipes. End on an inspiring note that makes them excited to start cooking.

Keep it warm and encouraging.

Format the response as HTML paragraphs using <p> tags.
"""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    content = response.choices[0].message.content
    
    # Ensure it's wrapped in HTML if not already
    if not content.strip().startswith('<'):
        content = content.replace('\n\n', '</p><p>')
        content = f"<p>{content}</p>"
    
    return content

# Keep the old function for backward compatibility
def generate_summary(recipes_list):
    """Legacy function - now generates full professional article"""
    return generate_professional_article("Recipe Collection", recipes_list)
