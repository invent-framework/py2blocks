export function createCollectionBlock(open_with, close_with, has_key_value=false) {
    return {
        init: function() {
            this.appendDummyInput("open_with")
                .appendField(open_with);
            this.setOutput(true, "value");
            this.setInputsInline(true);
            this.setColour("#ff9966");
        },
    
        saveExtraState: function() {
            return {
                items: this.itemCount,
            }
        },
    
        loadExtraState: function(state) {
            const targetCount = parseInt(state.items);
            this.itemCount = 0;
    
            this.updateShape(targetCount);
        },
    
        updateShape: function(targetCount) {
            if (this.getInput("close_with")) {
                this.removeInput("close_with");
            }
                
            while (this.itemCount < targetCount) {
                this.addItem();
            }
            while (this.itemCount > targetCount) {
                this.removeItem();
            }
    
            this.appendDummyInput("close_with")
                .appendField(close_with);
    
            this.updateControls();
        },
    
        addItem: function() {
            this.itemCount++;
            const count = this.itemCount.toString().padStart(6, '0');
    
            let input;
            if (this.itemCount > 1) {
                input = this.appendValueInput(`input_${count}`)
                    .appendField(",");
            }
            else {
                input = this.appendValueInput(`input_${count}`);
            }

            if (has_key_value) {
                input.connection.setCheck(["dict_item", "dict_unpack"]);
            }
        },
    
        removeItem: function() {
            const count = this.itemCount.toString().padStart(6, '0');
            this.removeInput(`input_${count}`);
            this.itemCount--;
        },
    
        createPlusField: function() {
            const plus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTUuNDM3NSA4LjU2MjVWNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVINS40Mzc1VjQuNDM3NUM1LjQzNzUgNC4xMzI4MSA1LjY3MTg4IDMuODc1IDYgMy44NzVDNi4zMDQ2OSAzLjg3NSA2LjU2MjUgNC4xMzI4MSA2LjU2MjUgNC40Mzc1VjUuOTM3NUg4LjA2MjVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDYuNTYyNVY4LjU2MjVDNi41NjI1IDguODkwNjIgNi4zMDQ2OSA5LjEyNSA2IDkuMTI1QzUuNjcxODggOS4xMjUgNS40Mzc1IDguODkwNjIgNS40Mzc1IDguNTYyNVpNMTIgNi41QzEyIDkuODI4MTIgOS4zMDQ2OSAxMi41IDYgMTIuNUMyLjY3MTg4IDEyLjUgMCA5LjgyODEyIDAgNi41QzAgMy4xOTUzMSAyLjY3MTg4IDAuNSA2IDAuNUM5LjMwNDY5IDAuNSAxMiAzLjE5NTMxIDEyIDYuNVpNNiAxLjYyNUMzLjMwNDY5IDEuNjI1IDEuMTI1IDMuODI4MTIgMS4xMjUgNi41QzEuMTI1IDkuMTk1MzEgMy4zMDQ2OSAxMS4zNzUgNiAxMS4zNzVDOC42NzE4OCAxMS4zNzUgMTAuODc1IDkuMTk1MzEgMTAuODc1IDYuNUMxMC44NzUgMy44MjgxMiA4LjY3MTg4IDEuNjI1IDYgMS42MjVaIiBmaWxsPSJibGFjayIvPgo8L3N2Zz4K",
                20, 
                20, 
                undefined, 
                () => {
                    this.updateShape(this.itemCount + 1);

                    if (has_key_value) {
                        const count = this.itemCount.toString().padStart(6, '0');
                        const input = this.getInput(`input_${count}`);
                        this.add_key_value(input);
                    }
                }
            );
            return plus;
        },
    
        createMinusField: function() {
            const minus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTguMDYyNSA1LjkzNzVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVIOC4wNjI1Wk0xMiA2LjVDMTIgOS44MjgxMiA5LjMwNDY5IDEyLjUgNiAxMi41QzIuNjcxODggMTIuNSAwIDkuODI4MTIgMCA2LjVDMCAzLjE5NTMxIDIuNjcxODggMC41IDYgMC41QzkuMzA0NjkgMC41IDEyIDMuMTk1MzEgMTIgNi41Wk02IDEuNjI1QzMuMzA0NjkgMS42MjUgMS4xMjUgMy44MjgxMiAxLjEyNSA2LjVDMS4xMjUgOS4xOTUzMSAzLjMwNDY5IDExLjM3NSA2IDExLjM3NUM4LjY3MTg4IDExLjM3NSAxMC44NzUgOS4xOTUzMSAxMC44NzUgNi41QzEwLjg3NSAzLjgyODEyIDguNjcxODggMS42MjUgNiAxLjYyNVoiIGZpbGw9ImJsYWNrIi8+Cjwvc3ZnPgo=",
                20, 
                20, 
                undefined, 
                () => {
                    this.updateShape(this.itemCount - 1);
                }
            );
            return minus;
        },
    
        updateControls: function() {
            if (this.getInput("controls")){
                this.removeInput("controls");
            }
    
            const controls = this.appendDummyInput("controls");
            controls.appendField(this.createPlusField());
            if (this.itemCount > 1) {
                controls.appendField(this.createMinusField());
            }
        },

        add_key_value: function(input) {
            const block = this.workspace.newBlock("dict_item");
            block.initSvg();
            block.render();
            input.connection.connect(block.outputConnection);
        },
    };
}

