import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Convert all the videos to lowres for testing')
parser.add_argument('--folder', type=str, default='data/obama/videos')
parser.add_argument('--output', type=str, default='data/obama/lowres_videos')
args = parser.parse_args()

for f in os.listdir(args.folder):
    if '.mp4' not in f:
        continue
    call =  "ffmpeg -i " + os.path.join(args.folder, f) + " -vf scale=\"250:trunc(ow/a/2)*2\" \"" + os.path.join(args.output, f) + "\""
    subprocess.call(call, shell=True)
