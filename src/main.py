import os
import shutil
from helpersblock import markdown_to_html_node

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
  template_contents = template_contents.replace("{{ itle }}", title)
  template_contents = template_contents.replace("{{ Content }}", html)
  with open(dest_path, 'w') as output:
    output.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for item in os.listdir(dir_path_content):
    source_path = os.path.join(dir_path_content, item)
    dest_path = os.path.join(dest_dir_path, item)

    if os.path.isfile(source_path) and source_path.endswith('.md'):
      src_file = open(source_path)
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
      
      html_filename = os.path.splitext(item)[0] + '.html'
      filepath = os.path.join(dest_dir_path, html_filename)
      
      os.makedirs(os.path.dirname(filepath), exist_ok=True)
      
      with open(filepath, 'w') as output:
        output.write(template_contents)
    elif os.path.isdir(source_path):
      print(f"Creating directory: {dest_path}")
      os.makedirs(dest_path, exist_ok=True)
      generate_pages_recursive(source_path, template_path, dest_path)
  




if __name__ == "__main__":
  main()