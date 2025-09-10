import tokenizer
import parser
import evaluator
import sys
<<<<<<< HEAD:topic-02-programs/runner.py
=======
import LIM.evaluator as evaluator
>>>>>>> e4deb5b (deleting debug print statements):LIM/runner.py

def run(text):
    tokens = tokenizer.tokenize(text)
    ast = parser.parse(tokens)
    evaluator.evaluate(ast)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1],"r") as f:
            source = f.read()
        run(source)


