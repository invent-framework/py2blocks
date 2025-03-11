/**
 * Portions of this code are derived from the Apache 2.0 licenced Makecode, a project of Microsoft.
 * https://github.com/microsoft/pxt
 */

import { DUPLICATE_ON_DRAG_MUTATION_KEY, isAllowlistedShadow, shouldDuplicateOnDrag } from "./duplicate-on-drag.js";

const eventUtils = Blockly.Events;
const Coordinate = Blockly.utils.Coordinate;
const dom = Blockly.utils.dom;

const BLOCK_LAYER = 50; // not exported by blockly

export class DuplicateOnDragStrategy {
	constructor(block) {
		this.block = block;
		this.workspace = block.workspace;
		this.startParentConn = null;
		this.startChildConn = null;
		this.startLoc = null;
		this.connectionCandidate = null;
		this.connectionPreviewer = null;
		this.dragging = false;
		this.dragOffset = new Coordinate(0, 0);
	}

	/** Returns true if the block is currently movable. False otherwise. */
	isMovable() {
		if (this.block.isShadow()) {
			return this.block.getParent()?.isMovable() ?? false;
		}

		return (
			this.block.isOwnMovable() &&
            !this.block.isDeadOrDying() &&
            !this.workspace.options.readOnly &&
            // We never drag blocks in the flyout, only create new blocks that are
            // dragged.
            !this.block.isInFlyout
		);
	}

	/**
	 * Handles any setup for starting the drag, including disconnecting the block
	 * from any parent blocks.
	 */
	startDrag(e) {
		if (this.block.isShadow() && !isAllowlistedShadow(this.block)) {
			this.startDraggingShadow(e);
			return;
		}

		this.dragging = true;
		if (!eventUtils.getGroup()) {
			eventUtils.setGroup(true);
		}
		this.fireDragStartEvent();

		this.startLoc = this.block.getRelativeToSurfaceXY();

		const previewerConstructor = Blockly.registry.getClassFromOptions(
			Blockly.registry.Type.CONNECTION_PREVIEWER,
			this.workspace.options,
		);
		this.connectionPreviewer = new previewerConstructor(this.block);

		// During a drag there may be a lot of rerenders, but not field changes.
		// Turn the cache on so we don't do spurious remeasures during the drag.
		dom.startTextWidthCache();
		this.workspace.setResizesEnabled(false);
		Blockly.blockAnimations.disconnectUiStop();

		const healStack = Boolean(e) && (e.altKey || e.ctrlKey || e.metaKey);

		if (this.shouldDisconnect(healStack)) {
			this.disconnectBlock(healStack);
		}
		this.block.setDragging(true);
		this.workspace.getLayerManager()?.moveToDragLayer(this.block);
	}

	/** Starts a drag on a shadow, recording the drag offset. */
	startDraggingShadow(e) {
		const parent = this.block.getParent();
		if (!parent) {
			throw new Error(
				"Tried to drag a shadow block with no parent. " +
                "Shadow blocks should always have parents.",
			);
		}
		this.dragOffset = Coordinate.difference(
			parent.getRelativeToSurfaceXY(),
			this.block.getRelativeToSurfaceXY(),
		);
		parent.startDrag(e);
	}

	/**
	 * Whether or not we should disconnect the block when a drag is started.
	 */
	shouldDisconnect(healStack) {
		return Boolean(this.block.getParent() ||
            (healStack &&
                this.block.nextConnection &&
                this.block.nextConnection.targetBlock()));
	}

	/**
	 * Disconnects the block from any parents. If `healStack` is true and this is
	 * a stack block, we also disconnect from any next blocks and attempt to
	 * attach them to any parent.
	 */
	disconnectBlock(healStack) {
		let clone;
		let target;
		let xml;
		const isShadow = this.block.isShadow();

		if (isShadow) {
			this.block.setShadow(false);
		}

		const mutation = this.block.mutationToDom?.();

		if (shouldDuplicateOnDrag(this.block)) {
			const output = this.block.outputConnection;

			if (!output?.targetConnection) {
				return;
			}

			xml = Blockly.Xml.blockToDom(this.block, true);

			if (!isShadow) {
				clone = Blockly.Xml.domToBlock(xml, this.block.workspace);
			}
			target = output.targetConnection;
		}

		this.startParentConn =
            this.block.outputConnection?.targetConnection ??
            this.block.previousConnection?.targetConnection;
		if (healStack) {
			this.startChildConn = this.block.nextConnection?.targetConnection;
		}

		if (target && isShadow) {
			target.setShadowDom(xml);
		}

		this.block.unplug(healStack);
		Blockly.blockAnimations.disconnectUiEffect(this.block);

		if (target && clone) {
			target.connect(clone.outputConnection);

			mutation.setAttribute(DUPLICATE_ON_DRAG_MUTATION_KEY, "false");
			this.block.domToMutation?.(mutation);
		}
	}

