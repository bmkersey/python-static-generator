from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.NORMAL_TEXT:
      new_nodes.append(node)
      continue
    parts = node.text.split(delimiter)
    if len(parts) % 2 == 0:
      raise Exception("Invalid markdown syntax.")
    for index,part in enumerate(parts):
      if not part:
        if index != len(parts) - 1 and index != 0:
          raise Exception("Invalid markdown syntax.")
        continue
      if index % 2 == 0:
        new_nodes.append(TextNode(part, TextType.NORMAL_TEXT))
      else:
        new_nodes.append(TextNode(part, text_type))
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node:
      if node.text_type == TextType.NORMAL_TEXT:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
          new_nodes.append(node)
          continue
        remaining_text = node.text
        for image_alt, image_link in images:
          parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
          if parts[0] :
            new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
          new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, image_link))
          remaining_text = parts[1] if len(parts) > 1 else ""
        if remaining_text:
          new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
      else:
        new_nodes.append(node)
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node:
      if node.text_type == TextType.NORMAL_TEXT:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
          new_nodes.append(node)
          continue
        remaining_text = node.text
        for link_text, link_url in links:
          parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
          if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
          new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, link_url))
          remaining_text = parts[1] if len(parts) > 1 else ""
        if remaining_text:
          new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
      else:
        new_nodes.append(node)
  return new_nodes
   
def text_to_textnodes(text):
  node = TextNode(text, TextType.NORMAL_TEXT) 
  nodes = split_nodes_image([node]) 
  nodes = split_nodes_link(nodes) 
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT) 
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT) 
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT) 
  return nodes