import pathlib
import re
import os
from datetime import datetime 

if os.environ.get('SECRET_TEXT') is None:
  SECRET_TEXT = "SECRET_TEXT is not set"
else:
  SECRET_TEXT = os.environ.get('SECRET_TEXT')

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
  r = re.compile(
      r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
      re.DOTALL,
  )
  if not inline:
      chunk = "\n{}\n".format(chunk)
  chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
  return r.sub(chunk, content)

if __name__ == "__main__":
  readme = root / "README.md"
  readme_contents = readme.open().read()
  
  dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  new_text = dt_string + " : " + SECRET_TEXT
  rewritten = replace_chunk(readme_contents, "replace-with-date", new_text)
  readme.open("w").write(rewritten)
