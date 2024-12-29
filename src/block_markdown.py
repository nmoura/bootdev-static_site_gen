import re

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    in_code_block = False
    lines = markdown.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                if current_block:
                    blocks.append('\n'.join(current_block).strip())
                current_block = [lines[i]]
                continue
            else:
                current_block.append(lines[i])
                if current_block:
                    blocks.append('\n'.join(current_block).strip())
                current_block = []
                continue
        if in_code_block or lines[i] != '':
            current_block.append(lines[i])
            if i == len(lines) -1:
                blocks.append('\n'.join(current_block).strip())
            continue
        if not in_code_block and lines[i] == '':
            if current_block:
                blocks.append('\n'.join(current_block).strip())
            current_block = []
            continue
    return blocks


def block_to_block_type(block):
    regex = re.compile(
                r'(?P<heading>#{1,6} .*)|'
                r'(?P<code>^```(\n|.)+```)|'
                r'(?P<quote>^>.*(\n>.+)+|^>.*)|'
                r'(?P<unordered_list>^(\*|\-) .*(\n(\*|\-) .*)+|^(\*|\-) .*)|'
                r'(?P<seems_ordered_list>^\d\. .*(\n\d\. .*)+|^\d\. .*)'
            )
    fullmatch = re.fullmatch(regex, block)
    if not fullmatch:
        return 'paragraph'
    for k, v in fullmatch.groupdict().items():
        if k == 'seems_ordered_list':
            return 'ordered_list' if _is_properly_ordered(block) else 'paragraph'
        elif v:
            return k


def _is_properly_ordered(block):
    i = 1
    lines = block.split('\n')
    for line in lines:
        if line.startswith(str(i)):
            i += 1
            continue
        else:
            return False
    return True


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case 'heading':
            return __header_block_to_html_nodes(block)
        case 'paragraph':
            return __paragraph_block_to_html_nodes(block)
        case 'quote':
            return __quote_block_to_html_nodes(block)
        case 'code':
            return __code_block_to_html_nodes(block)
        case 'unordered_list':
            return __unordered_list_block_to_html_nodes(block)
        case 'ordered_list':
            return __ordered_list_block_to_html_nodes(block)


def __header_block_to_html_nodes(md_header):
    header_size = len(re.match(r'^#+', md_header).group())
    cleaned_header = md_header.lstrip('#').strip()
    return __build_node_tree_from_text(cleaned_header, f"h{header_size}")


def __paragraph_block_to_html_nodes(md_paragraph):
    cleaned_paragraph = md_paragraph.strip()
    return __build_node_tree_from_text(cleaned_paragraph, "p")


def __code_block_to_html_nodes(md_code):
    cleaned_md_code = re.sub(r'(^```|```$)', '', md_code)
    return ParentNode("pre", [LeafNode("code", cleaned_md_code, None)], None)


def __quote_block_to_html_nodes(md_quote):
    cleaned_md_quote = re.sub(r'>(\s+)?', '', md_quote)
    return __build_node_tree_from_text(cleaned_md_quote, "blockquote")


def __ordered_list_block_to_html_nodes(md_list):
    list_nodes = []
    for item in md_list.split('\n'):
        cleaned_item = re.sub(r'\d+\. ', '', item).strip()
        list_nodes.append(__build_node_tree_from_text(cleaned_item, "li"))
    return ParentNode("ol", list_nodes, None)


def __unordered_list_block_to_html_nodes(md_list):
    list_nodes = []
    for item in md_list.split('\n'):
        cleaned_item = re.sub(r'(-|\*) ', '', item).strip()
        list_nodes.append(__build_node_tree_from_text(cleaned_item, "li"))
    return ParentNode("ul", list_nodes, None)


def __build_node_tree_from_text(text, tag=None):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    if len(html_nodes) > 1 or html_nodes[0].tag:
        return ParentNode(f"{tag}", html_nodes, None)
    else:
        return LeafNode(f"{tag}", text, None)


def markdown_to_html_node(markdown):
    html_nodes = []
    for block in markdown_to_blocks(markdown):
        html_nodes.append(block_to_html_node(block))
    return ParentNode("div", html_nodes, None)
