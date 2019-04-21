import sched, time
from subprocess import Popen, PIPE
s = sched.scheduler(time.time, time.sleep)

def run_downloader():
    process = Popen(['bash', '/home/azharichenko/Projects/wait-list/run_downloader'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    s.enter(60 * 60, 1, run_downloader)

s.enter(5 * 60, 1, run_downloader)
s.run()
