# Image Grid from Batch

## Description
Creates an image grid from a batch while preserving transparency (alpha channel).

## Parameters

### Images (required)
The batch of images to arrange in a grid. Format: RGBA or RGB.

### Grid Cols (required)
Number of columns in the grid.

### Grid Rows (required)
Number of rows in the grid.

### Padding (required)
Space in pixels between images.
- Min: 0
- Max: 100
- Default: 0

## Output
A single image containing the grid composed of the batch images.

## Notes
- If the batch contains fewer images than the grid (rows × cols), missing cells are filled with transparency.
- Transparency is fully preserved.
- The batch images must have the same dimensions.