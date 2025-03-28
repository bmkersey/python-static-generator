import os
import shutil
from helpersblock import markdown_to_html_node

def main():
  if os.path.exists("./public"):
    shutil.rmtree("./public")

  os.mkdir("./public")

  copy_static("./static", "./public")
  generate_page("./content/index.md", "./template.html", "./public/index.html")

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
  template_contents = template_contents.replace("{{ title }}", title)
  template_contents = template_contents.replace("{{ Content }}", html)
  with open(dest_path, 'w') as output:
    output.write(template_contents)






if __name__ == "__main__":
  main()