import unittest
from textnode import TextNode, TextType
from helpers import split_nodes_delimiter

class TestHelpers(unittest.TestCase):
  def test_balanced(self):
    node = TextNode("This is text. **This is bold text.** More normal text.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    self.assertEqual(new_nodes, [TextNode("This is text. ", TextType.NORMAL_TEXT),TextNode("This is bold text.", TextType.BOLD_TEXT),TextNode(" More normal text.", TextType.NORMAL_TEXT)])
  
  def test_no_delimiters(self):
    node = TextNode("This text has no delimiters.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    self.assertEqual(new_nodes, [TextNode("This text has no delimiters.", TextType.NORMAL_TEXT)])
  
  def test_unbalanced(self):
    node = TextNode("This is text. **This is bold text. More normal text.", TextType.NORMAL_TEXT)
    with self.assertRaises(Exception):
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
  
  def test_multiple_nodes(self):
    node = TextNode("This is text. **This is bold text.** More normal text.", TextType.NORMAL_TEXT)
    node2 = TextNode("The menu **doesnt** work if you live.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD_TEXT)
    self.assertEqual(new_nodes, [TextNode("This is text. ", TextType.NORMAL_TEXT),TextNode("This is bold text.", TextType.BOLD_TEXT),
      TextNode(" More normal text.", TextType.NORMAL_TEXT),TextNode("The menu ", TextType.NORMAL_TEXT),TextNode("doesnt", TextType.BOLD_TEXT),
      TextNode(" work if you live.", TextType.NORMAL_TEXT)
    ])

  def test_multiple_delim_instances(self):
    node = TextNode("The menu **doesnt** work if you **live.**", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    self.assertEqual(new_nodes,[TextNode("The menu ", TextType.NORMAL_TEXT), TextNode("doesnt", TextType.BOLD_TEXT),
      TextNode(" work if you ", TextType.NORMAL_TEXT), TextNode("live.", TextType.BOLD_TEXT)
    ])
  
  def test_start_delim(self):
    node = TextNode("**Here** is where you should be", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    self.assertEqual(new_nodes, [TextNode("Here", TextType.BOLD_TEXT), TextNode(" is where you should be", TextType.NORMAL_TEXT)])