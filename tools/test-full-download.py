# -*- coding: cp1252 -*-

import asyncio
import json
import queue
import requests
from pathlib import Path


from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession

term = '2201'
sections = []
session = FuturesSession(max_workers=16)

config = {
    'still_processing': True,
    'counter': 0,
    'queue':queue.Queue()
}

output_dir = Path('.') / 'dataout'

if not output_dir.exists():
    output_dir.mkdir()

output_dir /= term

if not output_dir.exists():
    output_dir.mkdir()


SECTION_DETAIL_URL = 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/{term}/{section_number}'

with open('section_numbers.json') as f:
    sections = json.load(f)

async def get_section(sections, config):
    global term
    for section in sections:
        future = session.get(SECTION_DETAIL_URL.format(term=term, section_number=section))
        config['queue'].put_nowait(future)
        await asyncio.sleep(0)
    config['still_processing'] = False

async def process_sections(config):
    while config['still_processing']:
        await asyncio.sleep(6)
        while not config['queue'].empty():
            future = config['queue'].get()
            response = future.result()
            with open(output_dir / (str(config['counter']) + '.html'), 'wb') as f:
                f.write(response.text.encode( 'UTF-8'))
            config['counter'] += 1
            config['queue'].task_done()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(get_section(sections, config), process_sections(config)))