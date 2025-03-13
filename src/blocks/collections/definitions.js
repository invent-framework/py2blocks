// WORK IN PROGRESS

Blockly.Blocks["List"] = {
    init: function() {
        this.appendDummyInput("list_start")
            .appendField("[");
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
        if (this.getInput("list_end")) {
            this.removeInput("list_end");
        }
            
        while (this.itemCount < targetCount) {
            this.addItem();
        }
        while (this.itemCount > targetCount) {
            this.removeItem();
        }

        this.appendDummyInput("list_end")
            .appendField("]");

        this.updateControls();
    },

    addItem: function() {
        this.itemCount++;
        const count = this.itemCount.toString().padStart(6, '0');

        if (this.itemCount > 1) {
            this.appendValueInput(`input_${count}`)
                .appendField(",");
        }
        else {
            this.appendValueInput(`input_${count}`);
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
};