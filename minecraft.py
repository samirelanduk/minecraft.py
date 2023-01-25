import os

def get_save_location():
    """Gets the location of the save files."""

    possibles = [
        os.path.expanduser("~/Library/Application Support/minecraft/saves"),
        os.path.expanduser("~/.minecraft/saves"),
    ]
    for possible in possibles:
        if os.path.exists(possible): return possible
    raise FileNotFoundError("Could not find saves")