import os
import json
import subprocess
from pathlib import Path

def run(command, get_output=False):
    """Runs a shell command."""

    if get_output:
        return subprocess.check_output(command, shell=True)
    return subprocess.call(
        command, shell=True, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


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
    return run("git status") == 0


def init_save(name):
    """Runs `git init` on a save folder."""

    if check_save_is_git(name): return
    save_loc = get_save_location() / name
    os.chdir(save_loc)
    run("git init")


def get_save_play_time(name):
    """Gets the number of minutes of play time in a save file."""
    
    save_loc = get_save_location() / name
    stats_jsons = os.listdir(save_loc / "stats")
    if len(stats_jsons) == 0:
        raise FileNotFoundError("No stats file for", name)
    with open(save_loc / "stats" / stats_jsons[0]) as f:
        stats = json.load(f)
    time = stats["stats"]["minecraft:custom"]["minecraft:play_time"]
    return round(time / 20 / 60, 2)



def get_last_save_time(name):
    """Gets the last save time from the commit messages."""

    save_loc = get_save_location() / name
    os.chdir(save_loc)
    try:
        text = run("git log", get_output=True)
    except subprocess.CalledProcessError: return 0
    last_commit_message = text.decode().split("\n\n")[1]
    try:
        return float(last_commit_message.strip())
    except ValueError: return 0


def commit_save_if_needed(name, wait=10):
    """Commits a save file if it has been long enough since last commit."""

    last_save_time = get_last_save_time(name)
    current_play_time = get_save_play_time(name)
    if current_play_time >= last_save_time + wait:
        save_loc = get_save_location() / name
        os.chdir(save_loc)
        print("Backing up", name)
        run("git add -A")
        run(f"git commit -m \"{current_play_time}\"")


def commit_saves_if_needed(wait=10):
    """Commits all save files if it has been long enough since their last
    commit."""

    saves = get_save_location()
    for loc in os.listdir(saves):
        if os.path.isdir(saves / loc) and check_save_is_git(saves / loc):
            commit_save_if_needed(loc, wait)


def watch(wait=10):
    """Continuously monitors the save files and commits when necessary."""
    
    while True:
        commit_saves_if_needed(wait=wait)


