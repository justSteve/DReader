#!/usr/bin/env python3
"""Daily OHLC cache for grading Trade Brigade newsletter calls. [dr-4ne]

Pulls daily bars from Yahoo via yfinance into data/prices.csv (long form:
date,symbol,open,high,low,close). Re-run to extend; symbols are the union
of the fixed index set and every ticker named in extractions/*.json.

    .venv/bin/python newsletters/tradebrigade/prices.py [--start 2024-07-01]
"""
import argparse, glob, json, sys
from pathlib import Path
import pandas as pd
import yfinance as yf

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "prices.csv"
FIXED = ["SPY", "^GSPC", "QQQ", "IWM", "SMH", "^TNX", "^VIX"]

def wanted_symbols():
    syms = set(FIXED)
    for p in glob.glob(str(HERE / "extractions" / "*.json")):
        try:
            d = json.load(open(p))
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr); continue
        for idea in d.get("swing_ideas", []):
            if idea.get("ticker"): syms.add(idea["ticker"].upper())
        for c in d.get("index_calls", []) + d.get("calls", []):
            if c.get("instrument") and c["instrument"] not in ("ES", "NQ", "SPX"):
                syms.add(c["instrument"].upper())
    return sorted(syms)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-07-01")
    ap.add_argument("--end", default=None)
    a = ap.parse_args()
    syms = wanted_symbols()
    df = yf.download(syms, start=a.start, end=a.end, progress=False,
                     auto_adjust=False, group_by="ticker", threads=True)
    rows = []
    for s in syms:
        if s not in df.columns.get_level_values(0):
            print(f"no data: {s}", file=sys.stderr); continue
        d = df[s].dropna(subset=["Close"])
        for dt, r in d.iterrows():
            rows.append((dt.date().isoformat(), s, round(float(r["Open"]), 4),
                         round(float(r["High"]), 4), round(float(r["Low"]), 4),
                         round(float(r["Close"]), 4)))
    out = pd.DataFrame(rows, columns=["date", "symbol", "open", "high", "low", "close"])
    if OUT.exists():  # Yahoo drops a few symbols per run; keep prior rows for anything that failed today
        old = pd.read_csv(OUT)
        keep = old[~old.symbol.isin(set(out.symbol))]
        if len(keep): print(f"kept {keep.symbol.nunique()} symbols from the previous cache", file=sys.stderr)
        out = pd.concat([out, keep], ignore_index=True)
    out.sort_values(["symbol", "date"], inplace=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"wrote {len(out)} rows for {out.symbol.nunique()} symbols -> {OUT}")
    print(out.groupby("symbol").date.agg(["min", "max", "count"]).to_string())

if __name__ == "__main__":
    main()
