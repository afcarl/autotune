import argparse
import os
import subprocess

def download_from_youtube(names, args):
    for progress, name in enumerate(names):
        vidpath = os.path.join(args.output_dir, name + ".mp4")
        command = 'youtube-dl -o ' + vidpath + ' -f ' + args.format
        if args.subtitles:
            command += ' --write-sub --convert-subs ' + args.subtitle_format
        if args.audios:
            command += ' --extract-audio --audio-format ' + args.audio_format
        command += ' https://www.youtube.com/watch?v=' + name
        subprocess.call(command, shell=True)
        print "Finished downloading %d / %d videos" % (progress+1, len(names))

def get_urls(filename):
    f = open(filename)
    urls = []
    for line in f:
        urls.append(line.strip().replace('https://www.youtube.com/watch?v=', ''))
    return urls

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Download a list of youtube videos')
    parser.add_argument('--url', type=str, default=None, \
        help="Use this command only when you want to download a single video")
    parser.add_argument('--urls', type=str, default='data/urls.txt')
    parser.add_argument('--output-dir', type=str, default='data/obama/videos')

    # VIDEOS
    parser.add_argument('--format', type=str, default='bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best')

    # AUDIOS
    parser.add_argument('--audio-format', type=str, default='mp3')
    parser.add_argument('--audios', action='store_true', default=False)

    # SUBTITLES
    parser.add_argument('--subtitle-format', type=str, default='srt')
    parser.add_argument('--subtitles', action='store_true', default=False)
    args = parser.parse_args()

    if args.url is not None and len(args.url) > 0:
        names = [args.url.replace('https://www.youtube.com/watch?v=', '')]
    else:
        names = get_urls(args.urls)
    download_from_youtube(names, args)
