class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    if not self.props:
      raise Exception("No props provided")
    return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag=tag, value=value, props=props)

  def to_html(self):
    if not self.value:
      raise ValueError("Missing value")
    if self.tag == None:
      return self.value
    if self.props != None:
      return f'<{self.tag} {" ".join([f'{key}="{value}"' for key, value in self.props.items()])}>{self.value}</{self.tag}>'
    return f'<{self.tag}>{self.value}</{self.tag}>'
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, children=children, props=props)
  
  def to_html(self):
    if not self.tag:
      raise ValueError("Missing tag")
    if not self.children:
      raise ValueError("Missing children")
    html = f"<{self.tag}"
    if self.props != None:
      html += " ".join([f' {key}="{value}"' for key, value in self.props.items()])
    html += ">"
    for child in self.children:
      html += child.to_html()
    html += f"</{self.tag}>"
    return html