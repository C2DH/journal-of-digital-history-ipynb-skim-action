import os
import sys
import json
import fire
import base64
import io
from PIL import Image


def save_notebook(data, file_name):
    # Serializing json
    json_object = json.dumps(data, indent=2)

    with open(file_name, "w") as f:
        # write json to f
        f.write(json_object)


def set_action_outputs(output_pairs):
    """


    Sets the GitHub Action outputs, with backwards compatibility for
    self-hosted runners without a GITHUB_OUTPUT environment file.

    Keyword arguments:
    output_pairs - Dictionary of outputs with values
    """
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            for key, value in output_pairs.items():
                print("{0}={1}".format(key, value), file=f)
    else:
        for key, value in output_pairs.items():
            print("::set-output name={0}::{1}".format(key, value))


def get_image_size(base64_image):
    # Decode the base64 image to binary
    image_data = base64.b64decode(base64_image)
    # Open the image using PIL
    image = Image.open(io.BytesIO(image_data))
    # Get the size of the image
    width, height = image.size
    return (width, height)


def skim_cell_images(cell):
    """
    Skim cell for images and add aspect-ratio tag to cell metadata.

    Parameters:
        cell (dict): Jupyter notebook cell.

    Returns:
        tuple: (cell, bool) where bool is True if cell was skimmed and False oth

    """
    tags = cell.get("metadata", {}).get("tags", [])
    # check if cell has tags
    if any("aspect-ratio" in tag for tag in tags):
        print(f"::debug::cell already has aspect-ratio tag! no need to skim")
        return (cell, False)

    # check if cell output contains an image
    outputs = cell.get("outputs", [])
    if not any(output.get("output_type") == "display_data" for output in outputs):
        print(f"::debug::cell does not have display_data output")
        return (cell, False)

    # get the first output where data dict contains "image/" key
    image_outputs = [
        output
        for output in outputs
        if any("image/" in key for key in output.get("data", {}).keys())
    ]
    if not image_outputs:
        print(f"::debug::cell does not have image output")
        return (cell, False)
    print(f"::debug::cell has {len(image_outputs)} image outputs")

    first_image_output = image_outputs[0]
    # get the first image mimetype
    mimetype = next(
        (key for key in first_image_output.get("data", {}).keys() if "image/" in key),
        None,
    )
    print(f"::debug::first image output has mimetype {mimetype}")
    base64_image = image_outputs[0].get("data", {}).get(mimetype, "")

    (width, height) = get_image_size(base64_image)
    aspect_ratio_tag = f"aspect-ratio-{width}-{height}"
    print(f"::debug::adding aspect-ratio tag {aspect_ratio_tag}")
    tags.append(aspect_ratio_tag)
    # update cell metadata
    cell["metadata"].update(
        {
            "tags": tags,
        }
    )
    return (cell, True)


def main(notebook=None):
    if notebook is None:
        print("::error::No path provided")
        sys.exit(1)
    workspace = os.getenv("GITHUB_WORKSPACE", "")
    notebook_filepath = os.path.join(workspace, notebook)
    notebook_filename = os.path.basename(notebook_filepath)
    skim_filepath = os.path.join(
        os.path.dirname(notebook_filepath), f"skim.{notebook_filename}"
    )
    if not os.path.exists(notebook_filepath):
        print(f"::error::Path {notebook_filepath} does not exist")
        sys.exit(1)

    print(f"::debug::Path {notebook_filepath} exists")

    with open(notebook_filepath) as f:
        data = json.load(f)
        cells = data.get("cells", [])
        size = len(cells)
        num_skimmed = 0
        for i in range(size):
            cell = cells[i]
            print(f"::debug::skim cell n.{i + 1} of {size}")
            (cell, skimmed) = skim_cell_images(cell)
            print(f"::debug::skimmed={skimmed}")
            if skimmed:
                num_skimmed += 1
            cells[i] = cell

        data.update({"cells": cells})
        print(f"::debug::Total num of cells: size={size}")
        print(f"::debug::Total num of skimmed: skimmed={num_skimmed}")
        set_action_outputs({"size": size, "skimmed": num_skimmed})
        save_notebook(data, skim_filepath)


if __name__ == "__main__":
    fire.Fire(main)
