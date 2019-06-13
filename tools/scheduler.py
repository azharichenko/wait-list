import sched, time, sys
from subprocess import Popen, PIPE
from pathlib import Path
s = sched.scheduler(time.time, time.sleep)

tool_path = Path('.') / 'tools'
tool_exists = tool_path.exists() and tool_path.is_dir()

if not tool_exists:
    print("Can't located tool directory", file=sys.stderr)
    exit()

downloader_script_path = tool_path / 'downloader.py'
fetch_script_path = tool_path / 'fetch-section-numbers'

tools_exist  = downloader_script_path.exists() and fetch_script_path.exists()
if not tool_exists:
    print("Can't find tools", file=sys.stderr)
    exit()

def chunks(l, n):
    """From: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def gather_available_files():
    """Returns a generator for pairs of file paths to section number part files"""
    section_number_path = Path('.') / 'output'
    files = [str(file.absolute()) for file in section_number_path.glob('section_numbers.*.json')]
    return chunks(files, 2)

def run_downloader():
    """Runs downloader script with section number part files"""
    section_files_pairs = gather_available_files()
    for pair in section_files_pairs:
        temp_processes = []
        for item in pair:
            temp_processes.append(
                Popen(['pipenv', 'run', 'python', './tools/downloader.py' , '--path', item], stdout=PIPE, stderr=PIPE)
            )
        for p in temp_processes:
            p.wait()
    s.enter(60 * 60, 1, run_downloader)

def run_section_number_scraper():
    """Runs fetch setcion numbers script
    This is done in case a section is either dropped or a new section has been formed
    """
    process = Popen(['pipenv', 'run', 'python', './fetch-section-numbers'], stdout=PIPE, stderr=PIPE)
    process.wait()
    s.enter(24 * 60 * 60, 1, run_section_number_scraper)

# Start off section number scraper, then start downloader loop
s.enter(0, 1, run_section_number_scraper)
s.enter(5 * 60, 1, run_downloader)
s.run()
