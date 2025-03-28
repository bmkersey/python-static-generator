from enum import Enum
import re
from helpersinline import text_to_textnodes
from htmlnode import text_node_to_html_node, ParentNode
from textnode import TextNode, TextType

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  stripped_blocks = []
  for block in blocks:
    if block and block != "":
      new_string = block.strip()
      stripped_blocks.append(new_string)
  return stripped_blocks

def block_to_block_type(block):
  if re.match(r'^#{1,6} ', block):
      return BlockType.HEADING
  elif block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  elif block.startswith(">"):
    lines = block.split("\n")
    for line in lines:
      if not line.startswith(">"):
        return BlockType.PARAGRAPH
    return BlockType.QUOTE
  elif block.startswith("- "):
    lines = block.split("\n")
    for line in lines:
      if not line.startswith("- "):
        return BlockType.PARAGRAPH
    return BlockType.UNORDERED_LIST
  elif block.startswith("1. "):
    lines = block.split("\n")
    is_ordered_list = True
    for i, line in enumerate(lines):
      expected = f"{i+1}. "
      if not line.startswith(expected):
        return BlockType.PARAGRAPH
    if is_ordered_list:
      return BlockType.ORDERED_LIST
  else:
    return BlockType.PARAGRAPH
  
def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  new_nodes = []
  for block in blocks:
    block_type = block_to_block_type(block)
    match block_type:
      case BlockType.PARAGRAPH:
        node = create_paragraph_node(block)
        new_nodes.append(node)
      case BlockType.HEADING:
        node = create_heading_node(block)
        new_nodes.append(node)
      case BlockType.CODE:
        node = create_code_node(block)
        new_nodes.append(node)
      case BlockType.QUOTE:
        node = create_quote_node(block)
        new_nodes.append(node)
      case BlockType.UNORDERED_LIST:
        node = create_ul_node(block)
        new_nodes.append(node)
      case BlockType.ORDERED_LIST:
        node = create_ol_node(block)
        new_nodes.append(node)
  parent_node = ParentNode("div", new_nodes)
  return parent_node

def create_ol_node(block):
  lines = block.split("\n")
  li_nodes = []
  for line in lines:
    if line and line[0].isdigit():
      item_text = line[3:].strip()
      li_node = create_li_node(item_text)
      li_nodes.append(li_node)
  ol_node = ParentNode("ol", li_nodes)
  return ol_node

def create_ul_node(block):
  lines = block.split("\n")
  li_nodes = []
  for line in lines:
    if line.startswith("-"):
      item_text = line[1:].strip()
      li_node = create_li_node(item_text)
      li_nodes.append(li_node)

  ul_node = ParentNode("ul", li_nodes)
  return ul_node

def create_li_node(content):
  children = text_to_children(content)
  li_node = ParentNode("li", children)
  return li_node

def create_quote_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if line.startswith(">"):
      new_line = line[1:].strip()
      new_lines.append(new_line)
    else:
      new_lines.append(line)
  
  content = "\n".join(new_lines)
  children = text_to_children(content)
  quote_node = ParentNode("blockquote", children)
  return quote_node

def create_paragraph_node(block):
  lines = block.split("\n")
  content = " ".join(lines)
  children = text_to_children(content)
  return ParentNode("p", children)
  
def create_code_node(block):
  content = block[3:-3].strip()
  text_node = TextNode(content, TextType.CODE_TEXT)
  code_node = text_node_to_html_node(text_node)
  pre_node = ParentNode("pre", [code_node])
  return pre_node

def create_heading_node(block):
  level = 0
  for char in block:
    if char == "#":
      level += 1
    else:
      break
  
  level = min(6,max(1,level))
  content = block[level +1:]

  children = text_to_children(content)
  return ParentNode(f"h{level}", children)

def text_to_children(block):
  text_nodes = text_to_textnodes(block)
  html_nodes = []
  for node in text_nodes:
    html_node = text_node_to_html_node(node)
    html_nodes.append(html_node)
  return html_nodes