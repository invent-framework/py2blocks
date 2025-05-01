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
                      
const alias = {
  init: function() {
    this.appendDummyInput()
      .appendField(new Blockly.FieldTextInput(''), 'name');
    this.setInputsInline(true)
    this.setOutput(true, "alias");
    this.setColour("#ffffff");
  }
};
Blockly.common.defineBlocks({alias: alias});

const Pass = {
  init: function() {
    this.appendDummyInput()
      .appendField('pass');
    this.setPreviousStatement(true, null);
    this.setColour("#ff0066");
  }
};
Blockly.common.defineBlocks({Pass: Pass});

  
const Break = {
  init: function() {
    this.appendDummyInput()
      .appendField('break');
    this.setPreviousStatement(true, null);
    this.setColour("#ff0066");
  }
};
Blockly.common.defineBlocks({Break: Break});


const Continue = {
  init: function() {
    this.appendDummyInput()
      .appendField('continue');
    this.setPreviousStatement(true, null);
    this.setColour("#ff0066");
  }
};
Blockly.common.defineBlocks({Continue: Continue});


const AliasAs = {
  init: function() {
    this.appendValueInput('name');
    this.appendDummyInput('')
      .appendField('as');
    this.appendValueInput('alias');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(225);
  }
};
Blockly.common.defineBlocks({AliasAs: AliasAs});