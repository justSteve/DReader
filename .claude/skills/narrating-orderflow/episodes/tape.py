"""Read-only door onto Strader's ES tape for the narration episode set. [dr-22w.4]

DReader owns nothing in Strader's repo: this imports ``market.orderflow`` and
reads the corpus, and writes only into this directory's ``.cache``
(gitignored). Everything downstream — the scanner and the fact-sheet builder —
goes through here so there is one definition of "the day" and one delta
convention (Databento: side 'B' = buy aggressor lifting the offer, 'A' = sell
aggressor hitting the bid; delta = buy - sell).
"""
from __future__ import annotations

import json
import os
import statistics
from bisect import insort
from datetime import date as _date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import sys

STRADER = os.environ.get("STRADER_ROOT", "/root/projects/Strader")
if STRADER not in sys.path:
    sys.path.insert(0, STRADER)

from market.orderflow.tradesource import iter_trades          # noqa: E402
from market.orderflow.moves import one_minute_atoms           # noqa: E402

CT = ZoneInfo("America/Chicago")
RTH_OPEN = (8, 30)
RTH_CLOSE = (15, 0)
CORPUS = Path(STRADER) / "data" / "corpus"
CACHE = Path(os.environ.get("EPISODE_CACHE",
                            Path(__file__).resolve().parent / ".cache"))


def ct(day: _date, hh: int, mm: int) -> datetime:
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=CT)


def rth_bounds(day: _date) -> tuple[datetime, datetime]:
    return ct(day, *RTH_OPEN), ct(day, *RTH_CLOSE)


def corpus_days(start: _date, end: _date) -> list[_date]:
    """Every corpus day in [start, end] that actually holds an ES file."""
    out = []
    for p in sorted(CORPUS.iterdir()):
        if not p.is_dir() or len(p.name) != 10 or not p.name[0].isdigit():
            continue
        d = _date.fromisoformat(p.name)
        if not (start <= d <= end):
            continue
        if any(f.name.startswith("databento_glbx_es") for f in p.iterdir()):
            out.append(d)
    return out


