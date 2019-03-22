from google.cloud import storage
from pathlib import Path
from json import dump
from courses import (
    SUBJECTS,
    get_term_courses,
    get_term_courses_from_response
)
import asyncio
from requests_futures.sessions import FuturesSession
import requests


CLASS_SEARCH_URL = 'https://psmobile.pitt.edu/app/catalog/classSearch'
CLASS_SEARCH_API_URL = 'https://psmobile.pitt.edu/app/catalog/getClassSearch'
SECTION_DETAIL_URL = 'https://psmobile.pitt.edu/app/catalog/classsection/UPITT/{term}/{section_number}'

storage_client = storage.Client()
bucket_name = 'wait-list-fall-2019'
bucket = storage_client.get_bucket(bucket_name)

term = '2201'

output_dir = Path('.') / 'out'

if not output_dir.exists():
    output_dir.mkdir()

output_dir /= term

if not output_dir.exists():
    output_dir.mkdir()



# Generate new CSRFToken

session_token = requests.Session()
session = FuturesSession(session=session_token, max_workers=16)

session_token.get(CLASS_SEARCH_URL)
crsf_token =  session_token.cookies['CSRFCookie']


def _get_payload(term, *, subject='', course='', section=''):
    """Make payload for request and generates CSRFToken for the request"""
    payload = {
        'CSRFToken':crsf_token,
        'term': term,
        'campus': 'PIT',
        'subject': subject,
        'acad_career': '',
        'catalog_nbr': course,
        'class_nbr': section
    }
    return payload

sections_numbers = []

async def get_subject(subject):
    try:
        print(subject)
        payload = _get_payload(term, subject=subject)
        future = session.post(CLASS_SEARCH_API_URL, data=payload)
        await asyncio.sleep(0)
        response = future.result()
        pitt_subject = get_term_courses_from_response(response, subject, term)
        await asyncio.sleep(0)
        for course in pitt_subject.courses:
            sections_numbers.extend(course.section_numbers)
        blob = storage.blob.Blob('initial/' + subject + '.json', bucket)
        with open(output_dir / (subject + '.json'), 'w') as f:
            dump(pitt_subject.to_dict(), f , indent='\t')
            await asyncio.sleep(0)
        with open(output_dir / (subject + '.json'), 'rb') as f:
            blob.upload_from_file(f)
    except:
        pass


loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.gather(*[get_subject(subject)
    for subject in SUBJECTS]))

with open('section_numbers.json', 'w') as f:
    dump(sections_numbers, f, indent='\t')
