import os
import sys
import json
import fire

def main(notebook=None):
    if notebook is None:
      print('::error::No path provided')
      sys.exit(1)
    if not os.path.exists(notebook):
      print(f'::error::Path {notebook} does not exist')
      sys.exit(1)
    with open(notebook) as f: 
      data = json.load(f)
      cells = data.get('cells', [])
      print(f"::set-output name=size::{len(cells)}")
    
if __name__ == "__main__":
    fire.Fire(main)
