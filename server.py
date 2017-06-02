from flask import Flask, request, render_template
from scripts import viterbi_phones, viterbi_words, naive_words, naive_phones
from scripts.utils import Phonetics, PhoneSimilarity
from scripts.cut_and_paste import cut_and_paste
from scripts import utils

import argparse
import json
import logging
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data={})

@app.route('/generate', methods=['POST'])
def generate():
    # Global variables
    clips_file = 'data/obama/gen/tmp.txt'
    phonemap_dir = 'data/obama/gen'
    wordmap = 'data/obama/gen/wordmap.json'
    word2phone = 'data/word2phones.json'
    phone_similarities = 'data/phone_similarities.json'
    videos = 'data/obama/lowres_videos'
    tmp = 'data/obama/tmp'
    final_video = 'data/obama/gen/tmp.mp4'

    # Delete the old video
    subprocess.call('rm ' + final_video, shell=True)
    subprocess.call('rm ' + clips_file, shell=True)

    # Parse arguments
    data = json.loads(request.data)
    script = data['script']
    logging.info(script)
    ngram = data['ngram']
    algorithm = data['algorithm']
    lines = script.split('.')

    # Create the video script
    if algorithm == 'dynamic' and ngram == 'words':
        words = utils.parse_words(lines)
        memory = json.load(open(wordmap))
        algorithm = viterbi_words.Viterbi(clips_file, words, memory, transition_penalty=-100, verbose=True)
        algorithm.run()
    elif algorithm == 'dynamic':
        phonetics = Phonetics(word2phone)
        phonesims = PhoneSimilarity(phone_similarities)
        phones = phonetics.parse_compound_phones(lines, int(ngram))
        memory = json.load(open(os.path.join(phonemap_dir, 'phonemap_' + str(ngram) + '.json')))
        algorithm = viterbi_phones.Viterbi(clips_file, phones, memory, phonesims, transition_penalty=-100, verbose=True)
        algorithm.run()
    elif algorithm == 'naive' and ngram == 'words':
        words = utils.parse_words(lines)
        memory = json.load(open(wordmap))
        naive_words.naive_words(clips_file, words, memory)
    else:
        phonetics = Phonetics(word2phone)
        phones = phonetics.parse_phones(lines)
        memory = json.load(open(os.path.join(phonemap_dir, 'phonemap_1.json')))
        naive_phones.naive_phones(clips_file, phones, memory, verbose=True)

    # Generate the video
    cut_and_paste(final_video, clips_file, videos, tmp)
    return 'ok'

if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--logfile", type=str, default='data/obama/gen/server.log')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(filename=args.logfile, level=logging.INFO)

    # Start server
    app.run(host='0.0.0.0', port=args.port)
