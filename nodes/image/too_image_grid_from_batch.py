import torch
from PIL import Image

class ImageGridFromBatch:
    """
    Creates a grid layout from a batch of images while preserving transparency.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "grid_cols": ("INT", {
                    "default": 2,
                    "min": 1,
                    "step": 1,
                }),
                "grid_rows": ("INT", {
                    "default": 2,
                    "min": 1,
                    "step": 1,
                }),
                "padding": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("grid_image",)
    FUNCTION = "create_grid"
    CATEGORY = "🔵TOO-Pack/image"

    def create_grid(self, images, grid_cols, grid_rows, padding=0):
        # images shape: [batch, height, width, channels]
        batch_size, h, w, channels = images.shape
        
        # Vérifier que le batch peut remplir la grille
        required_images = grid_rows * grid_cols
        if batch_size < required_images:
            # Pad with transparent images if needed
            pad_size = required_images - batch_size
            transparent = torch.zeros((pad_size, h, w, channels), device=images.device)
            images = torch.cat([images, transparent], dim=0)
        
        # Créer la grille
        grid_width = grid_cols * (w + padding) - padding
        grid_height = grid_rows * (h + padding) - padding
        
        # Préserver le canal alpha si présent
        result = torch.zeros((grid_height, grid_width, channels), device=images.device)
        
        # Remplir la grille
        for idx in range(required_images):
            row = idx // grid_cols
            col = idx % grid_cols
            
            y_start = row * (h + padding)
            x_start = col * (w + padding)
            y_end = y_start + h
            x_end = x_start + w
            
            img = images[idx]
            result[y_start:y_end, x_start:x_end] = img
        
        # Reshape pour le format de sortie [1, height, width, channels]
        result = result.unsqueeze(0)
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "ImageGridFromBatch": ImageGridFromBatch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageGridFromBatch": "TOO Image Grid from Batch with Alpha"
}