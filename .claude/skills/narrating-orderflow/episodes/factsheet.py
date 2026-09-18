"""Fact-sheet builder for a narration episode. [dr-22w.4]

Implements the REVISED input contract in SKILL.md: the session's levels, the
day's character so far, each minute's effort as a multiple of the day's typical
minute plus the running maxima on each side, result as displacement over time at
the level, volume at price split by aggressor with how much of it is recent, and
whether the level is one where obvious traders act. No percentiles, no cell
names — the percentiles the first fixture carried are exactly what the contract
dropped.

Two files per episode: facts.json is everything observable at the cutoff;
aftermath.json is held back from the narrator and used only to grade.

  python factsheet.py --day 2026-08-26 --cutoff 09:28 --level 7678.75 --id ep01
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

import tape
from market.orderflow.tradesource import iter_trades              # noqa: E402
from market.orderflow.moves import Atom, segment_moves            # noqa: E402

RECENT_MINUTES = 40          # 1-minute detail handed to the narrator
VAP_MINUTES = 10             # window whose volume-at-price is split by aggressor
AFTER_MINUTES = 45


def _five_minute(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for r in rows:
        hh, mm = int(r["t"][:2]), int(r["t"][3:])
        k = f"{hh:02d}:{(mm // 5) * 5:02d}"
        if not out or out[-1]["t"] != k:
            out.append({"t": k, "o": r["o"], "h": r["h"], "l": r["l"],
                        "c": r["c"], "vol": 0, "delta": 0})
        b = out[-1]
        b["h"] = max(b["h"], r["h"]); b["l"] = min(b["l"], r["l"])
        b["c"] = r["c"]; b["vol"] += r["v"]; b["delta"] += r["d"]
    return out


def _levels_in_play(doc, prior, rows, last_price, level) -> list[dict]:
    hi = max(rows, key=lambda r: r["h"]); lo = min(rows, key=lambda r: r["l"])
    cand = [
        (hi["h"], "session high so far", True, hi["t"]),
        (lo["l"], "session low so far", True, lo["t"]),
        (doc["overnight"]["high"], "overnight high", True, None),
        (doc["overnight"]["low"], "overnight low", True, None),
        (rows[0]["o"], "today's open", True, rows[0]["t"]),
    ]
    if prior:
        cand += [(prior["rth"]["high"], "prior session high", True, None),
                 (prior["rth"]["low"], "prior session low", True, None),
                 (prior["rth"]["close"], "prior session close", True, None),
                 (prior["rth"]["poc"], "prior session most-traded price", False, None)]
    out = []
    for p, what, obvious, when in cand:
        if p is None:
            continue
        out.append({"level": p, "what": what, "distance": round(p - last_price, 2),
                    "obvious_traders_act_here": obvious, "made_at": when,
                    "is_the_level_in_question": abs(p - level) < 0.5 if level else False})
    return sorted(out, key=lambda d: abs(d["distance"]))


def _at_the_level(rows: list[dict], level: float, band: float = 0.5) -> dict:
    touched = [r for r in rows if r["l"] - band <= level <= r["h"] + band]
    visits, prev = 0, None
    for r in rows:
        inside = r["l"] - band <= level <= r["h"] + band
        if inside and not prev:
            visits += 1
        prev = inside
    first = touched[0]["t"] if touched else None
    since = rows[[r["t"] for r in rows].index(first):] if first else []
    return {
        "level": level,
        "minutes_in_contact": len(touched),
        "separate_visits": visits,
        "first_touch": first,
        "minutes_since_first_touch": len(since),
        "points_travelled_since_first_touch":
            round(max((r["h"] for r in since), default=0) - min((r["l"] for r in since), default=0), 2)
            if since else None,
        "net_since_first_touch": round(since[-1]["c"] - since[0]["o"], 2) if since else None,
    }


def build(day: date, cutoff: str, level: float | None, ep_id: str, out_dir: Path,
          defends: str | None = None) -> dict:
    doc = tape.load_day(day)
    rows = doc["atoms"]
    idx = {r["t"]: i for i, r in enumerate(rows)}
    if cutoff not in idx:
        raise SystemExit(f"{cutoff}: not a minute of {day}'s session")
    ci = idx[cutoff]                      # last COMPLETED minute the narrator sees
    seen = rows[:ci + 1]
    med = tape.running_median([r["v"] for r in seen])
    typical = med[-1]
    prior_day, prior = tape.prior_session(day)
    base = tape.trailing_baseline(day)

    # running maxima per side, and which minute set them
    max_v = max(seen, key=lambda r: r["v"])
    max_b = max(seen, key=lambda r: r["d"])
    max_s = min(seen, key=lambda r: r["d"])

    recent = []
    rb = rs = 0
    for i, r in enumerate(seen):
        rb, rs = max(rb, r["d"]), max(rs, -r["d"])
        if i > ci - RECENT_MINUTES:
            recent.append({
                "t": r["t"], "o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"],
                "volume": r["v"], "effort_x": round(r["v"] / med[i], 2) if med[i] else None,
                "delta": r["d"], "net": r["net"],
                "max_buy_minute_so_far": rb, "max_sell_minute_so_far": rs,
                "set_a_new_max": ("buy" if r["d"] == rb and rb > 0 else
                                  "sell" if -r["d"] == rs and rs > 0 else None),
            })

    # the day's own legs so far — where the big moves started
    atoms = [Atom(ts=tape.atom_time(day, r), open=r["o"], high=r["h"], low=r["l"],
                  close=r["c"], volume=r["v"], delta=r["d"]) for r in seen]
    legs = sorted(segment_moves(atoms), key=lambda m: -abs(m.net_pts))[:3]

    hi = max(seen, key=lambda r: r["h"]); lo = min(seen, key=lambda r: r["l"])
    elapsed = len(seen)
    cum_vol = sum(r["v"] for r in seen)
    typ_cum = base["median_cum_volume"].get(str(elapsed - 1))

    # volume at price, aggressor-split, over the last VAP_MINUTES
    t0 = tape.atom_time(day, rows[max(0, ci - VAP_MINUTES + 1)])
    t1 = tape.atom_time(day, rows[ci]) + timedelta(minutes=1)
    open_ts, _ = tape.rth_bounds(day)
    recent_vap: dict[float, dict] = {}
    session_vap: dict[float, int] = {}
    for t in iter_trades(day, start_ts=open_ts, end_ts=t1):
        session_vap[t.price] = session_vap.get(t.price, 0) + t.size
        if t.ts >= t0:
            c = recent_vap.setdefault(t.price, {"bought": 0, "sold": 0})
            c["bought" if t.side == "B" else "sold"] += t.size
    vap = [{"price": p, "bought": v["bought"], "sold": v["sold"],
            "delta": v["bought"] - v["sold"],
            "session_volume_at_this_price": session_vap.get(p, 0),
            "share_arrived_in_last_10_min":
                round((v["bought"] + v["sold"]) / session_vap[p], 2) if session_vap.get(p) else None}
           for p, v in sorted(recent_vap.items(), reverse=True)]

    facts = {
        "episode": {"id": ep_id, "instrument": "ES", "day": day.isoformat(),
                    "cutoff_ct": cutoff,
                    "note": "Everything here was observable at the cutoff. "
                            "The narrator knows nothing after it."},
        "prior_session": ({"date": prior_day.isoformat(), **prior["rth"]} if prior else None),
        "overnight_before_the_open": {**doc["overnight"],
                      "range": (round(doc["overnight"]["high"] - doc["overnight"]["low"], 2)
                                if doc["overnight"]["high"] is not None else None)},
        "day_character": {
            "minutes_since_open": elapsed,
            "range_so_far": round(hi["h"] - lo["l"], 2),
            "recent_days_full_range": {"median": base["median_range"],
                                       "smallest": base["min_range"],
                                       "largest": base["max_range"],
                                       "days": len(base["days"]),
                                       "from": base["days"][0], "to": base["days"][-1]},
            "volume_so_far": cum_vol,
            "typical_volume_by_this_minute": typ_cum,
            "pace_vs_typical": round(cum_vol / typ_cum, 2) if typ_cum else None,
            "typical_minute_so_far": typical,
        },
        "session_so_far": {
            "open": seen[0]["o"], "last": seen[-1]["c"],
            "high": hi["h"], "high_time": hi["t"], "low": lo["l"], "low_time": lo["t"],
            "biggest_legs": [{"from": m.start_ts.strftime("%H:%M"),
                              "to": m.end_ts.strftime("%H:%M"),
                              "start_price": m.start_price, "end_price": m.end_price,
                              "net_points": m.net_pts, "minutes": m.minutes,
                              "volume": m.effort, "delta": m.force} for m in legs],
            "busiest_minute": {"t": max_v["t"], "volume": max_v["v"], "delta": max_v["d"]},
            "biggest_buy_delta_minute": {"t": max_b["t"], "volume": max_b["v"], "delta": max_b["d"]},
            "biggest_sell_delta_minute": {"t": max_s["t"], "volume": max_s["v"], "delta": max_s["d"]},
        },
        "levels_in_play": _levels_in_play(doc, prior, seen, seen[-1]["c"], level),
        "at_the_level": _at_the_level(seen, level) if level else None,
        "five_minute_bars_so_far": _five_minute(seen),
        "last_minutes": recent,
        "volume_at_price_last_10_min": vap,
    }

    after_rows = rows[ci + 1:ci + 1 + AFTER_MINUTES]
    c = seen[-1]["c"]
    aftermath = {
        "episode": ep_id, "cutoff_ct": cutoff,
        "minutes_after": [{"t": r["t"], "o": r["o"], "h": r["h"], "l": r["l"],
                           "c": r["c"], "volume": r["v"], "delta": r["d"]} for r in after_rows],
        "path": {
            "max_up": round(max((r["h"] for r in after_rows), default=c) - c, 2),
            "max_down": round(c - min((r["l"] for r in after_rows), default=c), 2),
            "net_30m": round(after_rows[29]["c"] - c, 2) if len(after_rows) > 29 else None,
            "net_45m": round(after_rows[-1]["c"] - c, 2) if after_rows else None,
            "session_close": rows[-1]["c"],
        },
    }
    if level is not None:
        aftermath["path"]["level"] = level
        aftermath["path"]["defended_side"] = defends
        # "Went the read's way" is measured from the CUTOFF price, not from the
        # level: at 2026-08-26 09:28 price already sat 3.5 points above the
        # level it had just defended, so four points clear of the LEVEL was
        # satisfied by the next minute and said nothing.
        if defends == "low":
            through = next((r["t"] for r in after_rows if r["l"] <= level - 1.0), None)
            away = next((r["t"] for r in after_rows if r["h"] >= c + 4.0), None)
        elif defends == "high":
            through = next((r["t"] for r in after_rows if r["h"] >= level + 1.0), None)
            away = next((r["t"] for r in after_rows if r["l"] <= c - 4.0), None)
        else:
            through = away = None
        aftermath["path"]["level_gave_way_at"] = through
        aftermath["path"]["four_points_the_read_s_way_at"] = away

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "facts.json").write_text(json.dumps(facts, indent=1))
    (out_dir / "aftermath.json").write_text(json.dumps(aftermath, indent=1))
    return {"facts": facts, "aftermath": aftermath}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--level", type=float, default=None)
    ap.add_argument("--id", required=True)
    ap.add_argument("--defends", choices=("low", "high"), default=None,
                    help="which side of the level the passive trader is holding")
    ap.add_argument("--dir", default=None)
    a = ap.parse_args()
    out = Path(a.dir) if a.dir else Path(__file__).resolve().parent / a.id
    r = build(date.fromisoformat(a.day), a.cutoff, a.level, a.id, out, a.defends)
    f, af = r["facts"], r["aftermath"]
    print(f"{a.id}  {a.day} {a.cutoff} CT  level {a.level}")
    print(f"  day character: {f['day_character']['range_so_far']} pts so far vs a "
          f"{f['day_character']['recent_days_full_range']['median']}-pt median day "
          f"({f['day_character']['recent_days_full_range']['smallest']}-"
          f"{f['day_character']['recent_days_full_range']['largest']} over "
          f"{f['day_character']['recent_days_full_range']['days']} days); "
          f"pace {f['day_character']['pace_vs_typical']}x; typical minute "
          f"{f['day_character']['typical_minute_so_far']}")
    print(f"  after: up {af['path']['max_up']} / down {af['path']['max_down']} / "
          f"30m {af['path']['net_30m']} / 45m {af['path']['net_45m']}")
    print(f"  wrote {out}/facts.json, {out}/aftermath.json")


if __name__ == "__main__":
    main()
