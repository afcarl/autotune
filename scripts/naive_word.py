import argparse
import json
import re
import os

def parse_lyrics(f):
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in open(f):
        words = line.lower().strip().split(' ')
        words = [regex.sub('', word) for word in words]
        output.extend(words)
    return output

def find(word, folder, verbose=False):
    for file in os.listdir(os.path.join(folder, 'alignment')):
        if '.txt' not in file:
            continue
        try:
            alignment = json.load(open(os.path.join(folder, 'alignment', file)))
        except:
            if verbose:
                print "| Could not parse alignment in file: %s" % file
        if word not in alignment['transcript']:
            continue
        for w in alignment['words']:
            if w['word'].lower() == word and w['case'] == 'success':
                return {'filename': file.replace('.txt', ''),
                        'starttime': w['start'],
                        'duration': w['end'] - w['start']}
    return None

def main(args):
    words = parse_lyrics(args.lyrics)
    output = []
    memory = {}
    for word in words:
        if word in memory:
            elem = memory[word]
        else:
            elem = find(word, args.data, verbose=args.verbose)
            memory[word] = elem
        if elem is None:
            print "| Cound not find %s" % word
            continue
        output.append(elem)
    f = open(args.output, 'w')
    f.write(json.dumps(output))
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)


