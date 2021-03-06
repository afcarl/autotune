folder="$1"
mkdir -p "data/${folder}/audios"
mkdir -p "data/${folder}/gen"
mkdir -p "data/${folder}/tmp"
mkdir -p "data/${folder}/videos"
mkdir -p "data/${folder}/subtitles"
mkdir -p "data/${folder}/alignment"
mkdir -p "data/${folder}/lowres_videos"
python scripts/download_youtube.py --audios --urls "data/${folder}/urls.txt" --output-dir "data/${folder}/audios"
python scripts/download_youtube.py --subtitles --urls "data/${folder}/urls.txt" --output-dir "data/${folder}/videos"
python scripts/parse_scripts.py --dir "data/${folder}/videos" --out "data/${folder}/subtitles"
python scripts/generate_lowres_videos.py --dir "data/${folder}/videos" --out "data/${folder}/lowres_videos"
