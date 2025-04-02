"""
Test suite for py2blocks.
"""

import py2blocks
import json
from pyscript import window
from pyscript.web import page, div
import upytest


def render_blocks(id, result):
    """
    Add a Blockly workspace to the DOM, with the given id, and render the
    blocks relating to the result of the conversion.
    """
    workspace_container = div(id=id)
    workspace_container.classes.add("blockly")
    page.append(workspace_container)
    workspace = window.Blockly.inject(
        workspace_container.id,
        {"renderer": "py2blocks", "theme": "py2blocks", "scrollbars": True},
    )
    window.Blockly.serialization.workspaces.load(result, workspace)
    window.workspace = workspace


async def test_with_syntax_error():
    """
    Ensure that any Python code containing a syntax error is handled gracefully.
    """
    # Syntax error: unexpected EOF while parsing
    python_code = "def f():\n    return 1 +\n"
    result = json.loads(py2blocks.py2blocks(python_code))
    assert result == {
        "error": {
            "lineno": 2,
            "offset": 15,
            "text": "    return 1 +\n",
            "message": "invalid syntax",
        }
    }, result


async def test_unsupported_code():
    """
    Ensure that any Python code that is not supported is handled gracefully by
    a catch_all block.
    """
    python_code = "match x:\n    case 'Relevant':\n        return 1"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_unsupported_code", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "catch_all",
                    "fields": {"code": python_code},
                }
            ]
        }
    }, result


