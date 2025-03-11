export class RenderInfo extends Blockly.zelos.RenderInfo {
	adjustXPosition_() {
		// Do nothing
	}

	getSpacerRowHeight_(prev, next) {
		if (next.hasStatement) {
			return 15;
		}
		if (this.topRow.hasPreviousConnection) {
			return 7;
		}
		return super.getSpacerRowHeight_(prev, next);
	}
}