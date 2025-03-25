import unittest
from htmlnode import HTMLNode

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