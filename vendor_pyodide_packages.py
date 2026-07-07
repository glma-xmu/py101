#!/usr/bin/env python3
"""
Vendor the NumPy + pandas wheels (and their dependencies) that Pyodide needs,
into docs/vendor/pyodide/, so `import numpy` / `import pandas` work in the runnable
code cells with NO foreign CDN at page load (GFW-safe once committed).

Run this ONCE, on a computer that can reach the Pyodide CDN, then commit the new
.whl files:

    python vendor_pyodide_packages.py
    git add docs/vendor/pyodide/*.whl
    git commit -m "Vendor numpy and pandas wheels for Pyodide"
    git push

If the default CDN is slow or blocked for you, change PYODIDE_CDN below to a mirror
(e.g. gcore/fastly jsDelivr, or a copy on your own server).
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PYODIDE_DIR = os.path.join(HERE, "docs", "vendor", "pyodide")
LOCK = os.path.join(PYODIDE_DIR, "pyodide-lock.json")

WANT = ["numpy", "pandas"]  # add packages here if a later chapter needs them
PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/v{version}/full/{file}"


def main():
    if not os.path.exists(LOCK):
        sys.exit("Could not find %s — run this from the repo root." % LOCK)

    lock = json.load(open(LOCK, encoding="utf-8"))
    version = lock.get("info", {}).get("version")
    packages = lock.get("packages", {})
    if not version or not packages:
        sys.exit("Unexpected pyodide-lock.json format.")

    def key(n):
        return n.lower().replace("_", "-")

    index = {key(n): p for n, p in packages.items()}

    # Resolve the full dependency closure of WANT.
    needed, stack = {}, list(WANT)
    while stack:
        n = key(stack.pop())
        if n in needed:
            continue
        p = index.get(n)
        if not p:
            print("  ! '%s' is not in the lock file — skipping" % n)
            continue
        needed[n] = p
        stack.extend(p.get("depends", []))

    print("Pyodide %s — need %d packages: %s"
          % (version, len(needed), ", ".join(sorted(needed))))

    for n, p in sorted(needed.items()):
        fn = p["file_name"]
        base = os.path.basename(fn)
        dest = os.path.join(PYODIDE_DIR, base)
        if os.path.exists(dest):
            print("  = %s (already present)" % base)
            continue
        url = fn if fn.startswith("http") else PYODIDE_CDN.format(version=version, file=base)
        print("  + downloading %s" % base)
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print("    FAILED (%s): %s" % (e, url))

    print("\nDone. Commit the new .whl files in docs/vendor/pyodide/.")


if __name__ == "__main__":
    main()
