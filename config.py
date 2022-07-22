class Config:
    PREFIX: str = "diff --git"
    POSTFIX: str = "2.32.0 (Skynet Git-132)"
    SPECIFICATIONS_DIR: str = "specifications"
    PATCHES_DIR: str = "patches"
    PROGRAM_DIR: str = "program"
    TMP_DIR: str = "tmp"
    MAX_TRIES_PATCH: int = 10
    TEMPERATURES = [0.0] + [0.7]*9

config: Config = Config()