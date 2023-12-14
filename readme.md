
| 基本機能 | ライブラリ |
| - | - |
| API | fastapi |
| lambda | sls |
| doc | fastapi |
| test | pytest |

```
poetry install --no-root
poetry run uvicorn main:app --reload
poetry run pytest
poetry run pytest --cov=.
poetry run pytest --cov=. -v --cov-report=html

# local実行
sls invoke local -f {function} --path {params.json}
sls invoke local -f api --path invoke.json

# デプロイ
sls deploy

# デプロイ一覧
sls deploy list --stage {env}

# 切り戻し (切り戻ししたときの元のものは消えない)
sls rollback --timestamp {timestamp} --stage {env}

# 全削除
sls remove --stage {env}
```

- [DockerでPoetryを使って環境構築しよう](https://book.st-hakky.com/hakky/try-poetry-on-docker/)