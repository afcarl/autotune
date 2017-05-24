import argparse
import json
import utils

def find(choices):
    curr = None
    for choice in choices:
        if curr is None or curr['duration'] < choice['duration']:
            curr = choice
    return curr

def main(output, words, memory):
    clips = []
    for word in words:
        if word in memory:
            choices = memory[word]
        else:
            print "| Cound not find %s" % word
            continue
        choice = find(choices)
        clips.append(choice)
    f = open(output, 'w')
    f.write(json.dumps(clips))
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate a naive greedy order of videos speaking the lyrics')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--wordmap', type=str, default='data/obama/gen/wordmap.json')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()

    words = utils.parse_words(utils.read_file(args.lyrics))
    memory = json.load(open(args.wordmap))
    main(args.output, words, memory)
