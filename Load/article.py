from sqlalchemy import Column, String, Integer

from base import Base

class Article(Base):
    __tablename__ = 'articles'
    # uid,body,title,url,newspaper_uid,host,token_title,token_body
    # uid,body,title,url,newspaper_uid,host,token_title,token_body
    uid = Column(String, primary_key=True)
    body = Column(String)
    title = Column(String)
    url = Column(String, unique = True)
    newspaper_uid = Column(String)
    host = Column(String)
    token_title = Column(Integer)
    token_body = Column(Integer)

    def __init__(self,
                uid,
                body,
                title,
                url,
                newspaper_uid,
                host,
                token_title,
                token_body):

        self.uid = uid
        self.body = body
        self.title = title
        self.url = url
        self.newspaper_uid = newspaper_uid
        self.host = host
        self.token_title = token_title
        self.token_body = token_body
