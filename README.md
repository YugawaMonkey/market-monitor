# Market Monitor — GitHub Pages公開用

## 公開方法

1. GitHubで公開用のリポジトリを作成します。GitHub Freeの場合はPublicを選びます。
2. このフォルダーの `index.html` と `.nojekyll` を、リポジトリの一番上にアップロードします。ZIPファイル自体や、フォルダーごとではなく、中身を配置してください。
3. リポジトリの **Settings → Pages** を開きます。
4. **Build and deployment → Source** で **Deploy from a branch** を選びます。
5. **Branch** をアップロード先のブランチ（通常 `main`）、フォルダーを **/(root)** にして **Save** を押します。
6. 公開処理の完了後、Pagesに表示される **Visit site** から開きます。

通常のプロジェクト用URLは `https://ユーザー名.github.io/リポジトリ名/` です。
ビルド、npm、APIキー、GitHub Secretsの設定は不要です。
既存リポジトリにindex.htmlがある場合は、上書き前に内容を確認してください。

公式手順：https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## ファイル

- `index.html`：HTML・CSS・JavaScript・統計計算を内蔵した公開用ファイル。名前を変更せず使用してください。
- `.nojekyll`：GitHub PagesでJekyllの処理を使わないための空ファイル。
- `README.md`：この説明。公開の動作には必須ではありません。

## 機能

- 15商品の選択、スマホ対応、6時間足のチャート、Market Signal。
- Contracts Overview：US100→NDX、US500→SPXのオプションページ。US30→DIA、XAUUSD→GLDは参考ETFの契約です。その他は商品チャートへのリンクです。
- 統計予測：USDJPY・AUDJPY・EURUSD・GBPUSD・BTCUSDの日次履歴を自動取得し、次回／5観測日先の中心・範囲・過去検証を表示。
- 未対応商品の統計予測は未接続と表示します。デモの数値は架空です。

## データ取得と依存先

GitHub Pagesは静的ファイルのホスティングです。このHTMLだけで画面と統計計算は動きますが、実データにはインターネット接続と下記の配信元が必要です。

| 用途 | 取得先 |
| --- | --- |
| チャート・Market Signal | TradingViewの公式埋め込み部品 |
| Macro Monitor | 既存の公開サイトの `/api/macro` |
| 統計予測用の価格履歴 | 既存の公開サイトの `/api/history`（ECB／Coin Metrics） |

既存APIのURL：`https://market-monitor-hx-0916.hongxy0816.chatgpt.site`

**元のSitesサイトを停止・削除・非公開化すると、GitHub Pages版でもマクロ指標と統計予測の自動取得が使えなくなります。** GitHub Pagesだけに完全移行した構成ではありません。既存APIは公開状態で維持してください。
将来APIを移転する場合は、同じ応答形式・外部サイトからのアクセス許可（CORS）を用意し、HTML内の `PUBLIC_ORIGIN` を移転先へ変更します。

各配信元の休場・遅延・取得制限で表示されない場合があります。無料枠や配信サービスの継続を保証するものではありません。

## データの扱い

為替の予測はECBの参考レートから当サイトが換算・計算したもので、OANDAの市場価格やECBの予測ではありません。BTCの日次データはCoin Metrics Communityの **CC BY-NC 4.0（非商用）** によります。出典・ライセンス表示を残してください。商用利用には別途条件の確認が必要です。
80%予測範囲は統計モデル上の水準であり、価格が必ず収まる範囲や実際の確率を保証しません。

## 手元で確認

`index.html` をブラウザーで開けます。ネット接続が必要です。ローカルファイルからの外部アクセスをブラウザーが制限する場合は、GitHub Pagesに公開して確認してください。
URL末尾に `?product=USDJPY#prediction` を付けると、USDJPYの統計予測から開けます。
