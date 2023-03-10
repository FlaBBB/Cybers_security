import fileinput
import re
from time import strptime

f_names = ['all.access.log'] # names of log files
lines = list(fileinput.input(f_names))
t_fmt = '%d/%b/%Y:%H:%M:%S' # format of time stamps
t_pat = re.compile(r'\[(.+?)\]') # pattern to extract timestamp
files = open('sorted.access.log', 'w')
for l in sorted(lines, key=lambda l: strptime(t_pat.search(l).group(1), t_fmt)):
    files.write(l+'\n')