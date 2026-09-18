"""Scenario scanner — finds candidate episodes for each row of the
narrating-orderflow scenario table in Strader's ES tape. [dr-22w.4]

The four rows, operationalized. Selection uses hindsight (it may look at the
whole day to pick an episode); the fact sheet the narrator later reads never
does.

  A  absorption at a low   sell aggression into an established low-side level,
                           price will not go lower
  B  absorption at a high  buy aggression into an established high-side level,
                           price will not go higher
  C  trapped participants  either of the above where the level was made or
                           broken in the last 15 minutes — a fresh session
                           extreme or a just-taken prior-day level, i.e. the
                           spot where obvious traders have just acted
  D  acceptance            an aggressive leg, then consolidation near its
                           extreme on lower volume by time
  N  null                  effort, effect and location all unremarkable: the
                           case the narrator must refuse to force into a row

Thresholds are stated here, not tuned: a candidate list is a prompt to look,
never a verdict (SKILL.md, "detector events are prompts not verdicts"). Every
finalist is read against the tape by hand before it enters the set.

  python scan.py --start 2026-08-03 --end 2026-09-17 [--class A] [--top 12]
"""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta

import tape

# --- absorption knobs
#
# CALIBRATED AGAINST THE KNOWN CASE, 2026-08-24 10:41-42 (measured 2026-09-18):
# those two bars are 1,796 and 2,627 contracts against a 2,484 median minute —
# effort 0.9x and 1.1x a normal minute, NOT a volume surge. What made them
# absorption was one-sided AGGRESSION at a level (-615 over the two minutes,
# 56% of the day's largest sell-delta minute) and zero displacement. A volume
# threshold cannot find this case; a delta-share threshold can.
EFF_X_MIN = 0.8          # window volume vs the day's typical minute, so far
DELTA_MIN = 400          # net aggression over the window, contracts
DELTA_SHARE_MIN = 0.35   # ... or that share of the day's biggest minute, same side
DELTA_FLOOR = 250        # under this the window is not aggression at all
WARMUP = 45              # minutes of session before a "share of the day" means anything
DISP_MAX = 0.75          # points price gave the aggressor (wrong way = ok)
RANGE_MAX = 3.5          # the window has to be a stall, not a swing
LEVEL_NEAR = 2.0         # points from the level being defended
FRESH_MIN = 15           # extreme made within this many minutes = "fresh"
# --- acceptance knobs
LEG_MIN_PTS = 4.0
LEG_EFF_X = 1.3
CONS_MIN = 10            # minutes of consolidation before the cutoff
CONS_RANGE_FRAC = 0.45   # of the leg's net
CONS_VOL_FRAC = 0.70     # of the leg's volume per minute
CONS_HOLD_FRAC = 0.30    # how far back into the leg price may sag
# --- null knobs
NULL_MIN = 10
NULL_EFF_X = 0.9
NULL_DELTA_MAX = 250
NULL_RANGE_MAX = 2.5
NULL_LEVEL_FAR = 4.0
AFTER = 30               # minutes of aftermath scored for the candidate list


def refs_at(day_doc: dict, prior: dict | None, i: int) -> dict:
    """Reference levels as they stand at minute i — session extremes so far,
    the overnight range, the prior session. Causal: nothing after minute i."""
    rows = day_doc["atoms"][:i + 1]
    hi = max(rows, key=lambda r: r["h"]); lo = min(rows, key=lambda r: r["l"])
    out = {
        "session_high": (hi["h"], "session high so far", rows.index(hi)),
        "session_low": (lo["l"], "session low so far", rows.index(lo)),
        "overnight_high": (day_doc["overnight"]["high"], "overnight high", None),
        "overnight_low": (day_doc["overnight"]["low"], "overnight low", None),
    }
    if prior:
        out["prior_high"] = (prior["rth"]["high"], "prior session high", None)
        out["prior_low"] = (prior["rth"]["low"], "prior session low", None)
        out["prior_close"] = (prior["rth"]["close"], "prior session close", None)
    return {k: v for k, v in out.items() if v[0] is not None}


