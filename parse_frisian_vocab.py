import pandas as pd
import json
import tqdm

VOCAB_PATH = "data/raw_frisian_vocab.txt"
WORD_DICT_PATH = "data/frisian_vocab.json"
POS_DICT_PATH = "data/frisian_dict.json"


POS = [
    "ADP",
    "NOUN",
    "PROPN",
    "VERB",
    "ADJ",
    "INTJ",
    "ADV",
    "NUM",
    "PRON",
    "CCONJ",
    "AUX",
    "DET"
]


def main():
    df = pd.read_csv(VOCAB_PATH, sep="\t", header=None)

    Pos2Word = {
        pos: []
        for pos in POS
    }
    Pos2Word["NOUN"] = {"common": [], "neuter": []}
    Word2Props = {}

    for i, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        word = row.iloc[0]
        example = row.iloc[1]
        props = row.iloc[2]
        
        if word not in Word2Props:
            Word2Props[word] = {}
        
        Word2Props[word][props] = example

        for pos in POS:
            if pos in props:
                if pos == "NOUN":
                    if "Gender.Com" in props:
                        Pos2Word[pos]["common"].append(word)
                    else:
                        Pos2Word[pos]["neuter"].append(word)
                    continue

                Pos2Word[pos].append(word)

    with open(WORD_DICT_PATH, "w") as w:
        json.dump(Word2Props, w, ensure_ascii=False, indent=2)
    with open(POS_DICT_PATH, "w") as w:
        json.dump(Pos2Word, w, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()