from utils import Phonetics, Node, read_file

import argparse
import json
import os


class Viterbi:
    def __init__(self, output, phones, memory, transition_penalty=0, verbose=False):
        self.output = output
        self.verbose = verbose
        self.phones = phones
        self.transition_penalty = transition_penalty

        self.memory = memory
        self.timesteps = []

    def unary(self, phone, p_obj):
        return 0

    def binary(self, prev, node):
        if prev.filename != node.filename:
            return self.transition_penalty
        if prev.start == node.prevstart:
            return 0
        return self.transition_penalty

    def run(self):
        # Calculate the unary values
        for progress, phone in enumerate(self.phones):
            if self.verbose and progress % 100 == 0:
                print "| Calculating unary values: %d / %d" % (progress, len(self.phones))
            if phone not in self.memory:
                print "| Cound not find %s" % phone
                continue
            else:
                elems = [Node(phone, self.unary(phone, elem), elem['filename'], elem['starttime'], elem['duration'], elem['prevstart']) for elem in self.memory[phone]]
            self.timesteps.append(elems)

        # calculate best path
        for timestep in range(len(self.timesteps)):
            #if self.verbose and timestep % 100 == 0:
            print "| Calculating timestep %d / %d, %d choices" % (timestep, len(self.timesteps), len(self.timesteps[timestep]))
            for node in self.timesteps[timestep]:
                if timestep == 0:
                    node.value = node.unary
                    continue
                for prev in self.timesteps[timestep-1]:
                    value = prev.value + self.binary(prev, node)
                    if node.prev is None or value > node.value:
                        node.prev = prev
                        node.value = value

        # Get the best sequence
        last = None
        for node in self.timesteps[-1]:
            if last is None:
                last = node
            elif last.value < node.value:
                last = node
        sequence = []
        duration_offset = 0
        while last is not None:
            if last.prev is not None and self.binary(last.prev, last) != self.transition_penalty:
                duration_offset += last.duration
            else:
                sequence.append({'filename': last.filename.replace('.txt', ''),
                                 'starttime': last.start,
                                 'duration': last.duration+duration_offset})
                duration_offset = 0
            last = last.prev
        sequence = sequence[::-1]
        print "Original number of clips: %d" % len(self.timesteps)
        print "Viterbi  number of clips: %d" % len(sequence)

        # Save the output
        f = open(self.output, 'w')
        f.write(json.dumps(sequence))
        f.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate the best sequence of videos')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--phonemap-dir', type=str, default='data/obama/gen')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--transition-penalty', type=int, default=-100)
    parser.add_argument('--ngram', type=int, default=5)
    parser.add_argument('--word2phone', type=str, default='data/word2phones.json')
    args = parser.parse_args()

    phonetics = Phonetics(args.word2phone)
    lines = read_file(args.lyrics)
    phones = phonetics.parse_compound_phones(lines, args.ngram)
    memory = json.load(open(os.path.join(args.phonemap_dir, 'phonemap_' + str(args.ngram) + '.json')))
    viterbi = Viterbi(args.output, phones, memory,
            transition_penalty=args.transition_penalty, verbose=args.verbose)
    viterbi.run()
