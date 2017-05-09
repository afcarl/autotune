import argparse
import json
import subprocess
import os


def main(args):
    subprocess.call('rm ' + os.path.join(args.tmp, 'filelist.txt'), shell=True)
    subprocess.call('rm ' + os.path.join(args.tmp, '*.mp4'), shell=True)
    script = json.load(open(args.script))
    filename = os.path.join(args.tmp, 'filelist.txt')
    filelist = open(filename, 'w')
    for index, elem in enumerate(script):
        name = elem['filename']
        start = str(elem['starttime'])
        duration = str(elem['duration'])
        outfile = os.path.join(args.tmp, str(index) + ".mp4")
        cut = "ffmpeg -ss " + start + " -i " + os.path.join(args.videos, name) + ".mp4 -t " + duration + " " + outfile
        print "="*89
        print cut
        subprocess.call(cut, shell=True)
        filelist.write('file \'' + str(index) + '.mp4\'\n')
    filelist.close()
    paste = "ffmpeg -f concat -i " + filename + " -c copy " + args.output
    print "="*89
    print paste
    subprocess.call(paste, shell=True)
    print "| Done."


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--videos', type=str, default='data/obama/lowres_videos')
    parser.add_argument('--script', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--tmp', type=str, default='data/obama/tmp')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.mp4')
    args = parser.parse_args()
    main(args)

