import os


def get_template_dir():
    return os.path.join(os.path.dirname(__file__), "prompts/templates")

def get_identities_dir():
    return os.path.join(os.path.dirname(__file__), "prompts/identities")

def get_prompt_dir(sub_dir=None, file=None):
    return os.path.join(os.path.dirname(__file__), f"prompts/{sub_dir}/{file}")
