import argparse
import sys
from gigathought import GigaThought

def parse_args():
    parser = argparse.ArgumentParser(description='Demoapp for GigaThought class usage')
    
    parser.add_argument('--credentials', type=str, help='credentials for GigaChat API')
    parser.add_argument('--config', type=str, help='path to the prompt config')
    parser.add_argument('--document', type=str, help='context document')

    return parser.parse_args(sys.argv[1:])

def main():
    args = parse_args()
    deepthought = GigaThought(args.credentials, args.config)
    
    while (True):
        with open(args.document, 'r', encoding = 'utf-8') as file:
            doc_data = file.read()
        
        question = input('Ask a question: ')
        answer = deepthought.ask(question, doc_data)
        print(f'Answer: {answer}')

if __name__ == '__main__':
    main()