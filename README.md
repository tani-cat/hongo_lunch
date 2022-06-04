# 本郷ランチ
hp: https://hongo-lunch.herokuapp.com/

## Conrtibuting
あまり時間が取れていないので、Issueにやりたいことを積んであります。
協力いただける方は、forkした上で `develop` にPRを出してください。

### 環境整備
手元で実行する際には、 `hongo_lunch/settings/local.py` を配置する必要があります。
`hongo_lunch/settings/secret_key.py` に、以下のようなコードを記述して配置してください。
```python
_SECRET_KEY_CODE = '(ここにシークレットキーの文字列)'
```

シークレットキーは、以下のサイトを参考に生成してください。
https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5#get_random_secret_key

### データ
以下のコマンドで読み込めます。
```python
python manage.py loaddata fixtures/import_data.json
```

管理者サイトのユーザーは `createsuperuser` で生成してください。

### 動作検証
http://127.0.0.1:8000/ で検証できます。

## 連絡先
[tanipen @Twitter](https://twitter.com/tanipen_3163)
