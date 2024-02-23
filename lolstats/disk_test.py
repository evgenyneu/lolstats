import os
import json

from .disk import (
    make_dir_if_not_exists,
    save_match,
    unsaved_matches,
    save_matches,
    save_player,
)

from tempfile import TemporaryDirectory


def test_make_dir_if_not_exists():
    with TemporaryDirectory() as tmpdir:
        new_dir_path = os.path.join(tmpdir, "new_dir")
        assert not os.path.exists(new_dir_path)

        make_dir_if_not_exists(new_dir_path)

        assert os.path.exists(new_dir_path)

        # Handle existing dir
        make_dir_if_not_exists(new_dir_path)


def test_save_match():
    with TemporaryDirectory() as tmpdir:
        match_id = "test_match_id"
        match_data = {"player": "TestPlayer", "result": "win"}

        save_match(tmpdir, match_id, match_data)

        expected_file_path = os.path.join(tmpdir, f"{match_id}.json")

        assert os.path.exists(expected_file_path)

        with open(expected_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert data == match_data


def test_unsaved_matches():
    with TemporaryDirectory() as tmpdir:
        # Simulate saving some matches
        # -------

        saved_match_ids = ["match1", "match2"]

        for match_id in saved_match_ids:
            with open(os.path.join(tmpdir, f"{match_id}.json"), "w") as f:
                f.write("dummy data")

        all_match_ids = saved_match_ids + ["match3", "match4"]

        # Check unsaved matches
        unsaved = unsaved_matches(tmpdir, all_match_ids)

        assert sorted(unsaved) == sorted(["match3", "match4"])


def test_save_matches():
    with TemporaryDirectory() as tmpdir:
        matches = [
            {
                "metadata": {"matchId": "match1"},
                "data": {"player": "Player1", "result": "win"},
            },
            {
                "metadata": {"matchId": "match2"},
                "data": {"player": "Player2", "result": "lose"},
            },
        ]

        save_matches(tmpdir, matches)

        for match in matches:
            match_id = match["metadata"]["matchId"]
            expected_file_path = os.path.join(tmpdir, f"{match_id}.json")

            assert os.path.exists(expected_file_path)

            with open(expected_file_path, "r", encoding="utf-8") as file:
                saved_data = json.load(file)
                assert saved_data == match


def test_save_player_when_file_does_not_exist():
    with TemporaryDirectory() as tmpdir:
        save_player("NewPlayer", "NP", "puuid1", tmpdir)

        file_path = os.path.join(tmpdir, "player_names.json")
        assert os.path.exists(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert data == {"puuid1": [{"name": "NewPlayer", "tag": "NP"}]}


def test_save_player_when_file_exists():
    with TemporaryDirectory() as tmpdir:
        # Prepopulate the file
        initial_data = {"puuid2": [{"name": "ExistingPlayer", "tag": "EP"}]}
        file_path = os.path.join(tmpdir, "player_names.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)

        # Add a new player
        save_player("NewPlayer", "NP", "puuid1", tmpdir)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert "puuid1" in data
            assert data["puuid1"] == [{"name": "NewPlayer", "tag": "NP"}]
            # Check existing player still there
            assert "puuid2" in data
            assert data["puuid2"] == initial_data["puuid2"]


def test_prevent_duplicate_entries():
    with TemporaryDirectory() as tmpdir:
        save_player("Player", "Tag", "puuid3", tmpdir)
        # Attempt to add the same player again
        save_player("Player", "Tag", "puuid3", tmpdir)

        file_path = os.path.join(tmpdir, "player_names.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Ensure only one entry exists for the player
            assert len(data["puuid3"]) == 1
            assert data["puuid3"] == [{"name": "Player", "tag": "Tag"}]