# ------------------------------------------------------------------ day ---
def load_day(day: _date, *, refresh: bool = False) -> dict:
    """RTH minute atoms + the overnight range, cached as JSON.

    Atoms are plain dicts (t = 'HH:MM' CT) so the cache is readable and the
    scanner never depends on Strader's dataclass shape.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{day.isoformat()}.json"
    if f.exists() and not refresh:
        return json.loads(f.read_text())

    open_ts, close_ts = rth_bounds(day)
    trades = list(iter_trades(day, start_ts=open_ts, end_ts=close_ts))
    if not trades:
        raise FileNotFoundError(f"{day}: no RTH prints")
    atoms = one_minute_atoms(trades)
    rows = [{"t": a.ts.astimezone(CT).strftime("%H:%M"), "o": a.open, "h": a.high,
             "l": a.low, "c": a.close, "v": a.volume, "d": a.delta,
             "net": round(a.close - a.open, 2), "rng": round(a.high - a.low, 2)}
            for a in atoms]

    hi = max(trades, key=lambda t: t.price)
    lo = min(trades, key=lambda t: t.price)
    # Overnight spans TWO corpus files. A corpus day is a calendar day in CT
    # (00:00-23:59), so the evening session that opens at 17:00 lives in the
    # PREVIOUS day's file — measured 2026-09-18, and the reason the first
    # fixture's "overnight (Sun 17:00 -> 08:30)" range was really a
    # midnight-to-open range. Whatever the files actually hold is reported in
    # `from`, because some days are missing their evening or their early hours
    # (2026-08-28 starts at 03:31; 2026-08-03 has nothing before the open).
    on = {"high": None, "low": None, "from": None}

    def _take(ts, price):
        on["high"] = price if on["high"] is None else max(on["high"], price)
        on["low"] = price if on["low"] is None else min(on["low"], price)
        if on["from"] is None:
            on["from"] = ts.astimezone(CT).strftime("%m-%d %H:%M")

    # ONLY the immediately preceding calendar day. Walking further back to
    # find an evening session silently splices a stale one in: 2026-08-31 is a
    # Monday whose Sunday reopen is missing from the corpus, and a two-day
    # search labelled the previous THURSDAY evening as its overnight range.
    prev = day - timedelta(days=1)
    evening = False
    if (CORPUS / prev.isoformat()).is_dir():
        try:
            for t in iter_trades(prev, start_ts=ct(prev, 17, 0)):
                _take(t.ts, t.price)
                evening = True
        except (FileNotFoundError, ValueError):
            pass
    for t in iter_trades(day, end_ts=open_ts):
        _take(t.ts, t.price)
    on["evening_session_present"] = evening

    vap: dict[str, int] = {}
    for t in trades:
        vap[str(t.price)] = vap.get(str(t.price), 0) + t.size
    poc = max(vap.items(), key=lambda kv: kv[1])

    day_doc = {
        "day": day.isoformat(),
        "rth": {"open": trades[0].price, "close": trades[-1].price,
                "high": hi.price, "high_t": hi.ts.astimezone(CT).strftime("%H:%M:%S"),
                "low": lo.price, "low_t": lo.ts.astimezone(CT).strftime("%H:%M:%S"),
                "range": round(hi.price - lo.price, 2),
                "volume": sum(a.volume for a in atoms),
                "poc": float(poc[0]), "poc_volume": poc[1]},
        "overnight": on,
        "atoms": rows,
    }
    f.write_text(json.dumps(day_doc))
    return day_doc


def prior_session(day: _date) -> tuple[_date, dict] | tuple[None, None]:
    """The most recent day BEFORE ``day`` that actually has an RTH session —
    a Saturday file exists in the corpus and holds no RTH prints."""
    for d in reversed(corpus_days(day - timedelta(days=10), day - timedelta(days=1))):
        try:
            return d, load_day(d)
        except (FileNotFoundError, ValueError):
            continue
    return None, None


def trailing_baseline(day: _date, n: int = 10) -> dict:
    """What a 'typical day' looks like around here — the comparison set the
    skill's scale rules demand for day character. Median RTH range, median RTH
    volume, and the median cumulative volume at each elapsed minute (the pace
    curve a session-so-far figure is read against).

    TEN days, not twenty, and the spread travels with the median. Measured
    2026-09-18: a 20-day window ending 2026-08-26 spans a regime change —
    137, 129 and 113-point days in late July beside 25 and 31-point days in
    late August — and its 44-point median describes no day in either half.
    The skill's own rule is that a cross-day comparison names its day type or
    is not made; min and max are carried so the fact sheet can say whether the
    median means anything."""
    days = [d for d in corpus_days(day - timedelta(days=60), day - timedelta(days=1))]
    ranges, volumes, cum_by_min = [], [], {}
    used = []
    for d in reversed(days):
        if len(used) >= n:
            break
        try:
            doc = load_day(d)
        except (FileNotFoundError, ValueError):
            continue
        if len(doc["atoms"]) < 200:          # a half day or a broken tape
            continue
        used.append(d.isoformat())
        ranges.append(doc["rth"]["range"])
        volumes.append(doc["rth"]["volume"])
        run = 0
        for i, a in enumerate(doc["atoms"]):
            run += a["v"]
            cum_by_min.setdefault(i, []).append(run)
    return {
        "days": sorted(used),
        "median_range": round(statistics.median(ranges), 2) if ranges else None,
        "min_range": min(ranges) if ranges else None,
        "max_range": max(ranges) if ranges else None,
        "median_volume": int(statistics.median(volumes)) if volumes else None,
        "median_cum_volume": {str(i): int(statistics.median(v))
                              for i, v in sorted(cum_by_min.items())},
    }


# -------------------------------------------------------------- helpers ---
def running_median(values: list[int]) -> list[float]:
    """Median of values[0:i+1] for each i — the day's typical minute *so far*,
    which is what a live narrator would have."""
    out, keep = [], []
    for v in values:
        insort(keep, v)
        m = len(keep)
        out.append(keep[m // 2] if m % 2 else (keep[m // 2 - 1] + keep[m // 2]) / 2)
    return out


def atom_time(day: _date, row: dict) -> datetime:
    hh, mm = row["t"].split(":")
    return ct(day, int(hh), int(mm))


def window_stats(rows: list[dict]) -> dict:
    return {"vol": sum(r["v"] for r in rows), "delta": sum(r["d"] for r in rows),
            "open": rows[0]["o"], "close": rows[-1]["c"],
            "high": max(r["h"] for r in rows), "low": min(r["l"] for r in rows),
            "disp": round(rows[-1]["c"] - rows[0]["o"], 2),
            "range": round(max(r["h"] for r in rows) - min(r["l"] for r in rows), 2)}
