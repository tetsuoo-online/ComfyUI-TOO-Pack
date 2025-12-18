# Krita Bridge 🎨

Automatically loads the latest image from the `input/krita/` folder for seamless Krita integration.

**Category:** `TOO-Pack/image`

---

## 📋 Features

- **Automatic loading** of latest image from krita folder
- **Real-time detection** of new files
- **Auto-update** during generation
- **Alpha support**: extracts alpha channel as mask
- **Auto-create** folder if doesn't exist
- **No parameters** - works directly

---

## ⚙️ Parameters

### Required Parameters

**No parameters required** - The node works automatically!

### Outputs

| Parameter | Type | Description |
|-----------|------|-------------|
| **image** | <span style="background-color:#7c2d12;color:#fb923c;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">IMAGE</span> | The loaded image (RGB) |
| **mask** | <span style="background-color:#4c1d95;color:#c4b5fd;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">MASK</span> | Mask extracted from alpha channel |

---

## 🎯 Setup

### Working Directory

The node automatically loads from:
```
ComfyUI/input/krita/
```

If the folder doesn't exist, it's created automatically on first launch.

### Export from Krita

1. **Open Krita**
2. **Create or modify** your image
3. **Export as PNG**: `File > Export`
4. **Destination**: `ComfyUI/input/krita/filename.png`
5. The node automatically detects the new file

### Recommended Workflow

```
Krita → Export PNG → ComfyUI/input/krita/ → Krita Bridge → [your workflow]
```

---

## 💡 Usage Examples

### Case 1: Simple loading
```python
# No configuration needed
# Node automatically loads latest image
```

### Case 2: Using alpha mask
```python
# Connect 'mask' to a mask node (Mask Composite, etc.)
# Krita image's alpha channel becomes usable mask
```

### Case 3: Iterative Krita ↔ ComfyUI workflow
```
1. Draw in Krita
2. Export → input/krita/sketch.png
3. ComfyUI detects and generates
4. Get result
5. Refine in Krita
6. Re-export → Node loads new version
```

### Case 4: Inpainting with Krita mask
```python
# Workflow:
# Krita Bridge (image + mask) → Inpaint Model → VAE Decode
# Krita's alpha mask defines inpainting area
```

### Case 5: Continuous monitoring mode
```python
# Node automatically checks for new files
# Ideal for rapid prototyping
# Edit in Krita → Save → Workflow updates
```

---

## 🔧 Technical Details

### File Detection

The node:
1. Scans `input/krita/` folder for all `.png` files
2. Finds file with **most recent modification**
3. Compares timestamp with last loaded file
4. Reloads if change detected

### Alpha Channel Handling

**RGBA image (with transparency):**
- RGB channels → `image` output
- Alpha channel → `mask` output (0-1 values)

**RGB image (no transparency):**
- RGB → `image` output
- Uniform white mask → `mask` output

### Automatic Update

The `IS_CHANGED` function returns current timestamp, forcing ComfyUI to:
- Re-evaluate node on every execution
- Detect new files in real-time
- Update image automatically

### Default Image

If no PNG file found:
- Returns black 512×512 image
- Returns white 512×512 mask
- Displays: `"KritaBridge: Waiting for images in input/krita/"`

---

## 🎨 Krita Integration

### Krita Configuration

1. **Set default export folder**
   - `Settings > Configure Krita > General`
   - Set default folder: `ComfyUI/input/krita/`

2. **Keyboard shortcut for quick export**
   - `Settings > Configure Krita > Keyboard Shortcuts`
   - Assign key to `Export`
   - Example: `Ctrl+Shift+E`

3. **Export format**
   - Format: **PNG**
   - Compression: as preferred
   - **Important**: Enable "Save alpha channel" if using mask

### Optimal Workflow

```
┌─────────┐    Export PNG    ┌──────────────┐
│  Krita  │ ───────────────> │ input/krita/ │
└─────────┘                   └──────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │ Krita Bridge │
                              └──────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
                ┌────────┐                        ┌──────┐
                │ image  │                        │ mask │
                └────────┘                        └──────┘
```

---

## 🔧 Troubleshooting

### ❌ "Waiting for images in input/krita/"
- The `input/krita/` folder is empty
- Export a PNG image from Krita to this folder

### ❌ Image not updating
- Check that file is in `.png` format
- Check folder read permissions
- Try exporting with a new filename

### ❌ Mask not working
- Check that Krita image contains alpha channel
- In Krita: `Layer > Convert > Convert Layer Type > Paint Layer with Alpha`
- Re-export as PNG with "Alpha channel" option

### ⚠️ Slow performance
- Too many files in `input/krita/` can slow scanning
- Regularly clean old files
- Node only loads one file (most recent)

### ⚠️ Old image loaded
- Node always loads file with most recent timestamp
- If you modify an old file, it may be reloaded
- Solution: always export with new name

---

## 📝 Notes

- Node auto-updates on **every execution**
- Only `.png` files are detected
- Most recent file selected (by modification date)
- Original resolution preserved
- All images converted to RGB (even if RGBA or other)

---

## 💡 Tips

### Smart naming
```
sketch_001.png
sketch_002.png
sketch_003.png
```
Latest number always loaded.

### Selection mask
Use transparency in Krita as selection mask for inpainting.

### Automatic export
Create a Krita action that automatically exports to correct folder.

### Multiple versions
Keep multiple exports to compare - node always loads most recent.

---

## 📄 License

MIT

---

## 🙏 Credits

- **ComfyUI** - Node-based framework
- **Krita** - Open-source digital painting software
- **PIL/Pillow** - Image manipulation

---

## 📧 Contact

To report a bug or suggest an improvement:
- Create an issue
- Submit a PR
