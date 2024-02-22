"""Save match data to disk"""

import json
import os
import glob


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

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the match
    with open(filename, "w") as file:
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
