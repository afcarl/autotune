import argparse
import json
import subprocess
import os


def main(args):
    script = json.load(open(args.script))
    filelist = open(os.path.join(args.tmp, 'filelist.txt'), 'w')
    for index, elem in enumerate(script):
        name = elem['filename']
        start = str(elem['starttime'])
        duration = str(elem['duration'])
        outfile = os.path.join(args.tmp, str(index) + ".mp4")
        cut = "ffmpeg -ss " + start + " -i " + os.path.join(args.data, 'videos', name) + ".mp4 -t " + duration + " " + outfile
        subprocess.call(cut, shell=True)
        filelist.write(outfile + '\n')
    filelist.close()
    paste = "ffmpeg -f concat -i " + filelist + " -c copy " + args.output
    subprocess.call(paste, shell=True)
    print "| Done."


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--script', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--tmp', type=str, default='data/obama/tmp')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.mp4')
    args = parser.parse_args()
    main(args)

