from os.path import join


class WordTokenizeCorpusReader:
    @staticmethod
    def read(data_folder, train_file=None, test_file=None):
        train = WordTokenizeCorpusReader.__read_data(join(data_folder, train_file))
        test = WordTokenizeCorpusReader.__read_data(join(data_folder, test_file))
        tagged_corpus = TaggedCorpus(train, test)
        return tagged_corpus

    @staticmethod
    def __read_data(data_file):
        text = open(data_file).read()
        sentences = text.split("\n")
        sentences = [WordTokenizeCorpusReader.__extract_tokens(s) for s in sentences]
        return sentences

    @staticmethod
    def __extract_tokens(s):
        sentence = []
        for item in s.split():
            tokens = item.split("_")
            tokens = [token for token in tokens if token]
            for i, token in enumerate(tokens):
                if i == 0:
                    sentence.append((token, "B-W"))
                else:
                    sentence.append((token, "I-W"))
        return sentence


class DataReader:
    @staticmethod
    def load_tagged_corpus(data_folder, train_file=None, test_file=None):
        train = DataReader.__read_tagged_data(join(data_folder, train_file))
        test = DataReader.__read_tagged_data(join(data_folder, test_file))
        tagged_corpus = TaggedCorpus(train, test)
        return tagged_corpus

    @staticmethod
    def __read_tagged_data(data_file):
        sentences = []
        raw_sentences = open(data_file).read().strip().split("\n\n")
        for s in raw_sentences:
            is_valid = True
            tagged_sentence = []
            for row in s.split("\n"):
                tokens = row.split("\t")
                tokens = [token.strip() for token in tokens]
                tagged_sentence.append(tokens)
            for row in tagged_sentence:
                if (len(row[0])) == 0:
                    is_valid = False
            if is_valid:
                sentences.append(tagged_sentence)
        return sentences


class TaggedCorpus:
    def __init__(self, train, test):
        self.train = train
        self.test = test

    def downsample(self, percentage):
        n = int(len(self.train) * percentage)
        self.train = self.train[:n]
        n = int(len(self.test) * percentage)
        self.test = self.test[:n]
        return self


def preprocess_vlsp2013(dataset):
    output = []
    for s in dataset:
        si = []
        for row in s:
            token, tag = row
            tag = "B-" + tag
            si.append([token, tag])
        output.append(si)
    return output

def preprocess_shoes_data(dataset):
    output = []
    for s in dataset:
        si = []
        for row in s:
            # Tách từng từ trong câu thành các token và tag
            tokens_tags = row[0].split()  # Tách các từ trong câu
            for token_tag in tokens_tags:
                token = token_tag.split('/')[0]  # Tách token
                tag = token_tag.split('/')[1].replace(' :', '')  # Tách tag và loại bỏ dấu ':'
                tag = "B-" + tag  # Thêm tiền tố "B-" vào tag
                si.append([token, tag])  # Thêm cặp token và tag vào danh sách

        output.append(si)  # Thêm danh sách các cặp vào output
    return output
