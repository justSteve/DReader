#!/usr/bin/env python3
"""Grade Layer-1 extractions against daily bars and write SCORECARD.md. [dr-4ne]

Windows are pre-registered, not chosen after the fact. The letter's send
time (from letters/index.json) is converted to US Eastern; then
  recap week    the Mon–Fri week ending on the last Friday <= send date
                (what the opener's "closed up/down X%" line describes)
  forward week  trading days of the following Mon–Fri week that are strictly
                after the send date (levels and swing ideas are for these)
  swing idea    trigger must fire within the forward week; outcome measured
                5 and 10 trading days after the trigger day, plus MFE/MAE
Baselines: SPY over the same windows, and "buy Monday open" for every idea.
Monday-open arithmetic uses SPY (Yahoo's ^GSPC open is not a real print);
close-to-close uses ^GSPC.

    .venv/bin/python newsletters/tradebrigade/grade.py
"""
import glob, json, statistics as st
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
PX = pd.read_csv(HERE / "data" / "prices.csv", parse_dates=["date"])
PX["date"] = PX["date"].dt.date
BARS = {s: g.set_index("date").sort_index() for s, g in PX.groupby("symbol")}
SPX = BARS["^GSPC"]; SPY = BARS["SPY"]
TDAYS = list(SPY.index)
INDEX = json.load(open(HERE / "letters" / "index.json"))
SENT = {v["file"][:10]: v["date_full"] if "date_full" in v else None for v in INDEX.values() if "file" in v}

def et_send_date(letter_date, tid_date=None):
    """ET calendar date of the send. index.json only keeps the UTC date, so use
    the filename date and the known 00:00–01:30 UTC send slot: UTC date - 1."""
    d = pd.Timestamp(letter_date).date()
    return d - timedelta(days=1)

def weeks_of(letter_date):
    et = et_send_date(letter_date)
    fri = et - timedelta(days=(et.weekday() - 4) % 7)          # last Friday <= et
    recap = [t for t in TDAYS if fri - timedelta(days=4) <= t <= fri]
    nmon = fri + timedelta(days=3)
    fwd = [t for t in TDAYS if nmon <= t <= nmon + timedelta(days=4) and t > et]
    return recap, fwd, et

def pct(a, b): return (b / a - 1) * 100

def grade_self(ss, recap):
    if not ss.get("found") or len(recap) < 2 or ss.get("basis") == "from_all_time_high": return None
    spy = SPY.loc[recap[0]:recap[-1]]; spx = SPX.loc[recap[0]:recap[-1]]
    if spy.empty or spx.empty: return None
    mon_open_fri_close = pct(spy.iloc[0]["open"], spy.iloc[-1]["close"])
    prev_idx = TDAYS.index(recap[0]) - 1
    fri_fri = pct(SPX.loc[TDAYS[prev_idx]]["close"], spx.iloc[-1]["close"]) if prev_idx >= 0 and TDAYS[prev_idx] in SPX.index else None
    runmax = spy["high"].cummax(); p2t = float(((spy["low"] / runmax) - 1).min() * 100)
    claimed = ss["pct"] * (1 if ss["direction"] == "up" else -1 if ss["direction"] == "down" else 0)
    cands = {"monday_open_to_friday_close": mon_open_fri_close, "friday_close_to_friday_close": fri_fri, "peak_to_trough": p2t}
    if ss["basis"] == "peak_to_trough":
        return {"claimed": claimed, "basis_stated": "peak_to_trough", "actual_stated_basis": p2t, "best_basis": "peak_to_trough",
                "abs_err_best": abs(abs(p2t) - abs(claimed)), "direction_ok": None, "actual_mon_open_fri_close": mon_open_fri_close,
                "actual_fri_fri": fri_fri, "quote": ss["quote"]}
    pool = {k: v for k, v in cands.items() if v is not None and k != "peak_to_trough"}
    best = min(pool, key=lambda k: abs(pool[k] - claimed))
    return {"claimed": claimed, "basis_stated": ss["basis"], "actual_stated_basis": pool.get(ss["basis"]),
            "actual_mon_open_fri_close": mon_open_fri_close, "actual_fri_fri": fri_fri,
            "best_basis": best, "abs_err_best": abs(pool[best] - claimed),
            "direction_ok": (claimed > 0) == (pool[best] > 0) if claimed else None, "quote": ss["quote"]}

