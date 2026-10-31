# 数え方クイズ 低学年イラスト配置・検証報告

作業日：2026/10/31（日本時間）
基準：Kussoon/games main `33eeb501b48e2c7c299e97c97ea70baf3d8338d7`。
対象：`kazoekata/kazoekata.html`。

## 結果

低学年50問すべてに画像を対応付けました。未対応は0問です。追加ZIPの5点を反映し、前回不足していた5問も表示確認しました。
新規画像は49ファイルです。「えほん」は提供候補と既存画像を目視比較し、同じ絵柄・文字だったため、既存480×320 WebPをそのまま再利用しました。
提供候補のpicture_book.webpは重複追加していません。既存ヘッダー画像も維持しています。
50問の画像合計は約3.37 MiB。最初の44追加WebPは再圧縮せず、今回の5PNGは1200×900・品質90のWebPへ変換しました。5点合計は約330 KiBです。HTMLへのBase64埋め込みはありません。

問題番号などの既存情報 → 画像 → 既存問題文 → 4択の順に表示します。
画像は白背景・object-fit:contain・幅上限360px・高さ上限260px（画面高の32%以内）で、縦横比を保ちます。追加キャプションはありません。
絵本の従来の画像専用例外を一般の画像表示へ統合し、元データの問題文「えほん」を画像下へ表示しています。
画像の読込に失敗しても画像枠を隠して問題文と回答を維持します。
問題切替時にはタイトルへのフォーカスで画像が画面外へ送られないよう、フォーカス時の自動スクロールを抑えてページ上部へ戻します。

## 未対応

未対応0問。追加ZIPにより以下の5問も対応済みです。

| 問題ID | 対象語 | 画像 |
|---|---|---|
| lower-005 | ペットボトル | images/pet-bottle.webp |
| lower-012 | タオル | images/towel.webp |
| lower-016 | 本 | images/book.webp |
| lower-022 | 自転車 | images/bicycle.webp |
| lower-033 | アリ | images/ant.webp |

## 対応上の補足

- タオル（lower-012）：追加画像は折り畳んだ単体のタオルです。設問の「ひろげた」と描写差があります。題材と正解「枚」は一致するため提供画像を配置し、問題文・正解は原文を維持しました。

- お米のつぶ（lower-041）：提供画像の「おこめ」を対応。精米・ばらの米粒を確認。問題文の「粒」を書き換えていません。
- あめ玉（lower-049）：提供画像の「あめ」を対応。棒なしの丸い飴ですが個包装は描かれています。問題文の「袋から出した」「棒のついていない」は変更していません。
- おりがみ、クレヨン、ストローなど：複数物や補助的な小物を含む提供候補をそのまま採用。画像の個数を答える問題には変更していません。
- 各画像の文字は提供一覧と目視照合。漢字の対象語は読みで一致させています。

## 検証結果

| 確認内容 | 結果 |
|---|---|
| 全200問の埋め込みJSON | mainと文字列単位で完全一致（問題文・選択肢候補・正解・解説を保全） |
| フッター・Umami設定 | mainと完全一致 |
| 画像50点 | 実画像デコード成功、設定寸法一致、対象語と目視照合 |
| 390×844 / 1366×768 | 各50問のpreview URLを開いて確認（計100回） |
| 画像取得 | 上記の各画面で50画像がHTTP 200相当のローカルファイル配信・画像decode成功 |
| 未対応 | 0問。追加5問も画像・既存問題文・4択・正答・次問遷移を確認 |
| 表示順・領域 | 画像が問題文より上、画面幅以内、画像と文字の重なりなし、横スクロールなし |
| 全4コース | 前回、各50問を2画面幅で完走（計400回答）。今回の変更は画像対応表のみで、全200問のJSON・ゲーム処理は前回と同一 |
| 4択・正誤・採点 | 各プレイ最初の1問を誤答、残り49問正答→49/50を確認 |
| 誤答再挑戦 | 1問のみ再挑戦→1/1を確認、元の50問結果も保持 |
| 同コース再挑戦・中断 | 再開50問・コース選択への復帰を確認 |
| ランダム出題 | 5回生成で各50件重複なし、順序の変化あり |
| 高学年preview | upper-001の先頭固定、低学年画像が表示されないことを確認 |
| 無効preview | コース選択に戻ることを確認 |
| 320 / 375 / 430px + dark | 画像の白背景、横スクロールなしを確認 |
| 画像404の模擬 | 画像枠だけ非表示、問題文と4択を維持 |
| 実行時JSエラー | 通常検証で0件 |

