class TOOIntSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("INT", {"default": 0, "min": -0x7fffffffffffffff, "max": 0x7fffffffffffffff}),
                "b": ("INT", {"default": 0, "min": -0x7fffffffffffffff, "max": 0x7fffffffffffffff}),
                "swap": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("a", "b")
    FUNCTION = "execute"
    CATEGORY = "\U0001f535TOO-Pack/utils"

    def execute(self, a, b, swap):
        return (b, a) if swap else (a, b)


NODE_CLASS_MAPPINGS = {"TOOIntSwap": TOOIntSwap}
NODE_DISPLAY_NAME_MAPPINGS = {"TOOIntSwap": "TOO INT Swap"}
