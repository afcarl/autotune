import argparse
import json
import os
import utils

def find(phoneme, folder, verbose=False):
    output = None
    for file in os.listdir(os.path.join(folder, 'alignment')):
        if '.txt' not in file:
            continue
        try:
            alignment = json.load(open(os.path.join(folder, 'alignment', file)))
        except:
            continue
        for w in alignment['words']:
            if w['case'] != 'success':
                continue
            start = w['start']
            for phone in w['phones']:
                p = phone['phone'][0:phone['phone'].index('_')]
                if phoneme == p \
                    and (output is None or output['duration'] < phone['duration']):
                    output = {'filename': file.replace('.txt', ''),
                              'starttime': start,
                              'duration': phone['duration']}
                start += phone['duration']
    return output

def main(args):
    phonetics = utils.Phonetics(args.word2phoneme)
    if args.verbose:
        print "| Parsing lyrics"
    phonemes = utils.parse_lyric_phonemes(args.lyrics, phonetics)
    if args.verbose:
        print "| Done parsing lyrics. %d phonemes found." % len(phonemes)
    output = []
    memory = {}
    for progress, phoneme in enumerate(phonemes):
        if args.verbose and progress % 100 == 0:
            print "Progress: %d / %d" % (progress, len(phonemes))
        if phoneme in memory:
            elem = memory[phoneme]
        else:
            elem = find(phoneme, args.data, verbose=args.verbose)
            memory[phoneme] = elem
        if elem is None:
            print "| Cound not find %s" % phoneme
            continue
        output.append(elem)
    f = open(args.output, 'w')
    f.write(json.dumps(output))
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate a naive greedy order of videos speaking the lyrics')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--word2phoneme', type=str, default='data/word2phoneme.json')
    args = parser.parse_args()
    main(args)


