from flask import Flask, request, render_template
from scripts.viterbi_phones import Viterbi
from scripts.utils import Phonetics
from scripts.cut_and_paste import cut_and_paste

import argparse
import json
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
    ngram = 2
    phonemap_dir = 'data/obama/gen'
    word2phone = 'data/word2phones.json'
    videos = 'data/obama/lowres_videos'
    tmp = 'data/obama/tmp'
    final_video = 'data/obama/gen/tmp.mp4'

    # Delete the old video
    subprocess.call('rm ' + final_video, shell=True)
    subprocess.call('rm ' + clips_file, shell=True)

    # Create the video
    script = request.data
    lines = script.split('.')
    phonetics = Phonetics(word2phone)
    phones = phonetics.parse_compound_phones(lines, ngram)
    memory = json.load(open(os.path.join(phonemap_dir, 'phonemap_' + str(ngram) + '.json')))
    viterbi = Viterbi(clips_file, phones, memory, transition_penalty=-100, verbose=True)
    viterbi.run()
    cut_and_paste(final_video, clips_file, videos, tmp)
    return 'ok'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
