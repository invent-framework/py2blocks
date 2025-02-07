const functionsColour = "#ff99aa";

const FunctionDef = {
    init: function() {
      this.appendDummyInput()
        .appendField('def')
        .appendField(new Blockly.FieldTextInput('my_function'), 'name')
        .appendField('(')
        .appendField(new Blockly.FieldLabelSerializable(''), 'args')
        .appendField('):');
      this.appendStatementInput('body');
      this.setInputsInline(true)
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(functionsColour);
    }
};
Blockly.common.defineBlocks({FunctionDef: FunctionDef});
  
const Pass = {
    init: function() {
      this.appendDummyInput()
        .appendField('pass');
      this.setPreviousStatement(true, null);
      this.setColour(functionsColour);
    }
};
Blockly.common.defineBlocks({Pass: Pass});
  
const Return = {
  init: function() {
    this.appendDummyInput()
      .appendField('return');
    this.appendValueInput('value');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setColour(functionsColour);
  }
};
Blockly.common.defineBlocks({Return: Return});
