"""
Test suite for py2blocks.
"""

import py2blocks
import json


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
                                "fields": {"id": "x"},
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "int",
                                            "fields": {"value": 1},
                                        }
                                    }
                                },
                                "next": {
                                    "type": "Return",
                                    "inputs": {
                                        "value": {
                                            "block": {
                                                "type": "Name",
                                                "fields": {"id": "x"},
                                            }
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


async def test_function_with_args_with_body_with_return():
    """
    Ensure that a simple function with arguments, a body, and a return statement
    is converted to Blockly JSON correctly.
    """
    python_code = "def test_function(x):\n    y = x + 1\n    return y"
    raw = py2blocks.py2blocks(python_code)
    result = json.loads(raw)
    expected = {
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
                                "fields": {"id": "y"},
                                "inputs": {
                                    "value": {
                                        "block": {
                                            "type": "BinOp",
                                            "fields": {"op": "Add"},
                                            "inputs": {
                                                "left": {
                                                    "block": {
                                                        "type": "Name",
                                                        "fields": {"id": "x"},
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
                                    "type": "Return",
                                    "inputs": {
                                        "value": {
                                            "block": {
                                                "type": "Name",
                                                "fields": {"id": "y"},
                                            }
                                        }
                                    },
                                },
                            }
                        },
                    },
                }
            ]
        }
    }
    assert (
        result == expected
    ), f"\n{raw}\nDoesn't equal\n{json.dumps(expected)}"
