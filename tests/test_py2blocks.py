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
                    "fields": {"name": "test_function"},
                    "inputs": {"body": {"block": {"type": "Pass"}}},
                }
            ]
        }
    }, result


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
                    "fields": {"name": "test_function"},
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
                    "fields": {"name": "test_function"},
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
                    "fields": {
                        "name": "test_function",
                        "args": ["x"],
                    },
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "Assign",
                                "fields": {"var": {"name": "y"}},
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "BinOp",
                                            "fields": {"op": "Add"},
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
                                                        "var": {"name": "y"}
                                                    },
                                                }
                                            }
                                        },
                                    },
                                },
                            }
                        },
                    },
                }
            ]
        }
    }, result


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
                    "fields": {"name": "outer_function"},
                    "inputs": {
                        "body": {
                            "block": {
                                "type": "FunctionDef",
                                "fields": {"name": "inner_function"},
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
                    "fields": {"name": "test_function"},
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
    correctly. I.e. the **foo is destructured into individual items.
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
