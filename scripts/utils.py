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

    def parse_lyric_phones(self, f):
        """
        f - raw textfile with words that need to be parsed
        """
        regex = re.compile('[^a-zA-Z\']')
        output = []
        for line in open(f):
            words = line.replace('-', ' ').lower().strip().split(' ')
            for word in words:
                word = regex.sub('', word)
                output.extend(self.get_phones(word))
        return output


def parse_lyric_words(f):
    """
    f - raw textfile with words that need to be parsed
    """
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in open(f):
        words = line.replace('-', ' ').lower().strip().split(' ')
        for word in words:
            word = regex.sub('', word)
            output.append(word)
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


def collect_phones(folder, verbose=False):
    phonemap = {}
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
            if w['case'] != 'success':
                continue
            start = w['start']
            for phone_obj in w['phones']:
                phone = phone_obj['phone'][0:phone_obj['phone'].index('_')]
                elem = {'filename': file.replace('.txt', ''),
                        'starttime': start,
                        'duration': phone_obj['duration'],
                        'prevstart': prevstart}
                prevstart = start
                start += phone_obj['duration']
                if phone not in phonemap:
                    phonemap[phone] = []
                phonemap[phone].append(elem)
    return phonemap
