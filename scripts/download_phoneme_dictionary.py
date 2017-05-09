import argparse
import json
import re
import os
import subprocess

parser = argparse.ArgumentParser(description='Download the phoneme dictionary and generate the mapping from words to phonemes')
parser.add_argument('--link', type=str, default='http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b')
parser.add_argument('--data', type=str, default='data')
parser.add_argument('--out', type=str, default='data/word2phoneme.json')
args = parser.parse_args()

# Download the file
phoneme_filename = os.path.join(args.data, 'phoneme_dict.txt')
download = 'wget ' + args.link + ' -O ' + phoneme_filename
subprocess.call(download, shell=True)

# Parse the file
regex = re.compile('[^a-zA-Z\']')
word2phoneme = {}
for line in open(phoneme_filename):
    if line.startswith(';;;'):
        continue
    elements = line.lower().strip().split(' ')
    word = regex.sub('', elements[0])
    phones = [regex.sub('', elem) for elem in elements[2:]]
    word2phoneme[word] = phones

# Print statistics
print "Total words: %d" % len(word2phoneme.keys())

# save file
save = open(args.out, 'w')
save.write(json.dumps(word2phoneme))

# Delete old phoneme
delete = 'rm ' + phoneme_filename
subprocess.call(delete, shell=True)
