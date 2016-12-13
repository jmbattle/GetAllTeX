# -*- coding: utf-8 -*-
"""File_Downloader.py: Script for automating multi-file downloads

__author__ = "Jason M. Battle"
"""

import os
import re
import bs4
import glob
import time
import requests
import numpy as np

PROXY = {'http':'168.219.61.252:8080'}
URL = 'http://ftp.kaist.ac.kr/tex-archive/systems/win32/miktex/tm/packages/'
DIR = r'C:\Users\admin\Desktop\tex'

if not os.path.isdir(DIR):
    os.makedirs(DIR)

# Get full HTML from target URL
response = requests.get(URL, proxies=PROXY)
# Convert HTML to searchable object
soup = bs4.BeautifulSoup(response.text, 'html.parser')
# Extract all hyperlinks matching .tar.lzma file extension  
links = np.ravel(filter(None, map(lambda x: re.findall(r'.*tar.lzma', x.text), soup.findAll('a'))))
# Check list of already downloaded files
files = map(lambda x: x.split('\\')[-1], glob.glob(DIR + '\\' + '*.tar.lzma'))
# Remove existing files from download list
links = [link for link in links if link not in files]

START = time.time()

for idx, link in enumerate(links):
    print 'Downloading %s (%i/%i)...%.2f%% Complete.' % (link, idx+1, len(links), ((idx+1)/float(len(links)))*100)
    # Get file data
    data = requests.get(URL + link, proxies=PROXY, stream=True)
    # Write data to local file
    with open(DIR + '\\' + link, 'wb') as f:
        for chunk in data.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    time.sleep(1)

END = time.time()
DURATION = ((END - START) / 3600, ((END - START) % 3600) / 60, (((END - START) % 3600) % 60))

print 'All downloads completed in %02i:%02i:%02i' % (DURATION[0], DURATION[1], DURATION[2])
