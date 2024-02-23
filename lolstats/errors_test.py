import pytest
from lolstats.errors import MyError, HttpError


def test_my_error_can_be_raised():
    with pytest.raises(MyError) as exc_info:
        raise MyError("An error occurred")

    assert str(exc_info.value) == "An error occurred"


def test_http_error_can_be_raised_with_status_code():
    with pytest.raises(HttpError) as exc_info:
        raise HttpError("Not Found", 404)

    assert str(exc_info.value) == "Not Found"
    assert exc_info.value.status_code == 404