def grade_levels(levels, week):
    out = []
    if not week: return out
    for L in levels:
        lvl = L["level"]
        src = SPX if L.get("instrument") == "SPX" else SPY
        w = src.loc[week[0]:week[-1]]
        if w.empty: continue
        touched = bool(((w["low"] <= lvl) & (w["high"] >= lvl)).any())
        dist = min(abs(r["low"] - lvl) if lvl < r["low"] else abs(r["high"] - lvl) if lvl > r["high"] else 0.0
                   for _, r in w.iterrows())
        out.append({**L, "touched": touched, "min_dist_pct": dist / lvl * 100,
                    "week_close": float(w.iloc[-1]["close"]), "closed_above": bool(w.iloc[-1]["close"] > lvl)})
    return out

def idea_outcome(sym, entry_day, entry_px, direction):
    b = BARS.get(sym)
    if b is None or entry_day not in b.index: return None
    i = list(b.index).index(entry_day)
    sgn = 1 if direction == "long" else -1
    fut = b.iloc[i:i + 11]
    def r(k): return sgn * pct(entry_px, fut.iloc[k]["close"]) if len(fut) > k else None
    hi = fut["high"].max(); lo = fut["low"].min()
    mfe = sgn * pct(entry_px, hi if sgn > 0 else lo); mae = sgn * pct(entry_px, lo if sgn > 0 else hi)
    spy_i = TDAYS.index(entry_day); spyf = SPY.iloc[spy_i:spy_i + 11]
    return {"entry_day": entry_day.isoformat(), "entry_px": round(entry_px, 4), "ret_5": r(5), "ret_10": r(10),
            "mfe_10": mfe, "mae_10": mae, "days_avail": len(fut) - 1,
            "spy_ret_5": pct(spyf.iloc[0]["open"], spyf.iloc[5]["close"]) if len(spyf) > 5 else None,
            "spy_ret_10": pct(spyf.iloc[0]["open"], spyf.iloc[10]["close"]) if len(spyf) > 10 else None}

def grade_ideas(ideas, week, recap):
    out = []
    for I in ideas:
        sym = I["ticker"]; b = BARS.get(sym)
        rec = {k: v for k, v in I.items() if k != "text"}
        if b is None or not week or week[0] not in b.index:
            rec["status"] = "no_data"; out.append(rec); continue
        trig = I["trigger"]
        if I.get("trigger_relative") == "over_prior_friday_high" and recap and recap[-1] in b.index:
            trig = float(b.loc[recap[-1]]["high"]); rec["trigger_resolved"] = trig
        rec["baseline"] = idea_outcome(sym, week[0], float(b.loc[week[0]]["open"]), I["direction"])
        if trig is None:
            rec["status"] = "no_trigger"; out.append(rec); continue
        ref = float(b.loc[week[0]]["open"])
        if not 0.7 <= trig / ref <= 1.3:
            # a swing trigger sits near the current price by construction; anything else is a
            # mis-parsed number (an indicator value, a split-adjusted history) and must not be traded
            rec["status"] = "trigger_implausible"; rec["ref_open"] = ref; out.append(rec); continue
        fired = None
        for d in week:
            if d not in b.index: continue
            r = b.loc[d]
            if I["direction"] == "long" and r["high"] >= trig: fired = (d, max(float(r["open"]), trig)); break
            if I["direction"] == "short" and r["low"] <= trig: fired = (d, min(float(r["open"]), trig)); break
        if not fired:
            rec["status"] = "not_triggered"; out.append(rec); continue
        rec["status"] = "triggered"; rec["outcome"] = idea_outcome(sym, fired[0], fired[1], I["direction"])
        out.append(rec)
    return out

def summarize(rows):
    xs = [x for x in rows if x is not None]
    if not xs: return "n/a"
    return f"n={len(xs)} mean={st.mean(xs):+.2f}% median={st.median(xs):+.2f}% win={sum(x>0 for x in xs)/len(xs)*100:.0f}%"

