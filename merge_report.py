import shutil
import textwrap
import os

#Traverse the QA folder
files = [f for f in os.listdir('.') if "QA" in f]
for f in files:
  # Extract css from file
    
  with open(os.path.join(os.path.abspath(f), "assets/style.css"), 'r') as f_name :
    old_file_content = f_name.read()
  #f_name = open('Exporter_QA\\assets\style.css', 'r')
  #old_file_content = f_name.read()
  #f_name.close()
  wrapper=textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t')
  css_string = wrapper.fill(old_file_content)
  new_file_content = "<style>\n" + css_string +"\n</style>"
  
  reports = [rep for rep in os.listdir(f) if ".html" in rep]

  # Modify html files
  for report in reports:
    with open(os.path.join(os.path.abspath(f), report), 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('<link href="assets/style.css" rel="stylesheet" type="text/css"/>', new_file_content)
        
    # Write the file out again
    with open(os.path.join(os.path.abspath(f), report), 'w') as file:
      file.write(filedata)
  
