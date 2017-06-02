import json
import re
import os


class Node:
    """
    Generic class used in the viterbi algorithm to dynamically find the maximum scoring
    sequence of video sequences where each sequence is represented as a Node object.
    """
    def __init__(self, name, unary, filename, start, duration, prevstart):
        self.name = name
        self.unary = unary
        self.filename = filename
        self.start = start
        self.duration = duration
        self.prevstart = prevstart
        self.prev = None

    def setPrev(self, node):
        self.prev = node

    def copy(self):
        return Node(self.name, self.unary,
                    self.filename, self.start,
                    self.duration, self.prevstart)

    def __str__(self):
        prevstart = -1
        if self.prevstart is not None:
            prevstart = self.prevstart
        return "Node<name: %s, unary: %d, file: %s, start: %2.2f, duration: %2.2f, prev: %2.2f>" \
                % (self.name, self.unary, self.filename, self.start, self.duration, prevstart)


def read_file(f):
    """
    Simply reads a file.
    f - raw textfile with words that need to be parsed
    """
    return open(f).readlines()

def parse_words(script):
    """
    Parses a str into its constinuent words.
    script - list of strings in a script
    """
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in script:
        words = line.replace('-', ' ').lower().strip().split(' ')
        for word in words:
            word = regex.sub('', word)
            output.append(word)
    return output


class Phonetics:
    """
    This class is responsible for converting words into phones. It also parses scripts into
    phones of varying n-grams.
    """
    def __init__(self, word2phone_file):
        """
        word2phone_file - string of filename of json map from word to list of phones
        """
        self.word2phone = json.load(open(word2phone_file))

    def get_phones(self, word):
        """
        word - a string containing one word
        """
        if word in self.word2phone:
            return self.word2phone[word]
        return []

    def parse_phones(self, script):
        """
        script - list of strings in a script
        """
        words = parse_words(script)
        output = []
        for word in words:
            output.extend(self.get_phones(word))
        return output

    def parse_compound_phones(self, script, ngram):
        """
        script - list of strings in a script
        """
        phones = self.parse_phones(script)
        output = []
        i = 0
        while i < len(phones):
            output.append('_'.join(phones[i:i+ngram]))
            i += ngram
        return output


class PhoneSimilarity:
    """
    This class is reponsible for handling similarity between phones and suggesting similar
    neighbors for phones and compound phones
    """
    def __init__(self, phone_similarity_file):
        """
        phone_similarity_file - string of filename of json map from word to list of phones
        """
        data = json.load(open(phone_similarity_file))
        self.phones = data['phones']
        self.similarities = data['similarities']
        self.neighbors = data['neighbors']

    def get_neighbors(self, phone):
        return self.neighbors[phone]

    def get_similarity(self, p1, p2):
        i1 = self.phones.index(p1)
        i2 = self.phones.index(p2)
        return self.similarities[i1][i2]

    def get_compound_neighbors(self, phone):
        phones = phone.split('_')
        neighbors = []
        for p in phones:
            neighbors.append(self.neighbors[p])
        output = neighbors[0]
        if len(neighbors) > 1:
            for i in range(1, len(neighbors)):
                tmp = []
                for prefix in output:
                    for suffix in neighbors[i]:
                        tmp.append(prefix+'_'+suffix)
                output = tmp
        return output

    def get_compound_similarity(self, p1, p2):
        p1s = p1.split('_')
        p2s = p2.split('_')
        assert(len(p1s) == len(p2s))
        score = 0.0
        for p1, p2 in zip(p1s, p2s):
            score += self.get_similarity(p1, p2)
        return score


def collect_words(folder, verbose=False):
    """
    Given a folder containing txt files with gentle outputs, this function
    creates a mapping from all the words seen to where and when they occur.
    """
    wordmap = {}
    for file in os.listdir(os.path.join(folder, 'alignment')):
        if '.txt' not in file:
            continue
        try:
            alignment = json.load(open(os.path.join(folder, 'alignment', file)))
        except:
            print "Could not parse %s" % file
            continue
        prevstart = None
        for w in alignment['words']:
            if w['case'] == 'success':
                elem = {'filename': file.replace('.txt', ''),
                        'starttime': w['start'],
                        'duration': w['end'] - w['start'],
                        'prevstart': prevstart}
                prevstart = w['start']
                word = w['word'].lower().strip()
                if word not in wordmap:
                    wordmap[word] = []
                wordmap[word].append(elem)
    return wordmap


def collect_phones(folder, N, verbose=False):
    phonemap = {}
    for file in os.listdir(os.path.join(folder, 'alignment')):
        # Basic parsing
        if '.txt' not in file:
            continue
        try:
            alignment = json.load(open(os.path.join(folder, 'alignment', file)))
        except:
            print "Could not parse %s" % file
            continue

        # State for file
        phonelist = []
        startlist = []
        durationlist = []
        prevstart = None

        # Iterate over data
        for w in alignment['words']:
            if w['case'] != 'success':
                continue
            start = w['start']
            for phone_obj in w['phones']:
                phone = phone_obj['phone'][0:phone_obj['phone'].index('_')]
                phonelist.append(phone)
                startlist.append(start)
                durationlist.append(phone_obj['duration'])
                if len(phonelist) >= N:
                    compound_phone = '_'.join(phonelist[-N:])
                    if len(startlist) >= 2*N:
                        prevstart = startlist[-2*N]
                    elem = {'filename': file.replace('.txt', ''),
                            'starttime': startlist[-N],
                            'duration': sum(durationlist[-N:]),
                            'prevstart': prevstart}
                    if compound_phone not in phonemap:
                        phonemap[compound_phone] = []
                    phonemap[compound_phone].append(elem)
                    phonelist = []
                start += phone_obj['duration']
    return phonemap
