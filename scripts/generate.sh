# method = viterbi/naive
# wp = word/phone
# script = textfile
method="$1"
wp="$2"
script="$3"
ngram="$4"
python scripts/${method}_${wp}.py --lyrics data/songs/lyrics/${script}.txt --output data/obama/gen/${script}_${method}_${wp}_${ngram}.txt --verbose --ngram ${ngram}
python scripts/cut_and_paste.py --script data/obama/gen/${script}_${method}_${wp}_${ngram}.txt --output data/obama/gen/${script}_${method}_${wp}_${ngram}.mp4
