import os
import re

from block_markdown import markdown_to_html_node
from copy_static_content import copy_static_content


def extract_title(markdown):
    search_result = re.search('^# .*', markdown, re.MULTILINE)
    if not search_result:
        raise Exception('markdown title not found')
    title = markdown[search_result.regs[0][0]:search_result.regs[0][1]].lstrip('#').strip()
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, 'r')
    markdown_content = markdown_file.read()
    markdown_file.close()
    template_file = open(template_path, 'r')
    template_content = template_file.read()
    template_file.close()
    content_in_html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    page = template_content.replace('{{ Title }}', title)
    page = page.replace('{{ Content }}', content_in_html)
    os.makedirs(os.path.split(dest_path)[0], exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    markdown_filepaths = []
    for ospath in os.walk(dir_path_content):
        for file in ospath[2]:
            if file.endswith('md'):
                markdown_filepaths.append(os.path.join(ospath[0], file))
    for markdown_file in markdown_filepaths:
        html_filepath = os.path.join(dest_dir_path, '/'.join(markdown_file.split('/')[1:]).rstrip('.md') + '.html')
        generate_page(markdown_file, template_path, html_filepath)


def main():
    copy_static_content()
    generate_pages_recursive('content/', 'template.html', 'public/')


if __name__ == '__main__':
    main()
