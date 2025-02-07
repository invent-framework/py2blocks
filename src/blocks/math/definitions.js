const mathColour = "#ff99aa";

const BinOp = {
  init: function() {
    this.appendValueInput('left');
    this.appendDummyInput('')
      .appendField(new Blockly.FieldDropdown([
          ['+', 'Add'],
          ['-', '-']
        ]), 'op');
    this.appendValueInput('right');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setTooltip('');
    this.setHelpUrl('');
    this.setColour("#97a2d8");
  }
};
Blockly.common.defineBlocks({BinOp: BinOp});