	/** Fire a UI event at the start of a block drag. */
	fireDragStartEvent() {
		const event = new (eventUtils.get(eventUtils.BLOCK_DRAG))(
			this.block,
			true,
			this.block.getDescendants(false),
		);
		eventUtils.fire(event);
	}

	/** Fire a UI event at the end of a block drag. */
	fireDragEndEvent() {
		const event = new (eventUtils.get(eventUtils.BLOCK_DRAG))(
			this.block,
			false,
			this.block.getDescendants(false),
		);
		eventUtils.fire(event);
	}

	/** Fire a move event at the end of a block drag. */
	fireMoveEvent() {
		if (this.block.isDeadOrDying()) {
			return;
		}
		const event = new (eventUtils.get(eventUtils.BLOCK_MOVE))(
			this.block,
		);
		event.setReason(["drag"]);
		event.oldCoordinate = this.startLoc;
		event.recordNew();
		eventUtils.fire(event);
	}

	/** Moves the block and updates any connection previews. */
	drag(newLoc) {
		if (this.block.isShadow()) {
			this.block.getParent()?.drag(Coordinate.sum(newLoc, this.dragOffset));
			return;
		}

		this.block.moveDuringDrag(newLoc);
		this.updateConnectionPreview(
			this.block,
			Coordinate.difference(newLoc, this.startLoc),
		);
	}

	/**
	 * Update the connection preview based on the dragging position.
	 */
	updateConnectionPreview(draggingBlock, delta) {
		const currCandidate = this.connectionCandidate;
		const newCandidate = this.getConnectionCandidate(draggingBlock, delta);
		if (!newCandidate) {
			this.connectionPreviewer.hidePreview();
			this.connectionCandidate = null;
			return;
		}
		const candidate =
            currCandidate &&
                this.currCandidateIsBetter(currCandidate, delta, newCandidate)
            	? currCandidate
            	: newCandidate;
		this.connectionCandidate = candidate;

		const { local, neighbour } = candidate;
		const localIsOutputOrPrevious =
            local.type === Blockly.ConnectionType.OUTPUT_VALUE ||
            local.type === Blockly.ConnectionType.PREVIOUS_STATEMENT;
		const neighbourIsConnectedToRealBlock =
            neighbour.isConnected() && !neighbour.targetBlock().isInsertionMarker();
		if (
			localIsOutputOrPrevious &&
            neighbourIsConnectedToRealBlock &&
            !this.orphanCanConnectAtEnd(
            	draggingBlock,
            	neighbour.targetBlock(),
            	local.type,
            )
		) {
			this.connectionPreviewer.previewReplacement(
				local,
				neighbour,
				neighbour.targetBlock(),
			);
			return;
		}
		this.connectionPreviewer.previewConnection(local, neighbour);
	}

	/**
	 * Returns true if the given orphan block can connect at the end of the
	 * top block's stack or row, false otherwise.
	 */
	orphanCanConnectAtEnd(
		topBlock,
		orphanBlock,
		localType
	) {
		const orphanConnection =
            localType === Blockly.ConnectionType.OUTPUT_VALUE
            	? orphanBlock.outputConnection
            	: orphanBlock.previousConnection;
		return Boolean(Blockly.Connection.getConnectionForOrphanedConnection(
			topBlock,
			orphanConnection,
		));
	}

	/**
	 * Returns true if the current candidate is better than the new candidate.
	 *
	 * We slightly prefer the current candidate even if it is farther away.
	 */
	currCandidateIsBetter(
		currCandiate,
		delta,
		newCandidate
	) {
		const { local: currLocal, neighbour: currNeighbour } = currCandiate;
		const localPos = new Coordinate(currLocal.x, currLocal.y);
		const neighbourPos = new Coordinate(currNeighbour.x, currNeighbour.y);
		const currDistance = Coordinate.distance(
			Coordinate.sum(localPos, delta),
			neighbourPos,
		);
		return (
			newCandidate.distance > currDistance - Blockly.config.currentConnectionPreference
		);
	}

