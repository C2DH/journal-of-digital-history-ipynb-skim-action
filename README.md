# Rearrange the ipynb file to fit web publishing

github action to handle ipynb file according to jdh guidelines
This action prints "Hello World" or "Hello" + the name of a person to greet to the log.

## Inputs

## `who-to-greet`

**Required** The name of the person to greet. Default `"World"`.

## Outputs

## `time`

The time we greeted you.

## Example usage

uses: c2dh/journal-of-digital-history-ipynb-skim-action
with:
who-to-greet: 'Mona the Octocat'
