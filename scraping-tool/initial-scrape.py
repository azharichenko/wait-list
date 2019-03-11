from google.cloud import storage
from pathlib import Path
from json import dump
from courses import (
    SUBJECTS,
    get_term_courses
)

storage_client = storage.Client()
bucket_name = 'wait-list-fall-2019'
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob('')

term = '2201'

output_dir = Path('.') / 'out'

if not output_dir.exists():
    output_dir.mkdir()

output_dir /= term

if not output_dir.exists():
    output_dir.mkdir()

sections_numbers = []
for subject in SUBJECTS[:2]:
    try:
        print(subject)
        pitt_subject = get_term_courses(term, subject)
        with open(output_dir / (subject + '.json'), 'w') as f:
            dump(pitt_subject.to_dict(), f , indent='\t')
        with open(output_dir / (subject + '.json'), 'r') as f:
            blob.upload_from_file(f)
    except:
        continue
