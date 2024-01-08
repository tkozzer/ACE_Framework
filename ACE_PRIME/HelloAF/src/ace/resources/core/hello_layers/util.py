import os
import json

def get_prompt_dir(sub_dir=None, file=None):
    PROMPTS = "prompts"
    if sub_dir is None and file is None:
        return os.path.join(os.path.dirname(__file__), PROMPTS)
    elif sub_dir is None:
        return os.path.join(os.path.dirname(__file__), f"{PROMPTS}/{file}")
    elif file is None:
        return os.path.join(os.path.dirname(__file__), f"{PROMPTS}/{sub_dir}")
    else:
        return os.path.join(os.path.dirname(__file__), f"{PROMPTS}/{sub_dir}/{file}")
    
def json_indent(data: dict) -> str:
    return json.dumps(data, indent=4)
