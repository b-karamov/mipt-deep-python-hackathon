## CommentHub

Исходный код приложения: доменные модели, сервисы, репозитории и демо-CLI в `main.py`.

### Структура проекта:
```
.
├── .gitignore
├── src
│   ├── README.md                # краткое описание исходников
│   ├── main.py                  # простое CLI
│   ├── domain                   # доменные сущности и валидация
│   │   ├── README.md
│   │   ├── descriptors.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── repository               # репозитории и контейнер
│   │   ├── README.md
│   │   ├── repository.py
│   │   ├── user_repository.py
│   │   ├── post_repository.py
│   │   └── comment_repository.py
│   └── service                  # бизнес-логика поверх домена/репозиториев
│       ├── README.md
│       ├── user_service.py
│       ├── post_service.py
│       └── comment_service.py
└── ...                          # прочие файлы/каталоги проекта
```
