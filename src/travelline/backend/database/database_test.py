#!/usr/bin/env python3


from travelline.backend.database.database_implementation import EmbeddingsDB

from datetime import datetime

def main() -> None:
    db = EmbeddingsDB("travelline/backend/database/database.db")

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    doc_name = "#0#_Как гость может изменить бронирование с сайта.txt"
    plain_text = ""
    with open(f"travelline/backend/database/docs_txt/{doc_name}", "r") as f:
        plain_text = f.read()

    #API_TEST

    db.delete_document(0)
    print(f"Document Exists? : {db.check_if_document_exists(0)}")

    db.add_document(doc_name, date_time, plain_text)
    print(f"Document Exists? : {db.check_if_document_exists(0)}")

    print(f"DateTime: {db.get_date_time(0)}")

    print(f"DocName: {db.get_doc_name(0)}")

    print(f"PlainText: {db.get_plain_text(0)[:10]}")

    print(f"Embedding: {db.get_embedding(0)}, with the shape of {db.get_embedding(0).shape}")

    plain_text = "New Plain Text"
    db.update_document(doc_name, date_time, plain_text)
    print()
    print(f"PlainText After Update: {db.get_plain_text(0)[:10]}")

    print(f"GetAllEmbeddings: {db.get_all_embeddings()}")

    db.disconnect_db()


if __name__ == "__main__":
    main()
