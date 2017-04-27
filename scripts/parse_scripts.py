import argparse
import re
import os

def condition(line):
    return '-->' in line \
        or len(line) == 0 \
        or re.search('[a-zA-Z]+', line) is None

def parse(args):
    for f in os.listdir(args.dir):
        suffix = '.en.srt'
        if suffix not in f:
            continue
        name = f.replace(suffix, '')
        ff = open(os.path.join(args.dir, f))
        lines = ff.readlines()
        ff.close()
        out = open(os.path.join(args.out, name + '.txt'), 'w')
        for i, line in enumerate(lines):
            if condition(line):
                continue
            out.write(line.strip() + '\n')
        out.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--dir', type=str, default='data/obama/videos')
    parser.add_argument('--out', type=str, default='data/obama/subtitles')
    args = parser.parse_args()
    parse(args)
