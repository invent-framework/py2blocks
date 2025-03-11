/**
 * Portions of this code are derived from the Apache 2.0 licenced Makecode, a project of Microsoft.
 * https://github.com/microsoft/pxt
 */

export const DUPLICATE_ON_DRAG_MUTATION_KEY = "duplicateondrag";

let draggableShadowAllowlist;
let duplicateRefs;

export function setDraggableShadowBlocks(ids) {
	draggableShadowAllowlist = ids;
}

/**
 * Configures duplicate on drag for a block's child inputs
 *
 * @param parentBlockType The type of the parent block
 * @param inputName The value input to duplicate blocks on when dragged. If not
 * specified, all child value inputs will be duplicated
 * @param childBlockType The type of the child block to be duplicated. If not specified,
 * any block attached to the input will be duplicated on drag
 * regardless of type
 */
export function setDuplicateOnDrag(parentBlockType, inputName, childBlockType) {
	if (!duplicateRefs) {
		duplicateRefs = [];
	}

	const existing = duplicateRefs.some((ref) => {
		return ref.parentBlockType === parentBlockType && ref.inputName === inputName && ref.childBlockType === childBlockType;
	});
	if (existing) {
		return;
	}

	duplicateRefs.push({
		parentBlockType,
		inputName,
		childBlockType
	});
}

export function isAllowlistedShadow(block) {
	return true;
}

export function shouldDuplicateOnDrag(block) {
	if (block.isShadow()) {
        return true;
    }
	return false;
}