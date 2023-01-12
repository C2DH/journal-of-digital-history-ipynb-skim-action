import os
import sys
import json
import fire

def save_notebook(data, file_name):
  # Serializing json
  json_object = json.dumps(data, indent=2)

  with open(file_name, 'w') as f:
    # write json to f
    f.write(json_object)


def set_action_output(output_name, value) :
    """Sets the GitHub Action output.

    Keyword arguments:
    output_name - The name of the output
    value - The value of the output
    """
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            print("{0}={1}".format(output_name, value), file=f)


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

    print(f"::debug::Path {notebook_filepath} exists")

    with open(notebook_filepath) as f: 
      data = json.load(f)
      cells = data.get('cells', [])
      for cell in cells:
        tags = cell.get('metadata', {}).get('tags', [])
        if 'test' not in tags:
          tags.append('test')
        cell['metadata'].update({
          'tags': tags,
        })
      data.update({ 'cells': cells })
      print(f"::debug::Total num of cells: {len(cells)}")
      set_action_output('size', len(cells))
      save_notebook(data, skim_filepath)

if __name__ == "__main__":
    fire.Fire(main)
