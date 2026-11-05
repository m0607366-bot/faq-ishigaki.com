# site/<ID>/index.html から「Q.」で始まる記事を集め、claude/questions.json に書き出す
import json, os, re, html, sys
SITE = "site"
out = []
for d in sorted(os.listdir(SITE), key=lambda x: int(x) if x.isdigit() else 0):
    if not d.isdigit(): continue
    p = os.path.join(SITE, d, "index.html")
    if not os.path.exists(p): continue
    s = open(p, encoding="utf-8").read()
    m = re.search(r'<h1 class="single-post-title entry-title">(.*?)</h1>', s, re.S)
    if not m: continue
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    if not re.match(r"^\s*Q[.．]", title): continue
    date = (re.search(r'class="single-post-date published[^"]*" datetime="([^"]+)"', s) or [None, ""])[1]
    cats = re.findall(r'rel="category tag">([^<]+)<', s.split('<div class="single_title">')[0])
    body = re.search(r'<div class="content">(.*?)<div class="bottom_ad', s, re.S)
    text = ""
    if body:
        t = re.sub(r"<hr[^>]*>", "\n---\n", body.group(1))
        t = re.sub(r"<br\s*/?>|</p>", "\n", t)
        t = html.unescape(re.sub(r"<[^>]+>", "", t))
        text = re.sub(r"\n\s*\n+", "\n", t).strip()
    out.append({"id": d, "title": title, "date": date, "cats": sorted(set(cats)), "text": text})
json.dump(out, open("claude/questions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "questions")
