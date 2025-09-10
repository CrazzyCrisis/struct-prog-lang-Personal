from tokenizer import tokenize
from parser import parse

printed_string = None

def evaluate(ast, environment):
    global printed_string
    printed_string = None
    if ast["tag"] == "program":
        last_value = None
        for statement in ast["statements"]:
            value = evaluate(statement, environment)
            last_value = value
        return last_value
    if ast["tag"] == "print":
        value = evaluate(ast["value"], environment)
        s = str(value)
        printed_string = s
        print(s)
    if ast["tag"] == "number":
        return ast["value"]
    if ast["tag"] == "identifier":
        name = ast["value"]
        if name in environment:
            return environment[name]
        if "$parent" in environment:
            return evaluate(ast,environment["$parent"])
        raise Exception(f"Error:Undefined variable [{name}]")
        # return environment[name]
    if ast["tag"] in ["+","-","*","/"]:
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        if ast["tag"] == "+":
            return left_value + right_value
        if ast["tag"] == "-":
            return left_value - right_value
        if ast["tag"] == "*":
            return left_value * right_value
        if ast["tag"] == "/":
            return left_value / right_value

def test_evaluate_number():
    print("testing evaluate number")
    assert evaluate({"tag":"number","value":4}, {}) == 4

def test_evaluate_identifier():
    print("testing evaluate identifier")
    assert evaluate({"tag":"identifier","value":"x"}, {"x":1.0}) == 1.0

def test_evaluate_addition():
    print("testing evaluate addition")
    ast = {
        "tag":"+",
        "left":{"tag":"number","value":1},
        "right":{"tag":"number","value":3}
        }
    assert evaluate(ast, {}) == 4

def test_evaluate_subtraction():
    print("testing evaluate subtraction")
    ast = {
        "tag":"-",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 1

def test_evaluate_multiplication():
    print("testing evaluate multiplication")
    ast = {
        "tag":"*",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 6

def test_evaluate_division():
    print("testing evaluate division")
    ast = {
        "tag":"/",
        "left":{"tag":"number","value":4},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 2

def eval(s, environment={}):
    tokens = tokenize(s)
    ast = parse(tokens)
    result = evaluate(ast, environment)
    return result

def test_evaluate_expression():
    print("testing evaluate expression")
    assert eval("1+2+3") == 6
    assert eval("1+2*3") == 7
    assert eval("(1+2)*3") == 9
    assert eval("(1.0+2.1)*3") == 9.3

def test_evaluate_print():
    print("testing evaluate print")
    assert eval("print 3") == None    
    assert printed_string == "3"
    assert eval("print 3.14") == None    
    assert printed_string == "3.14"
    assert eval("print x", {"x":1.0}) == None    
    assert printed_string == "1.0"
    assert eval("print x+y", {"x":1.0,"y":2.0}) == None    
    assert printed_string == "3.0"
    assert eval("print x+y", {"x":2.0,"$parent":{"y":4.0}}) == None    
    assert printed_string == "6.0"
    assert eval("print x+y", {"x":2.0,"$parent":{"y":4.0,"x":3.0}}) == None    
    assert printed_string == "6.0"
    assert eval("print x+y", {"x":2.0,"y":6.0,"$parent":{"y":4.0,"x":3.0}}) == None    
    assert printed_string == "8.0"
    assert eval("print x+y", {"x":2.0,"z":4.0,"$parent":{"$parent":{"y":4.0}}}) == None    
    assert printed_string == "6.0"



if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_identifier()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_evaluate_print()
    print("done.")

