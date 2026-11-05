# claude/new/*.json の回答を answers.json にまとめる（skip は skip.json へ）
import json, glob, os
a = json.load(open("claude/answers.json", encoding="utf-8"))
skip = json.load(open("claude/skip.json")) if os.path.exists("claude/skip.json") else []
for f in sorted(glob.glob("claude/new/*.json")):
    b = json.load(open(f, encoding="utf-8"))
    for k, v in b.items():
        if v == "skip":
            if k not in skip: skip.append(k)
        elif v.startswith("same:"):
            a[k] = dict(a[v[5:]])
        else:
            a[k] = {"updated": "2026-11", "text": v}
json.dump(a, open("claude/answers.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(skip, open("claude/skip.json", "w"), indent=0)
print("回答", len(a), "／対象外", len(skip))
