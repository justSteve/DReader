"""Build the narration fact sheet for the 2026-08-24 10:41-42 CT absorption episode from Strader's tape.
Two files: FACTS (observable up to the cutoff) and AFTERMATH (held back from the narrator)."""
import sys, json
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from collections import defaultdict
sys.path.insert(0, "/root/projects/Strader")
from market.orderflow.tradesource import iter_trades
from market.orderflow.moves import one_minute_atoms, grade_atoms_developing
CT = ZoneInfo("America/Chicago")
DAY = date(2026, 8, 24)
CUTOFF = datetime(2026, 8, 24, 10, 43, tzinfo=CT)      # narrator sees tape up to here
RTH0 = datetime(2026, 8, 24, 8, 30, tzinfo=CT)
out = {}
# --- prior session (Friday 08-21) RTH summary
def rth_summary(d):
    t0 = datetime(d.year, d.month, d.day, 8, 30, tzinfo=CT); t1 = t0 + timedelta(hours=6, minutes=45)
    hi = lo = None; o = c = None; vol = 0
    for t in iter_trades(d, start_ts=t0, end_ts=t1):
        if o is None: o = t.price
        hi = t.price if hi is None else max(hi, t.price); lo = t.price if lo is None else min(lo, t.price)
        c = t.price; vol += t.size
    return {"open": o, "high": hi, "low": lo, "close": c, "rth_volume": vol}
try:
    out["prior_session_2026-08-21_RTH"] = rth_summary(date(2026, 8, 21))
except FileNotFoundError:
    out["prior_session_2026-08-21_RTH"] = "unavailable"
# --- overnight (globex) range for 08-24 before RTH
gl = {"high": None, "low": None}
for t in iter_trades(DAY, start_ts=datetime(2026, 8, 23, 17, 0, tzinfo=CT), end_ts=RTH0):
    gl["high"] = t.price if gl["high"] is None else max(gl["high"], t.price)
    gl["low"] = t.price if gl["low"] is None else min(gl["low"], t.price)
out["overnight_range"] = gl
# --- RTH tape up to cutoff and beyond
trades_all = list(iter_trades(DAY, start_ts=RTH0, end_ts=datetime(2026, 8, 24, 12, 0, tzinfo=CT)))
trades = [t for t in trades_all if t.ts < CUTOFF]
atoms = one_minute_atoms(trades); dev = grade_atoms_developing(atoms)
def row(a, d=None):
    r = {"t": a.ts.strftime("%H:%M"), "o": a.open, "h": a.high, "l": a.low, "c": a.close, "vol": a.volume,
         "delta": a.delta, "net": round(a.net, 2), "range": round(a.range_pts, 2)}
    if d: r.update({"effort_pct_sofar": round(d["effort_pct_dev"], 1), "effect_pct_sofar": round(d["effect_pct_dev"], 1)})
    return r
# session-so-far stats
hod = max(trades, key=lambda t: t.price); lod = min(trades, key=lambda t: t.price)
out["session_open"] = trades[0].price
out["session_so_far"] = {
    "high": hod.price, "high_time": hod.ts.astimezone(CT).strftime("%H:%M:%S"),
    "low": lod.price, "low_time": lod.ts.astimezone(CT).strftime("%H:%M:%S"),
    "last": trades[-1].price, "minutes": len(atoms),
    "median_minute_volume": sorted(a.volume for a in atoms)[len(atoms)//2],
    "max_minute_volume": max(a.volume for a in atoms),
    "max_buy_delta_minute": row(max(atoms, key=lambda a: a.delta)),
    "max_sell_delta_minute": row(min(atoms, key=lambda a: a.delta)),
}
# 5-minute structure of the session so far (for the narrator's context)
five = defaultdict(lambda: {"o": None, "h": None, "l": None, "c": None, "vol": 0, "delta": 0})
for a in atoms:
    k = a.ts.replace(minute=(a.ts.minute // 5) * 5); b = five[k]
    if b["o"] is None: b["o"] = a.open
    b["h"] = a.high if b["h"] is None else max(b["h"], a.high); b["l"] = a.low if b["l"] is None else min(b["l"], a.low)
    b["c"] = a.close; b["vol"] += a.volume; b["delta"] += a.delta
out["five_minute_bars_so_far"] = [{"t": k.strftime("%H:%M"), **v} for k, v in sorted(five.items())]
# 1-minute detail for the window of interest
out["one_minute_detail_10:25_to_cutoff"] = [row(a, d) for a, d in zip(atoms, dev) if a.ts >= datetime(2026, 8, 24, 10, 25, tzinfo=CT)]
# volume at price in the absorption band during 10:38-10:43, split by aggressor
vap = defaultdict(lambda: {"buy": 0, "sell": 0})
for t in trades:
    if t.ts >= datetime(2026, 8, 24, 10, 38, tzinfo=CT):
        vap[t.price]["B" == t.side and "buy" or "sell"] += t.size
out["volume_at_price_10:38_to_cutoff"] = [{"price": p, **v, "delta": v["buy"] - v["sell"]} for p, v in sorted(vap.items(), reverse=True)]
# the same prices over the whole session so far (has this level traded before?)
lvl = defaultdict(int)
for t in trades: lvl[t.price] += t.size
band = sorted(vap)
out["session_volume_at_the_same_prices"] = [{"price": p, "session_volume": lvl[p]} for p in sorted(band, reverse=True)]
out["session_poc_so_far"] = max(lvl.items(), key=lambda kv: kv[1])
json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
# --- aftermath, held back
after = [t for t in trades_all if t.ts >= CUTOFF]
aa = one_minute_atoms(after)
json.dump({"one_minute_after_cutoff": [row(a) for a in aa[:35]],
           "path": {"high_to_11:15": max(a.high for a in aa[:32]), "low_to_11:15": min(a.low for a in aa[:32]), "close_11:15": aa[31].close if len(aa) > 31 else None}},
          open(sys.argv[2], "w"), indent=1, default=str)
print("facts:", sys.argv[1]); print("aftermath:", sys.argv[2])
