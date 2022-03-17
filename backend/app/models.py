from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class Post(Base):
    __tablename__="posts"
    post_id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(String,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String)
    description = Column(String)
    creation_time = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    post_status = Column(String,nullable=False,default=True)