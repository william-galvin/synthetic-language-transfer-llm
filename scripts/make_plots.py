import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["figure.titleweight"] = "bold"

# plt.rcParams['axes.prop_cycle'] = plt.cycler(color=["#3a86ff", "#8338ec", "#ff006e", '#ffbe0b']) 
colors = {
    "Frisian": "#3a86ff", 
    "Cebuano": "#8338ec", 
    "Yoruba": "#ff006e",
    "Occitan": "#ffbe0b"
}

file = "outputs/finetune_results.csv"
df = pd.read_csv(file).sort_values("finetune data (1000s)")

langs = df['lang'].unique()
pretrains = df['pretrain'].unique()

# Plotting
fig, ax = plt.subplots(figsize=(8, 5))

for lang, group in df[df['pretrain'] == "english"].groupby(['lang', 'pretrain']):
    if (lang[0] == "yoruba") : continue
    # key = f"{lang[0].capitalize()} pretrained on {lang[1].capitalize()} GPT2"
    key = lang[0].capitalize()
    ax.plot(group['finetune data (1000s)'], group['perplexity'], marker='o', linewidth=3, alpha=0.8, linestyle='-', label=key, color = colors[key])

ax.set_xlabel("Fine-tune Data Quantity (1000s of sentences)")
ax.set_ylabel("Perplexity")
plt.suptitle("Perplexity vs Quantity of Gold Standard Fine-tuning Data")
ax.set_title("Fully Trained English GPT-2")
ax.legend()
ax.set_yscale("log")

plt.savefig("plots/perplexity-vs-quantity.pdf")




################################
# plt 2
fig, ax = plt.subplots(figsize=(8, 5))

for lang, group in df[df['pretrain'].isin(["english5m", "synthetic_occitan", "synthetic_frisian", "synthetic_cebuano"])].groupby(['lang', 'pretrain']):
    if (lang[0] == "yoruba") : continue
    key = f"{lang[0].capitalize()} pretrained on {lang[1].replace('_', ' ' )}"
    ax.plot(
        group['finetune data (1000s)'], 
        group['perplexity'], 
        marker='o', 
        linewidth=3, 
        alpha=0.8, 
        linestyle='-' if "synth" not in lang[1] else "--", 
        label=key, color=colors[lang[0].capitalize()]
    )

ax.set_xlabel("Fine-tune Data Quantity (1000s of sentences)")
ax.set_ylabel("Perplexity")
ax.set_title("GPT-2 5M English and Synthetic Training Examples")
ax.set_yscale("log")
ax.legend()

plt.suptitle("Perplexity vs Quantity of Gold Standard Fine-tuning Data")
plt.savefig("plots/synth-perplexity-vs-quantity.pdf")