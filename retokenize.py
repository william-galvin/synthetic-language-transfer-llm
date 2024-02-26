import os
import argparse
import tokenizers
from transformers import GPT2TokenizerFast


def clean_leipzig_corpus(path):
    folder, basename = os.path.split(path)
    with open(path, "r", encoding="utf-8") as f_in:
        with open(f"{folder}/clean_{basename}", "w", encoding="utf-8") as f_out:
            for line in f_in.readlines():
                splits = line.split()
                f_out.write(" ".join(splits)[1:])
                f_out.write("<|endoftext|>\n")
    return f"{folder}/clean_{basename}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--save-dir", 
        help="Directory to save tokenizer. E.g.: 'tokenizers/frisian'"
    )
    parser.add_argument(
        "--corpus",
        help="Path to corpus to tokenize. E.g: 'data/frr_wikipedia_2021_10K/cleaned_frr_wikipedia_2021_10K-sentences.txt' "
    )
    parser.add_argument(
        "--clean-leipzig",
        action="store_true",
        dest="clean",
        help="If using a corpus from https://wortschatz.uni-leipzig.de/, this will strip line numbers and add end tokens"
    )
    args = parser.parse_args()

    english_tokenizer = tokenizer_en = GPT2TokenizerFast.from_pretrained("openai-community/gpt2")
    vocab_size = english_tokenizer.vocab_size

    corpus = args.corpus if not args.clean else clean_leipzig_corpus(args.corpus)

    tokenizer = tokenizers.ByteLevelBPETokenizer()
    tokenizer.train(
        vocab_size=vocab_size,
        files=corpus,
        special_tokens=["<|endoftext|>"],
        show_progress=True
    )
    # GPT-2 specific
    tokenizer.enable_truncation(max_length=1024)

    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    tokenizer.save_model(args.save_dir)
