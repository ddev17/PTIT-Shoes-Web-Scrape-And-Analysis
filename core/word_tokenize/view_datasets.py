import pandas as pd

# Đọc dữ liệu từ file txt
file_path = "/home/ddev/dev/underthesea/examples/word_tokenize/tmp/train.txt"
df = pd.read_csv(file_path, sep='\t', header=None, names=["ID", "Word", "Lemma", "POS", "Tag", "Feat", "Head", "DepRel", "Misc1", "Misc2"])
pd.set_option('display.max_rows', None)
# Hiển thị dữ liệu dưới dạng bảng
print(df)
