# TLDR; The Tokenizer/Lexical Analysis breaks the source into Tokens. 
# Tokens will be defined by the Tokenizer if the source code segment matches a regular expression inside of the patterns dictionary.
# If there is a match, the Tokenizer will create a new Token, which is basically a dictionary with various properties inside
# the properties of tokens are the following:
# tag; All tokens start with a tag, the tag is defined at the end of the regex entry.
# position; the position that the point in the source code where the token begins
# value; 
# a token may look like:
# {'tag': '+', 'position': 0, 'value': '+'}
# {'tag': '&&', 'position': 0, 'value': '&&'}
# {'tag': 'number', 'position': 0, 'value': 11.11}

import re

debugPrintLOD = 0 # At 0, no additional debuging will be printed, at 1 tokens will be printed and tests will be seperated by spaces

# Define patterns for tokens
patterns = [
    [r"print","print"],
    [r"true","true"],
    [r"false","false"],
    [r"if", "if"],
    [r"then", "then"],
    [r"and", "and"],
    [r"or", "or"],
    [r"\d*\.\d+|\d+\.\d*|\d+", "number"],
    [r"[a-zA-Z_][a-zA-Z0-9_]*", "identifier"],  # identifiers
    [r"\+", "+"],
    [r"\-", "-"],
    [r"\*", "*"],
    [r"\/", "/"],
    [r"\(", "("],
    [r"\)", ")"],
    [r"\;", ";"],
    [r"\<\=", "<="],
    [r"\<", "<"],
    [r"\>\=", ">="],
    [r"\>", ">"],
    [r"\=\=", "=="],
    [r"\!\=", "!="],
    [r"\!", "!"],
    [r"\&\&", "&&"],
    [r"\|\|", "||"],
    [r"\=", "="],

    [r"\s+","whitespace"],
    [r".","error"]
]

# sends the pattern portion of the global patterns dict to the re.compiler, which returns a regex obj (https://docs.python.org/3/library/re.html)
for pattern in patterns:
    pattern[0] = re.compile(pattern[0]) 

def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters): # While position is less then the length of the characters in the string
        tag, match = tokenizePatternMatch(characters,position)
        tokenizeSyntaxErrorCheck(tag)
        token = tokenizeAssignToken(tag,position,match)
        tokenizeNumbers(token)
        tokenizeBooleans(token)
        tokenizeRemoveWhiteSpace(token,tokens)
        position = match.end()
    tokenizeAppendEndOfStreamMarker(tokens, position)
    printList(tokens)
    return tokens

# For each pattern and tag in patterns, this will assign the first property to pattern and second property to tag of the patterns dict
# assign match to the result of the re.match function, if it doesn't match the current pattern, return false
# assert (confirm the expression is true) that match is true.
# Python can return mutiple things without resorting to an array. neat. idk if its preformant or not, but im using it here for my own understanding.
def tokenizePatternMatch(characters,position):
    for pattern, tag in patterns: 
        match = pattern.match(characters, position) 
        if match:
            break
    assert match 
    return tag, match

# If none of the patterns are matched, we have a syntax error. Make sure the error state is at the bottom of the patterns list.
def tokenizeSyntaxErrorCheck(tag):
    if tag == "error": 
        raise Exception("Syntax error")

# returns a tag and postion found by the match function and returns the whole match group as the value
# this is statements like "print" are assigned
def tokenizeAssignToken(tag,position,match):
    token = { 
        "tag":tag,
        "position":position,
        "value":match.group(0)
    }
    return token

# Check for numbers by checking the tag. If tag is "number", check if is a float by looking for a ".", otherwise it's an int.
def tokenizeNumbers(token):
    if token["tag"] == "number": 
        if "." in token["value"]:
            token["value"] = float(token["value"])
        else:
            token["value"] = int(token["value"])

# Check for boolean values by looking for matchest for true/false
def tokenizeBooleans(token):
        if token["tag"] in ["true","false"]: 
            token["value"] = (token["tag"] == "true") # If token["tag"] == true, return true and assign that to value, otherwise assign false
            token["tag"] = "boolean"

# Throw out the whitespce
def tokenizeRemoveWhiteSpace(token,tokens):
    if token["tag"] != "whitespace": 
        tokens.append(token)

# append end-of-stream marker so the parser knows where to end
def tokenizeAppendEndOfStreamMarker(tokens, position):
    tokens.append({
        "tag":None,
        "position":position,
        "value":None
    })

# prints each entry in a list onto a new line
def printList(_list):
    if debugPrintLOD > 0:
        for x in _list:
            print(x)
        print("------------------------------")

def importantPrint(value):
    if debugPrintLOD > 0: print(" ")
    print(value)


def test_simple_token():
    importantPrint("test simple token")
    examples = [item[1] for item in [
        [r"\+", "+"],
        [r"\-", "-"],
        [r"\*", "*"],
        [r"\/", "/"],
        [r"\(", "("],
        [r"\)", ")"],
        [r"\;", ";"],
        [r"\<\=", "<="],
        [r"\<", "<"],
        [r"\>\=", ">="],
        [r"\>", ">"],
        [r"\=\=", "=="],
        [r"\!\=", "!="],
        [r"\!", "!"],
        [r"\&\&", "&&"],
        [r"\|\|", "||"],
        [r"\=", "="]
    ]]


    for example in examples:
        t = tokenize(example)[0]
        assert t["tag"] == example
        assert t["position"] == 0
        assert t["value"] == example

def test_number_token():
    importantPrint("test number tokens")
    for s in ["1","11"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "number"
        assert t[0]["value"] == int(s)
    for s in ["1.1","11.11","11.",".11"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "number"
        assert t[0]["value"] == float(s)

def test_boolean_tokens():
    importantPrint("test boolean tokens")
    for s in ["true","false"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "boolean"
        assert t[0]["value"] == (s == "true")

def test_multiple_tokens():
    importantPrint("test multiple tokens")
    tokens = tokenize("1+2")
    assert tokens == [{'tag': 'number', 'position': 0, 'value': 1}, {'tag': '+', 'position': 1, 'value': '+'}, {'tag': 'number', 'position': 2, 'value': 2}, {'tag': None, 'value': None, 'position': 3}]

def test_whitespace():
    importantPrint("test whitespace...")
    tokens = tokenize("1 + 2")
    assert tokens == [{'tag': 'number', 'position': 0, 'value': 1}, {'tag': '+', 'position': 2, 'value': '+'}, {'tag': 'number', 'position': 4, 'value': 2}, {'tag': None, 'value': None, 'position': 5}]

def test_keywords():
    importantPrint("test keywords...")
    for keyword in [
        "print",
        "if",
        "then",
        "or",
        "and"
    ]:
        t = tokenize(keyword)
        assert len(t) == 2
        assert t[0]["tag"] == keyword, f"expected {keyword}, got {t[0]}"
        assert "value" not in t

def test_identifier_tokens():
    importantPrint("test identifier tokens...")
    for s in ["x", "y", "z", "alpha", "beta", "gamma"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "identifier"
        assert t[0]["value"] == s



def test_error():
    importantPrint("test error")
    try:
        t = tokenize("$1+2")
        assert False, "Should have raised an error for an invalid character."
    except Exception as e:
        assert "Syntax error" in str(e),f"Unexpected exception: {e}"

if __name__ == "__main__":
    test_simple_token()
    test_number_token()
    test_boolean_tokens()
    test_multiple_tokens()
    test_whitespace()
    test_keywords()
    test_identifier_tokens()
    test_error()