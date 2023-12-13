
| 基本機能 | ライブラリ |
| - | - |
| API | fastapi |
| lambda | sls |
| doc | fastapi |
| test | pytest |

```
poetry install --no-root
uvicorn main:app --reload
poetry run pytest
poetry run pytest --cov=. -v --cov-report=html

sls deploy
sls remove
```

- [DockerでPoetryを使って環境構築しよう](https://book.st-hakky.com/hakky/try-poetry-on-docker/)