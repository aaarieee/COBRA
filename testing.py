import json, random, run

test_type = {
    False: "PASS",
    True: "FAIL"
}

def generate_string(length):
    string = ""
    for x in range(length):
        string += chr(random.randint(0, 255))

    return string

def get_test_sample(typ):
    match typ:
        case "NUM":
            return random.randint(0, 100)
        case "LINE":
            return 'TEST "TEST TEST" 5'
        case "STR":
            return generate_string(15)
        case _:
            return typ


def test_function(func, args, does_crash=False):
    typ = test_type[does_crash]

    print()
    print("Testing", func.__name__)
    print("Arguments:", str(args))
    print("Expected:", typ)

    try:
        func(*args)
    except Exception as e:
        if does_crash:
            print("Actual: PASS")
            return True
        print("FAIL", typ, func.__name__, str(args), e)
        return False
    if does_crash:
        print("FAIL", typ, func.__name__, str(args))
    print("PASS", typ, str(func.__name__), str(args))
    return True

def execute_test(func, args, does_crash=False):
    test_function(getattr(run, func), args, does_crash)

with open("test.builtins.json", "r") as f:
    builtins = json.load(f)

for func in builtins:
    for x in range(3):
        passing = [get_test_sample(token) for token in builtins[func]["pass"]]
        failing = [get_test_sample(token) for token in builtins[func]["fail"]]
        test_function(getattr(run, func), passing)
        test_function(getattr(run, func), failing, True)