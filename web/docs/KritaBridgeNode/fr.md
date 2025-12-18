# Krita Bridge 🎨

Charge automatiquement la dernière image depuis le dossier `input/krita/` pour une intégration transparente avec Krita.

**Catégorie:** `TOO-Pack/image`

---

## 📋 Fonctionnalités

- **Chargement automatique** de la dernière image du dossier krita
- **Détection en temps réel** des nouveaux fichiers
- **Mise à jour automatique** pendant la génération
- **Support alpha** : extraction du canal alpha comme masque
- **Création auto** du dossier si inexistant
- **Sans paramètre** : fonctionne directement

---

## ⚙️ Paramètres

### Paramètres obligatoires

**Aucun paramètre requis** - Le node fonctionne automatiquement !

### Sorties

| Paramètre | Type | Description |
|-----------|------|-------------|
| **image** | <span style="background-color:#7c2d12;color:#fb923c;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">IMAGE</span> | L'image chargée (RGB) |
| **mask** | <span style="background-color:#4c1d95;color:#c4b5fd;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:0.9em;">MASK</span> | Le masque extrait du canal alpha |

---

## 🎯 Configuration

### Dossier de travail

Le node charge automatiquement depuis :
```
ComfyUI/input/krita/
```

Si le dossier n'existe pas, il est créé automatiquement au premier lancement.

### Export depuis Krita

1. **Ouvrir Krita**
2. **Créer ou modifier** votre image
3. **Exporter en PNG** : `Fichier > Exporter`
4. **Destination** : `ComfyUI/input/krita/nomdefichier.png`
5. Le node détecte automatiquement le nouveau fichier

### Workflow recommandé

```
Krita → Export PNG → ComfyUI/input/krita/ → Krita Bridge → [votre workflow]
```

---

## 💡 Exemples d'utilisation

### Cas 1 : Chargement simple
```python
# Aucune configuration nécessaire
# Le node charge automatiquement la dernière image
```

### Cas 2 : Utilisation du masque alpha
```python
# Connecter 'mask' à un node de masque (Mask Composite, etc.)
# Le canal alpha de l'image Krita devient un masque utilisable
```

### Cas 3 : Workflow itératif Krita ↔ ComfyUI
```
1. Dessiner dans Krita
2. Exporter → input/krita/sketch.png
3. ComfyUI détecte et génère
4. Récupérer le résultat
5. Retoucher dans Krita
6. Réexporter → Le node charge la nouvelle version
```

### Cas 4 : Inpainting avec masque Krita
```python
# Workflow :
# Krita Bridge (image + mask) → Inpaint Model → VAE Decode
# Le masque alpha de Krita définit la zone d'inpainting
```

### Cas 5 : Mode surveillance continue
```python
# Le node vérifie automatiquement les nouveaux fichiers
# Idéal pour le prototypage rapide
# Modifiez dans Krita → Sauvez → Le workflow se met à jour
```

---

## 🔧 Détails techniques

### Détection de fichiers

Le node :
1. Scanne le dossier `input/krita/` pour tous les fichiers `.png`
2. Trouve le fichier avec la **modification la plus récente**
3. Compare l'horodatage avec le dernier fichier chargé
4. Recharge si un changement est détecté

### Gestion du canal alpha

**Image RGBA (avec transparence) :**
- Canal RGB → sortie `image`
- Canal Alpha → sortie `mask` (valeurs 0-1)

**Image RGB (sans transparence) :**
- RGB → sortie `image`
- Masque blanc uniforme → sortie `mask`

### Mise à jour automatique

La fonction `IS_CHANGED` retourne le timestamp actuel, forçant ComfyUI à :
- Réévaluer le node à chaque exécution
- Détecter les nouveaux fichiers en temps réel
- Mettre à jour automatiquement l'image

### Image par défaut

Si aucun fichier PNG n'est trouvé :
- Retourne une image noire 512×512
- Retourne un masque blanc 512×512
- Affiche : `"KritaBridge: Waiting for images in input/krita/"`

---

## 🎨 Intégration Krita

### Configuration Krita

1. **Configurer le dossier d'export par défaut**
   - `Paramètres > Configurer Krita > Général`
   - Définir le dossier par défaut : `ComfyUI/input/krita/`

2. **Raccourci clavier pour export rapide**
   - `Paramètres > Configurer Krita > Raccourcis clavier`
   - Assigner une touche à `Exporter`
   - Exemple : `Ctrl+Shift+E`

3. **Format d'export**
   - Format : **PNG**
   - Compression : selon préférence
   - **Important** : Activer "Enregistrer le canal alpha" si vous utilisez le masque

### Workflow optimal

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

## 🔧 Dépannage

### ❌ "Waiting for images in input/krita/"
- Le dossier `input/krita/` est vide
- Exportez une image PNG depuis Krita dans ce dossier

### ❌ Image ne se met pas à jour
- Vérifiez que le fichier est bien au format `.png`
- Vérifiez les permissions de lecture du dossier
- Essayez d'exporter avec un nouveau nom de fichier

### ❌ Masque ne fonctionne pas
- Vérifiez que l'image Krita contient un canal alpha
- Dans Krita : `Calque > Convertir > Convertir le type de calque > Image avec canal alpha`
- Réexportez au format PNG avec option "Canal alpha"

### ⚠️ Performances lentes
- Trop de fichiers dans `input/krita/` peuvent ralentir le scan
- Nettoyez régulièrement les anciens fichiers
- Le node ne charge qu'un seul fichier (le plus récent)

### ⚠️ Ancienne image chargée
- Le node charge toujours le fichier avec l'horodatage le plus récent
- Si vous modifiez un vieux fichier, il peut être rechargé
- Solution : exportez toujours avec un nouveau nom

---

## 📝 Notes

- Le node se met à jour automatiquement à **chaque exécution**
- Seuls les fichiers `.png` sont détectés
- Le fichier le plus récent est sélectionné (par date de modification)
- La résolution d'origine est préservée
- Toutes les images sont converties en RGB (même si RGBA ou autre)

---

## 💡 Astuces

### Nommage intelligent
```
sketch_001.png
sketch_002.png
sketch_003.png
```
Le dernier numéro sera toujours chargé.

### Masque de sélection
Utilisez la transparence dans Krita comme masque de sélection pour l'inpainting.

### Export automatique
Créez une action Krita qui exporte automatiquement dans le bon dossier.

### Plusieurs versions
Gardez plusieurs exports pour comparer - le node charge toujours le plus récent.

---

## 📄 License

MIT

---

## 🙏 Crédits

- **ComfyUI** - Framework node-based
- **Krita** - Logiciel de peinture numérique open-source
- **PIL/Pillow** - Manipulation d'images

---

## 📧 Contact

Pour signaler un bug ou suggérer une amélioration :
- Créez une issue
- Proposez une PR
