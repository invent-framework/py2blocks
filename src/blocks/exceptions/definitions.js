import { createTryBlock } from "../../plugins/exceptions.js";

Blockly.Blocks["Try"] = createTryBlock();
Blockly.Blocks["TryElse"] = createTryBlock(true);
Blockly.Blocks["TryFinally"] = createTryBlock(false, true);
Blockly.Blocks["TryElseFinally"] = createTryBlock(true, true);

const ExceptAs = {
    init: function() {
      this.appendValueInput('type');
      this.appendDummyInput('')
        .appendField('as');
      this.appendValueInput('name');
      this.setInputsInline(true)
      this.setOutput(true, null);
      this.setColour(225);
    }
};
Blockly.common.defineBlocks({ExceptAs: ExceptAs});
                      