def main():
    letters = []
    for f in sorted(glob.glob(str(HERE / "extractions" / "L1_*.json"))):
        d = json.load(open(f))
        recap, week, et = weeks_of(d["letter_date"])
        if not week: continue
        g = {"letter_date": d["letter_date"], "sent_et": et.isoformat(), "subject": d["subject"],
             "recap_week": [x.isoformat() for x in recap], "week": [x.isoformat() for x in week],
             "self": grade_self(d["self_score"], recap), "levels": grade_levels(d["spy_levels"], week),
             "ideas": grade_ideas(d["swing_ideas"], week, recap),
             "spy_week": pct(SPY.loc[week[0]]["open"], SPY.loc[week[-1]]["close"])}
        letters.append(g)
    (HERE / "data" / "graded_L1.json").write_text(json.dumps(letters, indent=1, default=str))

    selfs = [g["self"] for g in letters if g["self"]]
    lv = [L for g in letters for L in g["levels"]]
    ideas = [I for g in letters for I in g["ideas"]]
    trig = [I for I in ideas if I["status"] == "triggered" and I.get("outcome")]
    base = [I for I in ideas if I.get("baseline")]
    L = ["# Trade Brigade newsletter scorecard (Layer 1: deterministic)\n",
         f"_Generated by `grade.py` from {len(letters)} letters ({letters[0]['letter_date']} → {letters[-1]['letter_date']}). "
         "Regex extraction only; interpretive calls (lean, conditionals, scenario tables) live in the Layer-2 files. "
         "Daily bars via Yahoo (yfinance). Windows are pre-registered — see the docstring._\n",
         "## 1. The weekly recap line (his own scorekeeping)\n",
         "Each letter opens with 'The S&P closed up/down X% …'. Graded on the basis he states (Monday open → Friday close on SPY; "
         "Friday → Friday close on ^GSPC); when the stated basis is ambiguous the closer convention is used and named. "
         "'Peak to trough' lines are graded as the week's max drawdown from its running high.\n"]
    if selfs:
        errs = [s["abs_err_best"] for s in selfs]; dir_ok = [s["direction_ok"] for s in selfs if s["direction_ok"] is not None]
        L.append(f"- Lines parsed: {len(selfs)}. Direction correct: {sum(dir_ok)}/{len(dir_ok)}. "
                 f"Median abs error {st.median(errs):.2f} pp; within 0.15 pp: {sum(e <= 0.15 for e in errs)}/{len(errs)}; worse than 0.5 pp: {sum(e > 0.5 for e in errs)}.")
        bases = {}
        for s in selfs: bases[s["best_basis"]] = bases.get(s["best_basis"], 0) + 1
        L.append(f"- Best-fit basis counts: {bases}. Stated basis matched best fit {sum(s['basis_stated']==s['best_basis'] for s in selfs)}/{len(selfs)} times.\n")
        L.append("| letter | recap week | claimed | Mon-open→Fri-close (SPY) | Fri→Fri (SPX) | best fit | err (pp) |\n|---|---|---:|---:|---:|---|---:|")
        for g in letters:
            s = g["self"]
            if s:
                ff = s['actual_fri_fri']
                L.append(f"| {g['letter_date']} | {g['recap_week'][0]}→{g['recap_week'][-1]} | {s['claimed']:+.2f}% | {s['actual_mon_open_fri_close']:+.2f}% | "
                         f"{(ff if ff is not None else float('nan')):+.2f}% | {s['best_basis'].split('_')[0]} | {s['abs_err_best']:.2f} |")
    L.append("\n## 2. SPY levels named for the week ahead\n")
    L.append("Every SPY price in the SPY sections, classed by the sentence's keywords. 'Touched' = the level fell inside a daily range during the forward week. "
             "A named level that price never approaches is decoration; one that is touched and then behaves as described is information.\n")
    if lv:
        by = {}
        for x in lv: by.setdefault(x["class"], []).append(x)
        L.append("| class | n | touched | median distance when missed |\n|---|---:|---:|---:|")
        for c, xs in sorted(by.items()):
            missed = [x["min_dist_pct"] for x in xs if not x["touched"]]
            L.append(f"| {c} | {len(xs)} | {sum(x['touched'] for x in xs)/len(xs)*100:.0f}% | {st.median(missed):.2f}% |" if missed else f"| {c} | {len(xs)} | 100% | – |")
        holds = [x for x in lv if x["class"] == "hold"]; th = [x for x in holds if x["touched"]]
        if holds:
            L.append(f"\n- 'Hold' levels: {sum(x['closed_above'] for x in holds)}/{len(holds)} saw SPY close the week above them. "
                     f"Of the {len(th)} that were actually tested, {sum(x['closed_above'] for x in th)} held into Friday's close.")
        brk = [x for x in lv if x["class"] == "break"]; tb = [x for x in brk if x["touched"]]
        if brk:
            L.append(f"- 'Break' levels: {len(tb)}/{len(brk)} were reached; of those, SPY closed the week below {sum(not x['closed_above'] for x in tb)}.")
    L.append("\n## 3. Swing stock scans\n")
    L.append("One paragraph per ticker in 'Swing Stock Scans'. Where a trigger price parses ('over 311', 'over Friday's high'), the idea is entered on the first forward-week day that trades through it, "
             "at the open if it gapped through. Returns are close-to-entry after 5 and 10 trading days; MFE/MAE are the best and worst excursions inside 10 days. "
             "Baseline: the same ticker bought at the forward week's first open with no trigger, and SPY over the same window.\n")
    st_ = {}
    for I in ideas: st_[I["status"]] = st_.get(I["status"], 0) + 1
    L.append(f"- Ideas: {len(ideas)} across {len(letters)} letters; status counts: {st_}.")
    if trig:
        L.append(f"- Triggered ideas, 5-day return: {summarize([I['outcome']['ret_5'] for I in trig])}")
        L.append(f"- Triggered ideas, 10-day return: {summarize([I['outcome']['ret_10'] for I in trig])}")
        L.append(f"- SPY over the same 10-day windows: {summarize([I['outcome']['spy_ret_10'] for I in trig])}")
        L.append(f"- Triggered ideas MFE/MAE (10d): mean best {st.mean([I['outcome']['mfe_10'] for I in trig]):+.2f}%, mean worst {st.mean([I['outcome']['mae_10'] for I in trig]):+.2f}%")
    if base:
        L.append(f"- ALL ideas bought at the first open, 10-day return: {summarize([I['baseline']['ret_10'] for I in base])}")
        L.append(f"- SPY over those windows: {summarize([I['baseline']['spy_ret_10'] for I in base])}")
    L.append("\n### Triggered ideas\n\n| letter | ticker | dir | trigger | entered | entry | 5d | 10d | MFE | MAE | SPY 10d |\n|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|")
    fmt = lambda v: "–" if v is None else f"{v:+.1f}%"
    for g in letters:
        for I in g["ideas"]:
            if I["status"] != "triggered": continue
            o = I["outcome"]
            L.append(f"| {g['letter_date']} | {I['ticker']} | {I['direction']} | {I.get('trigger_resolved', I['trigger'])} | {o['entry_day']} | {o['entry_px']} | {fmt(o['ret_5'])} | {fmt(o['ret_10'])} | {fmt(o['mfe_10'])} | {fmt(o['mae_10'])} | {fmt(o['spy_ret_10'])} |")
    L.append("\n## 4. Per-letter\n\n| letter | sent (ET) | subject | forward week SPY | levels (touched) | ideas (triggered) |\n|---|---|---|---:|---:|---:|")
    for g in letters:
        L.append(f"| {g['letter_date']} | {g['sent_et']} | {g['subject'][:44]} | {g['spy_week']:+.2f}% | {len(g['levels'])} ({sum(x['touched'] for x in g['levels'])}) | "
                 f"{len(g['ideas'])} ({sum(I['status']=='triggered' for I in g['ideas'])}) |")
    (HERE / "SCORECARD.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:34]))

if __name__ == "__main__":
    main()
