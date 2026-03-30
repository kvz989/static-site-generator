import os
import shutil
import sys
from pathlib import Path

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import extract_title, markdown_to_html_node
from textnode import TextNode, TextType


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    update_public()
    input_path = "content"
    template_path = "template.html"
    output_path = "docs"
    generate_page_recursive(input_path, template_path, output_path, basepath)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print("Generating pages...")
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(from_path):
            # swap extensions and call generate page
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            # recurse into subfolder
            generate_page_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = Path(from_path).read_text()
    template = Path(template_path).read_text()
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()
    title = extract_title(md)
    result = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    Path(dest_path).write_text(result)


def update_public():
    static_dir = "static"
    public_dir = "docs"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    static_path = Path(static_dir)
    public_path = Path(public_dir)
    copy_static(static_path, public_path)


def copy_static(src, dst):
    dst.mkdir(mode=0o755)
    for entry in src.iterdir():
        if entry.is_file():
            shutil.copy(entry, dst / entry.name)
        else:
            copy_static(entry, dst / entry.name)


if __name__ == "__main__":
    main()
