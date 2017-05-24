import argparse
import json
from utils import read_file, parse_words, Node


class Viterbi:
    def __init__(self, output, words, memory, transition_penalty=0, verbose=False):
        self.output = output
        self.verbose = verbose
        self.transition_penalty = transition_penalty

        self.words = words
        self.memory = memory
        self.timesteps = []

    def unary(self, word, w_obj):
        return 0

    def binary(self, prev, node):
        if prev.filename != node.filename:
            return self.transition_penalty
        if prev.start == node.prevstart:
            return 0
        return self.transition_penalty

    def run(self):
        # Calculate the unary values
        for progress, word in enumerate(self.words):
            if self.verbose and progress % 100 == 0:
                print "| Calculating unary values: %d / %d" % (progress, len(self.words))
            if word not in self.memory:
                print "| Cound not find %s" % word
                continue
            elems = [Node(word, self.unary(word, elem), elem['filename'], elem['starttime'], elem['duration'], elem['prevstart']) for elem in self.memory[word]]
            self.timesteps.append(elems)

        # calculate best path
        for timestep in range(len(self.timesteps)):
            if self.verbose and timestep % 100 == 0:
                print "| Calculating timestep %d / %d" % (timestep, len(self.timesteps))
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
    parser.add_argument('--wordmap', type=str, default='data/obama/gen/wordmap.json')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--transition-penalty', type=int, default=-100)
    args = parser.parse_args()

    words = parse_words(read_file(args.lyrics))
    memory = json.load(open(args.wordmap))
    viterbi = Viterbi(args.output, words, memory,
            transition_penalty=args.transition_penalty, verbose=args.verbose)
    viterbi.run()
