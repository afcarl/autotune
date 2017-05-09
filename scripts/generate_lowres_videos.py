import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Convert all the videos to lowres for testing')
parser.add_argument('--dir', type=str, default='data/obama/videos')
parser.add_argument('--out', type=str, default='data/obama/lowres_videos')
args = parser.parse_args()

for f in os.listdir(args.dir):
    if '.mp4' not in f:
        continue
    call =  "ffmpeg -i " + os.path.join(args.dir, f) + " -vf scale=\"250:trunc(ow/a/2)*2\" \"" + os.path.join(args.out, f) + "\""
    subprocess.call(call, shell=True)
