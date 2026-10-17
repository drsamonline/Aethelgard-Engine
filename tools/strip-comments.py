#!/usr/bin/env python3
"""
Strips comments and redundant whitespace from the game's JavaScript, for the
playable-only build.

Deliberately conservative: it walks the source character by character and
tracks whether it is inside a string, a template literal, or a regex, so a `//`
inside a string is never mistaken for a comment. Newlines are KEPT, because
JavaScript inserts semicolons at line breaks and removing them can change
behaviour. Nothing else is rewritten.

    python3 tools/strip-comments.py <src-dir> <out-dir>
"""
import pathlib, sys


def strip(src: str) -> str:
    out = []
    i, n = 0, len(src)
    state = "code"          # code | line | block | sq | dq | tpl | regex
    prev_sig = ""           # last significant char, for regex detection
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if state == "code":
            if c == "/" and nxt == "/":
                state = "line"; i += 2; continue
            if c == "/" and nxt == "*":
                state = "block"; i += 2; continue
            if c == "'":
                state = "sq"
            elif c == '"':
                state = "dq"
            elif c == "`":
                state = "tpl"
            elif c == "/" and prev_sig not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$)]}":
                state = "regex"
            out.append(c)
            if not c.isspace():
                prev_sig = c
            i += 1
            continue

        if state == "line":
            if c == "\n":
                state = "code"; out.append(c)
            i += 1
            continue

        if state == "block":
            if c == "*" and nxt == "/":
                state = "code"; i += 2
                # keep one space so `a/*x*/b` does not become `ab`
                if out and not out[-1].isspace(): out.append(" ")
                continue
            i += 1
            continue

        if state in ("sq", "dq", "tpl"):
            out.append(c)
            if c == "\\":
                if i + 1 < n: out.append(src[i + 1]); i += 2; continue
            elif (state == "sq" and c == "'") or (state == "dq" and c == '"') or (state == "tpl" and c == "`"):
                state = "code"
            i += 1
            continue

        if state == "regex":
            out.append(c)
            if c == "\\":
                if i + 1 < n: out.append(src[i + 1]); i += 2; continue
            elif c == "/":
                state = "code"
            elif c == "\n":            # not actually a regex after all
                state = "code"
            i += 1
            continue

    text = "".join(out)
    # collapse runs of blank lines and leading indentation, keep newlines
    lines = [ln.rstrip() for ln in text.split("\n")]
    kept, blank = [], False
    for ln in lines:
        if ln.strip() == "":
            if not blank: kept.append("")
            blank = True
        else:
            kept.append(ln.lstrip() if ln.strip().startswith(("}", ")", "]")) else ln)
            blank = False
    return "\n".join(kept)


def main():
    src_dir = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2])
    total_in = total_out = 0
    count = 0
    for p in sorted(src_dir.rglob("*.js")):
        rel = p.relative_to(src_dir)
        dst = out_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = p.read_text(encoding="utf-8")
        stripped = strip(text)
        dst.write_text(stripped, encoding="utf-8")
        total_in += len(text); total_out += len(stripped); count += 1
    print(f"  {count} files: {total_in//1024} KB -> {total_out//1024} KB "
          f"({100 - total_out * 100 // max(1, total_in)}% smaller)")


if __name__ == "__main__":
    main()
