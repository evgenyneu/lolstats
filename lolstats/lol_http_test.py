import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock, call

from lolstats.lol_http import (
    send_get_request,
    get_account_puuid,
    get_list_of_match_ids,
    get_match,
    get_matches,
)

from lolstats.errors import MyError, HttpError


@patch(
    "requests.get", return_value=Mock(status_code=200, json=lambda: {"key": "value"})
)
def test_send_get_request_success(mock_get):
    response = send_get_request("http://example.com")

    assert response == {"key": "value"}


@patch("requests.get", return_value=Mock(status_code=401, reason="Unauthorized"))
def test_send_get_request_unauthorised(mock_get):
    with pytest.raises(MyError) as excinfo:
        send_get_request("http://example.com")

    assert "401 Unauthorized. Your API key is missing or incorrect." in str(
        excinfo.value
    )


@patch("requests.get", return_value=Mock(status_code=403, reason="Forbidden"))
def test_send_get_request_forbidden(mock_get):
    with pytest.raises(MyError) as excinfo:
        send_get_request("http://example.com")

    assert "403 Forbidden. Your API key has expired." in str(excinfo.value)


@patch("time.sleep", return_value=None)
@patch(
    "requests.get",
    side_effect=[
        Mock(status_code=429, reason="Too Many Requests"),  # First attempt
        Mock(status_code=200, json=lambda: {"key": "value"}),  # Second attempt
    ],
)
def test_send_get_request_rate_limit_exceeded_and_success(mock_get, mock_sleep):
    response = send_get_request("http://example.com")

    assert response == {"key": "value"}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_with(10)


@patch("time.sleep", return_value=None)
@patch("requests.get", return_value=Mock(status_code=429, reason="Too Many Requests"))
def test_send_get_request_max_retries_exceeded(mock_get, mock_sleep):
    with pytest.raises(MyError) as excinfo:
        send_get_request("http://example.com", max_retries=3, retry_delay=1)

    assert "Max retries exceeded." in str(excinfo.value)
    assert mock_get.call_count == 3

    # Verify time.sleep was called correctly with doubling delay
    expected_calls = [call(1), call(2), call(4)]
    assert mock_sleep.call_args_list == expected_calls


@patch("lolstats.lol_http.send_get_request", return_value={"puuid": "test-puuid"})
def test_get_account_puuid_success(mock_send_get_request):
    puuid = get_account_puuid("americas", "PlayerName", "PlayerTag", "testkey")

    assert puuid == "test-puuid"

    mock_send_get_request.assert_called_with(
        "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/PlayerName/PlayerTag?api_key=testkey"
    )


@patch("lolstats.lol_http.send_get_request", side_effect=HttpError("Not Found", 404))
def test_get_account_puuid_not_found(mock_send_get_request):
    with pytest.raises(MyError) as excinfo:
        get_account_puuid("americas", "UnknownPlayer", "UnknownTag", "api_key")

    assert "Player UnknownPlayer#UnknownTag not found" in str(excinfo.value)


@patch(
    "lolstats.lol_http.send_get_request",
    side_effect=HttpError("Internal Server Error", 500),
)
def test_get_account_puuid_http_error(mock_send_get_request):
    with pytest.raises(HttpError) as excinfo:
        get_account_puuid("americas", "PlayerName", "PlayerTag", "api_key")

    assert "Internal Server Error" == str(excinfo.value)
    assert excinfo.value.status_code == 500


@patch("lolstats.lol_http.send_get_request", return_value=[1, 2, 3])
def test_get_list_of_match_ids(mock_send_get_request):
    result = get_list_of_match_ids(
        route="americas", puuid="puuid123", api_key="testkey"
    )

    assert result == [1, 2, 3]

    mock_send_get_request.assert_called_with(
        "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/puuid123/ids?api_key=testkey&start=0&count=20&endTime=&queue="
    )


@patch("lolstats.lol_http.send_get_request", return_value=[1, 2, 3])
def test_get_list_of_match_ids_with_all_params(mock_send_get_request):
    result = get_list_of_match_ids(
        route="americas",
        puuid="puuid123",
        api_key="testkey",
        start=5,
        count=15,
        end_time=123,
        queue=456,
    )

    assert result == [1, 2, 3]

    mock_send_get_request.assert_called_with(
        "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/puuid123/ids?api_key=testkey&start=5&count=15&endTime=123&queue=456"
    )


@patch("lolstats.lol_http.send_get_request", return_value={"data": 123})
def test_get_match(mock_send_get_request):
    result = get_match(route="americas", id="match123", api_key="testkey")

    assert result == {"data": 123}

    mock_send_get_request.assert_called_with(
        "https://americas.api.riotgames.com/lol/match/v5/matches/match123?api_key=testkey"
    )


# @patch("lolstats.lol_http.send_get_request", return_value={"data": 1})
# def test_get_matches(mock_send_get_request):
#     result = get_matches(route="americas", ids=["a", "b", "c"], api_key="testkey")

#     assert result == [1, 2, 3]

#     mock_send_get_request.assert_called_with(
#         "https://americas.api.riotgames.com/lol/match/v5/matches/match123?api_key=testkey"
#     )


@patch(
    "lolstats.lol_http.send_get_request",
    side_effect=[{"data": 1}, {"data": 2}, {"data": 3}],
)
def test_get_matches(mock_send_get_request):
    result = get_matches(route="americas", ids=["a", "b", "c"], api_key="testkey")

    assert result == [{"data": 1}, {"data": 2}, {"data": 3}]

    expected_calls = [
        call(
            "https://americas.api.riotgames.com/lol/match/v5/matches/a?api_key=testkey"
        ),
        call(
            "https://americas.api.riotgames.com/lol/match/v5/matches/b?api_key=testkey"
        ),
        call(
            "https://americas.api.riotgames.com/lol/match/v5/matches/c?api_key=testkey"
        ),
    ]

    assert mock_send_get_request.call_args_list == expected_calls
