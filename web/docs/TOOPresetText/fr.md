# TOO Preset Text Node

Node personnalisé pour ComfyUI permettant de gérer des presets de texte via une interface graphique.

## Utilisation

**Liste déroulante** : Sélectionnez un preset existant parmi la liste

**Bouton "Manage"** : Ouvre la fenêtre de gestion des presets où vous pouvez :
- Ajouter de nouveaux presets (bouton "Add New")
- Modifier les presets existants
- Supprimer des presets (en laissant le nom ou la valeur vide)

**Sortie** : Le node retourne le texte du preset sélectionné en sortie STRING

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
