import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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

ax.set_xlabel("Fine-tune Data Quantity (1000s of sentences)", fontsize=14)
ax.set_ylabel("Perplexity", fontsize=14)
plt.suptitle("Perplexity vs Quantity of Gold Standard Fine-tuning Data\nFully Trained English GPT-2", fontsize=14)
# ax.set_title("Fully Trained English GPT-2", fontsize=14)
ax.legend(fontsize=12)
ax.set_yscale("log")

plt.savefig("plots/perplexity-vs-quantity.pdf")




################################
file = "outputs/finetune_results.csv"
df = pd.read_csv(file).sort_values("finetune data (1000s)")


langs = df['lang'].unique()
pretrains = df['pretrain'].unique()

fig, ax = plt.subplots(figsize=(8, 5))

for lang, group in df[df['pretrain'].isin(["english5m", "synthetic_occitan", "synthetic_frisian", "synthetic_cebuano"])].groupby(['lang', 'pretrain']):
    if (lang[0] == "yoruba") : continue
    key = f"{lang[0].capitalize()} pretrained on {lang[1].replace('_', ' ' ).replace('occitan', 'Occitan').replace('english5m', 'English (5M)').replace('frisian', 'Frisian').replace('cebuano', 'Cebuano')}"
    ax.plot(
        group['finetune data (1000s)'], 
        group['perplexity'], 
        marker='o', 
        linewidth=3, 
        alpha=0.8, 
        linestyle='-' if "synth" not in lang[1] else "--", 
        label=key, color=colors[lang[0].capitalize()]
    )

ax.set_xlabel("Fine-tune Data Quantity (1000s of sentences)", fontsize=14)
ax.set_ylabel("Perplexity", fontsize=14)
# ax.set_title("GPT-2 Trained with 5M English and Synthetic Training Examples", fontsize=14)
ax.set_yscale("log")
# ax.legend(fontsize=12)
line = Line2D([0], [0], label='Frisian', linestyle="", color=colors["Frisian"], marker="s", markersize=10)
line2 = Line2D([0], [0], label='Occitan', linestyle="", color=colors["Occitan"], marker="s", markersize=10)
line3 = Line2D([0], [0], label='Cebuano', linestyle="", color=colors["Cebuano"], marker="s", markersize=10)
line4 = Line2D([0], [0], label='English (5M)', linestyle="-", color="black", linewidth=3)
line5 = Line2D([0], [0], label='Synthetic', linestyle="--", color="black", linewidth=3)

handles=[line, line2, line3, line4, line5]
plt.legend(handles=handles, fontsize=12)

plt.suptitle("Perplexity vs Quantity of Gold Standard Fine-tuning Data\nGPT-2 Trained with 5M English and Synthetic Training Examples", fontsize=14)
plt.savefig("plots/synth-perplexity-vs-quantity.pdf")


#############################################################
file = "outputs/finetune_results.csv"
df = pd.read_csv(file).sort_values("finetune data (1000s)")


langs = df['lang'].unique()
pretrains = df['pretrain'].unique()

fig, ax = plt.subplots(1, 3, figsize=(8, 6.25), sharex=True)

eng_frisian = df[(df["pretrain"] == "english") & (df["lang"] == "frisian")]
ax[0].plot(
    eng_frisian["finetune data (1000s)"],
    eng_frisian["perplexity"],
    marker='o', 
    linewidth=1.5, 
    alpha=0.8, 
    linestyle='-', 
    label=key, color="black"#colors["Frisian"]
)

cyborg_frisian = df[(df["pretrain"] == "synthetic_frisian_hybrid") & (df["lang"] == "frisian")]
ax[0].plot(
    cyborg_frisian["finetune data (1000s)"] / 2,
    cyborg_frisian["perplexity"],
    marker='o', 
    linewidth=3, 
    alpha=0.8, 
    linestyle='--', 
    label=key, color=colors["Frisian"]
)


