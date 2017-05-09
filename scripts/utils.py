import re

def parse_lyrics(f):
    regex = re.compile('[^a-zA-Z\']')
    output = []
    for line in open(f):
        words = line.lower().strip().split(' ')
        words = [regex.sub('', word) for word in words]
        output.extend(words)
    return output


