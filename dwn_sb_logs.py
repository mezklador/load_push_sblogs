#!/home/me/Documents/Codes/python/sb_dwn_logs/env/bin/python3

import os

import requests
from tqdm import tqdm


sb_logs_file = "http://soda-bar.fr/hide/loading_page.log"

if __name__ == '__main__':
    directory_name = "logs"
    here = os.getcwd()
    logs_dir = os.path.join(here, directory_name)

    if not os.path.isdir(logs_dir):
        os.makedirs(logs_dir)

    r = requests.get(sb_logs_file, stream=True)
    total_size = int(r.headers.get('content-length', 0))

    with open(os.path.join(logs_dir, 'current_sb_log.log'), 'wb') as f:
        for data in tqdm(r.iter_content(32*1024),
                         total=total_size, unit='B',
                         unit_scale=True):
            f.write(data)

