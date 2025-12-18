class ExtractFieldFromNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_name": ("STRING", {
                    "default": "Power Lora Loader",
                    "tooltip": "The class type of the node to extract from (e.g., 'Power Lora Loader', 'LoraLoader', 'KSampler')"
                }),
                "field_name": ("STRING", {
                    "default": "lora",
                    "multiline": False,
                    "tooltip": "The field to extract. Examples: 'lora' for Power Lora Loader, 'lora_name' for LoraLoader, 'sampler_name' for KSampler. Leave empty to extract all fields."
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
    CATEGORY = "too/utils"
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(cls, node_name, field_name, **kwargs):
        return float("nan")

    def extract(self, node_name, field_name, extra_pnginfo=None, prompt=None, unique_id=None):
        if prompt is None:
            return ("",)
        
        result_lines = []
        
        for node_id in prompt:
            node_data = prompt[node_id]
            class_type = node_data.get("class_type", "")
            
            if node_name.lower() in class_type.lower():
                inputs = node_data.get("inputs", {})
                
                for key, value in inputs.items():
                    should_extract = False
                    extracted_value = None
                    
                    if not field_name:
                        should_extract = True
                        extracted_value = value
                    elif key == field_name:
                        should_extract = True
                        extracted_value = value
                    elif isinstance(value, dict) and field_name in value:
                        if value.get("on", True):
                            should_extract = True
                            extracted_value = value.get(field_name, "")
                    
                    if should_extract and extracted_value is not None:
                        if isinstance(extracted_value, dict):
                            if "on" in extracted_value and not extracted_value.get("on", True):
                                continue
                            for dict_key, dict_value in extracted_value.items():
                                if dict_key != "on" and dict_value:
                                    result_lines.append(str(dict_value))
                        elif not isinstance(extracted_value, (list, dict)):
                            result_lines.append(str(extracted_value))
        
        output_string = "\n".join(result_lines)
        if output_string:
            output_string += "\n"
        
        return (output_string,)

NODE_CLASS_MAPPINGS = {
    "ExtractFieldFromNode": ExtractFieldFromNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtractFieldFromNode": "Extract Field From Node"
}
