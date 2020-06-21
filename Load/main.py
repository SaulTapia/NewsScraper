import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from article import Article
from base import Base, Engine, Session

logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(Engine)
    session = Session()
    articles = pd.read_csv(filename)
    # uid,body,title,url,newspaper_uid,host,token_title,token_body
    for index, row in articles.iterrows():
        logger.info(f'Saving article {index}')
        article = Article(  row['uid'],
                            row['body'],
                            row['title'],
                            row['url'],
                            row['newspaper_uid'],
                            row['host'],
                            row['token_title'],
                            row['token_body'])

        session.add(article)

    session.commit()
    session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='File to load into db',
                        type=str)
    
    args = parser.parse_args()

    main(args.filename)