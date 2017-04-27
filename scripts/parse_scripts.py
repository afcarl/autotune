import argparse
import re
import os

def condition(line):
    return '-->' in line \
        or len(line) == 0 \
        or re.search('[a-zA-Z]+', line) is None

def parse(directory):
    for f in os.listdir(directory):
        suffix = '.en.srt'
        if suffix not in f:
            continue
        name = f.replace(suffix, '')
        ff = open(os.path.join(directory, f))
        lines = ff.readlines()
        ff.close()
        out = open(os.path.join(directory, name + '.txt'), 'w')
        for i, line in enumerate(lines):
            if condition(line):
                continue
            out.write(line.strip() + '\n')
        out.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('-dir', type=str, default='data/obama_videos')
    args = parser.parse_args()
    parse(args.dir)


