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
        return None
    if ast["tag"] == "assign":
        target = ast["target"]
        assert target["tag"] == "identifier"
        value = evaluate(ast["value"], environment)
        environment[target["value"]] = value
        return None
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
    if ast["tag"] in ["<",">","<=",">=","==","!=","||","&&"]:
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        if ast["tag"] == "<":
            return left_value < right_value
        if ast["tag"] == ">":
            return left_value > right_value
        if ast["tag"] == "<=":
            return left_value <= right_value
        if ast["tag"] == ">=":
            return left_value >= right_value
        if ast["tag"] == "==":
            return left_value == right_value
        if ast["tag"] == "!=":
            return left_value != right_value
        if ast["tag"] == "&&":
            return left_value and right_value
        if ast["tag"] == "||":
            return left_value or right_value

def test_evaluate_number():
    print("testing evaluate number")
    assert evaluate({"tag":"number","value":4}, {}) == 4

    #Homework test case
    assert evaluate({"tag":"number","value":100.1}, {}) == 100.1

def test_evaluate_identifier():
    print("testing evaluate identifier")
    assert evaluate({"tag":"identifier","value":"x"}, {"x":1.0}) == 1.0

    #Homework test case
    assert evaluate({"tag":"identifier","value":"Wooooooooooow"}, {"Wooooooooooow":5}) == 5


def test_evaluate_addition():
    print("testing evaluate addition")
    ast = {
        "tag":"+",
        "left":{"tag":"number","value":1},
        "right":{"tag":"number","value":3}
        }
    assert evaluate(ast, {}) == 4

    #Homework test case
    HW_ast = {
        "tag":"+",
        "left":{"tag":"number","value":12.1},
        "right":{"tag":"number","value":2},
    }
    assert evaluate(HW_ast, {}) == 14.1

def test_evaluate_subtraction():
    print("testing evaluate subtraction")
    ast = {
        "tag":"-",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 1

    #Homework test case
    HW_ast = {
        "tag":"-",
        "left":{"tag":"number","value":12.1},
        "right":{"tag":"number","value":2},
    }
    assert evaluate(HW_ast, {}) == 10.1

def test_evaluate_multiplication():
    print("testing evaluate multiplication")
    ast = {
        "tag":"*",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 6

    #Homework test case
    HW_ast = {
        "tag":"*",
        "left":{"tag":"number","value":12.1},
        "right":{"tag":"number","value":2},
    }
    assert evaluate(HW_ast, {}) == 24.2

def test_evaluate_division():
    print("testing evaluate division")
    ast = {
        "tag":"/",
        "left":{"tag":"number","value":4},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast, {}) == 2

    #Homework test case
    HW_ast = {
        "tag":"/",
        "left":{"tag":"number","value":12.1},
        "right":{"tag":"number","value":2},
    }
    assert evaluate(HW_ast, {}) == 6.05

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
    
    # Homework Test Case
    assert eval("5+10+15*2-1") == 44

def test_relational_expressions():
    print("testing relational expressions")
    assert eval("3==3") == True
    assert eval("3==4") == False
    assert eval("3!=4") == True
    assert eval("3!=3") == False
    assert eval("3<4") == True
    assert eval("3<3") == False
    assert eval("4>3") == True
    assert eval("4>4") == False
    assert eval("3<=4") == True
    assert eval("3<=3") == True
    assert eval("3<=2") == False
    assert eval("4>=3") == True
    assert eval("4>=4") == True
    assert eval("4>=5") == False

    # Homework Test Case
    assert eval("10==10") == True
    assert eval("10!=9") == True

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

    # Homework Test Case
    assert eval("print x+y+z", {"x":2.0,"z":4.0,"$parent":{"$parent":{"y":4.0}}}) == None    
    assert printed_string == "10.0"

def test_evaluate_assignment():
    environment = {}
    eval("x=3", environment)
    assert environment["x"] == 3
    eval("y=4", environment)
    assert environment["y"] == 4
    eval("z=x+y", environment)
    assert environment["z"] == 7
    eval("x=2", environment)
    assert environment["x"] == 2

    environment = {"$parent":{"y":44.0}}
    eval("x=3", environment)
    assert environment["x"] == 3
    eval("y=4", environment)
    assert environment["y"] == 4
    eval("z=x+y", environment)
    assert environment["z"] == 7
    eval("x=2", environment)
    assert environment["x"] == 2 
    assert environment["$parent"]["y"] == 44.0


    # Homework Test Case
    environment = {"$parent":{"myGuy":125.3}}
    eval("BestBoy = 50",environment)
    assert environment["BestBoy"] == 50
    eval("myGuy = 100",environment)
    assert environment["myGuy"] == 100
    assert environment["$parent"]["myGuy"] == 125.3

    exit(0)


if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_identifier()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_relational_expressions()
    test_evaluate_print()
    test_evaluate_assignment()
    print("done.")

