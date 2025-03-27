import unittest
from helpersblock import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestHelpersBlock(unittest.TestCase):
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ]
      )
    
  def test_markdown_to_blocks_empty(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertListEqual([], blocks)

  def test_markdown_to_blocks_only_whitespace(self):
    md = "\n\n\n\n"
    blocks = markdown_to_blocks(md)
    self.assertListEqual([], blocks)

  def test_markdown_to_blocks_no_blanks(self):
    md = "This is a paragraph.\n\nThis is another paragraph."
    blocks = markdown_to_blocks(md)
    self.assertListEqual(["This is a paragraph.", "This is another paragraph."], blocks)

  def test_markdown_to_blocks_multi_blanks(self):
    md = "Heading\n\n\n\nParagraph\n\n\n\n- List Item"
    blocks = markdown_to_blocks(md)
    self.assertListEqual(["Heading", "Paragraph", "- List Item"], blocks)
  
  def test_markdown_to_blocks_no_breaks(self):
    md = "This is a single block of text spanning multiple lines, but it has no blank line breaks."
    blocks = markdown_to_blocks(md)
    self.assertListEqual(["This is a single block of text spanning multiple lines, but it has no blank line breaks."], blocks)

  def test_block_to_blocktype_header1(self):
    block = "# this is a heading"
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_block_to_blocktype_header6(self):
    block = "###### This is a heading"
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.HEADING)
  
  def test_block_to_blocktype_code(self):
    block = '```print("Hello world")```'
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.CODE)

  def test_block_to_blocktype_quote(self):
    block = """> I have a dream
> Four score and severn years ago""" 
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.QUOTE)
  
  def test_block_to_blocktype_unordered(self):
    block = """- First Item
- Second Item
- Third Item"""
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.UNORDERED_LIST)

  def test_block_to_blocktype_ordered(self):
    block = """1. Python
2. Javascript
3. Go"""
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.ORDERED_LIST)

  def test_paragraphs(self):
    self.maxDiff = None
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    
    self.assertEqual(
       html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
    )

  def test_markdown_to_html_heading(self):
    md = """
## This is a heading 2
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(html, "<div><h2>This is a heading 2</h2></div>")

  def test_markdown_to_html_quote(self):
    md = """
> This is a quote
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

  def test_markdown_to_html_unordered(self):
    md = """
- Burger King
- McDonalds
- Wendy's
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(html, "<div><ul><li>Burger King</li><li>McDonalds</li><li>Wendy's</li></ul></div>")

  def test_markdown_to_html_unordered(self):
    md = """
1. Burger King
2. McDonalds
3. Wendy's
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(html, "<div><ol><li>Burger King</li><li>McDonalds</li><li>Wendy's</li></ol></div>")