実行環境はLinux上のPlaywright + Chromium headless（136系）です。ローカルHTML/画像をリクエストへ返して検証し、Umamiへの通信はテスト時のみ遮断しました。製品HTMLの解析設定はそのままです。
日本語フォント導入後の環境で、今回も50問×2画面幅の表示検証を実行し、追加5問の正答・次問遷移と代表画面を確認しました。
**iPhone Safari、Chromebook Chromeの実機確認は未実施です。WebKit環境は起動要件を満たせず、Safariエンジンでの検証も未実施です。**
全50問を端末実機で確認済みという意味ではありません。幅の検証と実機検証を区別しています。
公開URLはmainが更新されるまで従来どおりです。mainへのマージ・公開は行っていません。

## 50問の対応一覧

詳細な元問題文・正解・画像内文字・検証状況は mapping.csv に収録しています。

| 問題ID | 対象語 | 画像ファイル名 | 対応状況 |
|---|---|---|---|
| lower-001 | えんぴつ | images/pencil.webp | 対応済 |
| lower-002 | ボールペン | images/ballpoint_pen.webp | 対応済 |
| lower-003 | クレヨン | images/crayon.webp | 対応済 |
| lower-004 | かさ | images/umbrella.webp | 対応済 |
| lower-005 | ペットボトル | images/pet-bottle.webp | 対応済 |
| lower-006 | 木 | images/tree.webp | 対応済 |
| lower-007 | 紙 | images/paper.webp | 対応済 |
| lower-008 | おりがみ | images/origami.webp | 対応済 |
| lower-009 | 写真 | images/photograph.webp | 対応済 |
| lower-010 | ストロー | images/straw.webp | 対応済 |
| lower-011 | ハンカチ | images/handkerchief.webp | 対応済 |
| lower-012 | タオル | images/towel.webp | 対応済 |
| lower-013 | お皿 | images/plate.webp | 対応済 |
| lower-014 | はがき | images/postcard.webp | 対応済 |
| lower-015 | シール | images/sticker.webp | 対応済 |
| lower-016 | 本 | images/book.webp | 対応済 |
| lower-017 | ノート | images/notebook.webp | 対応済 |
| lower-018 | 絵本 | images/ehon-open-book.webp | 対応済 |
| lower-019 | 辞書 | images/dictionary.webp | 対応済 |
| lower-020 | 雑誌 | images/magazine.webp | 対応済 |
| lower-021 | 車 | images/car.webp | 対応済 |
| lower-022 | 自転車 | images/bicycle.webp | 対応済 |
| lower-023 | テレビ | images/television.webp | 対応済 |
| lower-024 | パソコン | images/computer.webp | 対応済 |
| lower-025 | れいぞうこ | images/refrigerator.webp | 対応済 |
| lower-026 | せんたくき | images/washing_machine.webp | 対応済 |
| lower-027 | ねこ | images/cat.webp | 対応済 |
| lower-028 | いぬ | images/dog.webp | 対応済 |
| lower-029 | 金魚 | images/goldfish.webp | 対応済 |
| lower-030 | メダカ | images/medaka.webp | 対応済 |
| lower-031 | カエル | images/frog.webp | 対応済 |
| lower-032 | カブトムシ | images/rhinoceros_beetle.webp | 対応済 |
| lower-033 | アリ | images/ant.webp | 対応済 |
| lower-034 | 小鳥 | images/small_bird.webp | 対応済 |
| lower-035 | ニワトリ | images/chicken.webp | 対応済 |
| lower-036 | アヒル | images/duck.webp | 対応済 |
| lower-037 | ゾウ | images/elephant.webp | 対応済 |
| lower-038 | ウシ | images/cow.webp | 対応済 |
| lower-039 | ウマ | images/horse.webp | 対応済 |
| lower-040 | くつ | images/shoe_pair.webp | 対応済 |
| lower-041 | お米のつぶ | images/rice.webp | 対応済 |
| lower-042 | 豆 | images/beans.webp | 対応済 |
| lower-043 | りんご | images/apple.webp | 対応済 |
| lower-044 | みかん | images/mandarin_orange.webp | 対応済 |
| lower-045 | たまご | images/egg.webp | 対応済 |
| lower-046 | けしゴム | images/eraser.webp | 対応済 |
| lower-047 | ボール | images/ball.webp | 対応済 |
| lower-048 | 風船 | images/balloon.webp | 対応済 |
| lower-049 | あめ玉 | images/candy.webp | 対応済 |
| lower-050 | さいころ | images/dice.webp | 対応済 |

## 提供ファイル

- kazoekata.html：修正HTML
- images/：実行に必要な51画像（49追加＋既存絵本・既存ヘッダー）
- illustration-audit/mapping.csv：低学年50問の対応表・元問題文・正解・表示確認
- illustration-audit/unmatched.csv：未対応0問（ヘッダーのみ）
- illustration-audit/changed-files.txt：GitHub変更対象の一覧（既存2画像は変更対象外）
- illustration-audit/verification.json：検証集計と各問題の表示計測

ZIPはkazoekataディレクトリの形で収録しています。既存の同名ディレクトリへ重ねる構成です。
検証資料は管理者用で、ページ内ナビゲーションには追加していません。
