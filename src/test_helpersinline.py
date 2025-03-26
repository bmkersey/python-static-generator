import unittest
from textnode import TextNode, TextType
from helpersinline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links("This is text with a link [to youtube](https://www.youtube.com)")
    self.assertListEqual([("to youtube", "https://www.youtube.com")], matches)
  
  def test_split_images_single(self):
    node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) plus remaining text.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL_TEXT), TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" plus remaining text.", TextType.NORMAL_TEXT),
      ],
      new_nodes,
    )

  def test_split_muttiple_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.NORMAL_TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL_TEXT), TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" and another ", TextType.NORMAL_TEXT), TextNode("second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png")
      ],
      new_nodes,
    )

  def test_split_images_no_image(self):
    node = TextNode("This text has no images.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("This text has no images.", TextType.NORMAL_TEXT)], new_nodes)

  def test_split_images_multi_nodes(self):
    node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) plus remaining text.", TextType.NORMAL_TEXT)
    node2 = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.NORMAL_TEXT,
    )
    new_nodes = split_nodes_image([node, node2])
    self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL_TEXT), TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" plus remaining text.", TextType.NORMAL_TEXT),TextNode("This is text with an ", TextType.NORMAL_TEXT), TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
      TextNode(" and another ", TextType.NORMAL_TEXT), TextNode("second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png")
      ], new_nodes)
    
  def test_split_images_empty(self):
    node = ""
    new_nodes = split_nodes_image([node])
    self.assertListEqual([], new_nodes)

  def test_only_images(self):
    node = TextNode("![one](https://example.com/one.png)![two](https://example.com/two.png)", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("one", TextType.IMAGE_TEXT, "https://example.com/one.png"), TextNode("two", TextType.IMAGE_TEXT, "https://example.com/two.png")], new_nodes)
  
  def test_link_snigle(self):
    node = TextNode("Here is a link [Click Me](www.youtube.com) visit us!", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([TextNode("Here is a link ", TextType.NORMAL_TEXT), TextNode("Click Me", TextType.LINK_TEXT, "www.youtube.com"), TextNode(" visit us!", TextType.NORMAL_TEXT)], new_nodes)

  def test_split_link_multi(self):
    node = TextNode("Here is a link [Click Me](www.youtube.com) visit us! Or try [Click this one](www.twitch.tv)", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([TextNode("Here is a link ", TextType.NORMAL_TEXT), TextNode("Click Me", TextType.LINK_TEXT, "www.youtube.com"), TextNode(" visit us! Or try ", TextType.NORMAL_TEXT),
      TextNode("Click this one", TextType.LINK_TEXT, "www.twitch.tv")], new_nodes)
