# Original code from: cardenluo/ComfyUI-Apt_Preset - https://github.com/cardenluo/ComfyUI-Apt_Preset
# License: Apache-2.0 (make workflow easy)

class ViewCombo:
    """
    A node that splits multiline text into individual lines with pagination support.
    Useful for viewing and processing text data in workflows.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "text"}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
                "range_str": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Range selector (takes priority if filled). Dash for ranges: '0-2' (0,1,2), '4--1' (4,3,2,1,0). Comma for specific indices: '1,4' (1 and 4 only), '1,2,5' (1,2,5 only). Negatives supported: '-1' (last), '2--1' (2 to last)"
                }),
            },
            "hidden": {
                "workflow_prompt": "PROMPT", 
                "my_unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("STRING", "COMBO", "input_count", "output_count")
    OUTPUT_IS_LIST = (True, True, False, False)
    FUNCTION = "generate_strings"
    CATEGORY = "TOO-Pack/utils"
    
    def generate_strings(self, prompt, start_index, max_rows, range_str="", workflow_prompt=None, my_unique_id=None):
        """
        Split text into lines and return a paginated subset.
        
        Args:
            prompt: Multiline text to process
            start_index: Starting line index (0-based)
            max_rows: Maximum number of lines to return
            range_str: Range string (takes priority). Examples: '0-2', '1,2,5', '2,-1', '-1,3'
            workflow_prompt: Hidden workflow context
            my_unique_id: Hidden unique identifier
            
        Returns:
            Tuple containing:
            - List of raw text lines (STRING)
            - List of numbered text lines (COMBO)
            - Total number of non-empty lines in input (input_count)
            - Number of lines returned in current page (output_count)
        """
        # Split and filter out empty lines
        lines = [line for line in prompt.split('\n') if line.strip()]
        total_lines = len(lines)
        
        # Parse range if provided
        if range_str.strip():
            rows = self._parse_range(lines, range_str.strip())
            indices = self._get_indices_from_range(range_str.strip(), total_lines)
        else:
            # Use start_index and max_rows
            start_index = max(0, min(start_index, total_lines - 1))
            end_index = min(start_index + max_rows, total_lines)
            rows = lines[start_index:end_index]
            indices = list(range(start_index, end_index))
        
        # Create numbered version for COMBO output
        combo_rows = [f"{idx}: {line}" for idx, line in zip(indices, rows)]
        
        # Total count of non-empty lines in original text
        input_count = total_lines
        
        # Count of lines actually returned
        output_count = len(rows)
        
        return (rows, combo_rows, input_count, output_count)
    
    def _parse_range(self, lines, range_str):
        """Parse range string and return selected lines."""
        total = len(lines)
        
        # Handle comma-separated format first (specific indices list)
        # This takes priority to avoid confusion with negative numbers
        if ',' in range_str:
            parts = range_str.split(',')
            indices = [int(p.strip()) for p in parts]
            # Convert negative indices
            indices = [i if i >= 0 else total + i for i in indices]
            # Filter valid indices
            indices = [i for i in indices if 0 <= i < total]
            return [lines[i] for i in indices]
        
        # Handle range format with dash: "0-2" or "4--1" (negative end)
        # Need to distinguish "4--1" from "4-1" 
        if '-' in range_str:
            # Try to parse as range
            # Look for pattern: number followed by - followed by number
            import re
            match = re.match(r'^(-?\d+)-(-?\d+)$', range_str)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                
                # Handle negative indices
                if start < 0:
                    start = total + start
                if end < 0:
                    end = total + end
                
                # Ensure valid range
                start = max(0, min(start, total - 1))
                end = max(0, min(end, total - 1))
                
                # Determine direction
                if start <= end:
                    indices = list(range(start, end + 1))
                else:
                    indices = list(range(start, end - 1, -1))
                
                return [lines[i] for i in indices if 0 <= i < total]
        
        # Single index
        try:
            idx = int(range_str)
            if idx < 0:
                idx = total + idx
            if 0 <= idx < total:
                return [lines[idx]]
        except ValueError:
            pass
        
        return []
    
    def _get_indices_from_range(self, range_str, total):
        """Get the actual indices used for numbering."""
        # Handle comma-separated format first (specific indices)
        if ',' in range_str:
            parts = range_str.split(',')
            indices = [int(p.strip()) for p in parts]
            indices = [i if i >= 0 else total + i for i in indices]
            return [i for i in indices if 0 <= i < total]
        
        # Handle range format with dash
        if '-' in range_str:
            import re
            match = re.match(r'^(-?\d+)-(-?\d+)$', range_str)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                
                if start < 0:
                    start = total + start
                if end < 0:
                    end = total + end
                
                start = max(0, min(start, total - 1))
                end = max(0, min(end, total - 1))
                
                if start <= end:
                    return list(range(start, end + 1))
                else:
                    return list(range(start, end - 1, -1))
        
        # Single index
        try:
            idx = int(range_str)
            if idx < 0:
                idx = total + idx
            if 0 <= idx < total:
                return [idx]
        except ValueError:
            pass
        
        return []


NODE_CLASS_MAPPINGS = {
    "ViewCombo": ViewCombo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ViewCombo": "View Combo 📋"
}
