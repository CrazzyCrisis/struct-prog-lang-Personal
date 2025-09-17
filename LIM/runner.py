import tokenizer
import parser
import sys
import LIM.evaluator as evaluator

def run(text):
    tokens = tokenizer.tokenize(text)
    ast = parser.parse(tokens)
    evaluator.evaluate(ast)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            source = f.read()
        run(source)

