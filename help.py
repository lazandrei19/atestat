class Help:
    help = {
        "print": {
            "doc": "print - Prints all arguments, separated by space",
            "usage": "print <arg1> [args+]",
            "notes": "Args can have any type and be mixed"
        },
        "return": {
            "doc": "return - returns the value and ends current execution",
            "usage": "return <return_value>",
            "notes": "If this is called from inside an if, it won't terminate the context surrounding the if. For that you should use goto"
        },
        "set_var": {
            "doc": "set_var - used to define and set the values of variables",
            "usage": "set_var <var_id> [var_value]",
            "notes": "Not providing a value defaults to None"
        },
        "unset_var": {
            "doc": "unset_var - used to remove variables from the stack",
            "usage": "unset_var <var_id>",
            "notes": ""
        },
        "def_func": {
            "doc": "def_func - defines functions",
            "usage": "def_func <func_id> <func_args> <func_instr>",
            "notes": "func_args should be an array of variable names"
        },
        "rem_func": {
            "doc": "rem_func - removes a function",
            "usage": "rem_func <func_id>",
            "notes": "This can be used to redefine a function in the REPL"
        },
        "cmp": {
            "doc": "cmp - compares two values",
            "usage": "cmp <val1> <val2>",
            "notes": "returns -1 is val1 is smaller, 1 if val1 is bigger or 0 if the two are equal"
        },
        "and": {
            "doc": "and - and gate",
            "usage": "and <arg1> <arg2> [arg+]",
            "notes": "returns 0 if any one of the arguments if falsy"
        },
        "or": {
            "doc": "or - or gate",
            "usage": "and <arg1> <arg2> [arg+]",
            "notes": "returns 1 if any one of the arguments if truthy"
        },
        "not": {
            "doc": "not - not gate",
            "usage": "not <value>",
            "notes": "returns the opposite of any given input"
        },
        "if": {
            "doc": "if - conditional operator",
            "usage": "if <val1> <val2> <instr>",
            "notes": "Executes the instructions only if val1 equals val2"
        },
        "goto": {
            "doc": "goto - goes to a specific instruction",
            "usage": "goto <levels_up> <line>",
            "notes": "levels_up should be incremented with one if goto is inside an if instruction"
        },
        "import": {
            "doc": "import - imports and executes a file",
            "usage": "import <filename>",
            "notes": ""
        }
    }