async def test_function_no_args_no_body_no_return():
    """
    Ensure that a simple function is converted to Blockly JSON correctly.
    """
    python_code = "def test_function():\n    pass"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_function_no_args_no_body_no_return", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [],
                    },
                    "inputs": {"body": {"block": {"type": "Pass"}}},
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_function_no_args_no_body_with_return():
    """
    Ensure that a simple function with a return statement is converted to
    Blockly JSON correctly.
    """
    python_code = "def test_function():\n    return 1"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_function_no_args_no_body_with_return", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Return",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    }
                                },
                            }
                        }
                    },
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_function_no_args_with_body_with_return():
    """
    Ensure that a simple function with a body and a return statement is
    converted to Blockly JSON correctly.
    """
    python_code = "def test_function():\n    x = 1\n    return x"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_function_no_args_with_body_with_return", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Assign",
                                "fields": {"var": {"name": "x"}},
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    }
                                },
                                "next": {
                                    "block": {
                                        "type": "Return",
                                        "inputs": {
                                            "value": {
                                                "block": {
                                                    "type": "Name",
                                                    "fields": {
                                                        "var": {"name": "x"}
                                                    },
                                                }
                                            }
                                        },
                                    }
                                },
                            }
                        }
                    },
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_function_with_args_with_body_with_return():
    """
    Ensure that a simple function with arguments, a body, and a return statement
    is converted to Blockly JSON correctly.
    """
    python_code = "def test_function(x):\n    y = x + 1\n    return y"
    raw = py2blocks.py2blocks(python_code)
    result = json.loads(raw)
    render_blocks("test_function_with_args_with_body_with_return", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [{"name": "x"}],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Assign",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "BinOp",
                                            "inputs": {
                                                "left": {
                                                    "block": {
                                                        "type": "Name",
                                                        "fields": {
                                                            "var": {
                                                                "name": "x"
                                                            }
                                                        },
                                                    }
                                                },
                                                "right": {
                                                    "block": {
                                                        "type": "int",
                                                        "fields": {"value": 1},
                                                    }
                                                },
                                            },
                                            "fields": {"op": "Add"},
                                        }
                                    }
                                },
                                "fields": {"var": {"name": "y"}},
                                "next": {
                                    "block": {
                                        "type": "Return",
                                        "inputs": {
                                            "value": {
                                                "block": {
                                                    "type": "Name",
                                                    "fields": {
                                                        "var": {"name": "y"}
                                                    },
                                                }
                                            }
                                        },
                                    }
                                },
                            }
                        },
                        "arg_000001": {
                            "block": {
                                "type": "Argument",
                                "fields": {"name": "x"},
                            }
                        },
                    },
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_function_inside_another_function():
    """
    Ensure that a function inside another function is converted to Blockly JSON
    correctly.
    """
    python_code = "def outer_function():\n    def inner_function():\n        return 1\n    return inner_function"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_function_inside_another_function", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "outer_function",
                        "args": [],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "FunctionDef",
                                "extraState": {
                                    "create_new_model": True,
                                    "name": "inner_function",
                                    "args": [],
                                },
                                "inputs": {
                                    "body": {
                                        "block": {
                                            "type": "Return",
                                            "inputs": {
                                                "value": {
                                                    "block": {
                                                        "type": "int",
                                                        "fields": {"value": 1},
                                                    }
                                                }
                                            },
                                        }
                                    }
                                },
                                "next": {
                                    "block": {
                                        "type": "Return",
                                        "inputs": {
                                            "value": {
                                                "block": {
                                                    "type": "Name",
                                                    "fields": {
                                                        "var": {
                                                            "name": "inner_function"
                                                        }
                                                    },
                                                }
                                            }
                                        },
                                    }
                                },
                            }
                        }
                    },
                }
            ]
        }
    }, result
    assert (
        "outer_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."
    assert (
        "inner_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_calling_user_defined_function():
    # TODO: check number of args and keywords is reflected in the call block.
    python_code = "def test_function():\n    return 1\n\ntest_function()"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_calling_user_defined_function", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Return",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    }
                                },
                            }
                        }
                    },
                    "next": {
                        "block": {
                            "type": "Call",
                            "extraState": {
                                "name": "test_function",
                                "args": 0,
                                "kwargs": 0,
                            },
                            "inputs": {},
                        }
                    },
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_user_defined_function_with_args_and_kwargs():
    python_code = (
        "def test_function(x, y=1):\n    return x + y\n\ntest_function(2, y=3)"
    )
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_user_defined_function_with_args_and_kwargs", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [{"name": "x"}, {"name": "y"}],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Return",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "BinOp",
                                            "inputs": {
                                                "left": {
                                                    "block": {
                                                        "type": "Name",
                                                        "fields": {
                                                            "var": {
                                                                "name": "x"
                                                            }
                                                        },
                                                    }
                                                },
                                                "right": {
                                                    "block": {
                                                        "type": "Name",
                                                        "fields": {
                                                            "var": {
                                                                "name": "y"
                                                            }
                                                        },
                                                    }
                                                },
                                            },
                                            "fields": {"op": "Add"},
                                        }
                                    }
                                },
                            }
                        },
                        "arg_000001": {
                            "block": {
                                "type": "Argument",
                                "fields": {"name": "x"},
                            }
                        },
                        "arg_000002": {
                            "block": {
                                "type": "Argument",
                                "fields": {"name": "y"},
                            }
                        },
                    },
                    "next": {
                        "block": {
                            "type": "Call",
                            "extraState": {
                                "name": "test_function",
                                "args": 1,
                                "kwargs": 1,
                            },
                            "inputs": {
                                "arg_000001": {
                                    "block": {
                                        "type": "int",
                                        "fields": {"value": 2},
                                    }
                                },
                                "kwarg_000001": {
                                    "block": {
                                        "type": "keyword",
                                        "fields": {"arg": "y"},
                                        "inputs": {
                                            "value": {
                                                "block": {
                                                    "type": "int",
                                                    "fields": {"value": 3},
                                                }
                                            }
                                        },
                                    }
                                },
                            },
                        }
                    },
                }
            ]
        }
    }, result
    assert (
        "test_function" in py2blocks.USER_DEFINED_FUNCTIONS
    ), "Missing user defined function."


async def test_non_existent_user_defined_function_call():
    """
    Ensure that calling a non-existent user defined function is handled
    gracefully. The resulting block is the catch-all block.
    """
    python_code = "non_existent_function()"
    result = json.loads(py2blocks.py2blocks(python_code))
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "catch_all",
                    "fields": {"code": python_code},
                }
            ]
        }
    }, result


async def test_bool_op():
    """
    Ensure that a boolean operation is converted to Blockly JSON correctly.
    """
    python_code = "def test_function():\n    return True and False and True"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_bool_op", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "FunctionDef",
                    "extraState": {
                        "create_new_model": True,
                        "name": "test_function",
                        "args": [],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Return",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "BoolOp",
                                            "inputs": {
                                                "left": {
                                                    "block": {
                                                        "type": "bool",
                                                        "fields": {
                                                            "value": "True"
                                                        },
                                                    }
                                                },
                                                "right": {
                                                    "block": {
                                                        "type": "BoolOp",
                                                        "inputs": {
                                                            "left": {
                                                                "block": {
                                                                    "type": "bool",
                                                                    "fields": {
                                                                        "value": "False"
                                                                    },
                                                                }
                                                            },
                                                            "right": {
                                                                "block": {
                                                                    "type": "bool",
                                                                    "fields": {
                                                                        "value": "True"
                                                                    },
                                                                }
                                                            },
                                                        },
                                                        "fields": {
                                                            "op": "And"
                                                        },
                                                    }
                                                },
                                            },
                                            "fields": {"op": "And"},
                                        }
                                    }
                                },
                            }
                        }
                    },
                }
            ]
        }
    }, result


