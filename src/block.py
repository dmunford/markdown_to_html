from htmlnode import HTMLNode

block_type_paragraph = 'paragraph'
block_type_heading = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_unordered_list = 'unordered_list'
block_type_ordered_list = 'ordered_list'

def markdown_to_blocks(markdown):
    blocks = markdown.splitlines()
    blocks.append("")
    new_blocks = []
    new_block = ""
    for line in blocks:
        if line == '':
            new_blocks.append(new_block)
            new_block = ""
            continue
        if new_block == "":
            new_block = line.lstrip()
        else:
            new_block += f'\n{line.lstrip()}'
    new_blocks = [block.rstrip() for block in new_blocks if block]

    return new_blocks

def block_to_block_type(block):
    block = block.lstrip().rstrip()
    for i in range(1,7):
        if block.startswith("#"*i + " "):
            return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    is_quote = True
    is_ulist = True
    is_olist = True
    block = [line.lstrip().rstrip() for line in block.split("\n") if line]
    list_num = 1
    for line in block:
        if is_ulist:
            if not line.startswith("- ") and not line.startswith("* "):
                is_ulist = False
        if is_quote:
            if not line.startswith("> "):
                is_quote = False
        if is_olist:
            if line[0] != str(list_num) or line[1] != ".":
                is_olist = False
            else:
                list_num += 1
    if is_quote:
        return block_type_quote
    if is_ulist:
        return block_type_unordered_list
    if is_olist:
        return block_type_ordered_list

    return block_type_paragraph
