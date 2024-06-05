# chatbot

法政大学情報科学部の研究室をおすすめしてくれる ChatBot です。

1. 研究室紹介ページから各研究室に対応する単語をスクレイピングで取得
2. ユーザは単語の興味度合いを回答（Ex. 「機械学習について興味はありますか？」　→ 「あります」）
3. その単語に興味がある場合には、その単語が含まれている研究室を候補に追加
4. (研究室の候補数)　≦　３　になるまで、2~3を繰り返す
5. おすすめの研究室を提示

使用技術
以下の技術を使用しているため、それぞれライブラリ　または　パッケージを「pip install XXX」する必要があります
インストールされていない場合、正しくシステムが起動できないことがあります


1. スクレイピング   
   requests, beautifulsoup
3. Webフレームワーク   
   chatbotweb
5. BertModel   
   transformers, tensorflow, flax, fugashi, ipadic, janome, keras, torch

もしかしたら、Huggingfaceのインストールが必要かもしれないので、
https://huggingface.co/docs/transformers/ja/installation
を参照

