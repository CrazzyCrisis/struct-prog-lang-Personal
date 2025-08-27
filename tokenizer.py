import re

#Regular expressions, first one tests for numbers, 1) left side as many as possible,
# 2) right side as much possible, return the key "number
# second tests for +, return the key "+"
# if anything else is found, return an error
patterns = [
    [r"print","print"],
    [r"\d*\.\d+|\d+\.\d*|\d+","number"],
    [r"[a-zA-Z_][a-zA-Z0-9_]*","identifier"], #identifiers
    [r"\+", "+"], 
    [r"\-", "-"],
    [r"\*","*"],
    [r"\/","/"],
    [r"\)",")"],
    [r"\(","("],
    [r"\s+","whitespace"],
    [r".","error"]
]

#takes literal strings in patterns and compiles them into regular expression objects.
for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

#Splits characters into tokens. :)
def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        # find first matching token
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break

        assert match

        if tag == "error":
            raise Exception(f"Syntax error: illegal character :{[match.group(0)]}")

        token = {
            "tag":tag,
            "position":position,
            "value":match.group(0)
        }
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
        if token["tag"] != "whitespace":
            tokens.append(token)
        position = match.end()


    tokens.append({
        "tag":None,
        "value":None,
        "position":position
    })    
    return tokens

#Tests to make sure the tokenizer actually works, will split "2+3" into it's tokenized format and return that to the test. 
#If the assert passes, we good
def test_simple_expression():
    print("Test simple expresssions...")
    t = tokenize("2+3")
    assert t == [{'tag': 'number', 'position': 0, 'value': 2}, {'tag': '+', 'position': 1}, {'tag': 'number', 'position': 2, 'value': 3}, {'tag': None, 'position': 3}]
    print(t)
    exit(0)

#Bunch of little test just to figure out how the tokenizer works
def test_simple_tokens():
    print("test simple tokens...")
    for c in "+-*/":
        assert tokenize(c) == [
            {"tag":c,"position":0},
            {"tag":None,"position":1}
        ]
        print(str(tokenize(c)))

    '''
    assert tokenize("+") == [
        {"tag":"+","position":0},
        {"tag":None,"position":1}
    ]
    '''
    assert tokenize("3") == [
        {"tag":"number","position":0, "value":3},
        {"tag":None,"position":1}
    ]
    assert tokenize("3.1") == [
        {"tag":"number","position":0, "value":3.1},
        {"tag":None,"position":3}
    ]
    assert tokenize("31.12") == [
        {"tag":"number","position":0, "value":31.12},
        {"tag":None,"position":5}
    ]
    assert tokenize("3.1+5.6") == [
        {"tag":"number","position":0, "value":3.1},
        {"tag":"+","position":3},
        {"tag":"number","position":4, "value":5.6},
        {"tag":None,"position":7}
    ]

def test_whitespace():
    print("test whitespace")
    tokens = tokenize("1 + 2")
    '''
    assert tokens == [
        {"tag":"number", "position": 0, "value": 1},
        {"tag":"+", "position": 2},
        {"tag":"number", "position": 4, "value": 2}
        ]
    '''


#Need to learn how this works., how is this running?
if __name__ == "__main__":
    print("testing tokenizer...")
    test_simple_tokens()
    test_whitespace()
    test_simple_expression()
    print("done.")