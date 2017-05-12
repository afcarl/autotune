import argparse
import json
import utils

def find(choices):
    curr = None
    for choice in choices:
        if curr is None or curr['duration'] < choice['duration']:
            curr = choice
    return curr

def main(args):
    phonetics = utils.Phonetics(args.word2phones)
    if args.verbose:
        print "| Parsing lyrics"
    phones = phonetics.parse_lyric_phones(args.lyrics)
    if args.verbose:
        print "| Done parsing lyrics. %d phones found." % len(phones)
    output = []
    memory = json.load(open(args.phonemap))
    for progress, phone in enumerate(phones):
        if args.verbose and progress % 100 == 0:
            print "Progress: %d / %d" % (progress, len(phones))
        if phone in memory:
            choices = memory[phone]
            choice = find(choices)
        else:
            print "| Cound not find %s" % phone
            continue
        output.append(choice)
    f = open(args.output, 'w')
    f.write(json.dumps(output))
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate a naive greedy order of videos speaking the lyrics')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--phonemap', type=str, default='data/obama/gen/phonemap.json')
    parser.add_argument('--word2phones', type=str, default='data/word2phones.json')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    main(args)


