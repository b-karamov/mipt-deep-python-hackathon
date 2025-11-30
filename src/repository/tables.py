from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(255), nullable=False, unique=False),
    Column("created_date", DateTime, nullable=False)
)

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("content", Text, nullable=False),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("created_at", DateTime, nullable=False)
)

comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("post_id", Integer, ForeignKey("posts.id"), nullable=False),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("parent_id", Integer, ForeignKey("comments.id"), nullable=True),
    Column("text", Text, nullable=False),
    Column("created_at", DateTime, nullable=False)
)
