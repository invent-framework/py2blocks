"""
Test suite for py2blocks.
"""

import py2blocks
import json
from pyscript import window, document


def render_blocks(id, result):
    workspace_container = document.createElement("div")
    workspace_container.id = id
    workspace_container.className = "blockly"
    document.body.appendChild(workspace_container)
    workspace = window.Blockly.inject(
        workspace_container,
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
