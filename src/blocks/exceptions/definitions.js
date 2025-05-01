import { createTryBlock } from "../../plugins/exceptions.js";

Blockly.Blocks["Try"] = createTryBlock();
Blockly.Blocks["TryElse"] = createTryBlock(true);
Blockly.Blocks["TryFinally"] = createTryBlock(false, true);
Blockly.Blocks["TryElseFinally"] = createTryBlock(true, true);
                      