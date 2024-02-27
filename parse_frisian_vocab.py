import pandas as pd
import json
import tqdm

RAW_VOCAB_PATH = "data/raw_frisian_vocab.txt"
VOCAB_PATH = "data/frisian_vocab.txt"
DICT_PATH = "data/frisian_dict.txt"


def main():
    df = pd.read_csv(VOCAB_PATH, sep="\t", header=None)

    Map = {}
    for i, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        word = row.iloc[0]
        example = row.iloc[1]
        props = row.iloc[2]
        
        if word not in Map:
            Map[word] = {}
        
        Map[word][props] = example

    with open(DICT_PATH, "w") as w:
        json.dump(Map, w, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()