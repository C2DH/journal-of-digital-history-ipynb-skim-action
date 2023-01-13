# Rearrange the ipynb file to fit web publishing

Given a input `notebook` ipynb file present in the repository, this action provides the following functionalities:

- produce an `aspect-ratio` tags to correctly display image on JDH frontend, with information about height and width for every notebook cell containing an image
- save the "skimmed" notebook in another ipynb file next to the input notebook, its name prefixed with `skim.`

(upcoming) features:

- optionally reduce the size of the images in the output, or change the image format to save bits
- save generated outputs in image files and add their absolute urls in the cell metadata

## Basic usage

```yaml
- name: Skim a ipynb file
  uses: c2dh/journal-of-digital-history-ipynb-skim-action@master
  with:
    notebook: 'example/display-image.ipynb'
```

See [action.yml](action.yml) and our [example.yml](.github/workflows/example.yml) workflow.
As this action commmits and pushes to the repository, use appropriate github action events, like `workflow_dispatch`.

```yaml
on: [workflow_dispatch]

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: Test this action
    steps:
      - name: Skim example file
        id: skim
        uses: c2dh/journal-of-digital-history-ipynb-skim-action@master
        with:
          notebook: 'example/display-image.ipynb'
      - name: Use the output, if needed
        run: echo "number of cells ${{ steps.skim.outputs.size }}"
```