async def test_joinedstr():
    """
    The JoinedStr AST node is used to represent f-strings. Ensure that a simple
    f-string is converted to Blockly JSON correctly.
    """
    python_code = "f'Hello {name} from Python {x:3}'"
    result = json.loads(py2blocks.py2blocks(python_code))
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "JoinedStr",
                    "fields": {
                        "value": [
                            {"type": "str", "fields": {"value": "Hello "}},
                            {
                                "type": "FormattedValue",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "Name",
                                            "fields": {
                                                "var": {"name": "name"}
                                            },
                                        }
                                    },
                                    "format_spec": None,
                                },
                            },
                            {
                                "type": "str",
                                "fields": {"value": " from Python "},
                            },
                            {
                                "type": "FormattedValue",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "Name",
                                            "fields": {"var": {"name": "x"}},
                                        }
                                    },
                                    "format_spec": {
                                        "type": "JoinedStr",
                                        "fields": {
                                            "value": [
                                                {
                                                    "type": "str",
                                                    "fields": {"value": "3"},
                                                }
                                            ]
                                        },
                                    },
                                },
                            },
                        ]
                    },
                }
            ]
        }
    }, result


async def test_list():
    """
    Ensure that a list is converted to Blockly JSON correctly.
    """
    python_code = '["a", "b", "c"]'
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_list", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "List",
                    "extraState": {"items": 3},
                    "inputs": {
                        "input_000001": {
                            "block": {"type": "str", "fields": {"value": "a"}}
                        },
                        "input_000002": {
                            "block": {"type": "str", "fields": {"value": "b"}}
                        },
                        "input_000003": {
                            "block": {"type": "str", "fields": {"value": "c"}}
                        },
                    },
                }
            ]
        }
    }, result


async def test_tuple():
    """
    Ensure that a tuple is converted to Blockly JSON correctly.
    """
    python_code = '("a", "b", "c")'
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_tuple", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Tuple",
                    "extraState": {"items": 3},
                    "inputs": {
                        "input_000001": {
                            "block": {"type": "str", "fields": {"value": "a"}}
                        },
                        "input_000002": {
                            "block": {"type": "str", "fields": {"value": "b"}}
                        },
                        "input_000003": {
                            "block": {"type": "str", "fields": {"value": "c"}}
                        },
                    },
                }
            ]
        }
    }, result


async def test_set():
    """
    Ensure that a set is converted to Blockly JSON correctly.
    """
    python_code = '{"a", "b", "c"}'
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_set", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Set",
                    "extraState": {"items": 3},
                    "inputs": {
                        "input_000001": {
                            "block": {"type": "str", "fields": {"value": "a"}}
                        },
                        "input_000002": {
                            "block": {"type": "str", "fields": {"value": "b"}}
                        },
                        "input_000003": {
                            "block": {"type": "str", "fields": {"value": "c"}}
                        },
                    },
                }
            ]
        }
    }, result


async def test_dict():
    """
    Ensure that a dict is converted to Blockly JSON correctly.
    """
    python_code = '{"a": 1, "b": 2, "c": 3}'
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_dict", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Dict",
                    "extraState": {"items": 3},
                    "inputs": {
                        "input_000001": {
                            "block": {
                                "type": "dict_item",
                                "inputs": {
                                    "key": {
                                        "block": {
                                            "type": "str",
                                            "fields": {"value": "a"},
                                        }
                                    },
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    },
                                },
                            }
                        },
                        "input_000002": {
                            "block": {
                                "type": "dict_item",
                                "inputs": {
                                    "key": {
                                        "block": {
                                            "type": "str",
                                            "fields": {"value": "b"},
                                        }
                                    },
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 2},
                                        }
                                    },
                                },
                            }
                        },
                        "input_000003": {
                            "block": {
                                "type": "dict_item",
                                "inputs": {
                                    "key": {
                                        "block": {
                                            "type": "str",
                                            "fields": {"value": "c"},
                                        }
                                    },
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 3},
                                        }
                                    },
                                },
                            }
                        },
                    },
                }
            ]
        }
    }, result


