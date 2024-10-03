import os
from os import makedirs
from os.path import dirname
from languageflow.model.crf import CRF

from util.crf.conlleval import evaluate
from util.crf.pos_tag.features import template
from util.crf.pos_tag.model import CRFModel
from .load_data import load_dataset
from util.crf.pos_tag.custom_transformer import CustomTransformer

def train(X, y, model_path):
    train_set = list(zip(X, y))
    print("Loaded data for training")
    
    # Debugging: Print out the first few entries of X and y
    print("Sample data (X):", X[:5])
    print("Sample data (y):", y[:5])

    transformer = CustomTransformer(template)
    X_transformed, y_transformed = transformer.transform(train_set)

    # Debugging: Check transformed data
    print("Transformed data (X):", X_transformed[:5])
    print("Transformed data (y):", y_transformed[:5])

    # Training parameters
    params = {
        'c1': 1.0,
        'c2': 1e-3,
        'max_iterations': 1000,
        'feature.possible_transitions': True
    }

    folder = dirname(model_path)
    makedirs(folder, exist_ok=True)
    estimator = CRF(params=params, filename=model_path)
    estimator.fit(X_transformed, y_transformed)

def _remove_file(output_path):
    try:
        os.remove(output_path)
    except:
        pass


def train_test(train_path, test_path):
    model_path = "model.tmp.bin"
    output_path = "output.txt"
    _remove_file(output_path)
    
    # Open output file with UTF-8 encoding
    with open(output_path, "a", encoding="utf-8") as output:
        train(train_path, model_path)
        estimator = CRFModel.instance(model_path)

        test = load_dataset(test_path)
        for sample in test:
            sentence = [token[0] for token in sample]
            y_test = [token[1] for token in sample]
            y_pred = estimator.predict(sentence)
            for i in range(len(y_test)):
                line = "{}\tB-{}\tB-{}\n".format(y_pred[i][0], y_test[i], y_pred[i][1])
                output.write(line)
            output.write("\n")

        class Args(object):
            pass

        args = Args()
        args.latex = False
        args.raw = False
        args.delimiter = None
        args.oTag = "O"
        evaluate(open(output_path, encoding="utf-8"), args)  # Ensure evaluation reads with UTF-8

    os.remove(model_path)
    os.remove(output_path)
