from sbertembedding import SBertEmbedding

import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Demoapp for GigaThought class usage')
    
    parser.add_argument('--document', type=str, help='document to get embedding from')

    return parser.parse_args(sys.argv[1:])

def main():
    args = parse_args()
    embedding = SBertEmbedding()
    
    with open(args.document, 'r', encoding = 'utf-8') as file:
        doc_data = file.read()
    
    q = embedding.get(doc_data)
    print(f'Embedding: {q}')

if __name__ == '__main__':
    main()