#!/home/me/Documents/Codes/python/sb_dwn_logs/env/bin/python3

from datetime import datetime
import logging
import logging.config
import os
import re
import sys
from time import time

import requests
from tqdm import tqdm


logging.config.fileConfig('log_config.ini', defaults={'logfilename':'apilogs/downloads/timeline.log'})
logger = logging.getLogger(__name__)
'''
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s ~ %(levelname)s: %(message)s")
fh = logging.FileHandler("apilogs/downloads/timeline.log")
fh.setFormatter(formatter)
logger.addHandler(fh)
'''

sb_logs_file = "http://soda-bar.com/hide/loading_page.log"

if __name__ == '__main__':
    start = time()
    directory_name = "logs"
    here = os.getcwd()
    logs_dir = os.path.join(here, directory_name)

    if not os.path.isdir(logs_dir):
        os.makedirs(logs_dir)
    
    try:
        r = requests.get(sb_logs_file, stream=True)
        '''
        Check if status code if OK (200)
        '''
        if r.status_code != 200:
            r.raise_for_status()

        content_type = re.sub('[\s+]',
                              '',
                              r.headers['content-type']).split(';')[0]
        
        ''' Check if script is receiving the good data format
        (in case of error in URL)
         '''
        if content_type != 'text/plain':
            r.status_code = 500
            r.raise_for_status()

        total_size = int(r.headers.get('content-length', 0))

        now = datetime.now()

        filename_date = f"{now.year:}{now.month:02d}{now.day:02d}-{now.hour:02d}_{now.minute:02d}_{now.second:02d}.log"

        with open(os.path.join(logs_dir, filename_date), 'wb') as f:
            for data in tqdm(r.iter_content(32*1024),
                             total=total_size, unit='B',
                             unit_scale=True):
                f.write(data)
        end = time() - start
        logger.info(f"Downloaded {filename_date} to /logs/ in {end:.4f} sec.")

    except requests.exceptions.RequestException as e:
        logger.warning(f"Bad request: {e}")
        sys.exit(1)

    except requests.exceptions.Timeout as tm:
        logger.warning(f"Request Timeout: {tm}")
        sys.exit(1)

    except requests.exceptions.HTTPError as he:
        logger.warning(f"HTTP error: {he}")
        sys.exit(1)

