from moviepy.editor import VideoFileClip, concatenate_videoclips

import argparse
import json
import os
import subprocess


def main(args):
    script = json.load(open(args.script))
    clips = []
    for index, elem in enumerate(script):
        name = elem['filename']
        start = str(elem['starttime'])
        duration = str(elem['duration'])
        video_file = os.path.join(args.data, 'videos', name + '.mp4')
        clip = VideoFileClip(video_file).subclip(start, start+duration)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(args.output)
    mp4_file = args.output.replace( '.avi','.mp4')
    convert = 'ffmpeg -y -i "' + args.output + '" "' + '"-strict -2 -vcodec libx264 -qscale:v 1 "'+ mp4_file + '"'
    subprocess.call(convert, shell=True)
    print "| Done."


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--data', type=str, default='data/obama')
    parser.add_argument('--script', type=str, default='data/obama/gen/call_me_maybe.txt')
    parser.add_argument('--output', type=str, default='data/obama/gen/call_me_maybe.avi')
    args = parser.parse_args()
    main(args)

