const print_block = {
    init: function() {
      this.appendDummyInput('')
        .appendField('print(');
      this.appendValueInput('ARG0');
      this.appendDummyInput('')
        .appendField(')');
      this.setInputsInline(true)
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(225);
    }
};
Blockly.common.defineBlocks({print_block: print_block});
  