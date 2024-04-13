#! /usr/bin/env python3

"""
@author - Zaitsev Vasilii, 2024
please use:
pip install pypandoc
pip install pypandoc_binary
"""

from pathlib import Path
import os
import pypandoc
from pypandoc.pandoc_download import download_pandoc

IN_DIR_FILENAME = "../../docs"
OUT_DIR_FILENAME = "../../docs_txt"


def convert_files_to_txt(in_dir_filename: str, out_dir_filename: str) -> None:
    in_dir_path = Path(in_dir_filename).absolute()
    out_dir_path = Path(out_dir_filename).absolute()

    if not in_dir_path.exists():
        print(f"{in_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    if not out_dir_path.exists():
        print(f"{out_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    index = 0
    for filename in os.listdir(in_dir_path.as_posix()):
        filename = os.path.join(in_dir_path.as_posix(), filename)
        if filename.endswith(".docx"):
            convert_docx_to_txt(filename, out_dir_path.as_posix(), index)
            index += 1


def convert_docx_to_txt(filename: str, out_dir_filename: str, index: int) -> None:
    filename_crop = filename.split("/")[-1].split(".docx")[0]
    print(f"Found file: {filename_crop}, resulting directory = {out_dir_filename}")
    output = pypandoc.convert_file(filename, "plain", outputfile=f"{out_dir_filename}/#{index}#_{filename_crop}.txt")
    if output != "":
        print(f"File {filename_crop} - Error during convertion!")


def main() -> None:
    convert_files_to_txt(IN_DIR_FILENAME, OUT_DIR_FILENAME)


if __name__ == "__main__":
    main()
