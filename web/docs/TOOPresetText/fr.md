# TOO Preset Text Node

Node personnalisé pour ComfyUI permettant de gérer des presets de texte via une interface graphique.

## Installation

### 1. Fichiers Python

Copiez `preset_text.py` dans le dossier :
```
Comfyui-TOO-Pack/nodes/utils/preset_text.py
```

### 2. Fichiers JavaScript

Copiez `preset_text.js` dans le dossier :
```
Comfyui-TOO-Pack/web/preset_text.js
```

### 3. Mise à jour de __init__.py

Remplacez le fichier `__init__.py` à la racine de Comfyui-TOO-Pack par le nouveau fichier fourni.

### 4. Redémarrage

Redémarrez ComfyUI pour charger le nouveau node.

## Structure des fichiers

```
Comfyui-TOO-Pack/
├── __init__.py                    (modifié)
├── nodes/
│   └── utils/
│       └── preset_text.py         (nouveau)
├── web/
│   └── preset_text.js             (nouveau)
└── presets/
    └── text_presets.json          (créé automatiquement)
```

## Utilisation

### Ajouter le node

1. Dans ComfyUI, faites un clic droit dans l'espace de travail
2. Allez dans : `Add Node` → `TOO` → `utils` → `TOO Preset Text`

### Fonctionnalités

**Liste déroulante** : Sélectionnez un preset existant parmi la liste

**Bouton "Manage"** : Ouvre la fenêtre de gestion des presets où vous pouvez :
- Ajouter de nouveaux presets (bouton "Add New")
- Modifier les presets existants
- Supprimer des presets (en laissant le nom ou la valeur vide)

**Sortie** : Le node retourne le texte du preset sélectionné en sortie STRING

### Presets par défaut

Le node est livré avec 3 presets par défaut :
- `default negative` : "worst quality, low quality, jpeg artifacts"
- `remove` : "\\b"
- `regex : extract filename from` : "([^\\\\\/]+)_safetensors$"

### Sauvegarde

Les presets sont sauvegardés dans :
```
Comfyui-TOO-Pack/presets/text_presets.json
```

Ce fichier est créé automatiquement au premier lancement.

## Caractéristiques techniques

- **Catégorie** : TOO/utils
- **Type de sortie** : STRING
- **API REST** : 
  - GET `/too/presets/list` : Liste tous les presets
  - POST `/too/presets/save` : Sauvegarde les presets
- **Format de stockage** : JSON

## Notes

- Les presets sont partagés entre toutes les instances du node
- La modification des presets nécessite un rechargement de la page pour mettre à jour les dropdowns
- Les noms de presets doivent être uniques

## Améliorations futures possibles

- Support pour les champs multilignes (textarea) pour les valeurs
- Import/export de presets
- Catégorisation des presets
- Prévisualisation en temps réel
