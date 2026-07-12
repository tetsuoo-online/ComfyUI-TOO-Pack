# Image Grid from Batch

## Description
Crée une grille d'images à partir d'un batch, en préservant la transparence (canal alpha).

## Paramètres

### Images (obligatoire)
Le batch d'images à disposer en grille. Format : RGBA ou RGB.

### Grid Cols (obligatoire)
Nombre de colonnes dans la grille.

### Grid Rows (obligatoire)
Nombre de lignes dans la grille.

### Padding (obligatoire)
Espace (en pixels) entre les images.
- Min : 0
- Max : 100
- Défaut : 0

## Sortie
Une seule image contenant la grille composée des images du batch.

## Notes
- Si le batch contient moins d'images que la grille (rows × cols), les cellules manquantes seront remplies avec du transparent
- La transparence est entièrement préservée
- Les images du batch doivent avoir les mêmes dimensions