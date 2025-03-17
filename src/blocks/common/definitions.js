const catch_all = {
    init: function() {
      this.appendDummyInput()
        .appendField(new FieldMultilineInput(''), 'code');
      this.setInputsInline(true)
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#bbbbbb");
    }
};
Blockly.common.defineBlocks({catch_all: catch_all});
                      