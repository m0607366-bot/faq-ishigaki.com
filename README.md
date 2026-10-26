# 石垣島なんでも相談室（faq-ishigaki.com）

WordPress の表示を、見た目ごとそのまま静的ファイルにしたサイト。Cloudflare Workers の静的アセットで公開。

- `npm run fetch` … WordPress からページ・CSS・JS・画像を `site/` に写す（再実行で続きから。`node scripts/mirror.mjs --fresh` でHTMLを取り直し）
- `npm run deploy` … 公開
- `npm run deploy:www` … www.faq-ishigaki.com → faq-ishigaki.com の転送（`www/`）を公開

検索は Google のサイト内検索へ。
ドメインを切り替えた後は `npm run fetch` は使えない（WordPress に届かないため止まる。取り直すときは hosts で古いサーバーに向ける）。
apart（サブドメイン）は別のサイト。
