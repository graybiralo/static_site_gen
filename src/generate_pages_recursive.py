import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Construct full file paths
                markdown_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_file_path, dir_path_content)
                dest_file_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')
                
                # Generate the HTML page
                generate_page(markdown_file_path, template_path, dest_file_path)
                print(f"Generated {dest_file_path}")
