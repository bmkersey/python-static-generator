from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if not isinstance(node, TextNode):
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
