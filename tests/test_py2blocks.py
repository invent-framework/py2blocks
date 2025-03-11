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
        {"renderer": "zelos", "theme": "py2blocks", "scrollbars": True},
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
    # render_blocks("test_calling_user_defined_function", result)
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
                },
                {
                    "type": "function_call",
                    "fields": {"name": "test_function"},
                    "inputs": {},
                    "extraState": {"args": 0, "keywords": 0},
                },
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
    # render_blocks("test_user_defined_function_with_args_and_kwargs", result)
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
                },
                {
                    "type": "function_call",
                    "fields": {"name": "test_function"},
                    "inputs": {
                        "arg_000001": {
                            "block": {"type": "int", "fields": {"value": 2}}
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
                    "extraState": {"args": 1, "keywords": 1},
                },
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
    # TODO: Josh to create the expected bool_op block for:
    # render_blocks("test_bool_op", result)
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
                                                            "value": True
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
                                                                        "value": False
                                                                    },
                                                                }
                                                            },
                                                            "right": {
                                                                "block": {
                                                                    "type": "bool",
                                                                    "fields": {
                                                                        "value": True
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Dict",
                    "extraState": {"items": 3},
                    "inputs": {
                        "input_000001": {
                            "shadow": {
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
                            "shadow": {
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
                            "shadow": {
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
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
                                        "shadow": {
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
                },
                {
                    "type": "Assign",
                    "inputs": {
                        "value": {
                            "block": {
                                "type": "Dict",
                                "extraState": {"items": 2},
                                "inputs": {
                                    "input_000001": {
                                        "shadow": {
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
                                                        "fields": {"value": 2},
                                                    }
                                                },
                                            },
                                        }
                                    },
                                    "input_000002": {
                                        "shadow": {
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
                },
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
    # TODO: Josh to create the expected list block for:
    # render_blocks("test_bool_op", result)
    assert result == {
        "blocks": {
            "blocks": [
                {
                    "type": "Delete",
                    "inputs": {
                        "value": {
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
