const mathColour = "#ff99aa";

const int = {
  init: function() {
    this.appendDummyInput()
      .appendField(new Blockly.FieldNumber(0), "value");
    this.setInputsInline(true)
    this.setOutput(true, "int");
    this.setColour("#ffffff");
  }
};
Blockly.common.defineBlocks({int: int});

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