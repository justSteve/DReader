#!/usr/bin/env python3
"""Grade Layer-2 (interpretive) extractions and append to SCORECARD.md. [dr-4ne]

Rules are closed and mechanical once the reader has classed a call:
  hold_week              instrument closes the forward week above level
  no_acceptance_below    no daily close below level during the forward week
  break_then_lower       if a daily close < level occurs, Friday close < that close
  break_then_target      if a daily close < level occurs, a target is touched afterwards in the week
  reclaim_then_higher    if a daily close > level occurs, Friday close > that close
  reclaim_then_target    if a daily close > level occurs, a target is touched afterwards
  look_below_and_reclaim week low < level AND Friday close > level
  below_week             instrument closes the forward week below level
  range_hold             Friday close inside [low, high]
  target_reached         level touched within the forward week
Lean is graded on SPY Friday-to-Friday close of the forward week.
Validation: every level must appear verbatim in the letter text.
"""
import glob, json, re
from datetime import timedelta
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
PX = pd.read_csv(HERE / "data" / "prices.csv", parse_dates=["date"]); PX["date"] = PX["date"].dt.date
BARS = {s: g.set_index("date").sort_index() for s, g in PX.groupby("symbol")}
TDAYS = list(BARS["SPY"].index)

def fwd_week(letter_date):
    et = pd.Timestamp(letter_date).date() - timedelta(days=1)
    fri = et - timedelta(days=(et.weekday() - 4) % 7); nmon = fri + timedelta(days=3)
    return [t for t in TDAYS if nmon <= t <= nmon + timedelta(days=4) and t > et], fri

def appears(level, text):
    s = f"{level:.2f}"; alts = {s, s.rstrip("0").rstrip("."), f"{level:g}"}
    return any(a in text for a in alts)

def grade_call(c, w, prev_close):
    sym = c["instrument"]; b = BARS.get(sym)
    if b is None: return {"outcome": "no_data"}
    d = b.loc[w[0]:w[-1]]
    if d.empty: return {"outcome": "no_data"}
    lvl = c.get("level"); fri = float(d.iloc[-1]["close"]); lo = float(d["low"].min()); hi = float(d["high"].max())
    touched = lambda L: bool(((d["low"] <= L) & (d["high"] >= L)).any())
    r = c["rule"]; res = {"week_low": lo, "week_high": hi, "week_close": fri}
    if r == "hold_week":
        res["outcome"] = "pass" if fri > lvl else "fail"; res["touched"] = touched(lvl)
    elif r == "no_acceptance_below":
        below = d[d["close"] < lvl]; res["outcome"] = "pass" if below.empty else "fail"
        if not below.empty: res["first_close_below"] = below.index[0].isoformat()
    elif r in ("break_then_lower", "break_then_target"):
        below = d[d["close"] < lvl]
        if below.empty: res["outcome"] = "not_triggered"
        else:
            day = below.index[0]; c0 = float(below.iloc[0]["close"]); after = d.loc[day:].iloc[1:]
            res["triggered_on"] = day.isoformat()
            if r == "break_then_lower": res["outcome"] = "pass" if fri < c0 else "fail"
            else:
                hit = any(((after["low"] <= t) & (after["high"] >= t)).any() for t in c.get("targets", [])) if not after.empty else False
                res["outcome"] = "pass" if hit else ("fail" if not after.empty else "no_days_after")
    elif r in ("reclaim_then_higher", "reclaim_then_target"):
        above = d[d["close"] > lvl]
        if above.empty: res["outcome"] = "not_triggered"
        else:
            day = above.index[0]; c0 = float(above.iloc[0]["close"]); after = d.loc[day:].iloc[1:]
            res["triggered_on"] = day.isoformat()
            if r == "reclaim_then_higher": res["outcome"] = "pass" if fri > c0 else "fail"
            else:
                hit = any(((after["low"] <= t) & (after["high"] >= t)).any() for t in c.get("targets", [])) if not after.empty else False
                res["outcome"] = "pass" if hit else ("fail" if not after.empty else "no_days_after")
    elif r == "look_below_and_reclaim":
        res["outcome"] = "pass" if (lo < lvl and fri > lvl) else ("fail" if lo < lvl else "not_triggered")
    elif r == "below_week":
        res["outcome"] = "pass" if fri < lvl else "fail"; res["touched"] = touched(lvl)
    elif r == "range_hold":
        res["outcome"] = "pass" if c["low"] <= fri <= c["high"] else "fail"
    elif r == "target_reached":
        res["outcome"] = "pass" if touched(lvl) else "fail"
    else:
        res["outcome"] = "unknown_rule"
    return res

def grade_scenario(s):
    day = pd.Timestamp(s["grade_day"]).date(); y = BARS[s["yield_symbol"]]; m = BARS[s["market_symbol"]]
    i = TDAYS.index(day)
    yprev, ynow = float(y.loc[TDAYS[i - 1]]["close"]), float(y.loc[day]["close"])
    mprev = float(m.loc[TDAYS[i - 1]]["close"]); mo, mc = float(m.loc[day]["open"]), float(m.loc[day]["close"])
    ydir = "up" if ynow > yprev else "down" if ynow < yprev else "flat"
    mdir_cc = "up" if mc > mprev else "down"; mdir_oc = "up" if mc > mo else "down"
    return {"yield_prev": yprev, "yield_close": ynow, "yield_dir": ydir, "yield_ok": ydir == s["predicted_yield"],
            "mkt_prev_close": mprev, "mkt_open": mo, "mkt_close": mc, "mkt_dir_close_to_close": mdir_cc,
            "mkt_dir_open_to_close": mdir_oc, "mkt_ok_close_to_close": mdir_cc == s["predicted_market"],
            "mkt_ok_open_to_close": mdir_oc == s["predicted_market"]}

