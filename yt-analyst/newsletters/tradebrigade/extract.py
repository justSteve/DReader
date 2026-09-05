#!/usr/bin/env python3
"""Deterministic (Layer 1) extraction from Trade Brigade letters. [dr-4ne]

Regex only, no judgment — the analogue of Strader's listlevels.py. Emits
extractions/L1_<date>.json per letter with three signal families:

  self_score   the opener's "closed up/down X% from <basis>" recap line
  spy_levels   every SPY price named in the SPY sections, with its sentence
               and a keyword class (hold / break / target / mention)
  swing_ideas  one per "TICKER – Daily Chart" paragraph in Swing Stock Scans:
               trigger price + direction + other prices named

Validation rule (from Strader's Mancini contract): every price emitted must
appear verbatim in the letter text; the extractor only ever copies.

    .venv/bin/python newsletters/tradebrigade/extract.py [letters/2026-08-31_*.txt ...]
"""
import glob, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LETTERS = HERE / "letters"
OUT = HERE / "extractions"

SELF_RE = re.compile(
    r"(?:S&P|Price|Markets?)[^.\n]{0,80}?(closed|finished|was|is|are|gained|fell|rallied|dropped|lost|retraced|had|has|continued)[^.\n]{0,60}?"
    r"(up|down|higher|lower|gain(?:ed)?|loss|fell|rallied|dropped|lost|drawdown|decline)?[^.\n]{0,30}?(\d+(?:\.\d+)?)\s?%"
    r"([^.\n]{0,80})", re.I)
HEAD_RE = re.compile(r"^([A-Z]{1,5})\s+[–-]\s+((?:Daily|Weekly|Monthly|Hourly)(?:\s*/\s*(?:Daily|Weekly|Monthly|Hourly))*)(?:\s+[Cc]hart)?(?:,.*)?\s*$")
IDX_HEAD_RE = re.compile(r"^(SPY|QQQ|IWM|SMH|/ES|S&P (?:weekly|daily|hourly|monthly) chart|Market (?:Internals|Profile|internals|profile)|QQQE|Nasdaq)\b", re.I)

HOLD_KW = re.compile(r"must hold|as long as|holds?\b|support|higher low|reclaim|defend|hold(?:ing)?", re.I)
BREAK_KW = re.compile(r"\bbelow\b|\blose\b|\blost\b|\bbreak(?:down|s)?\b|acceptance|lower high|fail", re.I)
TARGET_KW = re.compile(r"toward|target|\binto\b|room|measured move|gap (?:close|fill)|upside|downside", re.I)

def sections(text):
    """Split into (heading, body) using the letter's own heading lines."""
    lines = text.splitlines()
    heads = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("** ") or HEAD_RE.match(s) or IDX_HEAD_RE.match(s) or s in (
                "Swing Stock Scans", "Economic & Earnings Calendar", "We're social!", "Swing Trade Ideas"):
            heads.append((i, s.lstrip("* ").strip()))
    out = []
    for k, (i, h) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out.append((h, "\n".join(lines[i + 1:j]).strip()))
    return out

def sentences(body):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", body.replace("\n", " ")) if s.strip()]

def self_score(text):
    m = re.search(r"Hey\s*!?\s*\n+(.{0,600})", text, re.S)
    opener = m.group(1) if m else text[:600]
    mm = None
    for cand in SELF_RE.finditer(opener):
        blob0 = cand.group(0).lower()
        if "tariff" in blob0 or re.search(r"from \d+(?:\.\d+)?% to", blob0) or float(cand.group(3)) > 15:
            continue
        if not cand.group(2) and cand.group(1).lower() in ("was", "is", "are", "had", "has", "closed", "finished", "continued"):
            # a bare verb with no direction word is not a recap of the move
            if not re.search(r"\b(up|down|higher|lower|gain|loss|fell|rallied|dropped|lost)\b", blob0):
                continue
        mm = cand; break
    if not mm:
        return {"found": False, "opener": opener[:300]}
    verb, dirword, pct, tail = mm.groups()
    blob = mm.group(0).lower()
    if re.search(r"\bdown\b|\blower\b|\bfell\b|\bloss\b|\blost\b|\bdropped\b|drawdown|decline", blob):
        direction = "down"
    elif re.search(r"\bup\b|\bhigher\b|\bgain|\brallied\b", blob):
        direction = "up"
    else:
        direction = "unknown"
    t = (mm.group(0) + tail).lower()
    if "all time high" in t or "all-time high" in t or "ath" in t.split():
        basis = "from_all_time_high"
    elif "monday's open" in t or "monday’s open" in t or "tuesday's open" in t:
        basis = "monday_open_to_friday_close"
    elif "peak to trough" in t:
        basis = "peak_to_trough"
    elif any(k in t for k in ("prior weekly close", "last week", "on the week", "from the prior", "weekly close", "friday", "this past week", "the week")):
        basis = "friday_close_to_friday_close"
    else:
        basis = "unknown"
    return {"found": True, "direction": direction, "pct": float(pct), "basis": basis,
            "quote": mm.group(0).strip()[:240]}

