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
import copy


# Contains definitions of built-in functions and their corresponding block
# templates.
BUILTIN_BLOCKS = {
    "print": {
        "type": "print_block",
        "inputs": {
            "ARG0": {"block": None}  # Will be filled with the first argument
        },
    },
}


# Contains definitions of user-defined functions and their corresponding block
# templates. This dictionary is populated by the user-defined functions in the
# Python code. Functions defined in this dictionary allow us to ensure the user
# doesn't try to call non-existent functions. The key is the function name and
# the value is the blockly id and metadata needed to generate a valid block for
# the function.
USER_DEFINED_FUNCTIONS = {}


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
    previous_node = None
    for node in tree.body:
        current_node = traverse_node(node)
        if previous_node:
            # We're recursing into the node tree so add the next block
            # to the previous node.
            previous_node["next"] = {"block": current_node}
        else:
            # The first block in the tree. Set it as the root.
            blocks["blocks"].append(current_node)
        previous_node = current_node
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


def register_builtin_block(name, template):
    """
    Register a new built-in function with its block template.

    Args:
        name (str): The name of the built-in function (e.g., 'print' or 'invent.publish').
        template (dict): The template to use for this function.
    """
    BUILTIN_BLOCKS[name] = template


def get_function_key(node):
    """
    Get the function key for the BUILTIN_BLOCKS dictionary.
    For module.function calls, combines the module and function name.

    Args:
        node (ast.Call): The function call node.

    Returns:
        str or None: The function key or None if it's not a simple name or attribute.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute) and isinstance(
        node.func.value, ast.Name
    ):
        # Handle module.function style calls (e.g., invent.subscribe)
        return f"{node.func.value.id}.{node.func.attr}"
    return None


def is_builtin_function(function_key):
    """
    Check if a function key is in the built-in collection.

    Args:
        function_key (str): The function key to check.

    Returns:
        bool: True if the function is a built-in, False otherwise.
    """
    return function_key in BUILTIN_BLOCKS


def extract_constant_value(arg_block):
    """
    Extract a constant value from an argument block if possible.

    Args:
        arg_block (dict): The block representing an argument.

    Returns:
        Any: The constant value if it can be extracted, otherwise None.
    """
    # Check if the block is a constant type
    if (
        arg_block
        and "type" in arg_block
        and "fields" in arg_block
        and "value" in arg_block["fields"]
    ):
        # Basic types: int, float, str, bool, etc.
        return arg_block["fields"]["value"]
    return None


def get_function_name(node):
    """
    Get a simple representation of the function name for function_call blocks.

    Args:
        node (ast.Call): The call node.

    Returns:
        str or None: A string representation of the function name if simple, None if complex.
    """
    if isinstance(node.func, ast.Name):
        # Simple function name
        return node.func.id
    elif isinstance(node.func, ast.Attribute) and isinstance(
        node.func.value, ast.Name
    ):
        # Module.function style
        return f"{node.func.value.id}.{node.func.attr}"
    return None


def catch_all(node, block):
    """
    If the node is not supported, we need to provide enough context for a
    catch-all block that just contains arbitrary code.
    """
    block["type"] = "catch_all"
    block["fields"] = {"code": ast.unparse(node)}
    return block


def apply_template(template, arg_blocks, kwarg_blocks):
    """
    Apply arguments to a template following a consistent pattern.
    This function makes a deep copy of the template and fills in placeholders.

    Args:
        template (dict): The template to fill.
        arg_blocks (list): List of blocks for positional arguments.
        kwarg_blocks (list): List of (name, block) tuples for keyword arguments.

    Returns:
        dict: A new block with the arguments applied to the template.
    """
    # Create a deep copy of the template to avoid modifying the original
    result = copy.deepcopy(template)

    # First, handle field mappings if present
    if "field_mapping" in result:
        field_mappings = result["field_mapping"]

        # Create a dictionary of keyword arguments for easier lookup
        kwarg_dict = {name: block for name, block in kwarg_blocks}

        # Apply field mappings
        for field_name, mapping in field_mappings.items():
            # Check if we need to map from a positional argument
            if "arg_index" in mapping and mapping["arg_index"] < len(
                arg_blocks
            ):
                arg_index = mapping["arg_index"]
                value = extract_constant_value(arg_blocks[arg_index])

                # If we successfully extracted a value, apply it to the field
                if value is not None:
                    # Apply the extracted value to the field
                    if "fields" in result:
                        result["fields"][field_name] = value

            # Check if we need to map from a keyword argument
            elif (
                "kwarg_name" in mapping and mapping["kwarg_name"] in kwarg_dict
            ):
                kwarg_name = mapping["kwarg_name"]
                value = extract_constant_value(kwarg_dict[kwarg_name])

                # If we successfully extracted a value, apply it to the field
                if value is not None:
                    # Apply the extracted value to the field
                    if "fields" in result:
                        result["fields"][field_name] = value

        # Remove the field_mapping from the result as it's not part of the Blockly format
        del result["field_mapping"]

    # Process the inputs dictionary if it exists
    if "inputs" in result:
        # Apply positional arguments (ARG0, ARG1, ARG2, etc.)
        for i, arg_block in enumerate(arg_blocks):
            arg_key = f"ARG{i}"
            if arg_key in result["inputs"]:
                # If there's a shadow block in the template
                if "shadow" in result["inputs"][arg_key]:
                    # Check if we can reuse the shadow block structure
                    shadow = result["inputs"][arg_key]["shadow"]
                    if (
                        shadow["type"] == arg_block["type"]
                        and "fields" in shadow
                        and "fields" in arg_block
                    ):
                        # Update the fields in the shadow block
                        for field_key, field_value in arg_block[
                            "fields"
                        ].items():
                            if field_key in shadow["fields"]:
                                shadow["fields"][field_key] = field_value
                    else:
                        # Types don't match, replace the shadow with the actual block
                        result["inputs"][arg_key] = {"block": arg_block}
                else:
                    # No shadow, just set the block directly
                    result["inputs"][arg_key]["block"] = arg_block

    # Apply keyword arguments that didn't get used in field mappings
    for kw_name, kw_block in kwarg_blocks:
        kw_key = f"KWARG_{kw_name}"
        # If the template has a specific placeholder for this keyword
        if "inputs" in result and kw_key in result["inputs"]:
            if "shadow" in result["inputs"][kw_key]:
                # Similar logic to positional args with shadows
                shadow = result["inputs"][kw_key]["shadow"]
                if (
                    shadow["type"] == kw_block["type"]
                    and "fields" in shadow
                    and "fields" in kw_block
                ):
                    for field_key, field_value in kw_block["fields"].items():
                        if field_key in shadow["fields"]:
                            shadow["fields"][field_key] = field_value
                else:
                    result["inputs"][kw_key] = {"block": kw_block}
            else:
                result["inputs"][kw_key]["block"] = kw_block
        else:
            # If the template doesn't have a specific placeholder, add it
            if "inputs" not in result:
                result["inputs"] = {}
            result["inputs"][kw_key] = {"block": kw_block}

    return result


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
        block["extraState"] = {
            "create_new_model": True,
            "name": node.name,
            "args": [{"name": arg.arg} for arg in node.args.args],
        }
        block["inputs"] = {"body": {}}
        body = traverse_body(node.body)
        if body:
            block["inputs"]["body"]["block"] = body
        # Iterate over args and create an Argument block within the corresponding input
        for i, arg in enumerate(node.args.args, start=1):
            block["inputs"][f"arg_{i:06}"] = {
                "block": {
                    "type": "Argument",
                    "fields": {"name": arg.arg},
                }
            }
        # Register the function for later use. TODO: FIXME for nested functions.
        USER_DEFINED_FUNCTIONS[node.name] = {
            "function_name": node.name,
            "args": [{"name": arg.arg} for arg in node.args.args],
        }
    elif isinstance(node, ast.Return):
        block["inputs"] = {
            "value": {
                "block": traverse_node(node.value),
            },
        }
    elif isinstance(node, ast.Constant):
        block["type"] = type(node.value).__name__
        if isinstance(node.value, bool):
            block["fields"] = {"value": str(node.value)}
        else:
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
                    "block": {
                        "type": "dict_unpack",
                        "inputs": {
                            "value": {"block": traverse_node(value)},
                        },
                    }
                }
            else:
                block["inputs"][f"input_{i:06}"] = {
                    "block": {
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
        block["extraState"] = {"items": len(node.targets)}
        block["inputs"] = {}
        for i, target in enumerate(node.targets, start=1):
            block["inputs"][f"input_{i:06}"] = {"block": traverse_node(target)}
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
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            block["type"] = "Not"
            block["inputs"] = {
                "value": {
                    "block": traverse_node(node.operand),
                },
            }
        else:
            block["inputs"] = {
                "value": {
                    "block": traverse_node(node.operand),
                },
            }
            block["fields"] = {"op": type(node.op).__name__}
    elif isinstance(node, ast.Call):
        # Get the function identifier (could be simple name or module.function)
        function_key = get_function_key(node)

        # Process positional arguments
        arg_blocks = [traverse_node(arg) for arg in node.args]

        # Process keyword arguments
        kwarg_blocks = [
            (kw.arg, traverse_node(kw.value))
            for kw in node.keywords
            if kw.arg is not None
        ]

        # Check if it's a built-in function with a pre-defined block template
        if function_key and is_builtin_function(function_key):
            # Get the template and apply the arguments
            template = BUILTIN_BLOCKS[function_key]
            block = apply_template(template, arg_blocks, kwarg_blocks)

            # Handle kwargs unpacking if present
            kwargs_unpack = [
                kw.value for kw in node.keywords if kw.arg is None
            ]
            if kwargs_unpack:
                if "inputs" not in block:
                    block["inputs"] = {}
                block["inputs"]["KWARGS_UNPACK"] = {
                    "block": traverse_node(kwargs_unpack[0])
                }
        elif function_key in USER_DEFINED_FUNCTIONS:
            # It's a user-defined function or a method call
            block["extraState"] = block.get("extraState", {})

            # Get function name for simple cases
            func_name = get_function_name(node)

            if func_name:
                block["extraState"]["name"] = func_name
                block["inputs"] = {}

            # Add positional arguments
            block["extraState"]["args"] = len(node.args)
            if "inputs" not in block:
                block["inputs"] = {}
            for i, arg in enumerate(node.args, start=1):
                block["inputs"][f"arg_{i:06}"] = {
                    "block": traverse_node(arg),
                }

            # Add keyword arguments
            block["extraState"] = block.get("extraState", {})
            block["extraState"]["kwargs"] = len(node.keywords)
            for i, keyword in enumerate(node.keywords, start=1):
                if keyword.arg is None:
                    # This is a **kwargs argument
                    block["inputs"][f"kwarg_{i:06}"] = {
                        "block": {
                            "type": "kwargs_unpack",
                            "inputs": {
                                "value": {
                                    "block": traverse_node(keyword.value)
                                },
                            },
                        },
                    }
                else:
                    block["inputs"][f"kwarg_{i:06}"] = {
                        "block": {
                            "type": "keyword",
                            "fields": {"arg": keyword.arg},
                            "inputs": {
                                "value": {
                                    "block": traverse_node(keyword.value)
                                },
                            },
                        },
                    }
        else:
            block = catch_all(node, block)
    else:
        block = catch_all(node, block)
    return block
