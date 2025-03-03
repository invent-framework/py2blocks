"""
A Python module, to be run in a worker using Pyodide (CPython) that takes
arbitrary Python code and converts it to a block-based representation expressed
as JSON conforming to the Blockly format.

We use the built-in Python AST module to parse the Python code and then
traverse the resulting AST to generate the Blockly JSON.

For more information about the Blockly JSON serialization format, see:

https://developers.google.com/blockly/guides/configure/web/serialization
"""

import ast
import json


def py2blocks(code):
    """
    Convert Python code to Blockly JSON.

    Args:
        code (str): The Python code to convert.

    Returns:
        str: The Blockly JSON representation of the Python code.
    """
    try:
        # Parse the Python code into an AST.
        tree = ast.parse(code)
        # Traverse the AST to generate the Blockly JSON.
        return json.dumps(traverse(tree))
    except SyntaxError as e:
        # Return some helpful context for the syntax error.
        context = {
            "lineno": e.lineno,
            "offset": e.offset,
            "text": e.text,
            "message": e.msg,
        }
        return json.dumps({"error": context})
    except Exception as e:
        # Catch all for all other errors.
        return json.dumps({"error": str(e)})


def traverse(tree):
    """
    Traverse the AST and generate the Blockly JSON.

    Args:
        tree (ast.AST): The AST to traverse.

    Returns:
        dict: The Blockly JSON representation of the AST.
    """
    # The root of the Blockly JSON.
    blocks = {
        "blocks": [],
    }
    # Traverse the AST and generate the Blockly JSON.
    for node in tree.body:
        blocks["blocks"].append(traverse_node(node))
    return {
        "blocks": blocks,
    }


def traverse_body(body):
    """
    Traverse the body of a node in the AST and generate the Blockly JSON.
    """
    node = body[0]
    the_rest = body[1:]
    block = traverse_node(node)
    if the_rest:
        block["next"] = (
            {"block": traverse_body(the_rest)} if the_rest else None
        )
    return block


def traverse_node(node):
    """
    Traverse a node in the AST and generate the Blockly JSON.
    """
    # The Blockly JSON representation of the node.
    block = {
        "type": type(node).__name__,
        # Add other global attributes here.
    }
    # Traverse the node and generate the Blockly JSON.
    if node is None:
        return node
    elif isinstance(node, ast.Pass):
        return block
    elif isinstance(node, ast.FunctionDef):
        block["fields"] = {"name": node.name}
        if node.args.args:
            block["fields"]["args"] = [arg.arg for arg in node.args.args]
        block["inputs"] = {"body": {}}
        body = traverse_body(node.body)
        if body:
            block["inputs"]["body"]["block"] = body
    elif isinstance(node, ast.Return):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
    elif isinstance(node, ast.Constant):
        block["type"] = type(node.value).__name__
        block["fields"] = {"value": node.value}
    elif isinstance(node, ast.Expr):
        block = traverse_node(node.value)
    elif isinstance(node, ast.FormattedValue):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
            "format_spec": traverse_node(node.format_spec),
        }
    elif isinstance(node, ast.JoinedStr):
        values = [traverse_node(value) for value in node.values]
        block["fields"] = {"value": values}
    elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        block["extraState"] = {"items": len(node.elts)}
        block["inputs"] = {}
        for i, elt in enumerate(node.elts, start=1):
            block["inputs"][f"input_{i:06}"] = {"block": traverse_node(elt)}
    elif isinstance(node, ast.Dict):
        block["extraState"] = {"items": len(node.keys)}
        block["inputs"] = {}
        for i, (key, value) in enumerate(zip(node.keys, node.values), start=1):
            if key is None:
                # This is a **some_dict argument to unpack.
                block["inputs"][f"input_{i:06}"] = {
                    "shadow": {
                        "type": "dict_unpack",
                        "inputs": {
                            "value": {"block": traverse_node(value)},
                        },
                    }
                }
            else:
                block["inputs"][f"input_{i:06}"] = {
                    "shadow": {
                        "type": "dict_item",
                        "inputs": {
                            "key": {"block": traverse_node(key)},
                            "value": {"block": traverse_node(value)},
                        },
                    }
                }
    elif isinstance(node, ast.Assign):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
        block["fields"] = {"var": {"name": node.targets[0].id}}
    elif isinstance(node, ast.Delete):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.targets[0]),
            },
        }
    elif isinstance(node, ast.AugAssign):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
        block["fields"] = {"var": {"name": node.target.id}}
    elif isinstance(node, ast.Name):
        block["fields"] = {"var": {"name": node.id}}
    elif isinstance(node, ast.BinOp):
        block["inputs"] = {
            "left": {
                "block": traverse_node(node.left),
            },
            "right": {
                "block": traverse_node(node.right),
            },
        }
        block["fields"] = {"op": type(node.op).__name__}
    elif isinstance(node, ast.BoolOp):
        # If there are two values, just use value[0] as left and value[1] as
        # right input.
        # If there are more than two values, use value[0] as left and create a
        # new ast.BoolOp (with the remaining values), as the right input.
        if len(node.values) == 2:
            block["inputs"] = {
                "left": {
                    "block": traverse_node(node.values[0]),
                },
                "right": {
                    "block": traverse_node(node.values[1]),
                },
            }
        else:
            block["inputs"] = {
                "left": {
                    "block": traverse_node(node.values[0]),
                },
                "right": {
                    "block": traverse_node(
                        ast.BoolOp(op=node.op, values=node.values[1:])
                    ),
                },
            }
        block["fields"] = {"op": type(node.op).__name__}
    else:
        # If the node is not supported, we need to provide enough context for
        # the catch-all block that just contains arbitrary code.
        block["type"] = "catch_all"
        block["fields"] = {"code": ast.unparse(node)}
    return block
