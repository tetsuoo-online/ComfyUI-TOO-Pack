import json


class ExtractWidgetFromNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_name": ("STRING", {
                    "default": "Power Lora Loader",
                    "tooltip": "The class type of the node to extract from (e.g., 'Power Lora Loader', 'LoraLoader', 'KSampler') OR the node ID (e.g., '#180', '#42')"
                }),
                "widget_names": ("STRING", {
                    "default": "lora, strength",
                    "multiline": False,
                    "tooltip": "Comma-separated list of widgets to extract. Examples: 'lora, strength' for Power Lora Loader (rgthree), 'lora_name, strength_model' for LoraLoader, 'seed, steps, cfg' for KSampler. Leave empty to extract all widgets."
                }),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID",
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract"
    CATEGORY = "🔵TOO-Pack/utils"
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(cls, node_name, widget_names, **kwargs):
        return float("nan")

    def extract(self, node_name, widget_names, extra_pnginfo=None, prompt=None, unique_id=None):
        if prompt is None:
            return ("",)

        widget_list = [w.strip() for w in widget_names.split(",")] if widget_names else []
        is_node_id = node_name.strip().startswith("#")
        target_node_id = node_name.strip()[1:] if is_node_id else None

        def find_widgets(value, out):
            """Recurse into a NON-matching input's value looking for widget_list keys
            one or more levels down (Power Lora Loader's per-row dicts, Pixaroma's
            JSON-stringified state and its nested loras[] list). Only called once the
            top-level key itself has already been ruled out as a direct match."""
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except ValueError:
                    if not widget_list and value:
                        out.append(value)
                    return
            if isinstance(value, dict):
                if "on" in value and not value.get("on", True):
                    return
                for k, v in value.items():
                    if k == "on":
                        continue
                    if widget_list and k in widget_list:
                        if isinstance(v, list):
                            out.extend(str(x) for x in v if x)
                        elif v not in (None, ""):
                            out.append(str(v))
                    elif isinstance(v, (dict, list)):
                        find_widgets(v, out)
                    elif not widget_list and v not in (None, ""):
                        out.append(str(v))
            elif isinstance(value, list):
                for item in value:
                    find_widgets(item, out)
            elif not widget_list and value not in (None, ""):
                out.append(str(value))

        result_lines = []
        for node_id in prompt:
            node_data = prompt[node_id]
            class_type = node_data.get("class_type", "")
            match = (str(node_id) == target_node_id) if is_node_id else (node_name.lower() in class_type.lower())
            if not match:
                continue
            node_results = []
            for key, value in node_data.get("inputs", {}).items():
                if isinstance(value, list):
                    continue  # a link ([source_node_id, slot]), never a widget value

                if widget_list and key in widget_list:
                    # Direct match on a plain widget (e.g. lora_name on a simple
                    # LoraLoader) or on a dict-valued one - append its contents as-is,
                    # no recursion needed since the key itself was what was asked for.
                    if isinstance(value, dict):
                        if value.get("on", True) is False:
                            continue
                        for dict_key, dict_value in value.items():
                            if dict_key != "on" and dict_value not in (None, ""):
                                node_results.append(str(dict_value))
                    else:
                        node_results.append(str(value))
                else:
                    find_widgets(value, node_results)
            if node_results:
                result_lines.append("\n".join(node_results))

        output_string = "\n".join(result_lines)
        if output_string:
            output_string += "\n"
        return (output_string,)

NODE_CLASS_MAPPINGS = {
    "ExtractWidgetFromNode": ExtractWidgetFromNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtractWidgetFromNode": "Extract Widget From Node 📋"
}