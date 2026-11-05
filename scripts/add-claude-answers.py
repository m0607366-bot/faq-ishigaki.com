# claude/answers.json の回答を、各記事（site/<ID>/index.html）の本文の下に書き足す。
# 何度実行してもよい（前に入れた回答は入れ替わる）。回答を消した記事からは枠も消える。
# 使い方:  python3 scripts/add-claude-answers.py   →  npm run deploy
import json, os, re, html

SITE = "site"
answers = json.load(open("claude/answers.json", encoding="utf-8"))
START, END = "<!-- claude-answer:start -->", "<!-- claude-answer:end -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\s*", re.S)
ANCHOR = '<div class="bottom_ad'

CSS = """<style>
.claude-answer{margin:2.5em 0 1.5em;padding:1.2em 1.4em;border:2px solid #d97757;border-radius:10px;background:#fdf6f2}
.claude-answer h2{margin:0 0 .7em!important;padding:0!important;border:0!important;background:none!important;font-size:1.15em;color:#b5532f}
.claude-answer h2:before,.claude-answer h2:after{display:none!important}
.claude-answer p,.claude-answer li{line-height:1.8}
.claude-answer ul{margin:.6em 0 .8em 1.3em;padding:0}
.claude-answer .claude-note{margin-top:1em;font-size:.85em;color:#666}
</style>"""

def linkify(s):
    s = html.escape(s)
    return re.sub(r"(https?://[^\s<）)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)

def to_html(text):
    out = []
    for para in re.split(r"\n\s*\n", text.strip()):
        lines = para.split("\n")
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{linkify(l[2:])}</li>" for l in lines) + "</ul>")
        else:
            out.append("<p>" + "<br>".join(linkify(l) for l in lines) + "</p>")
    return "\n".join(out)

def block(a):
    y, m = a["updated"].split("-")
    return (f'{START}\n{CSS}\n<section class="claude-answer">\n'
            f'<h2>🤖 Claudeの回答（{y}年{int(m)}月時点）</h2>\n{to_html(a["text"])}\n'
            f'<p class="claude-note">※AI（Claude）が{y}年{int(m)}月の時点で調べて書いた補足です。'
            f'お店の営業や制度は変わることがあるので、おでかけ前に各お店・役所に確認してください。</p>\n'
            f'</section>\n{END}\n')

added = removed = 0
for d in os.listdir(SITE):
    p = os.path.join(SITE, d, "index.html")
    if not d.isdigit() or not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    new = BLOCK_RE.sub("", s)
    if d in answers:
        i = new.find(ANCHOR)
        if i < 0:
            print("本文の終わりが見つからない:", d)
            continue
        new = new[:i] + block(answers[d]) + new[i:]
    if new != s:
        open(p, "w", encoding="utf-8").write(new)
        if d in answers: added += 1
        else: removed += 1
print(f"書き足し・更新 {added} 件、枠を外した {removed} 件（回答の数 {len(answers)}）")
