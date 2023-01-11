import os
import sys
import json
import fire

def main(notebook=None):
    if notebook is None:
      print('::error::No path provided')
      sys.exit(1)
    workspace = os.getenv("GITHUB_WORKSPACE", '')
    notebook_filepath = os.path.join(workspace, notebook)
    if not os.path.exists(notebook_filepath):
      print(f'::error::Path {notebook_filepath} does not exist')
      sys.exit(1)
    with open(notebook_filepath) as f: 
      data = json.load(f)
      cells = data.get('cells', [])
      print(f"::set-output name=size::{len(cells)}")
    
if __name__ == "__main__":
    fire.Fire(main)
