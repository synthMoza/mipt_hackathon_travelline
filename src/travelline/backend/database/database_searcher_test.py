#!/usr/bin/env python3

from travelline.backend.database.database_searcher_implementation import DB_Searcher
from travelline.backend.database.database_implementation import EmbeddingsDB
from datetime import datetime
from pathlib import Path
import os
import time


DOCS_TXT_DIR = "travelline/backend/database/docs_txt"

def fill_database(db) -> None:

    in_dir_path = Path(DOCS_TXT_DIR).absolute()
    if not in_dir_path.exists():
        print(f"{in_dir_path.as_posix()} does not exist! Exiting!")
        exit(-1)

    for filename in os.listdir(in_dir_path.as_posix()):
        filename_long = os.path.join(in_dir_path.as_posix(), filename)

        with open(filename_long, "r", encoding="utf-8") as file:
            doc_name = filename
            plain_text = file.read()
            date_time =  time.ctime(os.path.getmtime(filename_long))

            db.add_document(doc_name, date_time, plain_text)



def main() -> None:

    db = EmbeddingsDB("travelline/backend/database/database.db")
    searcher = DB_Searcher(db)
    fill_database(db)

    query = "Как создать групповую бронь в шахматке TL"
    searcher.ask_real_question(query)

    print("Full simularity list:")
    print(searcher.get_full_simularity_list())
    print("Reduced simularity list:")
    print(searcher.get_reduced_simularity_list(5))




if __name__ == "__main__":
    main()
