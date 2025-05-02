const loopsColor = "#98b8d8";

const For = {
  init: function() {
    this.appendValueInput('target')
      .appendField('for');
    this.appendValueInput('iter')
      .appendField('in');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({For: For});

const ForElse = {
  init: function() {
    this.appendValueInput('target')
      .appendField('for');
    this.appendValueInput('iter')
      .appendField('in');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.appendDummyInput('')
      .appendField('else:');
    this.appendStatementInput('else_body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({ForElse: ForElse});


const AsyncFor = {
  init: function() {
    this.appendValueInput('target')
      .appendField('async for');
    this.appendValueInput('iter')
      .appendField('in');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({AsyncFor: AsyncFor});

const AsyncForElse = {
  init: function() {
    this.appendValueInput('target')
      .appendField('async for');
    this.appendValueInput('iter')
      .appendField('in');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.appendDummyInput('')
      .appendField('else:');
    this.appendStatementInput('else_body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({AsyncForElse: AsyncForElse});

const While = {
  init: function() {
    this.appendValueInput('test')
      .appendField('while');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({While: While});

const WhileElse = {
  init: function() {
    this.appendValueInput('test')
      .appendField('while');
    this.appendDummyInput()
      .appendField(':');
    this.appendStatementInput('body');
    this.appendDummyInput('')
      .appendField('else:');
    this.appendStatementInput('else_body');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};
Blockly.common.defineBlocks({WhileElse: WhileElse});

                    