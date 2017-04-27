import argparse
import os
import subprocess

def align(args):
    for progress, f in enumerate(os.listdir(args.subtitles)):
        suffix = '.txt'
        if suffix not in f:
            continue
        name = f.replace(suffix, '')
        audio_file = os.path.join(args.audios, name + '.mp3')
        subtitle_file = os.path.join(args.subtitles, name + '.txt')
        alignment_file = os.path.join(args.alignment, name + '.txt')
        command = 'curl -F \"audio=@' + audio_file + '\" -F \"transcript=@' \
            + subtitle_file + '\" \"http://localhost:8765/transcriptions?async=false\"' \
            + ' > ' + alignment_file
        print (progress+1), command
        subprocess.call(command, shell=True)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--audios', type=str, default='data/obama/audios')
    parser.add_argument('--subtitles', type=str, default='data/obama/subtitles')
    parser.add_argument('--alignment', type=str, default='data/obama/alignment')
    args = parser.parse_args()
    align(args)


