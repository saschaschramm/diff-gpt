import os
from completion import Completion
import utils
import shutil
import subprocess
from config import config
from logging_utils import get_logger
from logging import Logger

logger: Logger = get_logger()

def generate_commit(prompt: str, temperature: float) -> str:
    completion: Completion = Completion(engine="code-davinci-002", 
                                        max_completion_tokens=200, 
                                        temperature=temperature, 
                                        stop=["\n2.32.0"])
    text: str = completion.create(prompt)
    return text

def apply_patch(patches_dir: str, file_name: str) -> str:
    patch_path: str = os.path.join(patches_dir, f"{file_name}.patch")
    return subprocess.getoutput(f"git apply {patch_path} -v")

def clean() -> None:
    if os.path.exists(config.PATCHES_DIR):
        shutil.rmtree(config.PATCHES_DIR)
    
    if os.path.exists(config.PROGRAM_DIR):
        shutil.rmtree(config.PROGRAM_DIR)

    if os.path.exists(config.TMP_DIR):
        shutil.rmtree(config.TMP_DIR)

    os.makedirs(config.PATCHES_DIR)
    os.makedirs(config.TMP_DIR)
    shutil.copyfile(src="0000.patch", 
                    dst=os.path.join(config.PATCHES_DIR, "0000.patch"))


def main() -> None:
    clean()
    num_files: int = len(os.listdir(config.SPECIFICATIONS_DIR))
    prompt: str = ""
    patch: str = ""
    for index in range(0, num_files):
        file_name: str = f"{index:04d}"
        logger.info(f"{file_name} -----------------------------------------------------")
        specification: str = utils.read_file(config.SPECIFICATIONS_DIR, file_name, "spec")

        if index > 0:
            prompt += f"{patch}\n\n\n"

        prompt += f"Subject: {specification}\n"
            
        logger.info(f"Specification: {specification}")
        utils.write_file(prompt, config.TMP_DIR, f"{file_name}", "prompt")

        num_tries: int = 1
        while num_tries < config.MAX_TRIES_PATCH:
            logger.info(f"Generate patch {file_name}.patch – {num_tries}/{config.MAX_TRIES_PATCH}")

            if index == 0:
                patch = utils.read_file(config.PATCHES_DIR, "0000", "patch")
            else:
                completion: str = generate_commit(
                        prompt=f"{prompt}{config.PREFIX}", 
                        temperature=config.TEMPERATURES[num_tries]
                    )
                patch = f"{config.PREFIX} {completion.strip()}\n{config.POSTFIX}"
                utils.write_file(patch, config.PATCHES_DIR, file_name, "patch")

            output: str = apply_patch(config.PATCHES_DIR, file_name)    
            if "error:" in output:
                logger.warning(output)
                num_tries += 1
            else:
                logger.info("Patch applied successfully")
                break        

        if num_tries == config.MAX_TRIES_PATCH:
            logger.error("Failed to apply patch")
            exit()


if __name__ == "__main__":
    main()