import unittest
from textnode import TextType, TextNode


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD_TEXT)
    node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
    self.assertEqual(node, node2)

  def test_different_text(self):
    node = TextNode("This is a text node", TextType.NORMAL_TEXT)
    node2 = TextNode("Chaos is the essence of life", TextType.NORMAL_TEXT)
    self.assertNotEqual(node, node2)

  def test_different_text_type(self):
    node = TextNode("This is a text node", TextType.NORMAL_TEXT)
    node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
    self.assertNotEqual(node, node2)

  def test_different_urls(self):
    node = TextNode("This is a text node", TextType.BOLD_TEXT, "www.test.com")
    node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
    self.assertNotEqual(node, node2)

if __name__ == "__main__":
  unittest.main()
