import os

def read_file(dir: str, filename: str, extension: str) -> str:
    path: str = os.path.join(dir, f"{filename}.{extension}")
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()

def write_file(string: str, dir: str, filename: str, extension: str = "txt") -> None:
    path: str = os.path.join(dir, f"{filename}.{extension}")
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(string)