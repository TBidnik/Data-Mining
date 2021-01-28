from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class MixIdUrl:
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id"))
)



class Post(Base, MixIdUrl):
    __tablename__ = "post"
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")
    tags = relationship("Tag", secondary=tag_post)

class Author(Base, MixIdUrl):
    __tablename__ = "author"
    name = Column(String, nullable=False)
    posts = relationship("Post")
    comment = relationship("Comment")

class Tag(Base, MixIdUrl):
    __tablename__ = "tag"
    name = Column(String, nullable=False)
    posts = relationship("Post", secondary=tag_post)


class Comment(Base, MixIdUrl):
    __tablename__ = "comment"
    text = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    parent = relationship("Comment")
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")

    @classmethod
    def create_from_json(cls, json_data: dict):
        return ""




