#!/usr/bin/env python3
"""
Insert a blank line before any Markdown list or table that directly follows a
paragraph line. MkDocs/python-markdown otherwise swallows the list/table into
the preceding paragraph (renders as run-on text). Skips fenced code blocks.
"""
import sys, re, glob, os

LIST_RE  = re.compile(r'^(\s*)([*+-]|\d+\.)\s+\S')
TABLE_RE = re.compile(r'^\s*\|.*\|')
HEAD_RE  = re.compile(r'^\s*#{1,6}\s')
FENCE_RE = re.compile(r'^\s*(```|~~~)')

def is_blank(s): return s.strip() == ''
def is_list(s):  return bool(LIST_RE.match(s))
def is_table(s): return bool(TABLE_RE.match(s))

def fix(lines):
    out, in_fence, changed = [], False, 0
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line); continue
        if not in_fence and (is_list(line) or is_table(line)):
            prev = out[-1] if out else ''
            # previous line is real paragraph text (not blank, not a list/table
            # item itself, not a heading) -> needs a separating blank line
            if (not is_blank(prev) and not is_list(prev) and not is_table(prev)
                    and not HEAD_RE.match(prev)):
                out.append('\n'); changed += 1
        out.append(line)
    return out, changed

def main():
    files = sys.argv[1:]
    total = 0
    for path in files:
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
        fixed, n = fix(lines)
        if n:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(fixed)
            total += n
            print(f"  {os.path.basename(path):32s} +{n} blank lines")
    print(f"TOTAL blank lines inserted: {total}")

if __name__ == '__main__':
    main()
