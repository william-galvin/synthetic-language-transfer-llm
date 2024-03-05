from datasets import load_dataset
from tqdm import tqdm  


if __name__ == "__main__":
    dataset = load_dataset("bookcorpus")

    with open("data/books.txt", "w") as w:
        for item in tqdm(dataset["train"]): 
            print(f"{item['text']}<|endoftext|>", file=w)