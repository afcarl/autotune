import argparse
import json
import utils
import os


class Node:
    def __init__(self, name, unary, filename, start, duration):
        self.name = name
        self.unary = unary
        self.filename = filename
        self.start = start
        self.duration = duration

        self.prev = None
        self.value = None

    def setNext(self, node):
        self.next = node

    def setPrev(self, node):
        self.prev = node

    def copy(self):
        return Node(self.name, self.unary,
                    self.filename, self.start,
                    self.duration)


class Viterbi:
    def __init__(self, args):
        self.output = args.output
        self.data = args.data
        self.verbose = args.verbose
        self.transition_penalty = args.transition_penalty

        self.words = utils.parse_lyric_words(args.lyrics)
        self.timesteps = []

    def unary(self, word, w_obj):
        return 0

    def binary(self, prev, node):
        if prev.filename != node.filename:
            return self.transition_penalty
        if prev.start + prev.duration - node.start <= 0.01:
            return 0
        return self.transition_penalty

    def find(self, word, folder, verbose=False):
        nodes = []
        for file in os.listdir(os.path.join(folder, 'alignment')):
            if '.txt' not in file:
                continue
            try:
                alignment = json.load(open(os.path.join(folder, 'alignment', file)))
            except:
                continue
            if word not in alignment['transcript']:
                continue
            for w in alignment['words']:
                unary = self.unary(word, w)
                if w['word'].lower() == word and w['case'] == 'success':
                    nodes.append(Node(word, unary, file.replace('.txt', ''),
                              w['start'], w['end'] - w['start']))
        return nodes


    def run(self):
        # Calculate the unary values
        memory = {}
        for progress, word in enumerate(self.words):
            if self.verbose and progress % 100 == 0:
                print "| Calculating unary values: %d / %d" % (progress, len(self.words))
            if word in memory:
                elems = [elem.copy() for elem in memory[word]]
            else:
                elems = self.find(word, self.data, verbose=self.verbose)
                memory[word] = elems
            if len(elems) is 0:
                print "| Cound not find %s" % word
                continue
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
        while last is not None:
          sequence.append({'filename': last.filename.replace('.txt', ''),
                          'starttime': last.start,
                          'duration': last.duration})
          last = last.prev

        # Save the output
        f = open(self.output, 'w')
        f.write(json.dumps(sequence[::-1]))
        f.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate the best sequence of videos')
    parser.add_argument('--lyrics', type=str, default='data/songs/lyrics/call_me_maybe.txt')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--transition-penalty', type=int, default=-100)
    args = parser.parse_args()
    viterbi = Viterbi(args)
    viterbi.run()