export function createComprehensionBlock(open_with, close_with, has_if=false) {
    return {
        init: function() {
            this.appendDummyInput("open_with")
                .appendField(open_with);
            this.appendValueInput("elt");
            this.setOutput(true, "value");
            this.setInputsInline(true);
            this.setColour("#ff9966");
        },

        saveExtraState: function() {
            return {
                items: this.itemCount,
            }
        },

        loadExtraState: function(state) {
            const targetCount = parseInt(state.items);
            this.itemCount = 0;

            this.updateShape(targetCount);
        },

        updateShape: function(targetCount) {
            if (this.getInput("close_with")) {
                this.removeInput("close_with");
            }

            while (this.itemCount < targetCount) {
                this.addItem();
            }
            while (this.itemCount > targetCount) {
                this.removeItem();
            }

            this.appendDummyInput("close_with")
                .appendField(close_with);

            this.updateControls();
        },

        addItem: function() {
            this.itemCount++;
            const count = this.itemCount.toString().padStart(6, '0');

            this.appendValueInput(`target_${count}`)
                .appendField("for");
            this.appendValueInput(`iter_${count}`)
                .appendField("in");
            if (has_if) {
                this.appendValueInput(`if_${count}`)
                    .appendField("if");
            }
        },

        removeItem: function() {
            const count = this.itemCount.toString().padStart(6, '0');
            this.removeInput(`target_${count}`);
            this.removeInput(`iter_${count}`);
            if (has_if) {
                this.removeInput(`if_${count}`);
            }
            this.itemCount--;
        },

        updateControls: function() {
            if (this.getInput("controls")){
                this.removeInput("controls");
            }

            const controls = this.appendDummyInput("controls");
            controls.appendField(this.createPlusField());
            if (this.itemCount > 1) {
                controls.appendField(this.createMinusField());
            }
        },

        createPlusField: function() {
            const plus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTUuNDM3NSA4LjU2MjVWNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVINS40Mzc1VjQuNDM3NUM1LjQzNzUgNC4xMzI4MSA1LjY3MTg4IDMuODc1IDYgMy44NzVDNi4zMDQ2OSAzLjg3NSA2LjU2MjUgNC4xMzI4MSA2LjU2MjUgNC40Mzc1VjUuOTM3NUg4LjA2MjVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDYuNTYyNVY4LjU2MjVDNi41NjI1IDguODkwNjIgNi4zMDQ2OSA5LjEyNSA2IDkuMTI1QzUuNjcxODggOS4xMjUgNS40Mzc1IDguODkwNjIgNS40Mzc1IDguNTYyNVpNMTIgNi41QzEyIDkuODI4MTIgOS4zMDQ2OSAxMi41IDYgMTIuNUMyLjY3MTg4IDEyLjUgMCA5LjgyODEyIDAgNi41QzAgMy4xOTUzMSAyLjY3MTg4IDAuNSA2IDAuNUM5LjMwNDY5IDAuNSAxMiAzLjE5NTMxIDEyIDYuNVpNNiAxLjYyNUMzLjMwNDY5IDEuNjI1IDEuMTI1IDMuODI4MTIgMS4xMjUgNi41QzEuMTI1IDkuMTk1MzEgMy4zMDQ2OSAxMS4zNzUgNiAxMS4zNzVDOC42NzE4OCAxMS4zNzUgMTAuODc1IDkuMTk1MzEgMTAuODc1IDYuNUMxMC44NzUgMy44MjgxMiA4LjY3MTg4IDEuNjI1IDYgMS42MjVaIiBmaWxsPSJibGFjayIvPgo8L3N2Zz4K",
                20, 
                20, 
                undefined, 
                () => {
                    this.updateShape(this.itemCount + 1);
                }
            );
            return plus;
        },
    
        createMinusField: function() {
            const minus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTguMDYyNSA1LjkzNzVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVIOC4wNjI1Wk0xMiA2LjVDMTIgOS44MjgxMiA5LjMwNDY5IDEyLjUgNiAxMi41QzIuNjcxODggMTIuNSAwIDkuODI4MTIgMCA2LjVDMCAzLjE5NTMxIDIuNjcxODggMC41IDYgMC41QzkuMzA0NjkgMC41IDEyIDMuMTk1MzEgMTIgNi41Wk02IDEuNjI1QzMuMzA0NjkgMS42MjUgMS4xMjUgMy44MjgxMiAxLjEyNSA2LjVDMS4xMjUgOS4xOTUzMSAzLjMwNDY5IDExLjM3NSA2IDExLjM3NUM4LjY3MTg4IDExLjM3NSAxMC44NzUgOS4xOTUzMSAxMC44NzUgNi41QzEwLjg3NSAzLjgyODEyIDguNjcxODggMS42MjUgNiAxLjYyNVoiIGZpbGw9ImJsYWNrIi8+Cjwvc3ZnPgo=",
                20, 
                20, 
                undefined, 
                () => {
                    this.updateShape(this.itemCount - 1);
                }
            );
            return minus;
        },

        updateControls: function() {
            if (this.getInput("controls")){
                this.removeInput("controls");
            }
            const controls = this.appendDummyInput("controls");
            controls.appendField(this.createPlusField());
            if (this.itemCount > 1) {
                controls.appendField(this.createMinusField());
            }
        }
    }
}