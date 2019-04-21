
import asyncio
import json
from pathlib import Path
import requests_async as requests
from google.cloud import storage
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some section data')
parser.add_argument('--path', type=str)
args = parser.parse_args()

gcppath = datetime.now().strftime("%Y%m%d%H%M") + '/'

term = '2201'
sections = []
storage_client = storage.Client()
bucket_name = 'wait-list-fall-2019'
bucket = storage_client.get_bucket(bucket_name)
session = requests.Session()

output_dir = Path('.') / 'temp'

if not output_dir.exists():
    output_dir.mkdir()

output_dir /= term

if not output_dir.exists():
    output_dir.mkdir()

storage_client = storage.Client.from_service_account_json(
        'service_account.json')

SECTION_DETAIL_URL = 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/{term}/{section_number}'

with open(args.path) as f:
    sections = json.load(f)

async def get_section(section):
    global term
    resp = await session.get(SECTION_DETAIL_URL.format(term=term, section_number=section))
    blob = storage_client.blob.Blob(gcppath + section + '.json', bucket)
    with open(output_dir / (section + '.html'), 'w') as f:
        f.writelines(resp.text)
    with open(output_dir / (section + '.html'), 'rb') as f:
         blob.upload_from_file(f)



loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.gather(*[get_section(section) for section in sections]))
