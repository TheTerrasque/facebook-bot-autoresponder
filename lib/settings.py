from yaml import load

def get_settings(filename="../settings.yaml"):
    with open(filename) as f:
        return load(f)