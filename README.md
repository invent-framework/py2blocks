# py2blocks

A Python module, to be run in a worker using Pyodide (CPython) that takes
arbitrary Python code and converts it to a block-based representation expressed
as JSON conforming to the Blockly format.

We use the built-in Python AST module to parse the Python code and then
traverse the resulting AST to generate the Blockly JSON.

For more information about the Blockly JSON serialization format, see:

https://developers.google.com/blockly/guides/configure/web/serialization


## Developer Setup

1. Create a virtual environment and activate it.
2. Install local packages with: `pip install -r requirements.txt`
3. Run the test suite via: `make serve` and visit
   [localhost:8000](http://localhost:8000/)
4. While the local server is running, changes to the source code are 
   automatically added to the archive used by the test framework. Simply
   refresh the browser to run the updated code.

That's it!

We expect folks to contribute and collaborate in the spirit of our
[Care of Community](./CODE_OF_CONDUCT.md) statement.

## Available blocks

In the JSON representation of block, each block has a `type` whose name relates
to the matching Python `ast` node type. Depending on the type of block, they
may contain other attributes. The available blocks can be found in the
`src/blocks` folder of this repository. Please see the README.md therein for
more information.

## Pre-defined vs User-defined functions

Sometimes, for ease of use, guidance and simplicity we will provide pre-defined
blocks that represent built-in functionality. For example, the builtin
`print` function in Python may have a simple, and equivalent, `print` block.

In addition, users may define their own functions via blocks, and will then
have to call these functions via a special `function_call` block.

For this to work, when py2blocks encounters a function call the following
algorithm is used:

* Is the name of the function in the `builtin` collection of pre-defined
  blocks?
* If `True`, use the provided template for that pre-defined block, to render
  the JSON output that constitutes the blockly object model.
* If `False`, just create a `function_call` block with the relevant name and
  arguments slotted into place.
* That's it!

We will provide mechanism for third parties to be able to pre-define blocks, in
addition to the blocks we provide automatically.