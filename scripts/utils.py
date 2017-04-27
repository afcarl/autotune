import os
import os.path
import re
import sys

try:
    import youtube_dl
except ImportError:
    print('You need to install youtube-dl to run this. Try running:\npip install youtube-dl')
    sys.exit()

def download_from_youtube(vid_url="https://www.youtube.com/watch?v=sy-kueG6KlA", save_path=None, name='youtubevid'):
    savepath = '.'+os.sep;
    savepath=save_path;

    #subtitlepath = savepath+os.sep+name+'.srt';

    vidpath = savepath+os.sep+name+'.%(ext)s';
    vidpathout = savepath+name+'.mp4';
    print("youtube downloader handles names weird, so hopefully this is an mp4...")
    #'sub-format': 'srt'
    #'format': '134',
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl':vidpath,
        'writesubtitles': True,
        'subtitlesformat':'[srt]'
    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vid_url])
    return vidpathout;


def vtt_to_srt(fileContents):
    replacement = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', fileContents)
    replacement = re.sub(r'WEBVTT\n\n', '', replacement)
    replacement = re.sub(r'^\d+\n', '', replacement)
    replacement = re.sub(r'\n\d+\n', '\n', replacement)
    return replacement

