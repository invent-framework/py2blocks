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
import numbers


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
        block["next"] = traverse_body(the_rest) if the_rest else None
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
    if isinstance(node, ast.FunctionDef):
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
    elif isinstance(node, ast.Assign):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
        block["fields"] = {"id": node.targets[0].id}
    elif isinstance(node, ast.AugAssign):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
        block["fields"] = {"id": node.target.id}
    elif isinstance(node, ast.Name):
        block["fields"] = {"id": node.id}
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
    """
    elif isinstance(node, ast.Expr):
        block["type"] = "expr"
        block["value"] = traverse_node(node.value)
    elif isinstance(node, ast.Call):
        block["type"] = "call"
        block["func"] = traverse_node(node.func)
        block["args"] = [traverse_node(a) for a in node.args]
        block["keywords"] = [traverse_node(k) for k in node.keywords]
    elif isinstance(node, ast.Name):
        block["type"] = "name"
        block["id"] = node.id
    elif isinstance(node, ast.Str):
        block["type"] = "str"
        block["s"] = node.s
    elif isinstance(node, ast.Num):
        block["type"] = "num"
        block["n"] = node.n
    elif isinstance(node, ast.BinOp):
        block["type"] = "binop"
        block["left"] = traverse_node(node.left)
        block["op"] = traverse_node(node.op)
        block["right"] = traverse_node(node.right)
    elif isinstance(node, ast.Add):
        block["type"] = "add"
    elif isinstance(node, ast.Sub):
        block["type"] = "sub"
    elif isinstance(node, ast.Mult):
        block["type"] = "mult"
    elif isinstance(node, ast.Div):
        block["type"] = "div"
    elif isinstance(node, ast.Mod):
        block["type"] = "mod"
    elif isinstance(node, ast.Pow):
        block["type"] = "pow"
    elif isinstance(node, ast.USub):
        block["type"] = "usub"
    return block
    """
    return block
