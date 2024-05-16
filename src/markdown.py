from htmlnode import HTMLNode
from block import (
        block_type_paragraph,
        block_type_heading,
        block_type_code,
        block_type_quote,
        block_type_unordered_list,
        block_type_ordered_list,
        markdown_to_blocks,
        block_to_block_type,
        )
from html_include import (
        text_node_to_html_node,
        text_to_textnodes,
    )
from os import (
        listdir,
        path,
        mkdir,
    )


def block_to_paragraph(block):
    # <p> </p>
    return "<p>"+block+"</p>"

def block_to_heading(block):
    # <h#> </h#> depending on # in block
    for i in range(1,7):
        if block.startswith("#"*i+" "):
            return f"<h{i}>"+block.lstrip("#"*i+" ")+f"</h{i}>"

def block_to_code(block):
    # <pre><code> </code></pre>
    return "<pre><code>"+block.strip("```").rstrip("```").strip()+"</code></pre>"

def block_to_quote(block):
    # <blockquote> </blockquote>
    blocks = block.split("\n")
    output_line = "<blockquote>"
    for line in blocks:
        output_line += line.lstrip("> ")
    output_line += "</blockquote>"
    return output_line

def block_to_unordered_list(block):
    #<ul> </ul> items: <li> </li>
    blocks = block.split("\n")
    output_line = "<ul>"
    for line in blocks:
        output_line += "<li>"+line.lstrip("* ").lstrip("- ")+"</li>"
    output_line += "</ul>"
    return output_line

def block_to_ordered_list(block):
    #<ol> </ol> items: <li> </li>
    blocks = block.split("\n")
    output_line = "<ol>"
    line_num = 1
    for line in blocks:
        output_line += "<li>"+line.lstrip(f"{line_num}. ")+"</li>"
        line_num += 1
    output_line += "</ol>"
    return output_line

def get_html(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return block_to_paragraph(block)
    if block_type == block_type_heading:
        return block_to_heading(block)
    if block_type == block_type_code:
        return block_to_code(block)
    if block_type == block_type_quote:
        return block_to_quote(block)
    if block_type == block_type_unordered_list:
        return block_to_unordered_list(block)
    if block_type == block_type_ordered_list:
        return block_to_ordered_list(block)
    raise Exception("Somethings fucky")

def markdown_to_html_node(markdown):
    output_html = "<div>"
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        output_html += get_html(block)
    output_html += "</div>"
    return output_html

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block.strip()) == block_type_heading:
            if block.strip().startswith("# "):
                return block.lstrip("# ")
    raise Exception("All pages need a single h1 header!")

def generate_page(from_path, template_path, dest_path):
    print("Generating page from "+from_path+" to "+dest_path+" using "+template_path)
    with open(from_path, 'r') as input_file:
        input_markdown = input_file.read()
        html_string = markdown_to_html_node(input_markdown)
        title = extract_title(input_markdown)
        del input_markdown
    text_nodes = text_to_textnodes(html_string)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    content = ""
    #for node in html_nodes:
    #    content += node.to_html()
    for text_node, html_node in zip(text_nodes, html_nodes):
        content += html_node.to_html()


    if not path.exists(dest_path):
        mkdir(dest_path)
    with open(dest_path+"/index.html", 'w') as output_file:
        with open(template_path, 'r') as template_file:
            for line in template_file:
                if "{{ Title }}" in line:
                    line = line.replace("{{ Title }}", title).rstrip()
                if "{{ Content }}" in line:
                    line = line.replace("{{ Content }}", content).rstrip()
                output_file.write(line) 

def generate_pages_recursively(from_path, template_path, dest_path):
    print("Generating pages from ", from_path)
    for file in listdir(from_path):
        print(file)
        file_path = path.join(from_path, file)
        if path.isfile(file_path):
            generate_page(file_path, template_path, dest_path)
        else:
            new_dest_path = path.join(dest_path, file)
            generate_pages_recursively(file_path, template_path, new_dest_path)
