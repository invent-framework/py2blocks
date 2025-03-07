const int = {
  init: function() {
    this.appendDummyInput()
      .appendField(new Blockly.FieldNumber(0), 'value');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour("#ffffff");
  }
};
Blockly.common.defineBlocks({int: int});

const str = {
  init: function() {
    this.appendDummyInput()
      .appendField(new Blockly.FieldTextInput(0), 'value');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour("#ffffff");
  }
};
Blockly.common.defineBlocks({str: str});
