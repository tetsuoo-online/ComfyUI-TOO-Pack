import { app } from "../../scripts/app.js";
import { ComfyDialog } from "../../scripts/ui.js";
import { api } from "../../scripts/api.js";

class PresetManagementDialog extends ComfyDialog {
    constructor(nodeWidget) {
        super();
        this.presets = {};
        this.nodeWidget = nodeWidget;
        this.element.classList.add("comfy-modal");
    }

    async loadPresets() {
        try {
            const response = await api.fetchApi("/too/presets/list");
            this.presets = await response.json();
        } catch (error) {
            console.error("Error loading presets:", error);
            this.presets = {};
        }
    }

    async savePresets(nodeWidget) {
        try {
            const response = await api.fetchApi("/too/presets/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ presets: this.presets }),
            });
            const result = await response.json();
            if (result.success) {
                // Update the widget options dynamically
                if (nodeWidget) {
                    const presetNames = Object.keys(this.presets);
                    nodeWidget.options.values = presetNames;
                    
                    // If current value is not in the new list, select the first preset
                    if (!presetNames.includes(nodeWidget.value)) {
                        nodeWidget.value = presetNames[0] || "";
                    }
                }
                
                this.close();
            } else {
                alert("Error saving presets: " + (result.error || "Unknown error"));
            }
        } catch (error) {
            console.error("Error saving presets:", error);
            alert("Error saving presets: " + error.message);
        }
    }

    createPresetRow(name, value) {
        const row = document.createElement("div");
        row.style.cssText = `
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        `;

        const nameLabel = document.createElement("label");
        nameLabel.textContent = "Name:";
        nameLabel.style.cssText = "color: #999; margin-right: 5px;";

        const nameInput = document.createElement("input");
        nameInput.type = "text";
        nameInput.value = name;
        nameInput.style.cssText = `
            background: #1a1a1a;
            border: 1px solid #444;
            color: #fff;
            padding: 8px;
            border-radius: 4px;
            width: 100%;
        `;

        const valueLabel = document.createElement("label");
        valueLabel.textContent = "Value:";
        valueLabel.style.cssText = "color: #999; margin-right: 5px;";

        const valueInput = document.createElement("input");
        valueInput.type = "text";
        valueInput.value = value;
        valueInput.style.cssText = `
            background: #1a1a1a;
            border: 1px solid #444;
            color: #fff;
            padding: 8px;
            border-radius: 4px;
            width: 100%;
        `;

        const nameCol = document.createElement("div");
        nameCol.appendChild(nameLabel);
        nameCol.appendChild(nameInput);

        const valueCol = document.createElement("div");
        valueCol.appendChild(valueLabel);
        valueCol.appendChild(valueInput);

        row.appendChild(nameCol);
        row.appendChild(valueCol);

        // Store references for later retrieval
        row.nameInput = nameInput;
        row.valueInput = valueInput;
        row.originalName = name;

        return row;
    }

    show() {
        this.loadPresets().then(() => {
            const content = document.createElement("div");
            content.style.cssText = `
                background: #2a2a2a;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 20px;
                max-width: 900px;
                width: 90vw;
                max-height: 80vh;
                overflow-y: auto;
                color: #fff;
            `;

            const title = document.createElement("h3");
            title.textContent = "Manage Text Presets";
            title.style.cssText = "margin-top: 0; color: #fff;";
            content.appendChild(title);

            const presetsContainer = document.createElement("div");
            presetsContainer.id = "presets-container";
            presetsContainer.style.cssText = "margin-bottom: 20px;";

            // Add existing presets
            for (const [name, value] of Object.entries(this.presets)) {
                presetsContainer.appendChild(this.createPresetRow(name, value));
            }

            content.appendChild(presetsContainer);

            // Add New button
            const addButton = document.createElement("button");
            addButton.textContent = "Add New";
            addButton.style.cssText = `
                width: 100%;
                padding: 12px;
                background: #0066cc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-bottom: 10px;
                font-size: 14px;
            `;
            addButton.onclick = () => {
                const newRow = this.createPresetRow("", "");
                presetsContainer.appendChild(newRow);
            };
            content.appendChild(addButton);

            // Help text
            const helpText = document.createElement("p");
            helpText.textContent = "To remove a preset set the name or value to blank";
            helpText.style.cssText = `
                color: #999;
                font-size: 12px;
                text-align: center;
                margin: 15px 0;
            `;
            content.appendChild(helpText);

            // Buttons container
            const buttonsContainer = document.createElement("div");
            buttonsContainer.style.cssText = `
                display: flex;
                gap: 10px;
                margin-top: 20px;
            `;

            const saveButton = document.createElement("button");
            saveButton.textContent = "SAVE";
            saveButton.style.cssText = `
                flex: 1;
                padding: 12px;
                background: #4a4a4a;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            `;
            saveButton.onclick = () => {
                // Collect all presets from the form
                const newPresets = {};
                const rows = presetsContainer.querySelectorAll("div[style*='grid']");
                
                rows.forEach(row => {
                    const name = row.nameInput.value.trim();
                    const value = row.valueInput.value.trim();
                    
                    // Only add if both name and value are not empty
                    if (name && value) {
                        newPresets[name] = value;
                    }
                });

                this.presets = newPresets;
                this.savePresets(this.nodeWidget);
            };

            const cancelButton = document.createElement("button");
            cancelButton.textContent = "CANCEL";
            cancelButton.style.cssText = `
                flex: 1;
                padding: 12px;
                background: #4a4a4a;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            `;
            cancelButton.onclick = () => this.close();

            buttonsContainer.appendChild(saveButton);
            buttonsContainer.appendChild(cancelButton);
            content.appendChild(buttonsContainer);

            super.show(content);
        });
    }
}

app.registerExtension({
    name: "TOO.PresetText",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TOOPresetText") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);

                // Get the preset widget (first widget, which is the dropdown)
                const presetWidget = this.widgets[0];

                // Add the Manage button
                const manageButton = this.addWidget(
                    "button",
                    "Manage",
                    "manage",
                    () => {
                        const dialog = new PresetManagementDialog(presetWidget);
                        dialog.show();
                    }
                );

                manageButton.serialize = false;

                return result;
            };
        }
    },
});
