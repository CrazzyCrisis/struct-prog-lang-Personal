from tokenizer import tokenize

DEBUG_TEXT_FLAG = 0

"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""

"""
    factor = <number> | <identifier> | "(" expression ")"
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
    statement = <print> expression | expression
"""

def parse_factor(tokens):
    """
    factor = <number> | "(" expression ")"
    """

    if DEBUG_TEXT_FLAG >= 3: print("parse_factor: START")
    token = tokens[0]
    if token["tag"] == "number":
        if DEBUG_TEXT_FLAG >= 2: print("TOKEN:{a}, TAG:{b}, VALUE:{c}".format(a = tokens[0],b="number",c=tokens[0]["value"]))
        if DEBUG_TEXT_FLAG >= 3: print("parse_factor: COMPLETE")

        return {
            "tag":"number",
            "value": token["value"]
        }, tokens[1:]
    
    if token["tag"] == "(":
        if DEBUG_TEXT_FLAG >= 2: print("TOKEN:{a}, TAG:{b}, VALUE:{c}".format(a = tokens[0],b="/(",c=tokens[0]["value"]))
        ast, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")"

        if DEBUG_TEXT_FLAG >= 2: print("TOKEN:{a}, TAG:{b}, VALUE:{c}".format(a = tokens[0],b="/)",c=tokens[0]["value"]))
        if DEBUG_TEXT_FLAG >= 3: 
            print("parse_factor: COMPLETE")

        return ast, tokens[1:]
    
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")



def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """

    if DEBUG_TEXT_FLAG >= 3: 
        print("Parse_Term: START")

    node, tokens = parse_factor(tokens)
    
    while tokens[0]["tag"] in ["*","/"]:    
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag":tag, "left":node, "right":right_node}
        if DEBUG_TEXT_FLAG >= 2: 
            print("TOKEN:{a}, TAG:{b}, RIGHT_NODE:{c}".format(a = tokens[0],b=tokens[0]["tag"],c=right_node))

    if DEBUG_TEXT_FLAG >= 3: 
        print("Parse_term: COMPLETE")
    return node, tokens


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """

    if DEBUG_TEXT_FLAG >= 3: 
        print("parse_expression: START")

    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+","-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag":tag, "left":node, "right":right_node}

    if DEBUG_TEXT_FLAG >= 2: 
        for token in tokens:
            print (token)

    if DEBUG_TEXT_FLAG >= 3: 
        print("parse_expression: COMPLETE")

    return node, tokens


def parse_statement(tokens):
    """
    statement = <print> expression | expression
    """
    if DEBUG_TEXT_FLAG >= 3: 
        print("parse_statement: START")

    if tokens[0]["tag"] == "print":
        value_ast, tokens = parse_expression(tokens[1:])
        ast = {
            'tag':'print',
            'value': value_ast
        }

    else:
        ast, tokens = parse_expression(tokens)

    if DEBUG_TEXT_FLAG >= 1: 
        for node in ast:
            print (node)

    if DEBUG_TEXT_FLAG >= 3: 
        print("parse_statement: COMPLETE")
    return ast, tokens


"""
---------------------TESTS-----------------------------
"""

def test_parse_factor():
    """
    factor = <number> | <identifier> | "(" expression ")"
    """
    print("testing parse_factor()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    for s in ["(1)","(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        s_n = s.replace("(","").replace(")","")
        assert ast=={'tag': 'number', 'value': int(s_n)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("(2+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_expression(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("1+2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term()")
    for s in ["1","22","333"]:
        tokens = tokenize(s)
        ast, tokens = parse_term(tokens)
        assert ast=={'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None 
    tokens = tokenize("2*4")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}


def test_parse_statement():
    """
    statement = <print> expression | expression
    """
    print("testing parse_statement()")
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("print 2*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': 'print', 'value': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}



def parse(tokens):
    ast, tokens = parse_statement(tokens)
    if DEBUG_TEXT_FLAG >= 1: 
        for node in ast:
            print (node)
    return ast

if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()
    print("done.")