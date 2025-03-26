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

const Compare = {
  init: function() {
    this.appendValueInput('left');
    this.appendDummyInput('')
      .appendField(new Blockly.FieldDropdown([
          ['==', 'Eq'],
          ['!=', 'NotEq'],
          ['<', 'Lt'],
          ['<=', 'LtE'],
          ['>', 'Gt'],
          ['>=', 'GtE'],
          ['in', 'In'],
          ['not in', 'NotIn'],
          ['is', 'Is'],
          ['is not', 'IsNot']
        ]), 'op');
    this.appendValueInput('right');
    this.setInputsInline(true)
    this.setOutput(true, "Compare");
    this.setColour(logicColor);
  }
};
Blockly.common.defineBlocks({Compare: Compare});

const IfExp = {
  init: function() {
    this.appendValueInput('body');
    this.appendDummyInput('')
      .appendField('if');
    this.appendValueInput('test');
    this.appendDummyInput('')
      .appendField('else');
    this.appendValueInput('orelse');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(logicColor);
  }
};
Blockly.common.defineBlocks({IfExp: IfExp});