	/**
	 * Returns the closest valid candidate connection, if one can be found.
	 *
	 * Valid neighbour connections are within the configured start radius, with a
	 * compatible type (input, output, etc) and connection check.
	 */
	getConnectionCandidate(
		draggingBlock,
		delta
	) {
		const localConns = this.getLocalConnections(draggingBlock);
		let radius = this.connectionCandidate
			? Blockly.config.connectingSnapRadius
			: Blockly.config.snapRadius;
		let candidate = null;

		for (const conn of localConns) {
			const { connection: neighbour, radius: rad } = conn.closest(radius, delta);
			if (neighbour) {
				candidate = {
					local: conn,
					neighbour: neighbour,
					distance: rad,
				};
				radius = rad;
			}
		}

		return candidate;
	}

	/**
	 * Returns all of the connections we might connect to blocks on the workspace.
	 *
	 * Includes any connections on the dragging block, and any last next
	 * connection on the stack (if one exists).
	 */
	getLocalConnections(draggingBlock) {
		const available = draggingBlock.getConnections_(false);
		const lastOnStack = draggingBlock.lastConnectionInStack(true);
		if (lastOnStack && lastOnStack !== draggingBlock.nextConnection) {
			available.push(lastOnStack);
		}
		return available;
	}

	/**
	 * Cleans up any state at the end of the drag. Applies any pending
	 * connections.
	 */
	endDrag(e) {
		if (this.block.isShadow()) {
			this.block.getParent()?.endDrag(e);
			return;
		}

		// Clear any remaining highlights
		if (this.startParentConn?.sourceBlock_) {
			this.startParentConn.sourceBlock_.unselect();
		}

		this.fireDragEndEvent();
		this.fireMoveEvent();

		dom.stopTextWidthCache();

		Blockly.blockAnimations.disconnectUiStop();
		this.connectionPreviewer.hidePreview();

		if (!this.block.isDeadOrDying() && this.dragging) {
			// These are expensive and don't need to be done if we're deleting, or
			// if we've already stopped dragging because we moved back to the start.
			this.workspace
				.getLayerManager()
				?.moveOffDragLayer(this.block, BLOCK_LAYER);
			this.block.setDragging(false);
		}

		if (this.connectionCandidate) {
			// Applying connections also rerenders the relevant blocks.
			this.applyConnections(this.connectionCandidate);
		}
		else {
			this.block.queueRender();
		}
		this.block.snapToGrid();

		// Must dispose after connections are applied to not break the dynamic
		// connections plugin. See #7859
		this.connectionPreviewer.dispose();
		this.workspace.setResizesEnabled(true);

		eventUtils.setGroup(false);
	}

	/** Connects the given candidate connections. */
	applyConnections(candidate) {
		const { local, neighbour } = candidate;
		local.connect(neighbour);

		const inferiorConnection = local.isSuperior() ? neighbour : local;
		const rootBlock = this.block.getRootBlock();

		Blockly.renderManagement.finishQueuedRenders().then(() => {
			Blockly.blockAnimations.connectionUiEffect(inferiorConnection.getSourceBlock());
			// bringToFront is incredibly expensive. Delay until the next frame.
			setTimeout(() => {
				rootBlock.bringToFront();
			}, 0);
		});
	}

	/**
	 * Moves the block back to where it was at the beginning of the drag,
	 * including reconnecting connections.
	 */
	revertDrag() {
		if (this.block.isShadow()) {
			this.block.getParent()?.revertDrag();
			return;
		}

		this.startChildConn?.connect(this.block.nextConnection);
		if (this.startParentConn) {
			switch (this.startParentConn.type) {
				case Blockly.ConnectionType.INPUT_VALUE:
					this.startParentConn.connect(this.block.outputConnection);
					break;
				case Blockly.ConnectionType.NEXT_STATEMENT:
					this.startParentConn.connect(this.block.previousConnection);
			}
		}
		else {
			this.block.moveTo(this.startLoc, ["drag"]);
			this.workspace
				.getLayerManager()
				?.moveOffDragLayer(this.block, BLOCK_LAYER);
			// Blocks dragged directly from a flyout may need to be bumped into
			// bounds.
			Blockly.bumpObjects.bumpIntoBounds(
				this.workspace,
				this.workspace.getMetricsManager().getScrollMetrics(true),
				this.block,
			);
		}

		this.startChildConn = null;
		this.startParentConn = null;

		this.connectionPreviewer.hidePreview();
		this.connectionCandidate = null;

		this.block.setDragging(false);
		this.dragging = false;
	}
}

export function setDuplicateOnDragStrategy(block) {
	block.setDragStrategy?.(new DuplicateOnDragStrategy(block));
}