import { setDuplicateOnDragStrategy } from "../../plugins/drag-strategy/drag-strategy.js";

const functionsColour = "#ff99aa";

const FunctionDef = {
	init: function() {
		this.appendDummyInput()
			.appendField("def")
			.appendField(new Blockly.FieldLabel(""), "name");
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
		this.setColour("#ff99aa");
		this.model = new ObservableProcedureModel(this.workspace, "");
		this.workspace.getProcedureMap().add(this.model);
	},

	destroy: function() {
		if (this.isInsertionMarker()) {
			return;
		}
		this.workspace.getProcedureMap().delete(this.model.getId());
	},

	doProcedureUpdate: function() {
		this.setFieldValue(this.model.getName(), "name");

		const args = this.model.getParameters();

    console.log(args);

		if (args.length > 0) {
			this.appendDummyInput()
				.appendField("(");	

			args.forEach((arg, index) => {
        index = index + 1;
        index = index.toString().padStart(6, '0');
				if (index > 1) {
					this.appendValueInput(`arg_${index}`)
						.appendField(",");
				}
				else {
					this.appendValueInput(`arg_${index}`);
				}
			});

			this.appendDummyInput()
				.appendField("):");	
		}
		else {
			this.appendDummyInput()
				.appendField("():");		
		}

		this.appendStatementInput("body");
	},

	saveExtraState(doFullSerialization) {
		const state = {
			"procedureId": this.model.getId()
		};

		if (doFullSerialization) {
			state["name"] = this.model.getName();
			state["args"] = this.model.getParameters().map((arg) => {
				return { name: arg.getName(), id: arg.getId() };
			});
			state["create_new_model"] = true;
		}
		
		return state;
	},

	loadExtraState(state) {
		const id = state["procedureId"];
		const map = this.workspace.getProcedureMap();
	
		if (map.has(id) && !state["create_new_model"]) {
			map.delete(this.model.getId());
			this.model = map.get(id);
			this.doProcedureUpdate();
			return;
		}

		this.model.setName(state["name"]);
		state["args"].forEach((arg) => {
			this.model.insertParameter(new ObservableParameterModel(this.workspace, arg["name"]));
		});
		this.doProcedureUpdate();
	}
};
Blockly.common.defineBlocks({FunctionDef: FunctionDef});

const Argument = {
	init: function() {
	  this.appendDummyInput()
			.appendField(new Blockly.FieldLabelSerializable(""), "name");
	  this.setInputsInline(true);
	  this.setOutput(true, null);
	  this.setColour("#ffa54c");
	  setDuplicateOnDragStrategy(this);
	}
};
Blockly.common.defineBlocks({Argument: Argument});
  
const Pass = {
    init: function() {
      this.appendDummyInput()
        .appendField('pass');
      this.setPreviousStatement(true, null);
      this.setColour(functionsColour);
    }
};
Blockly.common.defineBlocks({Pass: Pass});
  
const Return = {
  init: function() {
    this.appendDummyInput()
      .appendField('return');
    this.appendValueInput('value');
    this.setInputsInline(true)
    this.setPreviousStatement(true, null);
    this.setColour(functionsColour);
  }
};
Blockly.common.defineBlocks({Return: Return});
