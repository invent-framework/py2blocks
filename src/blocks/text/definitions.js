import { FieldString } from "../../fields/field_string.js";

const textColor = "#ccb3ff";

const str = {
  init: function() {
    this.appendDummyInput()
      .appendField(new FieldString(""), "value");
    this.setInputsInline(true)
    this.setOutput(true, "str");
    this.setColour("#ffffff");
  }
};
Blockly.common.defineBlocks({str: str});

const print_block = {
    init: function() {
      this.appendDummyInput('')
        .appendField('print(');
      this.appendValueInput('ARG0');
      this.appendDummyInput('')
        .appendField(')');
      this.setInputsInline(true)
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(textColor);
    }
};
Blockly.common.defineBlocks({print_block: print_block});
  