Blockly.Theme.defineTheme("py2blocks", {
	name: "py2blocks",
	base: Blockly.Themes.Classic,
	fontStyle: {
		family: "monospace"
	},
});

Blockly.Css.register(`
	.blocklyText {
		fill: black !important;
	}

	.py2blocks-renderer.py2blocks-theme .blocklyDropdownText {
    	fill: black !important;
    }

	.blocklyEditableText image {
		filter: invert(1);
	}
`);