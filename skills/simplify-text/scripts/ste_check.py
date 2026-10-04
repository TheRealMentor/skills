#!/usr/bin/env python3
"""Heuristic checker for STE-style writing.

Usage:
    python ste_check.py file.txt
    cat file.txt | python ste_check.py
    python ste_check.py file.txt --json --max-words 20

It flags hints, not verdicts. Code blocks and inline code are ignored.
"""
import argparse
import json
import re
import sys

SWAPS = {
    "utilize": "use", "utilise": "use", "leverage": "use", "commence": "start",
    "initiate": "start", "terminate": "stop", "facilitate": "help",
    "endeavor": "try", "ascertain": "find out", "demonstrate": "show",
    "subsequently": "then", "prior to": "before", "in order to": "to",
    "in the event that": "if", "with regard to": "about",
    "due to the fact that": "because", "at this point in time": "now",
    "a number of": "several / exact number", "sufficient": "enough",
    "obtain": "get", "purchase": "buy", "modify": "change", "ensure": "make sure",
    "assist": "help", "numerous": "many", "approximately": "about",
    "methodology": "method", "functionality": "feature", "robust": "(say what it does)",
    "seamless": "(say what it does)", "cutting-edge": "(say what it does)",
    "delve": "look at", "tapestry": "(cut)", "touch base": "talk",
    "circle back": "follow up", "low-hanging fruit": "easy wins",
    "move the needle": "have a clear effect", "deep dive": "detailed review",
    "bandwidth": "time / capacity", "ping me": "message me",
}

FILLER = [
    "it is important to note", "it should be noted", "please be advised",
    "needless to say", "at the end of the day", "in today's fast-paced",
    "ever-evolving", "let's dive in", "let's delve", "without further ado",
    "i hope this", "feel free to", "don't hesitate to", "in conclusion",
]

HEDGES = {"very", "really", "quite", "essentially", "basically", "simply", "arguably"}

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?"
    r"(\w+ed|built|made|done|given|shown|taken|written|run|sent|set|seen|known|found|kept|held|left)\b",
    re.I,
)
PERFECT_PROG = re.compile(
    r"\b(has|have|had)\s+(been\s+)?\w+(ed|en|ing)\b|\b(is|are|was|were)\s+\w+ing\b", re.I
)
AMBIG_MODALS = re.compile(r"\b(may|might)\b", re.I)
NOMINAL = re.compile(
    r"\b(make|made|give|given|perform|performed|carry out|conduct|provide|provided)\s+(a|an|the)?\s*\w+(tion|ment|sis|ance|ence)\b",
    re.I,
)


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def split_sentences(text):
    text = re.sub(r"^\s*([-*]|\d+[.)])\s+", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}|\n", text)
    return [p.strip() for p in parts if p.strip()]


def check(text, max_words):
    clean = strip_code(text)
    sentences = split_sentences(clean)
    issues = []
    lengths = []
    lower_all = clean.lower()
    for i, s in enumerate(sentences, 1):
        words = re.findall(r"[\w'-]+", s)
        n = len(words)
        lengths.append(n)
        sl = s.lower()
        if n > max_words:
            issues.append({"sentence": i, "type": "long", "detail": f"{n} words (cap {max_words})", "text": s})
        if PASSIVE.search(s):
            issues.append({"sentence": i, "type": "passive?", "detail": PASSIVE.search(s).group(0), "text": s})
        m = PERFECT_PROG.search(s)
        if m:
            issues.append({"sentence": i, "type": "tense", "detail": m.group(0), "text": s})
        if AMBIG_MODALS.search(s):
            issues.append({"sentence": i, "type": "may/might", "detail": AMBIG_MODALS.search(s).group(0), "text": s})
        if NOMINAL.search(s):
            issues.append({"sentence": i, "type": "noun-for-verb", "detail": NOMINAL.search(s).group(0), "text": s})
        if s.count(",") >= 4 or len(re.findall(r"\b(and|but|which|while)\b", sl)) >= 3:
            issues.append({"sentence": i, "type": "stacked ideas?", "detail": "many clauses", "text": s})
    for word, alt in SWAPS.items():
        for m in re.finditer(r"\b" + re.escape(word) + r"\b", lower_all):
            issues.append({"sentence": None, "type": "word", "detail": f"{word} -> {alt}", "text": ""})
    for phrase in FILLER:
        if phrase in lower_all:
            issues.append({"sentence": None, "type": "filler", "detail": phrase, "text": ""})
    for w in HEDGES:
        c = len(re.findall(r"\b" + w + r"\b", lower_all))
        if c:
            issues.append({"sentence": None, "type": "hedge", "detail": f"{w} x{c}", "text": ""})
    stats = {
        "sentences": len(sentences),
        "avg_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "max_words": max(lengths) if lengths else 0,
        "over_cap": sum(1 for n in lengths if n > max_words),
        "issue_count": len(issues),
    }
    return stats, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--max-words", type=int, default=25)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    stats, issues = check(text, a.max_words)
    if a.json:
        print(json.dumps({"stats": stats, "issues": issues}, indent=2))
        return
    print(f"Sentences: {stats['sentences']} | avg {stats['avg_words']} words | longest {stats['max_words']} | over cap: {stats['over_cap']}")
    print(f"Issues: {stats['issue_count']}")
    for it in issues:
        loc = f"S{it['sentence']}" if it["sentence"] else "  "
        print(f"  [{loc}] {it['type']}: {it['detail']}")


if __name__ == "__main__":
    main()
