#!/usr/bin/env python3

# author: Rafał Przywara, (c) 2016
# license: MIT
# usage: adams.py disk_number
#
# Source wav files should be placed in subfolders named 'disk 1', 'disk 2', 'disk 3'.
# Wave files are expected to be named 'Track nn' where nn is the track number on the disk.
# Output is generated into subfolder mp3.

import os
import re
import glob
import sys
import subprocess

phase = 1
disk = 1

cmd = ['lame', '-b 96', '-h', '--ta', 'Douglas Adams', '--tl', "The Hitchhiker's Guide To The Galaxy. Primary Phase", '--ty', '2005', '--tg', 'other']

output = 'mp3'

###

first = -1

if len(sys.argv) > 1:
	disk = int(sys.argv[1])

start_from = disk * 2 - 1

print('Starting from episode {} / disk {}'.format(start_from, disk))

###

e = re.compile('^\s*Episode\s+([0-9]+):')
t = re.compile('^[0-9]+\.[0-9]+\s+(.+)$')

tracklist = []
en = 0

with open('tracklist', 'r') as f:

	for line in f:
		m = t.match(line)
		if m:
			if not en:
				print('INVALID EPISODE 0')
				exit(1)
			tracklist.append({'episode': en, 'title': m.group(1)})
		else:
			m = e.match(line)
			if m:
				en = int(m.group(1))
				if en == start_from: first = len(tracklist)
			else:
				print('NOT PARSED: [{}]'.format(line))
				exit(2)

###

if first < 0:
	print('NO SUCH EPISODE {}'.format(start_from))
	exit(3)

if not os.path.exists(output): os.mkdir(output)

f = re.compile('^Track\s+([0-9]+)')
r = re.compile('[<>:"/\\\\|?*]')

files = {}
src = 'disk {}'.format(disk)

for file in glob.glob(os.path.join(src, '*.wav')):

	m = f.match(file[len(src)+1:])
	if m:
		index = first + int(m.group(1)) - 1
		title = tracklist[index]['title']
		name = '{:02}-{}-PH{}E{}.mp3'.format(index + 1, title, phase, tracklist[index]['episode'])
		name = os.path.join(output, r.sub('_', name))
		files[file] = name
	else: print('skipped [{}]'.format(file))

i = 1
for wav, mp3 in files.items():
	subprocess.run(cmd + ['--tt', title, '--tn', '{}/{}'.format(index + 1, len(tracklist)), wav, mp3])
	print('{}/{} OK: {} --> {}'.format(i, len(files), wav, mp3))
	i += 1

print('Processed {} files'.format(len(files)))
