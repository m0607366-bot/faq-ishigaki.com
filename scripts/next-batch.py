# まだ回答のない質問を n 本、短くして表示する
import json, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
q = json.load(open("claude/questions.json", encoding="utf-8"))
a = json.load(open("claude/answers.json", encoding="utf-8"))
skip = set(json.load(open("claude/skip.json"))) if __import__("os").path.exists("claude/skip.json") else set()
rest = [x for x in q if x["id"] not in a and x["id"] not in skip]
print("残り", len(rest))
for x in rest[:n]:
    t = x["text"].replace("\n", " / ")
    print(f'## {x["id"]} {x["date"]} {",".join(x["cats"])}\n{x["title"]}\n{t[:650]}\n')
