import os
import sys
import json
import fire
from git import Repo

def save_and_commit_notebook(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)
    repo = Repo()
    repo.index.add([file_name])
    repo.index.commit("Adding " + file_name + " to the repository")


def main(notebook=None):
    if notebook is None:
      print('::error::No path provided')
      sys.exit(1)
    workspace = os.getenv("GITHUB_WORKSPACE", '')
    notebook_filepath = os.path.join(workspace, notebook)
    notebook_filename = os.path.basename(notebook_filepath)
    skim_filepath = os.path.join(os.path.dirname(notebook_filepath), f'skim.{notebook_filename}')
    if not os.path.exists(notebook_filepath):
      print(f'::error::Path {notebook_filepath} does not exist')
      sys.exit(1)

    print(f'::debug::Path {notebook_filepath} exists')

    with open(notebook_filepath) as f: 
      data = json.load(f)
      cells = data.get('cells', [])
      print(f"::debug::num of cells: {len(cells)}")
      print(f"::set-output name=size::{30}")
      save_and_commit_notebook(data, skim_filepath)

if __name__ == "__main__":
    fire.Fire(main)
