def generate_html(recipes_list):
    html_content = ""
    for r in recipes_list:
        html_content += f"""
<h2>{r['title']}</h2>
<p>{r['description']}</p>
<a href="{r['url']}">Source</a>
"""
    return html_content
