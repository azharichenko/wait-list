import sched, time
from subprocess import Popen, PIPE
s = sched.scheduler(time.time, time.sleep)

def run_downloader():
    process = Popen(['bash', '/home/azharichenko/Projects/wait-list/run_downloader'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    s.enter(15 * 60, 1, run_downloader)

def run_section_number_scraper():
    process = Popen(['pipenv', 'run', 'python', '/home/azharichenko/Projects/wait-list/tools/fetch-section-numbers'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    s.enter(24 * 60 * 60, 1, run_section_number_scraper)

s.enter(5 * 60, 1, run_downloader)
s.enter(0, 1, run_section_number_scraper)
s.run()
