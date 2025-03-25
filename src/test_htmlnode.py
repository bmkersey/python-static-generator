import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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