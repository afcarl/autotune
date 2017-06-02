from utils import Phonetics, PhoneSimilarity, Node, read_file

import argparse
import json
import os


class Viterbi:
    def __init__(self, output, phones, memory, phone_similarities, transition_penalty=0, verbose=False):
        self.output = output
        self.verbose = verbose
        self.phones = phones
        self.transition_penalty = transition_penalty
        self.phone_similarities = phone_similarities

        self.memory = memory
        self.timesteps = []

    def unary(self, phone, p_neighbor):
        return self.phone_similarities.get_compound_similarity(phone, p_neighbor)

    def binary(self, prev, node):
        if node.prevstart is None:
            return self.transition_penalty
        if prev.filename != node.filename:
            return self.transition_penalty
        if abs(prev.start - node.prevstart) <= 10e-6:
            return 0
        return self.transition_penalty

    def run(self):
        output_phones = []
        # Calculate the unary values
        for progress, phone in enumerate(self.phones):
            if self.verbose and progress % 100 == 0:
                print "| Calculating unary values: %d / %d" % (progress, len(self.phones))
            elems = {}
            for phone_neighbor in self.phone_similarities.get_compound_neighbors(phone):
                if phone_neighbor not in self.memory:
                    continue
                for elem in self.memory[phone_neighbor]:
                    node = Node(phone, self.unary(phone, phone_neighbor), elem['filename'], \
                                elem['starttime'], elem['duration'], elem['prevstart'], \
                                elem['prevphone'])
                    if node.filename not in elems:
                        elems[node.filename] = []
                    elems[node.filename].append(node)
            if len(elems) > 0:
                self.timesteps.append(elems)
                output_phones.append(phone)

        # calculate best path
        currbest = None
        currbestvalue = -1000000
        for timestep in range(len(self.timesteps)):
            prevbest = currbest
            currbest = None
            currbestvalue = -1000000
            print "| Calculating timestep %d / %d, %d choices for phone: %s" % (timestep, \
                    len(self.timesteps), len(self.timesteps[timestep]), output_phones[timestep])
            for filename in self.timesteps[timestep]:
                for node in self.timesteps[timestep][filename]:
                    if timestep == 0:
                        node.value = node.unary
                    elif node.prevphone != output_phones[timestep] or node.filename not in self.timesteps[timestep-1]:
                        node.prev = prevbest
                        node.value = node.unary + node.prev.value + self.binary(node.prev, node)
                    else:
                        for prev in self.timesteps[timestep-1][node.filename]:
                            value = node.unary + prev.value + self.binary(prev, node)
                            if node.prev is None or node.value is None or value > node.value:
                                node.prev = prev
                                node.value = value
                    if currbest is None or node.value > currbestvalue:
                        currbest = node
                        currbestvalue = node.value

        # Get the best sequence
        last = None
        for filename in self.timesteps[-1]:
            for node in self.timesteps[-1][filename]:
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
        if self.verbose:
            print "OUTPUT: ", json.dumps(sequence)
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
    parser.add_argument('--phone-similarities', type=str, default='data/phone_similarities.json')
    args = parser.parse_args()

    phonesims = PhoneSimilarity(args.phone_similarities)
    phonetics = Phonetics(args.word2phone)
    lines = read_file(args.lyrics)
    phones = phonetics.parse_compound_phones(lines, args.ngram)
    memory = json.load(open(os.path.join(args.phonemap_dir, 'phonemap_' + str(args.ngram) + '.json')))
    viterbi = Viterbi(args.output, phones, memory, phonesims,
            transition_penalty=args.transition_penalty, verbose=args.verbose)
    viterbi.run()
