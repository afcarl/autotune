import json
import re
import os


class Node:
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
                    self.duration)

def read_file(f):
    """
    f - raw textfile with words that need to be parsed
    """
    return open(f).readlines()

def parse_words(script):
    """
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
