import os
import shutil
from helpersblock import markdown_to_html_node
from pathlib import Path
import sys

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
  
  if os.path.exists("./public"):
    shutil.rmtree("./public")

  os.mkdir("./public")

  copy_static("./static", "./public")
  generate_pages_recursive(dir_path_content, template_path, dir_path_public)

def copy_static(source, destination):
  for item in os.listdir(source):
    source_path = os.path.join(source, item)
    dest_path = os.path.join(destination, item)

    if os.path.isfile(source_path):
      print(f"Copying file: {source_path} to {dest_path}")
      shutil.copy(source_path, dest_path)
    else:
      print(f"Creating directory: {dest_path}")
      os.mkdir(dest_path)
      copy_static(source_path, dest_path)

def extract_title(markdown):
  lines = markdown.split("\n")
  title = ""
  for line in lines:
    if line.startswith("# "):
      title = line[2:]
      return title
  if not title:
    raise Exception("No title found.")


def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
  src_file = open(from_path)
  src_contents = src_file.read()
  src_file.close()

  template_file = open(template_path)
  template_contents = template_file.read()
  template_file.close()

  node = markdown_to_html_node(src_contents)
  html = node.to_html()

  title = extract_title(src_contents)
  template_contents = template_contents.replace("{{ Title }}", title)
  template_contents = template_contents.replace("{{ Content }}", html)

  html_filepath = os.path.dirname(dest_path)
  if html_filepath != "":
    os.makedirs(html_filepath, exist_ok=True)
      
  to_file = open(dest_path, "w")
  to_file.write(template_contents)
  to_file.close()
  
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for item in os.listdir(dir_path_content):
    source_path = os.path.join(dir_path_content, item)
    dest_path = os.path.join(dest_dir_path, item)

    if os.path.isfile(source_path):
      dest_path = Path(dest_path).with_suffix(".html")
      print(dest_path)
      generate_page(source_path, template_path, dest_path)
    else:
      generate_pages_recursive(source_path, template_path, dest_path)
  




if __name__ == "__main__":
  main()