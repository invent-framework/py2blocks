# Available blocks

[Blockly](https://developers.google.com/blockly) is a JavaScript library for
building block based coding environments. If you've ever used Scratch, you've
used Blockly, which provides the drag and drop code assembly for Scratch.

Blockly is a highly configurable library, and the blocks defined in this
directory relate directly to the JSON output from the `py2blocks` module. In
this way, aspects of Python's AST can be expressed as blocks. In other words,
a Python conditional (for example), becomes a "conditional" block for
Blockly.

Furthermore, these blocks are used and checked as part of our test suite (see
the `/tests` directory). We use a `render_blocks` function to take the result
of the test, and re-hydrate the JSON into the blocks defined in this directory.

Colour-scheme is based on Scratch's (for instance, function definitions and
function calls are all pink).