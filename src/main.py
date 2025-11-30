import asyncio
import shlex

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from repository.repository import Repository
from repository.tables import metadata
from service.comment_service import CommentService
from service.post_service import PostService
from service.user_service import UserService


DATABASE_URL = "sqlite+aiosqlite:///./commenthub.db"


def print_help() -> None:
    print(
        "Команды:\n"
        "  user add <username>\n"
        "  user list\n"
        "  post add <username> <title> <content>\n"
        "  post list\n"
        "  comment add <post_id> <username> <text>\n"
        "  comment reply <comment_id> <username> <text>\n"
        "  comment list <post_id>\n"
        "  help\n"
        "  quit\n"
    )


async def cli() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    repos = Repository(session_factory)
    user_service = UserService(repos)
    post_service = PostService(repos)
    comment_service = CommentService(repos)

    print("Простой CLI для CommentHub. Используй 'help' для подсказки.")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw:
            continue

        parts = shlex.split(raw)
        cmd = parts[0].lower()

        try:
            if cmd == "quit":
                break

            if cmd == "help":
                print_help()

            elif cmd == "user" and len(parts) >= 2:
                sub = parts[1]

                if sub == "add" and len(parts) >= 3:
                    user = await user_service.create_user(parts[2])
                    print(f"Создан пользователь: id={user.id}, username={user.username}")

                elif sub == "list":
                    users = await user_service.find_all()
                    for u in users:
                        print(f"{u.id}: {u.username} (created={u.created_date})")

                else:
                    print("Неправильная user-команда.")

            elif cmd == "post" and len(parts) >= 2:
                sub = parts[1]

                if sub == "add" and len(parts) >= 5:
                    username = parts[2]
                    title = parts[3]
                    content = " ".join(parts[4:])
                    post = await post_service.create_post(username, title, content)
                    print(
                        f"Опубликован пост: id={post.id}, title={post.title}, "
                        f"author={post.author.username}"
                    )

                elif sub == "list":
                    posts = await repos.posts.find_all()
                    for p in posts:
                        print(f"{p.id}: {p.title} by {p.author.username}")

                else:
                    print("Неправильная post-команда.")

            elif cmd == "comment" and len(parts) >= 2:
                sub = parts[1]

                if sub == "add" and len(parts) >= 5:
                    post_id = int(parts[2])
                    username = parts[3]
                    text = " ".join(parts[4:])
                    c = await comment_service.add_comment_to_post(post_id, username, text)
                    print(f"Создан комментарий: id={c.id} к посту {post_id}")

                elif sub == "reply" and len(parts) >= 5:
                    comment_id = int(parts[2])
                    username = parts[3]
                    text = " ".join(parts[4:])
                    c = await comment_service.reply_to_comment(comment_id, username, text)
                    print(f"Создан ответ: id={c.id} к комментарию {comment_id}")

                elif sub == "list" and len(parts) >= 3:
                    post_id = int(parts[2])
                    comments = await comment_service.get_comments_for_post(post_id)
                    for c in comments:
                        prefix = f"{c.id} (post {c.post.id})"
                        if c.parent:
                            prefix += f" reply_to={c.parent.id}"
                        print(f"{prefix}: {c.author.username} -> {c.text}")

                else:
                    print("Неправильная comment-команда.")

            else:
                print("Неизвестная команда, попробуй 'help'.")

        except Exception as exc:
            print(f"Ошибка: {exc}")

    await engine.dispose()


def main() -> None:
    asyncio.run(cli())


if __name__ == "__main__":
    main()
