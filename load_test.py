import os
import json
from unittest.mock import patch, Mock, call
from tempfile import TemporaryDirectory
from load import main


def test_main():
    with TemporaryDirectory() as tmpdir:
        # Save existing match
        # -------

        saved_match_ids = ["id1", "id2"]
        matches_dir = os.path.join(tmpdir, "matches")
        os.makedirs(matches_dir)

        for match_id in saved_match_ids:
            with open(os.path.join(matches_dir, f"{match_id}.json"), "w") as f:
                f.write("dummy data")

        with patch("requests.get") as mock_get, patch(
            "builtins.print"
        ) as mock_print, patch(
            "sys.argv",
            [
                "prog",
                "--name",
                "Faker",
                "--tag",
                "t1",
                "--region",
                "asia",
                "--key",
                "testkey",
                "--output",
                tmpdir,
                "--max",
                "2",
                "--queue",
                "123",
            ],
        ):
            mock_get.side_effect = [
                Mock(
                    status_code=200, json=lambda: {"puuid": "test-puuid"}
                ),  # get_account_puuid response
                Mock(
                    status_code=200, json=lambda: ["id1", "id2", "id3", "id4"]
                ),  # get_list_of_match_ids response
                Mock(
                    status_code=200,
                    json=lambda: {
                        "metadata": {"matchId": "id3"},
                        "data": {"player": "Player1", "result": "win"},
                    },
                ),  # get_match 1 response
                Mock(
                    status_code=200,
                    json=lambda: {
                        "metadata": {"matchId": "id4"},
                        "data": {"player": "Player2", "result": "loss"},
                    },
                ),  # get_match 2 response
            ]

            main()

            assert mock_print.call_args_list == [
                call(
                    f"\n\nSuccessfully loaded match data into '{tmpdir}' directory.\n4 total matches, 2 new."
                )
            ]

            # Check user is saved
            # -------

            expected_player_file_path = os.path.join(tmpdir, "player_names.json")
            assert os.path.exists(expected_player_file_path)

            with open(expected_player_file_path, "r", encoding="utf-8") as file:
                saved_data = json.load(file)

                assert saved_data == {"test-puuid": [{"name": "Faker", "tag": "t1"}]}

            # Check matches are saved
            # --------

            # Match id3
            # --------

            expected_file_path = os.path.join(matches_dir, "id3.json")
            assert os.path.exists(expected_file_path)

            with open(expected_file_path, "r", encoding="utf-8") as file:
                saved_data = json.load(file)

                assert saved_data == {
                    "metadata": {"matchId": "id3"},
                    "data": {"player": "Player1", "result": "win"},
                }

            # Match id4
            # --------

            expected_file_path = os.path.join(matches_dir, "id4.json")
            assert os.path.exists(expected_file_path)

            with open(expected_file_path, "r", encoding="utf-8") as file:
                saved_data = json.load(file)

                assert saved_data == {
                    "metadata": {"matchId": "id4"},
                    "data": {"player": "Player2", "result": "loss"},
                }

            assert mock_get.call_args_list == [
                call(
                    "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Faker/t1?api_key=testkey",
                    timeout=10,
                ),
                call(
                    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/test-puuid/ids?api_key=testkey&start=0&count=2&endTime=&queue=123",
                    timeout=10,
                ),
                call(
                    "https://asia.api.riotgames.com/lol/match/v5/matches/id3?api_key=testkey",
                    timeout=10,
                ),
                call(
                    "https://asia.api.riotgames.com/lol/match/v5/matches/id4?api_key=testkey",
                    timeout=10,
                ),
            ]
