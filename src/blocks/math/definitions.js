const mathColour = "#97a2d8";

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
          ['-', 'Sub'],
          ['*', 'Mult'],
          ['/', 'Div'],
          ['//', 'FloorDiv'],
          ['%', 'Mod'],
          ['**', 'Pow'],
          ['<<', 'LShift'],
          ['>>', 'RShift'],
          ['&', 'BitAnd'],
          ['|', 'BitOr'],
          ['^', 'BitXor'],
          ['@', 'MatMult']
        ]), 'op');
    this.appendValueInput('right');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(mathColour);
  }
};
Blockly.common.defineBlocks({BinOp: BinOp});

const UnaryOp = {
  init: function() {
    this.appendDummyInput()
      .appendField(new Blockly.FieldDropdown([
          ['+', 'UAdd'],
          ['-', 'USub'],
          ['~', 'UInvert']
        ]), 'op');
    this.appendValueInput('value');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(mathColour);
  }
};
Blockly.common.defineBlocks({UnaryOp: UnaryOp});