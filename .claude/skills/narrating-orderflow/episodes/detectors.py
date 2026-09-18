"""What Strader's mechanical detectors said at an episode's cutoff. [dr-22w.4]

The episode set has two jobs. One is practice material for narrating-orderflow.
The other is this: for each scenario a human reader can see in the tape, what
did the instrument emit? Absorption, climax and superlative come from
``market.orderflow.tape_events``; the effort/effect cell comes from
``moves.grade_atoms_developing``.

Both are run twice, from the RTH open and from the prior 17:00 Globex open,
because the sample the percentile is taken against changes the verdict — see
the finding recorded in README.md.

  python detectors.py --day 2026-08-26 --cutoff 09:28 [--window 30]
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import tape
from market.orderflow.tradesource import iter_trades                      # noqa: E402
from market.orderflow.moves import one_minute_atoms, grade_atoms_developing  # noqa: E402
from market.orderflow.tape_events import TapeEventDetector                # noqa: E402

CT = ZoneInfo("America/Chicago")


def run(day: date, cutoff: str, window: int = 30) -> dict:
    hh, mm = int(cutoff[:2]), int(cutoff[3:])
    end = tape.ct(day, hh, mm) + timedelta(minutes=1)     # cutoff minute is complete
    open_ts, _ = tape.rth_bounds(day)
    globex = tape.ct(day, 0, 0) - timedelta(hours=7)
    out = {"day": day.isoformat(), "cutoff_ct": cutoff, "window_minutes": window, "runs": {}}
    for label, start in (("from the RTH open", open_ts), ("from the Globex open", globex)):
        trades = list(iter_trades(day, start_ts=start, end_ts=end))
        if not trades:
            continue
        atoms = one_minute_atoms(trades)
        dev = grade_atoms_developing(atoms)
        det = TapeEventDetector()
        events = []
        for a, d in zip(atoms, dev):
            for ev in det.on_atom(a, d):
                events.append((a.ts.astimezone(CT), ev))
        first = end - timedelta(minutes=window)
        cells = [{"t": a.ts.astimezone(CT).strftime("%H:%M"), "volume": a.volume,
                  "delta": a.delta, "net": round(a.close - a.open, 2),
                  "effort_pct": round(d["effort_pct_dev"], 1),
                  "effect_pct": round(d["effect_pct_dev"], 1),
                  "cell": d["cell_dev"], "cell_name": d.get("cell_name_dev")}
                 for a, d in zip(atoms, dev) if a.ts.astimezone(CT) >= first]
        out["runs"][label] = {
            "atoms_in_sample": len(atoms),
            "events_in_window": [f"{t:%H:%M} {ev.kind} {ev.subtype} sig={ev.sig}"
                                 for t, ev in events if t >= first],
            "events_in_session": len(events),
            "last_minutes": cells[-8:],
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--window", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = run(date.fromisoformat(a.day), a.cutoff, a.window)
    if a.json:
        print(json.dumps(r, indent=1)); return
    print(f"{r['day']} cutoff {r['cutoff_ct']} CT — events in the last {a.window} minutes")
    for label, run_ in r["runs"].items():
        print(f"\n  {label} ({run_['atoms_in_sample']} minutes in the ranking sample, "
              f"{run_['events_in_session']} events in the session):")
        for e in run_["events_in_window"] or ["(none)"]:
            print(f"    {e}")
        print("    last minutes:")
        for c in run_["last_minutes"]:
            print(f"      {c['t']}  vol {c['volume']:6d}  d {c['delta']:+6d}  net {c['net']:+6.2f}  "
                  f"effort {c['effort_pct']:5.1f}  effect {c['effect_pct']:5.1f}  {c['cell']}")


if __name__ == "__main__":
    main()
