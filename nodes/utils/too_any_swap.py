class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class TOOAnySwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (any_type,),
                "b": (any_type,),
                "swap": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = (any_type, any_type)
    RETURN_NAMES = ("a", "b")
    FUNCTION = "execute"
    CATEGORY = "\U0001f535TOO-Pack/utils"

    def execute(self, a, b, swap):
        return (b, a) if swap else (a, b)


NODE_CLASS_MAPPINGS = {"TOOAnySwap": TOOAnySwap}
NODE_DISPLAY_NAME_MAPPINGS = {"TOOAnySwap": "TOO Any Swap"}
