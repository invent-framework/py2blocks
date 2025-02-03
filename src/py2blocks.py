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
    # Parse the Python code into an AST.
    tree = ast.parse(code)
    # Traverse the AST to generate the Blockly JSON.
    return json.dumps(traverse(tree))


def traverse(tree):
    """
    Traverse the AST and generate the Blockly JSON.

    Args:
        tree (ast.AST): The AST to traverse.

    Returns:
        dict: The Blockly JSON representation of the AST.
    """
    # The root of the Blockly JSON.
    blocks = {"type": "root", "children": []}
    # Traverse the AST and generate the Blockly JSON.
    for node in tree.body:
        blocks["children"].append(traverse_node(node))
    return blocks


def traverse_node(node):
    """
    Traverse a node in the AST and generate the Blockly JSON.

    Args:
        node (ast.AST): The node to traverse.

    Returns:
        dict: The Blockly JSON representation of the node.
    """
    # The Blockly JSON representation of the node.
    block = {"type": "statement", "children": []}
    # Traverse the node and generate the Blockly JSON.
    if isinstance(node, ast.FunctionDef):
        block["type"] = "function"
        block["name"] = node.name
        block["children"] = [traverse_node(n) for n in node.body]
    """
    elif isinstance(node, ast.Assign):
        block["type"] = "assign"
        block["targets"] = [traverse_node(n) for n in node.targets]
        block["value"] = traverse_node(node.value)
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
