import os
import subprocess
from pathlib import Path

def get_save_location():
    """Gets the location of the save files."""

    possibles = [
        os.path.expanduser("~/Library/Application Support/minecraft/saves"),
        os.path.expanduser("~/.minecraft/saves"),
    ]
    for possible in possibles:
        if os.path.exists(possible): return Path(possible)
    raise FileNotFoundError("Could not find saves")


def check_save_is_git(name):
    """Checks if a save has had `git init` run on it."""
    save_loc = get_save_location() / name
    os.chdir(save_loc)
    code = subprocess.call(
        "git status", shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return code == 0


def init_save(name):
    """Runs `git init` on a save folder."""

    if check_save_is_git(name): return
    save_loc = get_save_location() / name
    os.chdir(save_loc)
    subprocess.call(
        "git init", shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )