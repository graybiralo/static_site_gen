import os
import shutil
from generate_page import generate_page 
from generate_pages_recursive import generate_pages_recursive
def main():
    # Define directories
    source_directory = 'static'
    destination_directory = 'public'
    content_directory = 'content'
    template_path = 'template.html'
    
    # Ensure the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory {source_directory} does not exist.")
        return

    # Delete everything in the public directory
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
        print(f"Deleted all contents of {destination_directory}")
    
    # Recreate the public directory
    os.makedirs(destination_directory)
    print(f"Created destination directory {destination_directory}")

    # Copy all static files
    copy_directory_recursive(source_directory, destination_directory)
    print("Static files copied successfully.")

    # Generate HTML files from markdown
    if os.path.exists(template_path):
        generate_pages_recursive(content_directory, template_path, destination_directory)
        print("All pages generated successfully.")
    else:
        print("Template file does not exist.")


def copy_directory_recursive(src, dest):
    # Loop through the items in the source directory
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        # If it's a directory then recurse into it
        if os.path.isdir(src_item):
            print(f"Copying directory: {src_item} to {dest_item}")
            os.makedirs(dest_item, exist_ok=True)
            copy_directory_recursive(src_item, dest_item)
        else:
            # Otherwise it's a file so copy it
            print(f"Copying file: {src_item} to {dest_item}")
            shutil.copy2(src_item, dest_item)

if __name__ == "__main__":
    main()
