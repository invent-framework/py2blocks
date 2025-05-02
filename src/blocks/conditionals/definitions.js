import { createIfBlock, createWithBlock } from "../../plugins/conditionals.js";

Blockly.Blocks["If"] = createIfBlock();
Blockly.Blocks["AsyncIf"] = createIfBlock(true);
Blockly.Blocks["With"] = createWithBlock();
Blockly.Blocks["AsyncWith"] = createWithBlock(true);