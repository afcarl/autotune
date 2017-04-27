folder=$1
mkdir -p 'data/${folder}/audios'
mkdir -p 'data/${folder}/videos'
mkdir -p 'data/${folder}/subtitles'
mkdir -p 'data/${folder}/alignment'
python scripts/download_youtube.py --audios --urls 'data/${folder}/urls.txt' --output-dir 'data/${folder}/audios'
python scripts/download_youtube.py --subtitles --urls 'data/${folder}/urls.txt' --output-dir 'data/${folder}/videos'
python scripts/parse_scripts.py --dir 'data/${folder}/videos' --out 'data/${folder}/subtitles'
