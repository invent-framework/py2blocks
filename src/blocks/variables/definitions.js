const variablesColor = "#ffa54c";

const Assign = {
    init: function() {
      this.appendDummyInput()
        .appendField(new Blockly.FieldVariable(''), 'var')
        .appendField(new Blockly.FieldDropdown([
            ['=', '='],
            ['+=', '+='],
            ['-=', '-=']
          ]), 'op');
      this.appendValueInput('value');
      this.setInputsInline(true)
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(variablesColor);
    }
};

Blockly.common.defineBlocks({Assign: Assign});  

const Name = {
    init: function() {
      this.appendDummyInput('')
        .appendField(new Blockly.FieldVariable(''), 'var');
      this.setInputsInline(true)
      this.setOutput(true, "Name");
      this.setColour(variablesColor);
    }
  };
Blockly.common.defineBlocks({Name: Name});
  