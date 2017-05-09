import json
import re


class Phonetics:
    def __init__(self, word2phoneme_file):
        self.word2phone = json.load(open(word2phoneme_file))

    def get_phonemes(self, word):
        if word in self.word2phone:
            return self.word2phone[word]
        return []


def parse_lyric_phonemes(f, phonetics):
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in open(f):
        words = line.lower().strip().split(' ')
        for word in words:
            word = regex.sub('', word)
            output.extend(phonetics.get_phonemes(word))
    return output


def parse_lyric_words(f):
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in open(f):
        words = line.lower().strip().split(' ')
        for word in words:
            word = regex.sub('', word)
            output.append(word)
    return output


