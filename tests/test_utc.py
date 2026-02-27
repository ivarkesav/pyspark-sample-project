from datetime import datetime, timezone
from unittest.mock import patch

from app.job import display_utc_datetime


def test_display_utc_datetime(capsys):
    fixed_time = datetime(2025, 6, 15, 12, 30, 45, tzinfo=timezone.utc)
    with patch("app.job.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_time
        mock_dt.strftime = datetime.strftime
        display_utc_datetime()

    captured = capsys.readouterr()
    assert captured.out == (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        "Current UTC date/time: 2025-06-15 12:30:45 UTC\n"
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
    )
