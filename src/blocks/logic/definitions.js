const logicColor = "#98b8d8";

const bool = {
	init: function() {
	  this.appendDummyInput()
			.appendField(new Blockly.FieldDropdown([
				["True", "True"],
				["False", "False"]
		  ]), "value");
	  this.setInputsInline(true);
	  this.setOutput(true, "bool");
	  this.setColour(logicColor);
	}
};
Blockly.common.defineBlocks({bool: bool});


const BoolOp = {
    init: function() {
      this.appendValueInput('left');
      this.appendDummyInput('')
        .appendField(new Blockly.FieldDropdown([
            ['and', 'And'],
            ['or', 'Or']
          ]), 'op');
      this.appendValueInput('right');
      this.setInputsInline(true)
	    this.setOutput(true, "BoolOp");
      this.setColour(logicColor);
    }
  };
Blockly.common.defineBlocks({BoolOp: BoolOp});
  
const Not = {
  init: function() {
    this.appendDummyInput('')
      .appendField('not');
    this.appendValueInput('value');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(logicColor);
  }
};
Blockly.common.defineBlocks({Not: Not});