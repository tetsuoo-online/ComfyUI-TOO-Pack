# Comfyui-TOO-Pack

Custom nodes pack for ComfyUI - Category: `TOO-Pack`

## Installation

1. Navigate to your ComfyUI `custom_nodes` directory
2. Clone or copy this folder as `Comfyui-TOO-Pack`
3. Restart ComfyUI

```bash
cd ComfyUI/custom_nodes
git clone [your-repo-url] Comfyui-TOO-Pack
```

## Nodes

### 1. Smart Image Loader

**Category:** `too/images`

A flexible image loader that supports multiple input sources with priority order.

#### Inputs

- **seed** (required): Random seed for selection from lists/directories
- **txt_path** (optional): Path to a text file containing image paths (one per line)
- **img_path** (optional): Direct path to an image file
- **img_directory** (optional): Path to a directory containing images
- **image** (optional): Direct image input

#### Outputs

- **IMAGE**: The loaded image tensor
- **FILE_PATH**: Path to the loaded image file (or "external_input"/"none")

#### Priority Order

1. **txt_path**: Randomly selects one path from the text file
2. **img_path**: Loads the specific image file
3. **img_directory**: Randomly selects an image from the directory
4. **image**: Uses the provided image input

#### Supported Formats

PNG, JPG, JPEG, BMP, WEBP, TIFF

#### Example Usage

```python
# Text file (highest priority)
txt_path = "/path/to/image_list.txt"

# Direct image path
img_path = "/path/to/specific/image.png"

# Directory with images
img_directory = "/path/to/images/"
```

---

### 2. Extract Field From Node

**Category:** `too`

Extracts specific field values from nodes in the current workflow. Useful for extracting LoRA names, sampler settings, or any other node parameters.

#### Inputs

- **node_name** (required): The class type of the node to extract from
  - Examples: "Power Lora Loader", "LoraLoader", "KSampler"
- **field_name** (required): The field to extract
  - Examples: "lora", "lora_name", "sampler_name"
  - Leave empty to extract all fields

#### Outputs

- **STRING**: Extracted values (one per line, ending with newline)

#### Hidden Inputs

- **extra_pnginfo**: Workflow metadata
- **prompt**: Current workflow prompt
- **unique_id**: Node unique identifier

#### Features

- Case-insensitive node name matching
- Supports nested dictionary fields
- Respects "on/off" toggles in dictionary values
- Extracts all matching instances from the workflow

#### Example Usage

**Extract LoRA names from Power Lora Loader:**
```
node_name: "Power Lora Loader"
field_name: "lora"
```

**Extract sampler name from KSampler:**
```
node_name: "KSampler"
field_name: "sampler_name"
```

**Extract all fields from a node:**
```
node_name: "MyCustomNode"
field_name: (leave empty)
```

## Requirements

- ComfyUI
- Python 3.8+
- PyTorch
- Pillow (PIL)
- NumPy

## License

[Add your license here]

## Author

Tetsuoo

## Version

1.0.0
