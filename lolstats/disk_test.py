import os
import pytest
from .disk import make_dir_if_not_exists
from tempfile import TemporaryDirectory


def test_make_dir_if_not_exists():
    with TemporaryDirectory() as tmpdir:
        new_dir_path = os.path.join(tmpdir, "new_dir")
        assert not os.path.exists(new_dir_path)

        make_dir_if_not_exists(new_dir_path)

        assert os.path.exists(new_dir_path)

        # Handle existing dir
        make_dir_if_not_exists(new_dir_path)
