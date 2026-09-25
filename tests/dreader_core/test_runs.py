from datetime import datetime

from dreader_core import runs


class FrozenDT(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 25, 12, 0, 0)


def test_two_runs_in_one_second_get_two_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(runs, "datetime", FrozenDT)
    ts1, d1 = runs.new_run_dir(tmp_path)
    ts2, d2 = runs.new_run_dir(tmp_path)
    assert (ts1, ts2) == ("20260925-120000", "20260925-120000-2")
    assert d1.is_dir() and d2.is_dir() and d1 != d2
    assert d1.parent == tmp_path / "runs"


def test_run_log_appends_one_line(tmp_path):
    card = tmp_path / "CARD.md"
    card.write_text("# x\n")
    runs.append_run_log(card, "- a   \n")
    assert card.read_text() == "# x\n- a\n"


def test_timestamps_round_trip():
    assert runs.parse_ts("1:02:03") == 3723
    assert runs.parse_ts("05:30") == 330
    assert runs.parse_ts("95") == 95
    assert runs.parse_ts(None) is None
    assert runs.fmt_ts(3723) == "1:02:03"
    assert runs.fmt_ts(330) == "5:30"
