export function createIfBlock() {
    return {
        init: function() {
            this.appendValueInput('if')
                .appendField("if")

            this.appendDummyInput('if_colon')
                .appendField(":")
                .appendField(this.createPlusField(), 'plus');

            this.appendStatementInput('if_body');

            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setColour("#ff9966");
        },

        elseIfCount_: 0,
        hasElse_: false,

        saveExtraState: function() {
            if (!this.elseIfCount_ && !this.hasElse_) {
                return null;
            }
            const state = Object.create(null);
            if (this.elseIfCount_) {
              state['elseIfCount'] = this.elseIfCount_;
            }
            if (this.hasElse_) {
              state['hasElse'] = true;
            }
            return state;        
        },

        loadExtraState: function (state) {
            const targetCount = state['elseIfCount'] || 0;
            if (state['hasElse']) {
                this.addElse_();
            }
            this.updateShape_(targetCount);
        },        

        updateShape_: function (targetCount) {
            while (this.elseIfCount_ < targetCount) {
              this.addElseIf_();
            }
            while (this.elseIfCount_ > targetCount) {
              this.removeElseIf_();
            }
        },

        plus: function () {
            if (!this.hasElse_){
                this.addElse_();
            }
            else {
                this.addElseIf_();
            }
        },

        minus: function (index, isElse) {
            if (isElse) {
                this.removeElse_();
            }
            else {
                if (this.elseIfCount_ == 0) {
                    return;
                }      
                this.removeElseIf_(index);
            }
        },        

        addElseIf_: function () {
            this.elseIfCount_++;

            const count = this.elseIfCount_.toString().padStart(6, '0');

            this.appendValueInput(`elif_${count}`)
                .appendField("elif");

            this.appendDummyInput(`elif_${count}_colon`)
                .appendField(":")
                .appendField(this.createMinusField(this.elseIfCount_), `minus_${count}`);

            this.appendStatementInput(`elif_${count}_body`);

            if (this.getInput('else')) {
                this.moveInputBefore('else', null);
                this.moveInputBefore('else_body', null);
            }
        },

        removeElseIf_: function (index=undefined) {
            if (index !== undefined && index != this.elseIfCount_) {
                const elseIfIndex = index * 3;
                const inputs = this.inputList;

                // Elif Connection
                let connection = inputs[elseIfIndex].connection;
                if (connection.isConnected()) {
                    connection.disconnect();
                }

                // Elif Body Connection
                connection = inputs[elseIfIndex + 2].connection;
                if (connection.isConnected()) {
                    connection.disconnect();
                }

                this.bumpNeighbours();

                for (let i = elseIfIndex + 3, input; (input = this.inputList[i]); i++) {
                    if (input.name == 'else') {
                      break;
                    }
                    if (input.name.endsWith("body")){
                        const targetConnection = input.connection.targetConnection;
                        if (targetConnection) {
                          this.inputList[i - 3].connection.connect(targetConnection);
                        }
                    }
                }            
            }

            const count = this.elseIfCount_.toString().padStart(6, '0');
            this.removeInput(`elif_${count}`);
            this.removeInput(`elif_${count}_colon`);
            this.removeInput(`elif_${count}_body`);
            this.elseIfCount_--;
        },

        addElse_: function () {
            if (this.hasElse_) {
                return;
            }
            this.hasElse_ = true;

            this.appendDummyInput('else')
                .appendField("else:")
                .appendField(this.createMinusField(undefined, true), 'minus');

            this.appendStatementInput('else_body');
        },

        removeElse_: function () {
            if (!this.hasElse_) {
                return;
            }
            this.hasElse_ = false;
            this.removeInput('else');
            this.removeInput('else_body');
        },

        createPlusField: function() {
            const plus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTUuNDM3NSA4LjU2MjVWNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVINS40Mzc1VjQuNDM3NUM1LjQzNzUgNC4xMzI4MSA1LjY3MTg4IDMuODc1IDYgMy44NzVDNi4zMDQ2OSAzLjg3NSA2LjU2MjUgNC4xMzI4MSA2LjU2MjUgNC40Mzc1VjUuOTM3NUg4LjA2MjVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDYuNTYyNVY4LjU2MjVDNi41NjI1IDguODkwNjIgNi4zMDQ2OSA5LjEyNSA2IDkuMTI1QzUuNjcxODggOS4xMjUgNS40Mzc1IDguODkwNjIgNS40Mzc1IDguNTYyNVpNMTIgNi41QzEyIDkuODI4MTIgOS4zMDQ2OSAxMi41IDYgMTIuNUMyLjY3MTg4IDEyLjUgMCA5LjgyODEyIDAgNi41QzAgMy4xOTUzMSAyLjY3MTg4IDAuNSA2IDAuNUM5LjMwNDY5IDAuNSAxMiAzLjE5NTMxIDEyIDYuNVpNNiAxLjYyNUMzLjMwNDY5IDEuNjI1IDEuMTI1IDMuODI4MTIgMS4xMjUgNi41QzEuMTI1IDkuMTk1MzEgMy4zMDQ2OSAxMS4zNzUgNiAxMS4zNzVDOC42NzE4OCAxMS4zNzUgMTAuODc1IDkuMTk1MzEgMTAuODc1IDYuNUMxMC44NzUgMy44MjgxMiA4LjY3MTg4IDEuNjI1IDYgMS42MjVaIiBmaWxsPSJibGFjayIvPgo8L3N2Zz4K",
                20, 
                20, 
                undefined, 
                () => {
                    this.plus();
                }
            );
            return plus;
        },
    
        createMinusField: function(index, isElse=false) {
            const minus = new Blockly.FieldImage(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTguMDYyNSA1LjkzNzVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVIOC4wNjI1Wk0xMiA2LjVDMTIgOS44MjgxMiA5LjMwNDY5IDEyLjUgNiAxMi41QzIuNjcxODggMTIuNSAwIDkuODI4MTIgMCA2LjVDMCAzLjE5NTMxIDIuNjcxODggMC41IDYgMC41QzkuMzA0NjkgMC41IDEyIDMuMTk1MzEgMTIgNi41Wk02IDEuNjI1QzMuMzA0NjkgMS42MjUgMS4xMjUgMy44MjgxMiAxLjEyNSA2LjVDMS4xMjUgOS4xOTUzMSAzLjMwNDY5IDExLjM3NSA2IDExLjM3NUM4LjY3MTg4IDExLjM3NSAxMC44NzUgOS4xOTUzMSAxMC44NzUgNi41QzEwLjg3NSAzLjgyODEyIDguNjcxODggMS42MjUgNiAxLjYyNVoiIGZpbGw9ImJsYWNrIi8+Cjwvc3ZnPgo=",
                20, 
                20, 
                undefined, 
                () => {
                    this.minus(index, isElse);
                }
            );
            return minus;
        },
    }
}

export function createWithBlock() {
    return {
        init: function() {
            this.appendDummyInput()
                .appendField("with");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
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
            if (this.getInput("with_colon") && this.getInput("body")) {
                this.removeInput("with_colon");
                this.removeInput("body");
            }
                
            while (this.itemCount < targetCount) {
                this.addItem();
            }
            while (this.itemCount > targetCount) {
                this.removeItem();
            }

            this.updateControls();
    
            this.appendDummyInput("with_colon")
                .appendField(":")

            this.appendStatementInput("body");
    
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
        },

        add_default_block: function(input) {
            const block = this.workspace.newBlock(default_block);
            block.initSvg();
            block.render();
            input.connection.connect(block.outputConnection);
        },
    };
}