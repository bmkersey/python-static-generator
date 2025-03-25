import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    node = HTMLNode("anchor", "Click Me", None, {"href":"www.test.com", "_target":"_blank"})
    expected = 'href="www.test.com" _target="_blank"'
    self.assertEqual(node.props_to_html(), expected)

  def test_props_to_html_none(self):
    node = HTMLNode("header", "The Company")
    with self.assertRaises(Exception) as context:
      node.props_to_html()
  
  def test_props_to_html_class(self):
    node = HTMLNode("header", "The Company", None, {"class":"bold flex"})
    expected = 'class="bold flex"'
    self.assertEqual(node.props_to_html(), expected)

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
  
  def test_leaf_to_html_a(self):
    node = LeafNode("a", "Click Me", {"href":"www.test.com", "target":"_blank"})
    expected = '<a href="www.test.com" target="_blank">Click Me</a>'
    self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>",
    )
  
  def test_to_html_no_children(self):
    parent_node = ParentNode("p", None)
    with self.assertRaises(ValueError):
      parent_node.to_html()

  def test_to_html_no_tag(self):
    parent_node = ParentNode(None, [LeafNode("p", "Here is some text")])
    with self.assertRaises(ValueError):
      parent_node.to_html()

  def test_to_html_with_multi_children(self):
    child_node1 = LeafNode("li", "child1")
    child_node2 = LeafNode("li", "child2")
    parent_node = ParentNode("ul", [child_node1, child_node2])
    self.assertEqual(parent_node.to_html(), "<ul><li>child1</li><li>child2</li></ul>")

class TestTextToHTML(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.NORMAL_TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold(self):
    node = TextNode("This is text.", TextType.BOLD_TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is text.")

  def test_italic(self):
    node = TextNode("This is text.", TextType.ITALIC_TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is text.")

  def test_code(self):
    node = TextNode("This is text.", TextType.CODE_TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is text.")

  def test_image(self):
    node = TextNode("This is text.", TextType.IMAGE_TEXT, "www.test.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, None)
    self.assertEqual(html_node.props, {"src":"www.test.com", "alt":"This is text."})

  def test_link(self):
    node = TextNode("This is text.", TextType.LINK_TEXT, "www.test.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is text.")
    self.assertEqual(html_node.props, {"href": "www.test.com"})