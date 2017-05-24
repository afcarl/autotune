import argparse
import json
import utils

def find(choices):
    curr = None
    for choice in choices:
        if curr is None or curr['duration'] < choice['duration']:
            curr = choice
    return curr

def main(output, phones, memory, verbose=False):
    clips = []
    for progress, phone in enumerate(phones):
        if verbose and progress % 100 == 0:
            print "Progress: %d / %d" % (progress, len(phones))
        if phone in memory:
            choices = memory[phone]
            choice = find(choices)
        else:
            print "| Cound not find %s" % phone
            continue
        clips.append(choice)
    f = open(output, 'w')
    f.write(json.dumps(clips))
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

    phonetics = utils.Phonetics(args.word2phones)
    if args.verbose:
        print "| Parsing lyrics"
    phones = phonetics.parse_phones(utils.read_file(args.lyrics))
    if args.verbose:
        print "| Done parsing lyrics. %d phones found." % len(phones)
    memory = json.load(open(args.phonemap))
    main(args.output, phones, memory, verbose=args.verbose)


