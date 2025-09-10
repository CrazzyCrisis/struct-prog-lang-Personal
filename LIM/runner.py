import tokenizer
import parser
import sys
import evaluate

def run(text):
    tokens = tokenizer.tokenize(text)
    ast = parser.parse(tokens)
    evaluate.evaluate(ast)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            source = f.read()
        run(source)

