/**
 * ComfyUI Color Picker Widget
 * Creates a custom color input type with picker
 */

import { app } from "../../scripts/app.js";

// Helper function to convert hex to RGB
function hexToRgb(hex) {
    // Ensure hex is a string
    if (typeof hex !== "string") {
        return { r: 32, g: 160, b: 176 };
    }
    
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 32, g: 160, b: 176 };
}

// Helper to ensure color object is valid
function ensureColorObject(value) {
    if (!value) {
        return {
            hex: "#20A0B0",
            r: 32,
            g: 160,
            b: 176,
            a: 1.0
        };
    }
    
    if (typeof value === "string") {
        const rgb = hexToRgb(value);
        return {
            hex: value.toUpperCase(),
            r: rgb.r,
            g: rgb.g,
            b: rgb.b,
            a: 1.0
        };
    }
    
    if (typeof value === "object" && value.hex) {
        return value;
    }
    
    return {
        hex: "#20A0B0",
        r: 32,
        g: 160,
        b: 176,
        a: 1.0
    };
}

// Create the color widget
function createColorWidget(node, inputName, inputData, app) {
    const defaultValue = inputData[1]?.default || {
        hex: "#20A0B0",
        r: 32,
        g: 160,
        b: 176,
        a: 1.0
    };
    
    const widget = {
        name: inputName,
        type: "TOO_COLOR",
        value: ensureColorObject(defaultValue),
        
        draw: function(ctx, node, width, y) {
            const color = ensureColorObject(this.value);
            
            // Draw the color preview box
            const padding = 10;
            const boxSize = 50;
            const boxX = padding;
            const boxY = y + padding;
            
            // Draw background (for transparency visualization)
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(boxX, boxY, boxSize, boxSize);
            
            // Draw checkerboard pattern for alpha
            const checkSize = 5;
            ctx.fillStyle = "#cccccc";
            for (let i = 0; i < boxSize; i += checkSize) {
                for (let j = 0; j < boxSize; j += checkSize) {
                    if ((i + j) % (checkSize * 2) === 0) {
                        ctx.fillRect(boxX + i, boxY + j, checkSize, checkSize);
                    }
                }
            }
            
            // Draw color with alpha
            ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${color.a})`;
            ctx.fillRect(boxX, boxY, boxSize, boxSize);
            
            // Draw border
            ctx.strokeStyle = "#666";
            ctx.lineWidth = 1;
            ctx.strokeRect(boxX, boxY, boxSize, boxSize);
            
            // Draw hex text
            ctx.fillStyle = "#ddd";
            ctx.font = "12px monospace";
            ctx.fillText(color.hex, boxX + boxSize + 10, boxY + 15);
            ctx.fillText(`rgba(${color.r}, ${color.g}, ${color.b}, ${color.a.toFixed(2)})`, 
                       boxX + boxSize + 10, boxY + 35);
        },
        
        mouse: function(event, pos, node) {
            if (event.type === "pointerdown") {
                const color = ensureColorObject(this.value);
                
                // Create color picker input
                const input = document.createElement("input");
                input.type = "color";
                input.value = color.hex;
                
                input.addEventListener("input", (e) => {
                    const hex = e.target.value;
                    const rgb = hexToRgb(hex);
                    
                    this.value = {
                        hex: hex.toUpperCase(),
                        r: rgb.r,
                        g: rgb.g,
                        b: rgb.b,
                        a: color.a || 1.0
                    };
                    
                    app.graph.setDirtyCanvas(true);
                });
                
                input.addEventListener("change", (e) => {
                    const hex = e.target.value;
                    const rgb = hexToRgb(hex);
                    
                    this.value = {
                        hex: hex.toUpperCase(),
                        r: rgb.r,
                        g: rgb.g,
                        b: rgb.b,
                        a: color.a || 1.0
                    };
                    
                    app.graph.setDirtyCanvas(true);
                });
                
                input.click();
            }
        },
        
        computeSize: function(width) {
            return [width, 70];
        }
    };
    
    node.addCustomWidget(widget);
    
    return { widget: widget };
}

// Register the extension
app.registerExtension({
    name: "too.ColorInput",
    
    registerCustomNodes() {
        class ColorInputNode {
            color = "#20A0B0";
        }
        
        ColorInputNode.title = "Color Input";
        ColorInputNode.category = "too/mixlab";
    },
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ColorInput") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                return result;
            };
        }
    },
    
    getCustomWidgets(app) {
        return {
            TOO_COLOR(node, inputName, inputData, app) {
                return createColorWidget(node, inputName, inputData, app);
            }
        };
    }
});