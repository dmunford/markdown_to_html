from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_link,
        text_type_image,
    )
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

block_type_paragraph = 'paragraph'
block_type_heading = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_unordered_list = 'unordered_list'
block_type_ordered_list = 'ordered_list'

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(value = text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag = "b", value = text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag = "i", value = text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode(tag = "code", value = text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode(tag = "a", value = text_node.text, props={"href":text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode(tag="img", value = "", props={"src":text_node.url, "alt":text_node.text})
    raise Exception("No matching text type...")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if type(old_node) != TextNode:
            new_nodes.append(old_node)
            continue
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter)%2 != 0:
            raise Exception("No closing delimiter in node\n" + old_node.text)
        split_nodes = old_node.text.split(delimiter)
        for i, node in enumerate(split_nodes):
            if len(node) == 0:
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(node, text_type_text))
            else:
                new_nodes.append(TextNode(node, text_type))
    return new_nodes

def extract_markdown_images(text):
    # regex r"!\[(.*?)\]\((.*?)\)"
    found_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return found_images

def extract_markdown_links(text):
    # regex r"\[(.*?)\]\((.*?)\)"
    found_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return found_links

def split_nodes_image(old_nodes):
    new_nodes = []
    extracted_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            node_text = node.text
            extract_image = extract_markdown_images(node_text)
            for i, image in enumerate(extract_image):
                node_text = node_text.split(f"![{image[0]}]({image[1]})")
                extracted_nodes.append(node_text[0])
                extracted_nodes.append(image)
                node_text = node_text[-1]
            extracted_nodes.append(node_text)
        else:
            extracted_nodes.append(node)
    extracted_nodes = [node for node in extracted_nodes if node]
    for i, node in enumerate(extracted_nodes):
        if type(node) == str:
            new_nodes.append(TextNode(node, text_type_text))
        elif type(node) == TextNode:
            new_nodes.append(node)
        else:
            new_nodes.append(TextNode(node[0], text_type_image, node[1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    extracted_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            node_text = node.text
            extract_link = extract_markdown_links(node_text)
            for i, link in enumerate(extract_link):
                node_text = node_text.split(f"[{link[0]}]({link[1]})")
                extracted_nodes.append(node_text[0])
                extracted_nodes.append(link)
                node_text = node_text[-1]
            extracted_nodes.append(node_text)
        else:
            extracted_nodes.append(node)
    extracted_nodes = [node for node in extracted_nodes if node]
    for i, node in enumerate(extracted_nodes):
        if type(node) == str:
            new_nodes.append(TextNode(node, text_type_text))
        elif type(node) == TextNode:
            new_nodes.append(node)
        else:
            new_nodes.append(TextNode(node[0], text_type_link, node[1]))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, text_type_text)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    delims = [
            ("**", text_type_bold),
            ("*", text_type_italic),
            ("`", text_type_code),
            ]
    for delim in delims:
        new_nodes = split_nodes_delimiter(new_nodes, delim[0], delim[1])

    return new_nodes
