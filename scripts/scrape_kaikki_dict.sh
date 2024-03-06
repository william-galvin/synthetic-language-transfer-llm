
# Frisian
# TODO: If you use this to generate Frisian, make sure to pass a string of
# relevant conjugation affixes seperated by whitespace if you want to jusst
#
# python scripts/scrape_kaikki_dict.py \
#     --raw_dict_filename="kaikki.org-dictionary-Frisian.json" \
#     --output_filename="frisian_dict.json" \
#     # --split_gender="" \
#     # --split_verbs="" \
#     # --verb_conjugations=""

# Occitan
# python scripts/scrape_kaikki_dict.py \
#     --raw_dict_filename="kaikki.org-dictionary-Occitan.json" \
#     --output_filename="occitan_dict.json" \
#     # --split_gender=True \
#     # --split_verbs=True \
#     # --verb_conjugations="ar ir re er"

# Cebuano
python scripts/scrape_kaikki_dict.py \
    --raw_dict_filename="kaikki.org-dictionary-Cebuano.json" \
    --output_filename="cebuano_dict.json" \
    --split_gender=False \
    --split_verbs=False \
    # --verb_conjugations=""

python scripts/scrape_kaikki_dict.py --raw_dict_filename="kaikki.org-dictionary-Cebuano.json" --output_filename="cebuano_dict.json" --split_gender=False --split_verbs=False