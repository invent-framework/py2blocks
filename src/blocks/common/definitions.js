import { FieldString } from "../../fields/field_string.js";

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
