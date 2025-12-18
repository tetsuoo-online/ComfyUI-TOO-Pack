# Collection Categorizer (LLM) 🗂️

Un node ComfyUI qui scanne automatiquement vos dossiers et catégorise le contenu avec un LLM local (Ollama).

---

## 📋 Fonctionnalités

- **Scan automatique** de dossiers (fichiers vidéo, archives, documents)
- **Catégorisation intelligente** via LLM local (Ollama)
- **Scan récursif** optionnel des sous-dossiers
- **Seed reproductible** pour des résultats identiques
- **Modèles personnalisés** Ollama supportés
- **Sauvegarde automatique** du JSON
- **Compatible** avec Collection Manager
- **100% local** - aucune API externe

---

## ⚙️ Paramètres

### Paramètres principaux

| Paramètre | Type | Description | Défaut |
|-----------|------|-------------|--------|
| **ollama_model** | <span style="background-color:#2d3748;color:#a0aec0;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">COMBO</span> | Modèle LLM à utiliser (ou "custom") | `qwen2.5:7b` |
| **custom_ollama_model** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Nom du modèle si "custom" sélectionné | - |
| **folder_path** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Chemin du dossier à scanner | - |
| **scan_subfolders** | <span style="background-color:#3d2d52;color:#a78bfa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">BOOLEAN</span> | Scanner récursivement les sous-dossiers | `False` |
| **save_json** | <span style="background-color:#3d2d52;color:#a78bfa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">BOOLEAN</span> | Sauvegarder automatiquement le JSON | `True` |
| **collection_title** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Titre de la collection | `Ma Collection` |
| **content_type** | <span style="background-color:#2d3748;color:#a0aec0;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">COMBO</span> | Type de contenu (ou "custom") | `films` |

### Paramètres optionnels

| Paramètre | Type | Description | Défaut |
|-----------|------|-------------|--------|
| **custom_type_name** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Nom du type si "custom" sélectionné | - |
| **custom_categories** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Critères de catégorisation personnalisés (multiline) | (vide = LLM décide) |
| **seed** | <span style="background-color:#1e4d3e;color:#34d399;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">INT</span> | Seed pour résultats reproductibles | `0` (aléatoire) |

### Sorties

| Paramètre | Type | Description |
|-----------|------|-------------|
| **json_output** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Le JSON de la collection complète |
| **summary** | <span style="background-color:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">STRING</span> | Résumé de la catégorisation |

---

## 💡 Exemples

### Cas 1 : Films avec catégories automatiques
- `content_type`: films
- `custom_categories`: (vide)
- Le LLM décide des catégories (Genre, Époque, etc.)

### Cas 2 : Séries avec critères personnalisés
- `content_type`: series
- `custom_categories`: "Genre, Année, Studio"
- Le LLM catégorise selon ces critères

### Cas 3 : Type personnalisé
- `content_type`: custom
- `custom_type_name`: "Documentaires"
- `custom_categories`: "Thème, Durée"

### Cas 4 : Modèle personnalisé
- `ollama_model`: custom
- `custom_ollama_model`: "mistral:7b"

### Cas 5 : Résultats reproductibles
- `seed`: 42
- Toujours le même résultat avec les mêmes paramètres

### Format de sortie (JSON)

```json
{
  "title": "Ma Collection",
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
      "name": "Comédie",
      "subcategories": [],
      "games": ["Superbad", "The Hangover"]
    }
  ]
}
```

---

## 🚀 Installation

### Prérequis

1. **Ollama** installé et en cours d'exécution
   ```bash
   # Télécharger : https://ollama.ai
   ollama --version
   ```

2. **Python requests** (pour l'API HTTP locale)
   ```bash
   pip install requests --break-system-packages
   ```

3. **Au moins un modèle LLM**
   ```bash
   ollama pull qwen2.5:7b
   ```

### Installation du node

```bash
cd ComfyUI/custom_nodes/
# Copier collection_categorizer.py dans ce dossier
```

Redémarrer ComfyUI

---

## 🎯 Types de fichiers supportés

### Vidéos
`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`

### Archives
`.cbz`, `.cbr`, `.zip`, `.rar`

### Documents
`.epub`, `.pdf`, `.mobi`

### Dossiers
Les sous-dossiers sont traités comme des items individuels (sauf si `scan_subfolders` activé)

---

## 🤖 Modèles recommandés

| Modèle | Taille | Vitesse | Qualité | Usage |
|--------|--------|---------|---------|--------|
| **qwen2.5:7b** | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | Recommandé |
| **gemma3:12b** | 12B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Meilleur qualité |
| **llama3.1:8b** | 8B | ⚡⚡⚡ | ⭐⭐⭐⭐ | Très fiable |
| **gemma3:4b** | 4B | ⚡⚡⚡⚡ | ⭐⭐⭐ | Rapide |

---

## 🔧 Dépannage

### ❌ "Impossible de se connecter à Ollama"
- Vérifiez qu'Ollama est démarré : `ollama serve`
- Vérifiez le port : `http://localhost:11434`

### ❌ "JSON invalide"
- Essayez un autre modèle (qwen2.5:7b recommandé)
- Réduisez le nombre d'items (< 100)

### ❌ "Items non catégorisés"
- Le LLM a peut-être raté certains items
- Essayez avec un seed différent
- Modifiez `custom_categories` pour guider le LLM

### ⚠️ Caractères bizarres (ÃƒÂ©, Ãƒ )
- Vérifiez l'encodage UTF-8 (normalement corrigé dans cette version)

---

## 📝 Notes

- **Seed = 0** : résultats aléatoires à chaque exécution
- **Seed > 0** : résultats identiques avec mêmes paramètres
- Le JSON est sauvegardé dans le dossier scanné
- Le node valide que tous les items sont catégorisés
- Compatible avec le format Collection Manager

---

## 📄 License

MIT

---

## 🙏 Crédits

- **Claude AI**
- **Ollama** - Local LLM runtime
- **ComfyUI** - Node-based UI framework
- **Collection Manager** - JSON format compatibility

---

## 📧 Contact

Pour signaler un bug ou suggérer une amélioration :
- Créez une issue
- Proposez une PR
