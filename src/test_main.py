import unittest
from main import extract_title

class TestMain(unittest.TestCase):
  def test_extract_title(self):
    md ="""
# Holy Moly Guacamole
"""
    title = extract_title(md)
    self.assertEqual(title, "Holy Moly Guacamole")

  def test_extract_title_none(self):
    md = """"""
    with self.assertRaises(Exception):
      title = extract_title(md)