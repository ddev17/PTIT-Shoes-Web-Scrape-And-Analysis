from os.path import dirname, join
from underthesea.models.fast_crf_sequence_tagger import FastCRFSequenceTagger
from underthesea.pipeline.word_tokenize.regex_tokenize import tokenize

output_dir = join(dirname(__file__), "tmp/ws_20220222")
sentence = "Tôi cần 1 mẫu giày Adidas màu đỏ có size 42 chất liệu vải"
tokens = tokenize(sentence)
tokens_ = [[token] for token in tokens]

model = FastCRFSequenceTagger()
model.load(output_dir)
y = model.predict(tokens_)
for token, x in zip(tokens, y):
    print(token, "\t", x)
