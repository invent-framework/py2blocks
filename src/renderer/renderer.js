import { RenderInfo } from "./info.js";

export class Renderer extends Blockly.zelos.Renderer {
    makeRenderInfo_(block) {
        return new RenderInfo(this, block);
    }
}

Blockly.blockRendering.register("py2blocks", Renderer);