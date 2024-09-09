import os
from new_function_textnode import markdown_to_html_node  
from extract_title import extract_title  

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as file:
        markdown_content = file.read()

    # Read the template file
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()

    # Extract title from markdown
    try:
        title = extract_title(markdown_content)
    except ValueError as e:
        raise RuntimeError(f"Error extracting title: {e}")

    # Replace placeholders in the template
    html_page = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, 'w') as file:
        file.write(html_page)

    print(f"Page generated and saved to {dest_path}")