HIGH_SIDE = ("session_high", "overnight_high", "prior_high", "prior_close")
LOW_SIDE = ("session_low", "overnight_low", "prior_low", "prior_close")


def nearest(refs: dict, price: float, side_keys) -> tuple[str, float, float]:
    best = min(((k, refs[k][0], abs(price - refs[k][0]))
                for k in side_keys if k in refs), key=lambda t: t[2])
    return best


def aftermath(rows: list[dict], i: int, n: int = AFTER) -> dict:
    seg = rows[i + 1:i + 1 + n]
    if not seg:
        return {}
    c = rows[i]["c"]
    return {"max_up": round(max(r["h"] for r in seg) - c, 2),
            "max_down": round(c - min(r["l"] for r in seg), 2),
            "close_after": seg[-1]["c"], "net_after": round(seg[-1]["c"] - c, 2),
            "minutes": len(seg)}


def scan_day(day: date, prior_doc: dict | None) -> list[dict]:
    doc = tape.load_day(day)
    rows = doc["atoms"]
    if len(rows) < 300:
        return []
    # A day the corpus holds on a dying contract is not a quiet day, and its
    # minutes cannot be compared to anything. Measured 2026-09-18: the ES
    # capture stayed on ESU6 through 2026-09-17 while volume had moved to
    # ESZ6 — 09-16 prints 110,926 contracts against a ~1.0M median and a
    # 122.75-point range. Holidays (2026-09-07) fail the same test.
    base = tape.trailing_baseline(day)
    if base["median_volume"] and doc["rth"]["volume"] < 0.5 * base["median_volume"]:
        print(f"  {day}: skipped (volume {doc['rth']['volume']:,} is "
              f"{doc['rth']['volume'] / base['median_volume']:.0%} of the recent median "
              f"— roll, holiday or a gap in the tape)")
        return []
    med = tape.running_median([r["v"] for r in rows])
    out: list[dict] = []
    last = len(rows) - AFTER - 1
    warm_buy = max((r["d"] for r in rows[:WARMUP]), default=0)
    warm_sell = max((-r["d"] for r in rows[:WARMUP]), default=0)

    # ---------------------------------------------------- A / B / C ---
    max_buy, max_sell = max(200, warm_buy), max(200, warm_sell)
    for i in range(WARMUP, last):
        max_buy = max(max_buy, rows[i]["d"])
        max_sell = max(max_sell, -rows[i]["d"])
        refs = refs_at(doc, prior_doc, i)
        for L in (2, 3, 4, 5, 6):
            if i - L + 1 < 0:
                continue
            W = rows[i - L + 1:i + 1]
            s = tape.window_stats(W)
            eff_x = s["vol"] / (L * med[i]) if med[i] else 0
            if eff_x < EFF_X_MIN or s["range"] > RANGE_MAX:
                continue
            for sign, keys, edge, runmax in ((-1, LOW_SIDE, "low", max_sell),
                                             (1, HIGH_SIDE, "high", max_buy)):
                d = s["delta"] * sign                      # aggression with the side
                share = d / runmax
                if d < DELTA_FLOOR or (d < DELTA_MIN and share < DELTA_SHARE_MIN):
                    continue
                if sign * s["disp"] > DISP_MAX:            # it got paid: not absorption
                    continue
                key, level, dist = nearest(refs, s[edge], keys)
                if dist > LEVEL_NEAR:
                    continue
                # fresh? the level was made or taken in the last FRESH_MIN minutes
                fresh = False
                if key in ("session_high", "session_low"):
                    made_i = refs[key][2]
                    fresh = made_i is not None and (i - L + 1) - made_i <= FRESH_MIN
                else:
                    before = rows[max(0, i - L + 1 - FRESH_MIN):i - L + 1]
                    if before:
                        fresh = max(r["h"] for r in before) >= level >= min(r["l"] for r in before)
                cls = "C" if fresh else ("B" if sign > 0 else "A")
                # The level being DEFENDED is where the aggression met the wall
                # — the window's own extreme — not the named level nearby. The
                # first cut reported the named one and put the anchor two
                # points from any price that traded (2026-08-26 09:28: it named
                # the 08:30 session low 7678.75 while the fight was at 7680.50).
                # The named level travels along as the reference that makes the
                # spot an obvious one.
                defended = s[edge]
                out.append({
                    "class": cls, "day": day.isoformat(), "cutoff": rows[i]["t"],
                    "window_minutes": L, "side": "buyers" if sign > 0 else "sellers",
                    "defends": edge, "level": defended,
                    "level_kind": f"{refs[key][1]} {level:g}, {round(dist, 2):g} away",
                    "reference": refs[key][1], "reference_level": level,
                    "level_dist": round(dist, 2),
                    "effort_x": round(eff_x, 2), "delta": s["delta"],
                    "delta_share": round(share, 2), "max_same_side_minute": runmax,
                    "displacement": s["disp"], "window_range": s["range"],
                    "volume": s["vol"], "last": rows[i]["c"],
                    "score": round(share * (1.0 + DISP_MAX - sign * s["disp"])
                                   * (1.0 + LEVEL_NEAR - dist) * min(eff_x, 2.0), 2),
                    "after": aftermath(rows, i),
                })

    # ------------------------------------------------------------ D ---
    # NOT built on moves.segment_moves: a zigzag leg ENDS at its extreme, and
    # it only ends because price later retraced the reversal threshold. Taking
    # the minutes after a leg end therefore samples the start of the counter-
    # move by construction — the first cut of this scanner did exactly that and
    # produced seven acceptance candidates in two months, none of which
    # continued. Legs are read here straight off the minutes instead.
    for i in range(WARMUP, last):
        for K in (8, 10, 14):
            for M in (5, 10, 15, 20):
                j0, j1 = i - K + 1 - M, i - K
                if j0 < 0:
                    continue
                leg = rows[j0:j1 + 1]
                ls = tape.window_stats(leg)
                net = ls["disp"]
                if abs(net) < LEG_MIN_PTS or ls["range"] <= 0:
                    continue
                if abs(net) / ls["range"] < 0.6:            # one-way, not a round trip
                    continue
                leg_vpm = ls["vol"] / len(leg)
                if leg_vpm < LEG_EFF_X * med[i]:
                    continue
                C = rows[i - K + 1:i + 1]
                cs = tape.window_stats(C)
                vpm = cs["vol"] / len(C)
                up = net > 0
                near = (min(r["l"] for r in C) >= ls["close"] - CONS_HOLD_FRAC * abs(net)
                        if up else
                        max(r["h"] for r in C) <= ls["close"] + CONS_HOLD_FRAC * abs(net))
                if not near or vpm > CONS_VOL_FRAC * leg_vpm:
                    continue
                if cs["range"] > min(CONS_RANGE_FRAC * abs(net), 12.0):
                    continue
                if abs(cs["disp"]) > min(0.35 * abs(net), 6.0):
                    continue
                out.append({
                    "class": "D", "day": day.isoformat(), "cutoff": rows[i]["t"],
                    "window_minutes": K, "side": "up" if up else "down",
                    # Acceptance inverts the absorption geometry: the side being
                    # HELD is the consolidation's far edge, and the level worth
                    # watching is that edge, not the leg's extreme. An up leg
                    # accepted means dips into the consolidation low are bought;
                    # the read is wrong when that low gives way.
                    "defends": "low" if up else "high",
                    "level": (min(r["l"] for r in C) if up else max(r["h"] for r in C)),
                    "leg_end": ls["close"],
                    "level_kind": f"leg {rows[j0]['t']}\u2192{rows[j1]['t']} ({net:+g} pts, {M}m)",
                    "level_dist": 0.0, "effort_x": round(leg_vpm / med[i], 2),
                    "delta": cs["delta"], "displacement": cs["disp"],
                    "window_range": cs["range"], "volume": cs["vol"], "last": rows[i]["c"],
                    "quiet_x": round(vpm / leg_vpm, 2),
                    "score": round(abs(net) / 4 * (leg_vpm / med[i])
                                   * (1.0 + CONS_VOL_FRAC - vpm / leg_vpm)
                                   * (1.0 + CONS_RANGE_FRAC - cs["range"] / abs(net)), 2),
                    "after": aftermath(rows, i),
                })

    # ------------------------------------------------------------ N ---
    for i in range(40, last):
        W = rows[i - NULL_MIN + 1:i + 1]
        s = tape.window_stats(W)
        if s["vol"] > NULL_EFF_X * NULL_MIN * med[i] or abs(s["delta"]) > NULL_DELTA_MAX:
            continue
        if s["range"] > NULL_RANGE_MAX:
            continue
        refs = refs_at(doc, prior_doc, i)
        dist = min(abs(rows[i]["c"] - v[0]) for v in refs.values())
        if dist < NULL_LEVEL_FAR:
            continue
        prior20 = rows[max(0, i - 20):i + 1]
        if max(r["h"] for r in prior20) - min(r["l"] for r in prior20) > 5.0:
            continue
        out.append({
            "class": "N", "day": day.isoformat(), "cutoff": rows[i]["t"],
            "window_minutes": NULL_MIN, "side": "neither", "defends": None,
            "level": rows[i]["c"], "level_kind": f"nothing within {round(dist,2)} pts",
            "level_dist": round(dist, 2),
            "effort_x": round(s["vol"] / (NULL_MIN * med[i]), 2), "delta": s["delta"],
            "displacement": s["disp"], "window_range": s["range"], "volume": s["vol"],
            "last": rows[i]["c"],
            "score": round(dist * (1.0 - s["vol"] / (NULL_MIN * med[i])), 2),
            "after": aftermath(rows, i),
        })
    return out


