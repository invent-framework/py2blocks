import { createCollectionBlock } from "../../plugins/collections.js";

Blockly.Blocks["List"] = createCollectionBlock("[", "]");
Blockly.Blocks["Tuple"] = createCollectionBlock("(", ")");
Blockly.Blocks["Set"] = createCollectionBlock("{", "}");
Blockly.Blocks["Dict"] = createCollectionBlock("{", "}", true);

Blockly.Blocks["dict_item"] = {
    init: function() {
        this.appendValueInput("key");
        this.appendDummyInput()
            .appendField(":");
        this.appendValueInput("value");
        this.setInputsInline(true);
        this.setOutput(true, "dict_item");
        this.setColour("#ff9966");
    }
}