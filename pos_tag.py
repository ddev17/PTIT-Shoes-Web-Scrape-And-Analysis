import argparse
import os
from os.path import abspath

from util.crf.pos_tag import pos_tag

parser = argparse.ArgumentParser("pos_tag.py")
text_group = parser.add_argument_group("The following arguments are mandatory for text option")
text_group.add_argument("--text", metavar="TEXT", help="text to predict")
file_group = parser.add_argument_group("The following arguments are mandatory for file option")
file_group.add_argument("--fin", help="file input")
file_group.add_argument("--fout", help="file output")
parser.add_argument("--model", help="path to load model")

args = parser.parse_args()

if __name__ == '__main__':
    if not (args.text or args.fin):
        parser.print_help()

    model = None
    if args.model:
        model = abspath(args.model)
    if args.text:
        text = args.text
        label = pos_tag(text, format="text", model_path=model)
        print(label)

    if args.fin or args.fout:
        if not (args.fout and args.fin):
            parser.error("Options --fin and --fout must be set together")
        file_in = args.fin
        file_out = args.fout
        try:
            os.rm(args.fout)
        except:
            pass
        f = open(file_out, "a")
        for text in open(file_in):
            text = text.strip()
            output = pos_tag(text, format="text", model_path=model) + "\n"
            f.write(output)

# (pos_tag) E:\ptit\khdl\PTIT-Shoes-Web-Scrape-And-Analysis>python pos_tag.py --text "adidas giay" --model 