import argparse
import json
import subprocess
import os


def cut_and_paste(output, script, videos, tmp):
    subprocess.call('rm ' + os.path.join(tmp, 'filelist.txt'), shell=True)
    subprocess.call('rm ' + os.path.join(tmp, '*.mp4'), shell=True)
    filename = os.path.join(tmp, 'filelist.txt')
    filelist = open(filename, 'w')
    script = json.load(open(script))
    for index, elem in enumerate(script):
        name = elem['filename']
        start = str(elem['starttime'])
        duration = str(elem['duration'])
        outfile = os.path.join(tmp, str(index) + ".mp4")
        cut = "ffmpeg -ss " + start + " -i " + os.path.join(videos, name) + ".mp4 -t " + duration + " " + outfile
        print "="*89
        print cut
        subprocess.call(cut, shell=True)
        filelist.write('file \'' + str(index) + '.mp4\'\n')
    filelist.close()
    paste = "ffmpeg -f concat -i " + filename + " -c copy " + output
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

    cut_and_paste(args.output, args.script, args.videos, args.tmp)
