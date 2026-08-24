#!/usr/bin/env python3
"""
Collect financial data from the SEC's EDGAR APIs.

Everything here is public-domain US government data, so unlike CRSP or Compustat
it can be handed to students freely. Nothing is written into docs/ — output lands
in an untracked ./edgar_out/ folder for distribution over the college network.

The SEC asks two things of automated clients, and enforces both:

  1. A User-Agent naming a real person and contact address. Requests without one
     get 403. Set CONTACT below.
  2. No more than 10 requests/second. This script sleeps between calls.

Note that data.sec.gov sends no CORS headers, so a browser cannot fetch it —
these endpoints only work server-side, which is why this is a script you run
rather than something a Pyodide cell could do.

Usage
-----
    python scripts/fetch_edgar.py tickers
    python scripts/fetch_edgar.py frame Assets CY2023Q1I
    python scripts/fetch_edgar.py facts AAPL
    python scripts/fetch_edgar.py panel CY2023Q1I
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

# --- CHANGE THIS to your own name and email before running -------------------
CONTACT = "Guoliang Ma glma@iastate.edu"
# -----------------------------------------------------------------------------

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "edgar_out")
RATE_LIMIT_SECONDS = 0.15  # ~7 requests/second, comfortably inside the SEC's limit

_last_call = [0.0]


def get_json(url, soft=False):
    """Fetch one JSON document, respecting the SEC's User-Agent and rate rules.

    soft=True returns None on 404 instead of exiting, so a caller can try several
    candidate XBRL tags and keep the first that exists.
    """
    wait = RATE_LIMIT_SECONDS - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={
        "User-Agent": CONTACT,
        "Accept-Encoding": "gzip",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        if e.code == 404 and soft:
            return None          # this tag/period simply does not exist
        sys.exit("HTTP %s for %s\n  (403 usually means the User-Agent is missing "
                 "or does not name a contact)" % (e.code, url))
    finally:
        _last_call[0] = time.time()


def ensure_out():
    os.makedirs(OUT_DIR, exist_ok=True)
    return OUT_DIR


def write_csv(name, fieldnames, rows):
    path = os.path.join(ensure_out(), name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("  wrote %s  (%d rows)" % (path, len(rows)))
    return path


# --- The four endpoints worth knowing ----------------------------------------

def cmd_tickers(_args):
    """CIK <-> ticker <-> company name. The join key for everything else."""
    data = get_json("https://www.sec.gov/files/company_tickers.json")
    rows = [{"cik": v["cik_str"], "ticker": v["ticker"], "name": v["title"]}
            for v in data.values()]
    rows.sort(key=lambda r: r["cik"])
    write_csv("company_tickers.csv", ["cik", "ticker", "name"], rows)


def fetch_frame(concept, period, unit="USD", taxonomy="us-gaap", soft=False):
    """One concept, one period, EVERY filer that reported it — a cross-section."""
    url = "https://data.sec.gov/api/xbrl/frames/%s/%s/%s/%s.json" % (
        taxonomy, concept, unit, period)
    return get_json(url, soft=soft)


def cmd_frame(args):
    d = fetch_frame(args.concept, args.period, args.unit)
    rows = [{"cik": r["cik"], "entityName": r["entityName"], "loc": r.get("loc", ""),
             "end": r["end"], "value": r["val"]} for r in d["data"]]
    print("  %s %s: %d filers" % (args.concept, args.period, len(rows)))
    write_csv("frame_%s_%s.csv" % (args.concept, args.period),
              ["cik", "entityName", "loc", "end", "value"], rows)


def cmd_facts(args):
    """Every XBRL fact one company ever filed. Large: tens of MB for a big filer."""
    data = get_json("https://www.sec.gov/files/company_tickers.json")
    cik = None
    for v in data.values():
        if v["ticker"].upper() == args.ticker.upper():
            cik = v["cik_str"]
            break
    if cik is None:
        sys.exit("ticker %r not found" % args.ticker)
    facts = get_json("https://data.sec.gov/api/xbrl/companyfacts/CIK%010d.json" % cik)
    path = os.path.join(ensure_out(), "facts_%s.json" % args.ticker.upper())
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(facts, fh)
    concepts = facts.get("facts", {}).get("us-gaap", {})
    print("  %s (CIK %d): %d us-gaap concepts -> %s" % (args.ticker.upper(), cik, len(concepts), path))


# --- The useful one: build a teaching panel ----------------------------------

# (column name, candidate XBRL tags in priority order, unit, instant|duration)
#
# Two things make this list less obvious than it looks, and both are worth
# showing students rather than hiding:
#
#   * Balance-sheet items are *instants* (a stock at a date) and use a period
#     ending in "I": CY2023Q1I. Income-statement items are *durations* (a flow
#     over a span): CY2023Q1 or CY2023. Asking for the wrong one returns almost
#     nothing rather than an error.
#   * There is no single revenue tag. Since ASC 606 most filers report
#     RevenueFromContractWithCustomer*, while others still use Revenues or
#     SalesRevenueNet. We try each in turn and keep the first value found for
#     each firm.
PANEL_ITEMS = [
    ("Assets",      ["Assets"],              "USD", "instant"),
    ("Liabilities", ["Liabilities"],         "USD", "instant"),
    ("Equity",      ["StockholdersEquity"],  "USD", "instant"),
    ("Revenue",     ["RevenueFromContractWithCustomerExcludingAssessedTax",
                     "RevenueFromContractWithCustomerIncludingAssessedTax",
                     "Revenues",
                     "SalesRevenueNet"],     "USD", "duration"),
    ("NetIncome",   ["NetIncomeLoss"],       "USD", "duration"),
]


def periods_for(period):
    """Return (instant_period, duration_period) for a user-supplied period.

    CY2023Q1I -> ("CY2023Q1I", "CY2023Q1)      quarterly
    CY2023Q1  -> ("CY2023Q1I", "CY2023Q1")     same thing, written either way
    CY2023    -> ("CY2023Q4I", "CY2023")       annual: year-end stock, full-year flow
    """
    p = period.rstrip("I")
    if "Q" in p:
        return p + "I", p
    return p + "Q4I", p


def cmd_panel(args):
    """Join several concepts on CIK: one row per firm, one column per item."""
    instant, duration = periods_for(args.period)
    print("  instants from %s, durations from %s" % (instant, duration))
    merged = {}
    report = []
    for column, tags, unit, kind in PANEL_ITEMS:
        per = instant if kind == "instant" else duration
        filled, used = 0, []
        for tag in tags:
            d = fetch_frame(tag, per, unit, soft=True)
            if not d or not d.get("data"):
                continue
            added = 0
            for r in d["data"]:
                row = merged.setdefault(r["cik"],
                                        {"cik": r["cik"], "entityName": r["entityName"]})
                if column not in row:          # first tag that has this firm wins
                    row[column] = r["val"]
                    added += 1
            if added:
                used.append("%s+%d" % (tag.replace("RevenueFromContractWithCustomer", "RFCC"), added))
            filled += added
        report.append("%s=%d [%s]" % (column, filled, ", ".join(used) or "none"))
    rows = sorted(merged.values(), key=lambda r: r["cik"])
    for line in report:
        print("    " + line)
    cols = ["cik", "entityName"] + [c for c, _, _, _ in PANEL_ITEMS]
    write_csv("panel_%s.csv" % args.period, cols, rows)
    complete = sum(1 for r in rows if all(c in r for c, _, _, _ in PANEL_ITEMS))
    print("  %d firms total, %d with every item present" % (len(rows), complete))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tickers", help="CIK/ticker/name map").set_defaults(func=cmd_tickers)

    f = sub.add_parser("frame", help="one concept, one period, all filers")
    f.add_argument("concept")
    f.add_argument("period", help='e.g. CY2023Q1I (instant) or CY2023 (duration)')
    f.add_argument("--unit", default="USD")
    f.set_defaults(func=cmd_frame)

    c = sub.add_parser("facts", help="every fact for one company")
    c.add_argument("ticker")
    c.set_defaults(func=cmd_facts)

    pa = sub.add_parser("panel", help="several concepts joined on CIK")
    pa.add_argument("period", help="e.g. CY2023Q1I")
    pa.set_defaults(func=cmd_panel)

    args = p.parse_args()
    if "example.com" in CONTACT:
        sys.exit("Set CONTACT at the top of this file to your own name and email.")
    args.func(args)


if __name__ == "__main__":
    main()
