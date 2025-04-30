export function createTryBlock(hasElse=false, hasFinally=false) {
    return {
        init: function() {
            this.appendDummyInput('try')
                .appendField("try:")
                .appendField(this.createPlusField(), 'plus');

            this.appendStatementInput('body');

            if (hasElse) {
                this.appendDummyInput('else')
                    .appendField("else:")
                
                this.appendStatementInput('else_body');
            }

            if (hasFinally) {
                this.appendDummyInput('finally')
                    .appendField("finally:")
                
                this.appendStatementInput('finally_body');
            }
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setColour("#ff9966");
        },

        handlerCount_: 0,

        saveExtraState: function() {
            if (!this.handlerCount_) {
                return null;
            }
            const state = Object.create(null);
            if (this.handlerCount_) {
              state['handlerCount'] = this.handlerCount_;
            }
            return state;        
        },

        loadExtraState: function (state) {
            const targetCount = state['handlerCount'] || 0;
            this.updateShape_(targetCount);
        },        

        updateShape_: function (targetCount) {
            while (this.handlerCount_ < targetCount) {
              this.addException_();
            }
            while (this.handlerCount_ > targetCount) {
              this.removeException_();
            }
        },

        plus: function () {
            this.addException_();
        },

        minus: function (index) {
            this.removeException_(index);
        },        

        addException_: function () {
            this.handlerCount_++;

            const count = this.handlerCount_.toString().padStart(6, '0');

            this.appendValueInput(`handler_${count}`)
                .appendField("except");
            
            if (this.handlerCount_ > 1) {
                this.appendDummyInput(`handler_${count}_colon`)
                    .appendField(":")
                    .appendField(this.createMinusField(this.handlerCount_), `minus_${count}`);
            }
            else {
                this.appendDummyInput(`handler_${count}_colon`)
                    .appendField(":")
            }

            this.appendStatementInput(`handler_${count}_body`);


            if (this.getInput('else')) {
                this.moveInputBefore('else', null);
                this.moveInputBefore('else_body', null);
            }

            if (this.getInput('finally')) {
                this.moveInputBefore('finally', null);
                this.moveInputBefore('finally_body', null);
            }
        },

        removeException_: function (index=undefined) {
            if (index !== undefined && index != this.handlerCount_) {
                const handlerIndex = index * 2;
                const inputs = this.inputList;

                // Handler Connection
                let connection = inputs[handlerIndex].connection;
                if (connection.isConnected()) {
                    connection.disconnect();
                }

                // Handler Body Connection
                connection = inputs[handlerIndex + 2].connection;
                if (connection.isConnected()) {
                    connection.disconnect();
                }

                this.bumpNeighbours();

                for (let i = handlerIndex + 3, input; (input = this.inputList[i]); i++) {
                    if (input.name.endsWith("body")){
                        const targetConnection = input.connection.targetConnection;
                        if (targetConnection) {
                          this.inputList[i - 3].connection.connect(targetConnection);
                        }
                    }
                }            
            }

            const count = this.handlerCount_.toString().padStart(6, '0');
            this.removeInput(`handler_${count}`);
            this.removeInput(`handler_${count}_colon`);
            this.removeInput(`handler_${count}_body`);
            this.handlerCount_--;
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