def main():
    letters = []
    for f in sorted(glob.glob(str(HERE / "extractions" / "L2_*.json"))):
        d = json.load(open(f)); w, fri = fwd_week(d["letter_date"])
        text = next(Path(HERE / "letters").glob(f"{d['letter_date']}_*.txt")).read_text()
        spy = BARS["SPY"]; pdays = [x for x in TDAYS if x <= fri]
        prev_close = float(spy.loc[pdays[-1]]["close"]) if pdays else None
        wk_ret = (float(spy.loc[w[-1]]["close"]) / prev_close - 1) * 100 if prev_close and w else None
        lean = d["lean"]; lean_ok = None
        if wk_ret is not None and lean["direction"] in ("bullish", "bearish"):
            lean_ok = (wk_ret > 0) == (lean["direction"] == "bullish")
        calls = []
        for c in d["calls"]:
            bad = [L for L in [c.get("level")] + c.get("targets", []) + [c.get("low"), c.get("high")] if L is not None and not appears(L, text)]
            g = grade_call(c, w, prev_close) if w else {"outcome": "no_week"}
            calls.append({**c, "validated": not bad, "unvalidated_levels": bad, **g})
        scen = [{**s, "result": grade_scenario(s)} for s in d.get("scenarios", []) if s.get("grade_day")]
        letters.append({"letter_date": d["letter_date"], "week": [x.isoformat() for x in w], "spy_week_ret": wk_ret,
                        "lean": lean, "lean_ok": lean_ok, "calls": calls, "scenarios": scen})
    (HERE / "data" / "graded_L2.json").write_text(json.dumps(letters, indent=1, default=str))
    L = ["\n## 5. Layer 2 — interpretive calls (read by Claude, graded by rule)\n",
         "Each recent letter was read in full and its conditional statements classed into closed rule types (see `grade2.py`). "
         "Every level was checked to appear verbatim in the letter. Lean is graded on SPY's Friday-to-Friday return for the forward week.\n",
         "| letter | lean | conv. | hedged | SPY week | lean ok | calls pass/fail/not-trig |\n|---|---|---|---|---:|---|---|"]
    for g in letters:
        oc = [c["outcome"] for c in g["calls"]]
        L.append(f"| {g['letter_date']} | {g['lean']['direction']} | {g['lean']['conviction']} | {'yes' if g['lean']['hedged'] else 'no'} | "
                 f"{(g['spy_week_ret'] if g['spy_week_ret'] is not None else float('nan')):+.2f}% | {'✓' if g['lean_ok'] else '✗' if g['lean_ok'] is False else '–'} | "
                 f"{oc.count('pass')}/{oc.count('fail')}/{oc.count('not_triggered')} |")
    L.append("\n| letter | call | rule | level | outcome | detail |\n|---|---|---|---:|---|---|")
    for g in letters:
        for c in g["calls"]:
            det = ", ".join(f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}" for k, v in c.items()
                            if k in ("week_low", "week_high", "week_close", "triggered_on", "touched", "first_close_below"))
            L.append(f"| {g['letter_date']} | {c['id']} | {c['rule']} | {c.get('level', f'{c.get(chr(108)+chr(111)+chr(119))}-{c.get(chr(104)+chr(105)+chr(103)+chr(104))}')} | **{c['outcome']}**{'' if c['validated'] else ' (unvalidated!)'} | {det} |")
    for g in letters:
        for s in g["scenarios"]:
            r = s["result"]
            L.append(f"\n**Scenario — {s['event']}** ({g['letter_date']} letter). Actual: {s['actual']['branch']} "
                     f"(NFP {s['actual']['nfp']:,} vs {s['actual']['consensus']:,} consensus). Predicted yields {s['predicted_yield']}, market {s['predicted_market']}. "
                     f"10-yr {r['yield_prev']:.2f}→{r['yield_close']:.2f} ({r['yield_dir']}, {'✓' if r['yield_ok'] else '✗'}); "
                     f"SPY prior close {r['mkt_prev_close']:.2f}, open {r['mkt_open']:.2f}, close {r['mkt_close']:.2f}: "
                     f"close-to-close {r['mkt_dir_close_to_close']} ({'✓' if r['mkt_ok_close_to_close'] else '✗'}), open-to-close {r['mkt_dir_open_to_close']} ({'✓' if r['mkt_ok_open_to_close'] else '✗'}).")
    sc = HERE / "SCORECARD.md"; txt = sc.read_text()
    txt = txt.split("\n## 5. Layer 2")[0].rstrip("\n") + "\n" + "\n".join(L) + "\n"
    sc.write_text(txt); print("\n".join(L))

if __name__ == "__main__":
    main()
