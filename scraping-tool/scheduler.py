from subprocess import Popen, PIPE

process = Popen(['pipenv', 'run', 'python', './scraping-tool/downloader.py', '--path' ' ./output/section_numbers.0.json', '--gcppath', ' "initial_run/"'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout)
print(stderr)