import argparse
import sys
from gigachat_module import GigaThought, GigaDetailizer

def parse_args():
    parser = argparse.ArgumentParser(description="Demoapp for GigaThought class usage")

    parser.add_argument("--credentials", type=str, help="credentials for GigaChat API", required=True)
    parser.add_argument("--thought_config", type=str, help="path to the GigaThought prompt config", required=True)
    parser.add_argument("--detailizer_config", type=str, help="path to the GigaDetailizer prompt config", required=True)
    parser.add_argument("--document", type=str, help="path to the document", required=True)

    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()
    deep_thought = GigaThought(args.credentials, args.thought_config)
    deep_detailizer = GigaDetailizer(args.credentials, args.detailizer_config)

    chat_history = ''
    while True:
        with open(args.document, "r", encoding="utf-8") as file:
            doc_data = file.read()

        question = input("Ask a question: ")
        
        real_question, chat_history = deep_detailizer.detailize(question, chat_history)
        print(f'Chat history: {chat_history}')
        print(f'Detailized question: {real_question}')
        
        answer = deep_thought.ask(real_question, doc_data)
        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
