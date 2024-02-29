import matplotlib.pyplot as plt
import pandas as pd

file = "outputs/finetune_results.csv"
df = pd.read_csv(file)


langs = df['lang'].unique()
pretrains = df['pretrain'].unique()

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

for lang, group in df.groupby(['lang', 'pretrain']):
    key = f"{lang[0].capitalize()} pretrained on {lang[1].capitalize()} GPT2"
    ax.plot(group['finetune data (1000s)'], group['perplexity'], marker='o', linestyle='-', label=key)

ax.set_xlabel("Fine-tune Data Quantity (1000s of sentences)")
ax.set_ylabel("Perplexity")
ax.set_title("Perplexity vs Quantity of Gold Standard Fine-tuning Data")
ax.legend()

plt.tight_layout()
plt.savefig("plots/perplexity-vs-quantity.pdf")