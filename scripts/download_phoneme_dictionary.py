import argparse
import json
import re
import os
import subprocess

parser = argparse.ArgumentParser(description='Download the phone dictionary and generate the mapping from words to phones')
parser.add_argument('--link', type=str, default='http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b')
parser.add_argument('--data', type=str, default='data')
parser.add_argument('--out', type=str, default='data/word2phones.json')
args = parser.parse_args()

# Download the file
phone_filename = os.path.join(args.data, 'phone_dict.txt')
download = 'wget ' + args.link + ' -O ' + phone_filename
subprocess.call(download, shell=True)

# Parse the file
regex = re.compile('[^a-zA-Z\']')
word2phone = {}
for line in open(phone_filename):
    if line.startswith(';;;'):
        continue
    elements = line.lower().strip().split(' ')
    word = regex.sub('', elements[0])
    phones = [regex.sub('', elem) for elem in elements[2:]]
    word2phone[word] = phones

# Print statistics
print "Total words: %d" % len(word2phone.keys())

# save file
save = open(args.out, 'w')
save.write(json.dumps(word2phone))

# Delete old phone
delete = 'rm ' + phone_filename
subprocess.call(delete, shell=True)
