from sqlalchemy import TIMESTAMP, Column, Integer, Boolean, String, text, ForeignKey
from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='true')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner=relationship("User")

class User(Base):
    __tablename__ = 'users'

    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer,primary_key=True, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
