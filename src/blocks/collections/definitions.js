import { createCollectionBlock } from "../../plugins/collections.js";

const collectionsColor = "#ff9966";

Blockly.Blocks["List"] = createCollectionBlock("[", "]");
Blockly.Blocks["Tuple"] = createCollectionBlock("(", ")");
Blockly.Blocks["Set"] = createCollectionBlock("{", "}");
Blockly.Blocks["Dict"] = createCollectionBlock("{", "}", true);
Blockly.Blocks["Delete"] = createCollectionBlock("del", "");

const dict_item = {
    init: function() {
        this.appendValueInput("key");
        this.appendDummyInput()
            .appendField(":");
        this.appendValueInput("value");
        this.setInputsInline(true);
        this.setOutput(true, "dict_item");
        this.setColour(collectionsColor);
    }
}
Blockly.common.defineBlocks({dict_item: dict_item});

const dict_unpack = {
    init: function() {
      this.appendDummyInput()
        .appendField('**');
      this.appendValueInput('value');
      this.setInputsInline(true)
      this.setOutput(true, "dict_unpack");
      this.setColour(collectionsColor);
    }
};
Blockly.common.defineBlocks({dict_unpack: dict_unpack});

const list_unpack = {
    init: function() {
      this.appendDummyInput()
        .appendField('*');
      this.appendValueInput('value');
      this.setInputsInline(true)
      this.setOutput(true, "list_unpack");
      this.setColour(collectionsColor);
    }
};
Blockly.common.defineBlocks({list_unpack: list_unpack});
  
const Subscript = {
  init: function() {
    this.appendValueInput('value');
    this.appendDummyInput('')
      .appendField('[');
    this.appendValueInput('slice');
    this.appendDummyInput('')
      .appendField(']');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(collectionsColor);
  }
};
Blockly.common.defineBlocks({Subscript: Subscript});

const Slice = {
  init: function() {
    this.appendValueInput('lower');
    this.appendDummyInput('')
      .appendField(':');
    this.appendValueInput('upper');
    this.appendDummyInput('')
      .appendField(',');
    this.appendValueInput('step');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(collectionsColor);
  }
};
Blockly.common.defineBlocks({Slice: Slice});

