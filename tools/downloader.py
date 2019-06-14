
import asyncio
import json
from pathlib import Path
import requests_async as requests
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some section data')
parser.add_argument('--path', type=str)
args = parser.parse_args()

term = '2201'
sections = []

session = requests.Session()

output_dir = Path('.') / 'data'

if not output_dir.exists():
    output_dir.mkdir()

output_dir = output_dir / term 

if not output_dir.exists():
    output_dir.mkdir()

output_dir = output_dir / datetime.now().strftime("%Y%m%d%I%M")

if not output_dir.exists():
    output_dir.mkdir()

SECTION_DETAIL_URL = 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/{term}/{section_number}'

with open(args.path) as f:
    sections = json.load(f)

async def get_section(section):
    global term
    resp = await session.get(SECTION_DETAIL_URL.format(term=term, section_number=section))
    with open(output_dir / (section + '.html'), 'w') as f:
        f.writelines(resp.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[get_section(section) for section in sections]))
