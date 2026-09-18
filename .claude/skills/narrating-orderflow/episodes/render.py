"""Render an episode's facts.json as the readable practice briefing. [dr-22w.4]

Same information the narrator's JSON carries, laid out for a human — this is
what Steve reads when he wants to try the episode himself, and what a reviewer
checks a narration against.

  python render.py ep01 > ep01/briefing.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROMPT = """You are an orderflow analyst narrating the ES futures tape for a \
discretionary trader who is watching the screen with you. It is {day}, {cutoff} \
Central. The fact sheet holds everything observable up to this moment: the prior \
session, the overnight range, the session so far, the day's character against \
recent days, 5-minute bars, 1-minute detail with each minute's effort as a \
multiple of the day's typical minute and the running biggest buy and sell \
minutes, the levels in play, and volume at price by aggressor for the last ten \
minutes with how much of each price's day arrived in them. Delta convention: \
positive = buyers lifting the offer, negative = sellers hitting the bid.

Read the file, then write the narration you would give the trader right now \
about what the tape is doing and what it means. You know nothing after {cutoff}. \
Return only the narration text."""


def table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    head = "| " + " | ".join(h for h, _ in cols) + " |"
    rule = "|" + "|".join("---" for _ in cols) + "|"
    body = ["| " + " | ".join(
        ("" if r.get(k) is None else f"{r[k]:g}" if isinstance(r.get(k), float) else str(r.get(k)))
        for _, k in cols) + " |" for r in rows]
    return "\n".join([head, rule, *body])


def main() -> None:
    d = Path(sys.argv[1])
    f = json.loads((d / "facts.json").read_text())
    e, dc, s = f["episode"], f["day_character"], f["session_so_far"]
    rr = dc["recent_days_full_range"]
    p = f["prior_session"]
    o = f["overnight_before_the_open"]
    out = [f"# Practice briefing — ES, {e['day']}, cutoff {e['cutoff_ct']} CT",
           "",
           "Everything below was observable at the cutoff; nothing after it is included. "
           "The prompt is at the bottom. The scenario this episode belongs to, what the "
           "detectors said, and what happened next are in `key.md` — do not open it until "
           "you have written your narration.",
           "", "## Session context", ""]
    if p:
        out.append(f"- Prior session {p['date']} RTH: open {p['open']:g}, high {p['high']:g}, "
                   f"low {p['low']:g}, close {p['close']:g} ({p['range']:g}-pt range), "
                   f"most-traded price {p['poc']:g}")
    if o.get("high") is not None:
        out.append(f"- Overnight, from {o['from']} CT to the open: high {o['high']:g}, "
                   f"low {o['low']:g} ({o['range']:g} pts)")
    out += [
        f"- Today opened {s['open']:g}. Session high {s['high']:g} at {s['high_time']}, "
        f"session low {s['low']:g} at {s['low_time']}. Last {s['last']:g}.",
        f"- {dc['minutes_since_open']} minutes in, the day has covered {dc['range_so_far']:g} points. "
        f"The last {rr['days']} sessions ({rr['from']} → {rr['to']}) ran {rr['smallest']:g} to "
        f"{rr['largest']:g} points, median {rr['median']:g}.",
        f"- Volume so far {dc['volume_so_far']:,} against {dc['typical_volume_by_this_minute']:,} "
        f"by this minute on a typical recent day — {dc['pace_vs_typical']}× the usual pace. "
        f"Typical minute so far: {dc['typical_minute_so_far']:,.0f} contracts.",
        f"- Busiest minute {s['busiest_minute']['t']} ({s['busiest_minute']['volume']:,}). "
        f"Biggest buy minute {s['biggest_buy_delta_minute']['t']} "
        f"({s['biggest_buy_delta_minute']['delta']:+,}), biggest sell minute "
        f"{s['biggest_sell_delta_minute']['t']} ({s['biggest_sell_delta_minute']['delta']:+,}).",
        "", "### The day's biggest legs so far", "",
        table(s["biggest_legs"], [("from", "from"), ("to", "to"), ("start", "start_price"),
                                 ("end", "end_price"), ("net", "net_points"),
                                 ("min", "minutes"), ("vol", "volume"), ("delta", "delta")]),
        "", "## Levels in play", "",
        table(f["levels_in_play"], [("level", "level"), ("what", "what"),
                                    ("distance from last", "distance"),
                                    ("obvious traders act here", "obvious_traders_act_here")]),
    ]
    if f.get("at_the_level"):
        a = f["at_the_level"]
        out += ["", "## At the level", "",
                f"- {a['level']:g}: first touched {a['first_touch']}, "
                f"{a['separate_visits']} separate visits, {a['minutes_in_contact']} minutes in contact.",
                f"- Since that first touch: {a['minutes_since_first_touch']} minutes, "
                f"{a['points_travelled_since_first_touch']:g} points of travel, "
                f"{a['net_since_first_touch']:+g} net."]
    out += ["", "## 5-minute bars, open to cutoff", "",
            table(f["five_minute_bars_so_far"],
                  [("t", "t"), ("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"),
                   ("vol", "vol"), ("delta", "delta")]),
            "", f"## 1-minute detail, last {len(f['last_minutes'])} minutes", "",
            table(f["last_minutes"],
                  [("t", "t"), ("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"),
                   ("vol", "volume"), ("effort ×", "effort_x"), ("delta", "delta"),
                   ("net", "net"), ("max buy so far", "max_buy_minute_so_far"),
                   ("max sell so far", "max_sell_minute_so_far"), ("new max", "set_a_new_max")]),
            "", "## Volume at price, last 10 minutes (aggressor split)", "",
            table(f["volume_at_price_last_10_min"],
                  [("price", "price"), ("bought (lifted offer)", "bought"),
                   ("sold (hit bid)", "sold"), ("delta", "delta"),
                   ("session vol at price", "session_volume_at_this_price"),
                   ("share from last 10 min", "share_arrived_in_last_10_min")]),
            "", "## The prompt", "", "> " + PROMPT.format(day=e["day"], cutoff=e["cutoff_ct"]).replace("\n", "\n> "),
            ""]
    print("\n".join(out))


if __name__ == "__main__":
    main()
