import argparse
import json
import utils

parser = argparse.ArgumentParser(description='Generate a map connecting word and when they occur in ')
parser.add_argument('--data', type=str, default='data/obama')
parser.add_argument('--verbose', action='store_true', default=False)
parser.add_argument('--wordmap', type=str, default='data/obama/gen/wordmap.json')
parser.add_argument('--phonemap', type=str, default='data/obama/gen/phonemap.json')
args = parser.parse_args()

wordmap = utils.collect_words(args.data, verbose=args.verbose)
f = open(args.wordmap, 'w')
f.write(json.dumps(wordmap))
f.close()
phonemap = utils.collect_phones(args.data, verbose=args.verbose)
f = open(args.phonemap, 'w')
f.write(json.dumps(phonemap))
f.close()
