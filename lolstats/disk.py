"""Save match data to disk"""

import json
import os
import glob


def make_dir_if_not_exists(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_match(directory, id, match):
    """
    Save match to disk.

    Parameters
    ----------
    directory : str
      Path to directory where the match is saved.

    id : str
      Match id.

    match : dict
      Match data.
    """

    filename = f"{directory}/{id}.json"
    make_dir_if_not_exists(directory)

    # Save the match
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(match, file, indent=2)


def unsaved_matches(directory, ids):
    """
    Return the list of match IDs for matches that are not saved to disk.

    Parameters
    ----------
    directory: str
      Directory where the matches are stored.

    ids : list os str
     List of match IDs.

    Returns
    -------
    list of str
      List of match IDs for matches that are not saved to disk.
    """

    if os.path.exists(directory):
        existing_files = os.listdir(directory)
    else:
        existing_files = []

    return [id for id in ids if f"{id}.json" not in existing_files]


def save_matches(directory, matches):
    """
    Save matches to disk.

    Parameters
    ----------
    directory : str
      Path to directory where the match is saved.

    matches : list of dict
      List of match dictionaries, where each dictionary contains match details.
    """

    for match in matches:
        id = match["metadata"]["matchId"]
        save_match(directory=directory, id=id, match=match)


def remove_all_files(directory):
    """
    Removes all files in a directory.

    Parameters
    ----------
    directory: str
      Directory where the matches are stored.
    """
    files = glob.glob(os.path.join(directory, "*"))

    for f in files:
        if os.path.isfile(f):
            os.remove(f)


def save_player(name, tag, puuid, directory):
    """
    Save a player's name and tag to a mapping based on their puuid
    and store it to disk in JSON format.

    Parameters
    ----------
    name : str
        Gamer name part from Riot ID: Name#Tag
    tag : str
        Gamer tag line part from Riot ID: Name#Tag
    puuid : str
        The player's unique identifier.
    directory : str
        The directory where data will be stored.
    """
    make_dir_if_not_exists(directory)
    file_path = os.path.join(directory, "player_names.json")

    # Load existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Update the data with the new player information
    if puuid not in data:
        data[puuid] = []

    # Prepare the player entry
    new_entry = {"name": name, "tag": tag}

    # Check for duplicate entry
    if new_entry not in data[puuid]:
        data[puuid].append(new_entry)

    # Write the updated data back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