async def test_dict_with_pompoms_to_unpack():
    """
    Ensure that a dict as {"a": 1, **foo} is converted to Blockly JSON
    correctly. I.e. the **foo (pompom foo) is destructured into individual
    key-value items in the new dict.
    """
    python_code = 'd = {"a": 1}\nd2 = {"b": 2, **d}'
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_dict_with_pompoms_to_unpack", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Assign",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Dict",
                                "extraState": {"items": 1},
                                "inputs": {
                                    "input_000001": {
                                        "block": {
                                            "type": "dict_item",
                                            "inputs": {
                                                "key": {
                                                    "block": {
                                                        "type": "str",
                                                        "fields": {
                                                            "value": "a"
                                                        },
                                                    }
                                                },
                                                "value": {
                                                    "block": {
                                                        "type": "int",
                                                        "fields": {"value": 1},
                                                    }
                                                },
                                            },
                                        }
                                    }
                                },
                            }
                        }
                    },
                    "fields": {"var": {"name": "d"}},
                    "next": {
                        "block": {
                            "type": "Assign",
                            "inputs": {
                                "value": {
                                    "block": {
                                        "type": "Dict",
                                        "extraState": {"items": 2},
                                        "inputs": {
                                            "input_000001": {
                                                "block": {
                                                    "type": "dict_item",
                                                    "inputs": {
                                                        "key": {
                                                            "block": {
                                                                "type": "str",
                                                                "fields": {
                                                                    "value": "b"
                                                                },
                                                            }
                                                        },
                                                        "value": {
                                                            "block": {
                                                                "type": "int",
                                                                "fields": {
                                                                    "value": 2
                                                                },
                                                            }
                                                        },
                                                    },
                                                }
                                            },
                                            "input_000002": {
                                                "block": {
                                                    "type": "dict_unpack",
                                                    "inputs": {
                                                        "value": {
                                                            "block": {
                                                                "type": "Name",
                                                                "fields": {
                                                                    "var": {
                                                                        "name": "d"
                                                                    }
                                                                },
                                                            }
                                                        }
                                                    },
                                                }
                                            },
                                        },
                                    }
                                }
                            },
                            "fields": {"var": {"name": "d2"}},
                        }
                    },
                }
            ]
        }
    }, result


async def test_del_variable():
    """
    Using the del keyword to delete a variable is converted to Blockly JSON
    correctly.
    """
    python_code = "del my_variable"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_del_variable", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Delete",
                    "extraState": {"items": 1},
                    "inputs": {
                        "input_000001": {
                            "block": {
                                "type": "Name",
                                "fields": {"var": {"name": "my_variable"}},
                            }
                        }
                    },
                }
            ]
        }
    }, result


async def test_basic_builtin_block():
    """
    Ensure that a built-in function call is converted to the appropriate
    block template.
    """
    python_code = "print('Hello, World!')"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_basic_builtin_block", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "print_block",
                    "inputs": {
                        "ARG0": {
                            "block": {
                                "type": "str",
                                "fields": {"value": "Hello, World!"},
                            }
                        }
                    },
                }
            ]
        }
    }, result


async def test_not_block():
    """
    Ensure that the NOT operator is converted to Blockly JSON correctly.
    """
    python_code = "not True"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_not_block", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Not",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "bool",
                                "fields": {"value": "True"},
                            }
                        }
                    },
                }
            ]
        }
    }, result


async def test_unary_operator_that_is_not_NOT():
    """
    Ensure that a unary operator that is not the NOT operator is converted to
    Blockly JSON correctly.
    """
    python_code = "-1"
    result = json.loads(py2blocks.py2blocks(python_code))
    # TODO: Josh to implement a UnaryOp block
    render_blocks("test_unary_operator_that_is_not_NOT", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "UnaryOp",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "int",
                                "fields": {"value": 1},
                            }
                        }
                    },
                    "fields": {"op": "USub"},
                }
            ]
        }
    }, result