def spy_levels(secs):
    out = []
    for h, body in secs:
        if not (h.startswith("SPY") or h.lower().startswith("s&p")):
            continue
        for s in sentences(h + " " + body if h.lower().startswith("s&p") else body):
            for pm in re.finditer(r"(?<![\d.])(\d{3,4}(?:,\d{3})?(?:\.\d{1,2})?)(?![\d%])", s):
                lvl = float(pm.group(1).replace(",", ""))
                if 300 <= lvl <= 1200: inst = "SPY"
                elif 2500 <= lvl <= 9000: inst = "SPX"
                else: continue
                if HOLD_KW.search(s) and not BREAK_KW.search(s): cls = "hold"
                elif BREAK_KW.search(s) and not HOLD_KW.search(s): cls = "break"
                elif TARGET_KW.search(s): cls = "target"
                else: cls = "mention"
                out.append({"section": h, "instrument": inst, "level": lvl, "class": cls, "sentence": s[:260]})
    seen, uniq = set(), []
    for o in out:
        k = (o["level"], o["sentence"])
        if k not in seen: seen.add(k); uniq.append(o)
    return uniq

def swing_ideas(secs):
    out, active = [], False
    for h, body in secs:
        if h.startswith("Swing"):
            active = True; continue
        if not active:
            continue
        if h.startswith("We're social") or h.startswith("Economic"):
            break
        m = HEAD_RE.match(h)
        if not m:
            continue
        ticker, tf = m.group(1), m.group(2)
        prices = [float(x) for x in re.findall(r"(?<![\d.])(\d{1,4}(?:\.\d{1,2})?)(?![\d%])", body)
                  if 0.5 <= float(x) <= 20000]
        low = body.lower()
        direction = "short" if re.search(r"\bshort(?:ing| setup| idea| entry| side| candidate| this| the)\b|\bputs?\b|breakdown (?:under|below)|break(?:s|ing)? (?:down )?(?:under|below)", low) else "long"
        trig = None; trig_kind = None
        for tm in re.finditer(r"(?:over|above|through|reclaim(?:s|ing)?(?: of)?|breakout(?: level)?(?: potentially)?(?: over| of)?|clear(?:s|ing)?|break(?:s|ing)? (?:out )?(?:over|above|of))\s+(?:the\s+)?\$?(\d{1,4}(?:\.\d{1,2})?)(\s*(?:sma|ema|dma|day|-day|week|month|psych|%))?", low):
            if tm.group(2) or re.match(r"\s*(?:and|&|/)\s*\d+\s*(?:sma|ema|dma|day|week|month|moving)", low[tm.end():]):
                continue
            trig, trig_kind = float(tm.group(1)), "over"; break
        else:
            tm = re.search(r"(?:under|below|loses?|breaks? (?:down )?(?:below|under))\s+\$?(\d{1,4}(?:\.\d{1,2})?)", low)
            if tm and direction == "short":
                trig, trig_kind = float(tm.group(1)), "under"
        rel = None
        if re.search(r"over (?:friday|last week|the week)'?s? high", low): rel = "over_prior_friday_high"
        elif re.search(r"over (?:monday|the day)'?s? high", low): rel = "over_day_high"
        out.append({"ticker": ticker, "timeframe": tf, "direction": direction,
                    "trigger": trig, "trigger_kind": trig_kind, "trigger_relative": rel,
                    "prices": sorted(set(prices)), "text": body[:600]})
    return out

def extract(path):
    text = Path(path).read_text()
    head = text.splitlines()
    subject = head[0].lstrip("# ").strip() if head else ""
    date = Path(path).name[:10]
    secs = sections(text)
    return {"letter_date": date, "subject": subject, "file": Path(path).name,
            "self_score": self_score(text),
            "spy_levels": spy_levels(secs),
            "swing_ideas": swing_ideas(secs),
            "sections": [h for h, _ in secs]}

def main():
    files = sys.argv[1:] or sorted(glob.glob(str(LETTERS / "20*.txt")))
    OUT.mkdir(exist_ok=True)
    tot = {"letters": 0, "self": 0, "levels": 0, "ideas": 0, "ideas_with_trigger": 0}
    for f in files:
        d = extract(f)
        (OUT / f"L1_{d['letter_date']}.json").write_text(json.dumps(d, indent=1))
        ntrig = sum(1 for i in d["swing_ideas"] if i["trigger"] or i["trigger_relative"])
        tot["letters"] += 1; tot["self"] += int(bool(d["self_score"]["found"]))
        tot["levels"] += len(d["spy_levels"]); tot["ideas"] += len(d["swing_ideas"]); tot["ideas_with_trigger"] += ntrig
        ss = d["self_score"]
        print(f"{d['letter_date']}  self={ss.get('direction','-')}/{ss.get('pct','-')}/{str(ss.get('basis','-'))[:12]:12}"
              f" spy_levels={len(d['spy_levels']):2d} ideas={len(d['swing_ideas']):2d} triggers={ntrig}")
    print(tot)

if __name__ == "__main__":
    main()
