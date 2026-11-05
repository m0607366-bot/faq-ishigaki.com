# 石垣島なんでも相談室（faq-ishigaki.com）

WordPress の表示を、見た目ごとそのまま静的ファイルにしたサイト。Cloudflare Workers の静的アセットで公開。

- `npm run fetch` … WordPress からページ・CSS・JS・画像を `site/` に写す（再実行で続きから。`node scripts/mirror.mjs --fresh` でHTMLを取り直し）
- `npm run deploy` … 公開
- `npm run deploy:www` … www.faq-ishigaki.com → faq-ishigaki.com の転送（`www/`）を公開

検索は Google のサイト内検索へ。
ドメインを切り替えた後は `npm run fetch` は使えない（WordPress に届かないため止まる。取り直すときは hosts で古いサーバーに向ける）。
apart（サブドメイン）は別のサイト。

## Claudeの回答（2026年11月〜）

「Q.」の各記事の本文の下に「🤖 Claudeの回答（YYYY年M月時点）」の枠を足している。

- `claude/questions.json` … `site/<ID>/index.html` から集めた「Q.」の記事（`python3 scripts/extract-questions.py` で作り直せる）
- `claude/answers.json` … 回答の本体。`{"<記事ID>": {"updated": "YYYY-MM", "text": "…"}}`（段落は空行、箇条書きは「- 」）
- `claude/skip.json` … 回答しない記事ID
- `claude/new/*.json` … 2026年11月に20本ずつ書いた下書き（`scripts/merge-batch.py` で answers.json にまとめた）
- `python3 scripts/add-claude-answers.py` … answers.json を各記事に書き足す（何度実行してもよい。前の枠は入れ替わる）→ `npm run deploy`

毎年5月1日・11月1日に、予約作業（Claude）が回答を見直して add-claude-answers.py まで実行し、deploy を頼むメッセージを送る。
