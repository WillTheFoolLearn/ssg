import os, shutil
from inline import markdown_to_blocks, markdown_to_html_node

def move_files(path = ""):

    src_dir = "static"
    dest_dir = "public"

    if not path:
        shutil.rmtree(dest_dir)
        os.mkdir(dest_dir)
    
    path_contents = os.listdir(os.path.join(src_dir, path))

    for contents in path_contents:
        content_path = os.path.join(src_dir, path, contents)

        if os.path.isfile(content_path):
            dest_location = os.path.join(dest_dir, path)
            if os.path.exists(os.path.join(dest_location)):
                shutil.copy(content_path, dest_location)

            else:
                os.mkdir(os.path.join(dest_dir, path))
                shutil.copy(content_path, dest_location)
        else:
            move_files(os.path.join(path, contents))

    return

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
        else:
            raise Exception("Good job, doofus")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path_contents = open(from_path)
    template_path_contents = open(template_path)

    page_title = extract_title(from_path_contents.read())

    from_path_contents = open("content/index.md")

    html_code = markdown_to_html_node(from_path_contents.read()).to_html()

    html = template_path_contents.read().replace("{{ Title }}", page_title).replace("{{ Content }}", html_code)

    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)

    temp_site = open(dest_path, "w")
    temp_site.write(html)
    temp_site.close()
    from_path_contents.close()
    template_path_contents.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not dest_dir_path:
        os.mkdir(dest_dir_path)

    path_contents = os.listdir(dir_path_content)

    for contents in path_contents:
        content_path = os.path.join(dir_path_content, contents)

        if os.path.isfile(content_path):
            from_path_contents = open(content_path)
            template_path_contents = open(template_path)

            page_title = extract_title(from_path_contents.read())

            from_path_contents = open(content_path)

            html_code = markdown_to_html_node(from_path_contents.read()).to_html()

            html = template_path_contents.read().replace("{{ Title }}", page_title).replace("{{ Content }}", html_code)

            os.makedirs(dest_dir_path, exist_ok=True)

            file_name = contents.split(".")[0]
            html_file = file_name + ".html"

            temp_site = open(os.path.join(dest_dir_path, html_file), "w")
            temp_site.write(html)
            temp_site.close()
            from_path_contents.close()
            template_path_contents.close()

        else:
            generate_pages_recursive(os.path.join(dir_path_content, contents), template_path, os.path.join(dest_dir_path, contents))

    
def main():
    move_files()
    generate_pages_recursive("content", "template.html", "public")
    return

main()
