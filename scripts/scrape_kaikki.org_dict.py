import json

'''
This script will parse any language dictionary json file from kaikki.org and produce a json file
that stores part of speech (pos) --> [words].

Json files that come from kaikki.org has one json object per line, where each json object corresponds to an entry
for a word (and includes a shit ton of lingusitc info for that word). This script simply goes through each word/json object,
extracts the pos for each lexical entry, and stores that lexical entry in our new json object that maps pos --> [word].
'''

# Our kaikki.org-dictionary-Occitan.json file is in a special JSON format where there are multiple
# JSON objects and each is seperated by a newline.

# Initialize an empty list to store parsed JSON objects
parsed_objects = []

# Open the JSON file and read it line by line
# Change both depending on which json you want to parse and where you want to store your new json file
raw_language_dict_filename = 'kaikki.org-dictionary-Occitan.json'
pos_to_word_filename = 'occitan_dict.json'
# raw_language_dict_filename = 'kaikki.org-dictionary-Inuktitut.json'  # Change this depending on which json you want to parse
# pos_to_word_filename = 'inuktitut_dict.json'
# raw_language_dict_filename = 'kaikki.org-dictionary-Yoruba.json'  # Change this depending on which json you want to parse
# pos_to_word_filename = 'yoruba_dict.json'
with open(raw_language_dict_filename, 'r') as file:
    for line in file:
        # Parse each line as JSON and append it to the list
        parsed_objects.append(json.loads(line))

# Create a dictionary to store words grouped by part of speech
words_by_pos = {}

# Iterate over each entry and group words by part of speech
for entry in parsed_objects:
    pos = entry.get('pos')
    word = entry.get('word')
    if pos and word:
        if pos not in words_by_pos:
            if pos == "noun" or pos == "verb":
                words_by_pos[pos] = {}
            else:
                words_by_pos[pos] = []
        
        if pos == "noun":
            # If pos = "noun", then determine if the gender
            # is masc or fem
            tags = entry.get('senses')[0].get('tags')
            gend = 'underspecified'
            if tags and 'masculine' in tags:
                gend = 'masculine'
            elif tags and 'feminine' in tags:
                gend = 'feminine'

            if gend not in words_by_pos[pos]:
                words_by_pos[pos][gend] = []

            words_by_pos[pos][gend].append(word)
        elif pos == "verb":
            # If pos = "verb", then determine if c1 (ar),
            # c2 (ir), or c3 (re)
            inf = word[:-2]
            conjugation = word[-2:]  # Slice to get the last two characters

            # We only want verbs that end in -ar, -ir, or -re/-er
            if conjugation not in ["ar", "ir", "re", "er"]:
                continue

            if conjugation not in words_by_pos[pos]:
                words_by_pos[pos][conjugation] = []

            words_by_pos[pos][conjugation].append(inf)
        else:
            # If the pos isn't a noun or verb, then this pos just has a list as it's
            # value and we can insert the word directly here
            words_by_pos[pos].append(word)

# Write the dictionary to a new JSON file
with open(pos_to_word_filename, 'w') as file:
    json.dump(words_by_pos, file, indent=4, ensure_ascii=False)