def dedupe(cands: list[dict], apart: int = 20) -> list[dict]:
    """One candidate per cluster: the same stall fires at several window
    lengths and several adjacent minutes."""
    kept: list[dict] = []
    for c in sorted(cands, key=lambda c: -c["score"]):
        h, m = c["cutoff"].split(":")
        t = int(h) * 60 + int(m)
        if any(k["day"] == c["day"] and k["class"] == c["class"]
               and abs(t - (int(k["cutoff"][:2]) * 60 + int(k["cutoff"][3:]))) < apart
               for k in kept):
            continue
        kept.append(c)
    return kept


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--class", dest="cls", default=None)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    days = tape.corpus_days(date.fromisoformat(a.start), date.fromisoformat(a.end))
    cands: list[dict] = []
    for d in days:
        try:
            _, prior_doc = tape.prior_session(d)
            cands.extend(scan_day(d, prior_doc))
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"  {d}: skipped ({type(e).__name__}: {e})")
    kept = dedupe(cands)
    if a.out:
        json.dump(kept, open(a.out, "w"), indent=1)
    for cls in (a.cls,) if a.cls else ("A", "B", "C", "D", "N"):
        rows = [c for c in kept if c["class"] == cls][:a.top]
        print(f"\n=== class {cls} — {len([c for c in kept if c['class']==cls])} candidates, top {len(rows)}")
        print(f"{'day':11} {'cutoff':6} {'L':>2} {'side':8} {'level':>9} {'kind':26} "
              f"{'effX':>5} {'delta':>6} {'disp':>6} {'score':>7}  after(up/down/net)")
        for c in rows:
            af = c["after"]
            print(f"{c['day']:11} {c['cutoff']:6} {c['window_minutes']:2d} {c['side']:8} "
                  f"{c['level']:9g} {c['level_kind'][:26]:26} {c['effort_x']:5.2f} "
                  f"{c['delta']:6d} {c['displacement']:6.2f} {c['score']:7.2f}  "
                  f"{af.get('max_up','-')}/{af.get('max_down','-')}/{af.get('net_after','-')}")


if __name__ == "__main__":
    main()
