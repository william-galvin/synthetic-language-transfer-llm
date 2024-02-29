import os 
import argparse
import random
from typing import *

def comma_sep_int_list(astr) -> List[int]:
    if astr is None or astr == 'None':
        return []
    else:
        return list(map(lambda x: int(x.strip()), astr.split(',')))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Path to data file to split")
    parser.add_argument(
        "--splits",
        help="Thousands of sentences to split. E.g: [1, 10, 50, 99]. Note that 1k will be held for validation", 
        type=comma_sep_int_list
    )
    args = parser.parse_args()

    random.seed(0)
    with open(args.data, "r") as f:
        data = f.readlines()
    random.shuffle(data)

    folder, basename = os.path.split(args.data)

    validation, training = data[:1000], data[1000:]

    with open(os.path.join(folder, f"validation_1k_{basename}"), "w") as f:
        validation.sort()
        f.writelines(validation)

    for i in args.splits:
        with open(os.path.join(folder, f"training_{i}k_{basename}"), "w") as f:
            sentences = training[: i * 1000]
            sentences.sort()
            f.writelines(sentences)


if __name__ == "__main__":
    main()