eng_occitan = df[(df["pretrain"] == "english") & (df["lang"] == "occitan")]
ax[1].plot(
    eng_occitan["finetune data (1000s)"],
    eng_occitan["perplexity"],
    marker='o', 
    linewidth=1.5, 
    alpha=0.8, 
    linestyle='-', 
    label=key, color="black"#colors["Occitan"]
)

cyborg_occitan = df[(df["pretrain"] == "synthetic_occitan_hybrid") & (df["lang"] == "occitan")]
ax[1].plot(
    cyborg_occitan["finetune data (1000s)"] / 2,
    cyborg_occitan["perplexity"],
    marker='o', 
    linewidth=3, 
    alpha=0.8, 
    linestyle='--', 
    label=key, color=colors["Occitan"]
)

eng_cebuano = df[(df["pretrain"] == "english") & (df["lang"] == "cebuano")]
ax[2].plot(
    eng_cebuano["finetune data (1000s)"],
    eng_cebuano["perplexity"],
    marker='o', 
    linewidth=1.5, 
    alpha=0.8, 
    linestyle='-', 
    label=key, color="black"#colors["Cebuano"]
)

cyborg_cebuano = df[(df["pretrain"] == "synthetic_cebuano_hybrid") & (df["lang"] == "cebuano")]
ax[2].plot(
    cyborg_cebuano["finetune data (1000s)"] / 2 ,
    cyborg_cebuano["perplexity"],
    marker='o', 
    linewidth=3, 
    alpha=0.8, 
    linestyle='--', 
    label=key, color=colors["Cebuano"]
)

ax[0].set_yscale("log")
ax[1].set_yscale("log")
ax[2].set_yscale("log")

ax[0].set_title("Frisian", fontsize=14)
ax[1].set_title("Occitan", fontsize=14)
ax[2].set_title("Cebuano", fontsize=14)


# ax[0].set_xlabel("1000s of Gold-standard data points")
# ax[1].set_xlabel("1000s of Gold-standard data points")
fig.supxlabel("\nFine-tune Data Quantity\n(1000s of gold-standard sentences)", fontsize=14)
fig.supylabel("Perplexity", fontsize=14)

# ax[0].set_xscale("log")
# ax[1].set_xscale("log")
# ax[2].set_xscale("log")

# for lang, group in df[df['pretrain'].isin(["english", "synthetic_cebuano_hybrid", "synthetic_frisian_hybrid", "synthetic_occitan_hybrid"])].groupby(['lang', 'pretrain']):
#     if (lang[0] == "yoruba") : continue
#     key = f"{lang[0].capitalize()} pretrained on {lang[1].replace('_', ' ' ).replace('occitan', 'Occitan').replace('english5m', 'English (5M)').replace('frisian', 'Frisian').replace('cebuano', 'Cebuano')}"
#     ax[i].plot(
#         group['finetune data (1000s)'] / (1 if "synth" not in lang[1] else 2), 
#         group['perplexity'], 
#         marker='o', 
#         linewidth=3, 
#         alpha=0.8, 
#         linestyle='-' if "synth" not in lang[1] else "--", 
#         label=key, color=colors[lang[0].capitalize()]
#     )

# ax[i].set_xlabel("Fine-tune Data Quantity (1000s of sentences)", fontsize=14)
# ax[i].set_ylabel("Perplexity", fontsize=14)
# ax[i].set_title("GPT-2: 5M English and Synthetic Training Examples", fontsize=14)
# ax[i].set_yscale("log")
# ax.legend(fontsize=12)

plt.suptitle("Perplexity vs Quantity of Gold Standard Fine-tuning Data\nFully Trained GPT-2 with Synthetic and Gold-Standard Fine-Tuning Data", fontsize=14)



from matplotlib.lines import Line2D
line = Line2D([0], [0], label='Pure', linestyle="-", color="black")
line2 = Line2D([0], [0], label='Hybrid', linestyle="--", color="red")
handles=[line, line2]
fig.legend(handles=handles, loc=(.81, 0), fontsize=12)
# plt.tight_layout()

plt.savefig("plots/synth-perplexity-vs-quantity-cyborg.pdf")