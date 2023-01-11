import os
import sys

def main(path):
    workspace = os.getenv("GITHUB_WORKSPACE")
    filepath = f"Hello {path} in {workspace}!"

    print(f"::set-output name=ipynb::{filepath}")
    
if __name__ == "__main__":
    path = sys.argv[1]
    print(main(path))
