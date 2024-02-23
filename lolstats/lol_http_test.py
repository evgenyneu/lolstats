import pytest
from unittest.mock import patch, Mock, call
from .lol_http import send_get_request
from .errors import MyError, HttpError


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
