import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown format, section not closed")
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r'\!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)


def __split_nodes_helper(old_nodes, extract_fn, text_type):
    new_nodes = []
    for old_node in old_nodes:
        extracted_md_items = extract_fn(old_node.text)
        if not extracted_md_items:
            new_nodes.append(old_node)
            continue
        sections = []
        remaining = old_node.text
        for i in range(len(extracted_md_items)):
            split_delimiter = f"[{extracted_md_items[i][0]}]({extracted_md_items[i][1]})"
            if text_type == TextType.IMAGE:
                split_delimiter = '!' + split_delimiter
            splitted = remaining.split(split_delimiter, 1)
            if len(splitted) != 2:
                raise ValueError("Invalid markdown, section not closed")
            if len(splitted[0]) > 0:
                sections.append(TextNode(splitted[0], TextType.TEXT))
            sections.append(TextNode(extracted_md_items[i][0], text_type, extracted_md_items[i][1]))
            if len(splitted[1]) > 0:
                remaining = splitted[1]
                if i == len(extracted_md_items) - 1:
                    sections.append(TextNode(splitted[1], TextType.TEXT))
        new_nodes.extend(sections)
    return new_nodes 


def split_nodes_image(old_nodes):
    return __split_nodes_helper(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return __split_nodes_helper(old_nodes, extract_markdown_links, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
