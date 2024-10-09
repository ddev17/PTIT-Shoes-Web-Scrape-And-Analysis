import argparse
import os
from util.crf.train import train, train_test
from util.crf.load_data import load_dataset

def main():
    parser = argparse.ArgumentParser("train.py")
    parser.add_argument("mode", default="train", nargs="?",
                        help="available modes: train, train-test")
    parser.add_argument("--train", help="train folder")
    parser.add_argument("--test", help="test folder")
    parser.add_argument("--model", help="path to save model")
    args = parser.parse_args()
    mode = args.mode
    
    if mode == "train":
        if not (args.train and args.model):
            parser.error("Mode train requires --train and --model")
        train_path = os.path.abspath(args.train)
        model_path = os.path.abspath(args.model)

        # Load dataset
        dataset = load_dataset(train_path)

        if not dataset:
            print("No valid data found for training.")
            return

        # Unpack dataset into features and labels
        try:
            X, y = zip(*dataset)
        except ValueError as ve:
            print("Error unpacking dataset:", ve)
            print("Dataset contents:", dataset)
            return

        # Ensure X and y have the same length
        if len(X) != len(y):
            print(f"Mismatch in lengths: X has {len(X)} items and y has {len(y)} items.")
            return

        # Check for empty entries
        if any(not x or not y for x, y in zip(X, y)):
            print("Found empty entries in the dataset.")
            return

        # Call the train function
        try:
            train(X, y, model_path=model_path)
            print("Model is saved in {}".format(model_path))
        except Exception as e:
            print("Error during training:", e)

    elif mode == "train-test":
        if not (args.train and args.test):
            parser.error("Mode train-test requires --train and --test")
        train_path = os.path.abspath(args.train)
        test_path = os.path.abspath(args.test)
        train_test(train_path=train_path, test_path=test_path)

if __name__ == "__main__":
    main()


# python train.py --train tmp/shoe_data/train.txt --test tmp/shoe_data/test.txt --model tmp/model.bin