async def test_compare():
    """
    Ensure that a comparison is converted to Blockly JSON correctly.
    """
    python_code = "1 < 2 > 5"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_compare", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Compare",
                    "inputs": {
                        "left": {
                            "block": {"type": "int", "fields": {"value": 1}}
                        },
                        "right": {
                            "block": {
                                "type": "Compare",
                                "inputs": {
                                    "left": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 2},
                                        }
                                    },
                                    "right": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 5},
                                        }
                                    },
                                },
                                "fields": {"op": "Gt"},
                            }
                        },
                    },
                    "fields": {"op": "Lt"},
                }
            ]
        }
    }, result


async def test_if_exp():
    """
    Ensure that an if expression is converted to Blockly JSON correctly.
    """
    python_code = "x = 1 if True else 2"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_if_exp", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Assign",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "IfExp",
                                "inputs": {
                                    "test": {
                                        "block": {
                                            "type": "bool",
                                            "fields": {"value": "True"},
                                        }
                                    },
                                    "body": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    },
                                    "orelse": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 2},
                                        }
                                    },
                                },
                            }
                        }
                    },
                    "fields": {"var": {"name": "x"}},
                }
            ]
        }
    }, result


async def test_attribute():
    """
    Ensure that an attribute is converted to Blockly JSON correctly.
    """
    python_code = "x.y.z"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_attribute", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Attribute",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Attribute",
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "Name",
                                            "fields": {"var": {"name": "x"}},
                                        }
                                    }
                                },
                                "fields": {"attr": "y"},
                            }
                        }
                    },
                    "fields": {"attr": "z"},
                }
            ]
        }
    }, result


async def test_namedexpr():
    """
    Ensure that a named expression is converted to Blockly JSON correctly.
    """
    python_code = "print(x := 1)"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_namedexpr", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "print_block",
                    "inputs": {
                        "ARG0": {
                            "block": {
                                "type": "NamedExpr",
                                "inputs": {
                                    "target": {
                                        "block": {
                                            "type": "Name",
                                            "fields": {"var": {"name": "x"}},
                                        }
                                    },
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    },
                                },
                            }
                        }
                    },
                }
            ]
        }
    }, result


async def test_subscript_index():
    """
    Ensure that a subscript is converted to Blockly JSON correctly.
    """
    python_code = "x[0]"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_subscript", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Subscript",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Name",
                                "fields": {"var": {"name": "x"}},
                            }
                        },
                        "slice": {
                            "block": {"type": "int", "fields": {"value": 0}}
                        },
                    },
                }
            ]
        }
    }, result


async def test_subscript_dict_key():
    """
    Ensure that a subscript is converted to Blockly JSON correctly.
    """
    python_code = "x['key']"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_subscript", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Subscript",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Name",
                                "fields": {"var": {"name": "x"}},
                            }
                        },
                        "slice": {
                            "block": {
                                "type": "str",
                                "fields": {"value": "key"},
                            }
                        },
                    },
                }
            ]
        }
    }, result


async def test_slice_no_step():
    """
    Ensure that a slice is converted to Blockly JSON correctly.
    """
    python_code = "x[0:2]"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_slice", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Subscript",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Name",
                                "fields": {"var": {"name": "x"}},
                            }
                        },
                        "slice": {
                            "block": {
                                "type": "Slice",
                                "inputs": {
                                    "lower": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 0},
                                        }
                                    },
                                    "upper": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 2},
                                        }
                                    },
                                    "step": {"block": None},
                                },
                            }
                        },
                    },
                }
            ]
        }
    }, result


async def test_slice_with_step():
    """
    Ensure that a slice is converted to Blockly JSON correctly.
    """
    python_code = "x[0:2,3]"
    result = json.loads(py2blocks.py2blocks(python_code))
    render_blocks("test_slice", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Subscript",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Name",
                                "fields": {"var": {"name": "x"}},
                            }
                        },
                        "slice": {
                            "block": {
                                "type": "Slice",
                                "inputs": {
                                    "lower": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 0},
                                        }
                                    },
                                    "upper": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 2},
                                        }
                                    },
                                    "step": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 3},
                                        }
                                    },
                                },
                            }
                        },
                    },
                }
            ]
        }
    }, result

async def test_list_comp():
    result = {
        "blocks": {
            "blocks": [
                {
                    "type": "ListComp",
                    "extraState": {
                        "items": 1,
                    }
                }
            ]
        }
    }
    render_blocks("test_list_comp", result)
    assert True