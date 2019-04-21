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

term = '2201'

requirements = ['SCGE', 'DSGE']

output_dir = Path('.') / 'output'

if not output_dir.exists():
    output_dir.mkdir()

loop = asyncio.get_event_loop()

# Generate new CSRFToken and Session
token_session = requests.Session()
session = FuturesSession(session=token_session, max_workers=16)

token_session.get(CLASS_SEARCH_URL)
crsf_token = token_session.cookies['CSRFCookie']

count = 0

def _get_payload(term, *, subject='', course='', section='', crse_attr=''):
    """Make payload for request and generates CSRFToken for the request"""
    global crsf_token
    payload = {
        'CSRFToken':crsf_token,
        'term': term,
        'campus': 'PIT',
        'subject': subject,
        'acad_career': '',
        'catalog_nbr': course,
        'class_nbr': section,
        'crse_attr':  crse_attr
    }
    return payload

sections_numbers = []

async def get_subject(subject):
    global session, count
    print(subject)
    payload = _get_payload(term, subject=subject)
    future = session.post(CLASS_SEARCH_API_URL, data=payload)
    await asyncio.sleep(0)
    response = future.result()
    pitt_subject = get_term_courses_from_response(response, subject, term)
    for course in pitt_subject.courses:
        await asyncio.sleep(0)
        sections_numbers.extend(course.section_numbers)


async def get_gen_eds(attr):
    global session, count
    print(attr)
    payload = _get_payload(term, crse_attr=attr)
    future = session.post(CLASS_SEARCH_API_URL, data=payload)
    await asyncio.sleep(0)
    response = future.result()
    pitt_subject = get_term_courses_from_response(response, 'SEARCH', term)
    for course in pitt_subject.courses:
        await asyncio.sleep(0) 
        sections_numbers.extend(course.section_numbers)
    

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.gather(*[get_subject(subject)
    for subject in SUBJECTS], *[get_gen_eds(attr) for attr in requirements]))

sections_numbers = sorted(list(set(sections_numbers)))
for i in range((len(sections_numbers) // 60) + 1):
    with open(output_dir / 'section_numbers.{}.json'.format(i), 'w') as f:
        try:
            dump(sections_numbers[60 * i: 60 * (i + 1)], f, indent='\t')
        except:
            dump(sections_numbers[60 * i:], f, indent='\t')    
