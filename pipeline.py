import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import datetime

logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal', 'elpais', 'cnn', 'pagina12']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('Starting extraction process')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python3', 'main.py', news_site_uid], cwd='./Extract')
        subprocess.run(['find', '.', '-name', f'{news_site_uid}*',
                        '-exec', 'mv', '{}', f'../Transform/{news_site_uid}_.csv',
                        ';'], cwd='./Extract')

def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = f'{news_site_uid}_.csv'
        clean_data_filename = f'clean_{dirty_data_filename}'

        subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./Transform')
        subprocess.run(['rm', dirty_data_filename], cwd='./Transform')
        subprocess.run(['mv', clean_data_filename, f'../Load/{news_site_uid}_.csv'],
        cwd='./Transform')

def _load():
    logger.info('Starting loading process')
    for news_site_uid in news_sites_uids:
        now = datetime.datetime.now().strftime('%Y_%m_%d')
        clean_data_filename = f'{news_site_uid}_.csv'
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./Load')
        subprocess.run(['rm', clean_data_filename], cwd='./Load')
        subprocess.run(['mv', 'newspaper.db', f'../Databases/{news_site_uid}_{now}.db'], cwd='./Load')


if __name__ == "__main__":
    main()