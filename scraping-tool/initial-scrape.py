from pathlib import Path
from json import dump
from courses import (
    SUBJECTS,
    get_term_courses
)

term = '2201'

output_dir = Path('.') / 'out'

if not output_dir.exists():
    output_dir.mkdir()

output_dir /= term

if not output_dir.exists():
    output_dir.mkdir()

for subject in SUBJECTS:
    try:
        print(subject)
        pitt_subject = get_term_courses(term, subject)
        with open(output_dir / (subject + '.json'), 'w') as f:
            dump(pitt_subject.to_dict(), f , indent='\t')
    except:
        continue
