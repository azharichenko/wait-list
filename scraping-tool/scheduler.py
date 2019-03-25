import sched, time
from subprocess import Popen, PIPE
s = sched.scheduler(time.time, time.sleep)

def run_downloader():
    process = Popen(['./run_downloader'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    s.enter(15 * 60, 1, run_downloader)

s.enter(15 * 60, 1, run_downloader)
s.run()