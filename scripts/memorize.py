import argparse
import json
import os
import utils

parser = argparse.ArgumentParser(description='Generate a map connecting word and when they occur in ')
parser.add_argument('--data', type=str, default='data/obama')
parser.add_argument('--verbose', action='store_true', default=False)
parser.add_argument('--outdir', type=str, default='data/obama/gen')
parser.add_argument('--ngrams', type=int, default=[1, 2, 3, 4, 5], nargs='+')
args = parser.parse_args()

wordmap = utils.collect_words(args.data, verbose=args.verbose)
f = open(os.path.join(args.outdir, 'wordmap.json'), 'w')
f.write(json.dumps(wordmap))
f.close()
for n in args.ngrams:
    phonemap = utils.collect_phones(args.data, n, verbose=args.verbose)
    f = open(os.path.join(args.outdir, 'phonemap_' + str(n) + '.json'), 'w')
    f.write(json.dumps(phonemap))
    f.close()
