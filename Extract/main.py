import argparse
import logging
import re
import requests
import datetime
import csv
import pandas as pd
import lxml.html as html
logging.basicConfig(level=logging.INFO)
from common import config

logger = logging.getLogger(__name__)
is_root_path = re.compile(r'^/.+$')


def _news_scraper(news_site_uid):
    paths = config()['news_sites'][news_site_uid]
    host = paths['url']
    logging.info(f'Beginning scraper for {host}')

    try:
        response = requests.get(paths['url'])
        if response.status_code == 200:
            logger.info(f'Parsing url...')
            final_articles = []

            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(paths['queries']['XPATH_HOMEPAGE_LINKS_TO_ARTICLES'])

            good_links = _fix_links(links_to_news, host)

            
            for i, link in enumerate(good_links):
                try:
                    article_response = requests.get(link, timeout=6)
                    article = article_response.content.decode('utf-8')
                    article_parsed = html.fromstring(article)
                    article_elements = {}

                    title = article_parsed.xpath(paths['queries']['XPATH_TITLE'])
                    if len(title):
                        article_elements['title'] = title[0]
                    else:
                        article_elements['title'] = None

                    body = article_parsed.xpath(paths['queries']['XPATH_BODY'])  
                    p_elements = []
                    for text in body:
                        if str(text)[0] in [',', '.', ' ']:
                            p_elements.append(str(text))
                        else:
                            p_elements.append(' ' + str(text))


                    body = ''.join(p_elements)
                    if len(body):
                        article_elements['body'] = body
                    else:
                        article_elements['body'] = None


                    date = article_parsed.xpath(paths['queries']['XPATH_DATE'])
                    if len(date):
                        article_elements['date'] = date[0]
                    else:
                        article_elements['date'] = None

                    author = article_parsed.xpath(paths['queries']['XPATH_AUTHOR'])
                    if len(author):
                        article_elements['author'] = author[0]
                    else:
                        article_elements['author'] = None

                    article_elements['url'] = link
                    final_articles.append(article_elements)

                    logger.info(f'Article {i+1}/{len(good_links)} scraped!')
                except Exception as e:
                    print(e)


            return final_articles

        else:
            print(f'Error. Status code {response.status_code}')


    except ValueError as ve:
        print(ve)

def _fix_links(links_to_news, host):
    logger.info('Fixing links')
    fixed_links_aux = []
    for link in links_to_news:
        if link[0] == '/':
            fixed_links_aux.append(host + link)
        else:
            fixed_links_aux.append(link)
    fixed_links = []
    for link in fixed_links_aux:
        if link[-1] == '/':
            fixed_links.append(link[:-1])
        else:
            fixed_links.append(link)

    return fixed_links
            
    
def _save_articles(data, news_site_uid):
    print('Saving data...')
    
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{news_site_uid}_{now}_articles.csv'
    df = pd.DataFrame(data)
    df.to_csv(out_file_name, index = False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='News site to be scraped',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    articles = _news_scraper(args.news_site)
    _save_articles(articles, args.news_site)
