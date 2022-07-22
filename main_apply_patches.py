import os
import subprocess
import shutil
from config import config

if os.path.exists("program"):
    shutil.rmtree("program")

if __name__ == "__main__":
    patches_dir: str = os.path.join("patches")
    files: list[str] = os.listdir(patches_dir)
    files.sort()

    for file in files:
        path: str = os.path.join(config.PATCHES_DIR, file)
        if file.endswith(".patch"):
            print("Applying patch " + path)
            output: str = subprocess.getoutput(f"git apply {path}")
            if output.startswith("error:"):
                print(output)
                exit()