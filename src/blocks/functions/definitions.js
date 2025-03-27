import { setDuplicateOnDragStrategy } from "../../plugins/drag-strategy/drag-strategy.js";

const functionsColor = "#ff99aa";

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

// TODO: Add support for inline function definitions & predefined procedure models
const Call = {
	init: function() {
		this.appendDummyInput()
			.appendField(new Blockly.FieldLabel(""), "name");
		this.setColour(functionsColor);
		this.setInputsInline(true);
		this.setPreviousStatement(true, null);
		this.setNextStatement(true, null);
	},
	saveExtraState() {
		return {
			"name": this.name,
			"args": this.argsCount,
			"kwargs": this.kwargsCount
		};	
	},
	loadExtraState(state) {
		if (state.name) {
			this.name = state.name;
			this.setFieldValue(this.name, "name");
			this.argsCount = state.args;
			this.kwargsCount = state.kwargs;
			this.doProcedureUpdate();
		}
	},
	doProcedureUpdate: function() {		
		if (this.argsCount || this.kwargsCount) {
			this.appendDummyInput()
				.appendField("(");

			for (let i = 0; i < this.argsCount; i++) {
				let index = i + 1;
				index = index.toString().padStart(6, '0');
				if (index > 1) {
					this.appendValueInput(`arg_${index}`)
						.appendField(",");
				}
				else {
					this.appendValueInput(`arg_${index}`);
				}
			}

			if (this.argsCount > 0 && this.kwargsCount > 0) {
				this.appendDummyInput()
					.appendField(",");
			}

			for (let i = 0; i < this.kwargsCount; i++) {
				let index = i + 1;
				index = index.toString().padStart(6, '0');
				if (index > 1) {
					this.appendValueInput(`kwarg_${index}`)
						.appendField(",");
				}
				else {
					this.appendValueInput(`kwarg_${index}`);
				}
			}

			this.appendDummyInput()
				.appendField(")");
		}
		else {
			this.appendDummyInput()
				.appendField("()");
		}
	}
};
Blockly.common.defineBlocks({Call: Call});

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
      this.setColour(functionsColor);
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
    this.setColour(functionsColor);
  }
};
Blockly.common.defineBlocks({Return: Return});

const keyword = {
	init: function() {
	  this.appendDummyInput()
		.appendField(new Blockly.FieldLabelSerializable(''), 'arg')
		.appendField('=');
	  this.appendValueInput('value');
	  this.setInputsInline(true)
	  this.setOutput(true, null);
	  this.setColour(functionsColor);
	}
};
Blockly.common.defineBlocks({keyword: keyword});  

const Attribute = {
	init: function() {
	  this.appendValueInput('value');
	  this.appendDummyInput('')
		.appendField('.')
		.appendField(new Blockly.FieldTextInput(''), 'attr');
	  this.setInputsInline(true)
	  this.setOutput(true, null);
	  this.setColour(functionsColor);
	}
};
Blockly.common.defineBlocks({Attribute: Attribute});
  