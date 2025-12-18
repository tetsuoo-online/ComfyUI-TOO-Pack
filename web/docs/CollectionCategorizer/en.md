# Collection Categorizer (LLM) 🗂️

A ComfyUI node that automatically scans your folders and categorizes content with a local LLM (Ollama).

---

## 📋 Features

- **Automatic scanning** of folders (video files, archives, documents)
- **Smart categorization** via local LLM (Ollama)
- **Recursive scanning** of subfolders (optional)
- **Reproducible seed** for identical results
- **Custom Ollama models** supported
- **Auto-save** JSON output
- **Compatible** with Collection Manager
- **100% local** - no external APIs

---

## ⚙️ Parameters

### Main Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| **ollama_model** | <span style="background-color:#2d3748;color:#a0aec0;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">COMBO</span> | LLM model to use (or "custom") | `qwen2.5:7b` |
| **custom_ollama_model** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Model name if "custom" selected | - |
| **folder_path** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Path to folder to scan | - |
| **scan_subfolders** | <span style="background-color:#3d2d52;color:#a78bfa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">BOOLEAN</span> | Recursively scan subfolders | `False` |
| **save_json** | <span style="background-color:#3d2d52;color:#a78bfa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">BOOLEAN</span> | Auto-save JSON output | `True` |
| **collection_title** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Collection title | `Ma Collection` |
| **content_type** | <span style="background-color:#2d3748;color:#a0aec0;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">COMBO</span> | Content type (or "custom") | `films` |

### Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| **custom_type_name** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Type name if "custom" selected | - |
| **custom_categories** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Custom categorization criteria (multiline) | (empty = LLM decides) |
| **seed** | <span style="background-color:#1e4d3e;color:#34d399;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">INT</span> | Seed for reproducible results | `0` (random) |

### Outputs

| Parameter | Type | Description |
|-----------|------|-------------|
| **json_output** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | The complete collection JSON |
| **summary** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Categorization summary |

---

## 💡 Examples

### Case 1: Movies with automatic categories
- `content_type`: films
- `custom_categories`: (empty)
- LLM decides categories (Genre, Era, etc.)

### Case 2: TV Series with custom criteria
- `content_type`: series
- `custom_categories`: "Genre, Year, Studio"
- LLM categorizes by these criteria

### Case 3: Custom type
- `content_type`: custom
- `custom_type_name`: "Documentaries"
- `custom_categories`: "Theme, Duration"

### Case 4: Custom model
- `ollama_model`: custom
- `custom_ollama_model`: "mistral:7b"

### Case 5: Reproducible results
- `seed`: 42
- Always same result with same parameters

### Output Format (JSON)

```json
{
  "title": "My Collection",
  "icon": "🎬",
  "type": "Films",
  "filename": "films.json",
  "categories": [
    {
      "id": 1,
      "name": "Science Fiction",
      "subcategories": [],
      "games": ["Blade Runner", "The Matrix"]
    },
    {
      "id": 2,
      "name": "Comedy",
      "subcategories": [],
      "games": ["Superbad", "The Hangover"]
    }
  ]
}
```

---

## 🚀 Installation

### Requirements

1. **Ollama** installed and running
   ```bash
   # Download: https://ollama.ai
   ollama --version
   ```

2. **Python requests** (for local HTTP API)
   ```bash
   pip install requests --break-system-packages
   ```

3. **At least one LLM model**
   ```bash
   ollama pull qwen2.5:7b
   ```

### Node installation

```bash
cd ComfyUI/custom_nodes/
# Copy collection_categorizer.py to this folder
```

Restart ComfyUI

---

## 🎯 Supported File Types

### Videos
`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`

### Archives
`.cbz`, `.cbr`, `.zip`, `.rar`

### Documents
`.epub`, `.pdf`, `.mobi`

### Folders
Subfolders are treated as individual items (unless `scan_subfolders` enabled)

---

## 🤖 Recommended Models

| Model | Size | Speed | Quality | Usage |
|-------|------|-------|---------|--------|
| **qwen2.5:7b** | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | Recommended |
| **gemma3:12b** | 12B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality |
| **llama3.1:8b** | 8B | ⚡⚡⚡ | ⭐⭐⭐⭐ | Very reliable |
| **gemma3:4b** | 4B | ⚡⚡⚡⚡ | ⭐⭐⭐ | Fast |

---

## 🔧 Troubleshooting

### ❌ "Cannot connect to Ollama"
- Check Ollama is running: `ollama serve`
- Check port: `http://localhost:11434`

### ❌ "Invalid JSON"
- Try another model (qwen2.5:7b recommended)
- Reduce number of items (< 100)

### ❌ "Uncategorized items"
- LLM may have missed some items
- Try with different seed
- Modify `custom_categories` to guide LLM

### ⚠️ Strange characters (ÃƒÂ©, Ãƒ )
- Check UTF-8 encoding (should be fixed in this version)

---

## 📝 Notes

- **Seed = 0**: random results each run
- **Seed > 0**: identical results with same parameters
- JSON is saved in the scanned folder
- Node validates all items are categorized
- Compatible with Collection Manager format

---

## 📄 License

MIT

---

## 🙏 Credits

- **Claude AI**
- **Ollama** - Local LLM runtime
- **ComfyUI** - Node-based UI framework
- **Collection Manager** - JSON format compatibility

---

## 📧 Contact

To report a bug or suggest an improvement:
- Create an issue
- Submit a PR
