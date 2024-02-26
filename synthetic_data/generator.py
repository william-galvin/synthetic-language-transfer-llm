import math
import os
import random
import random as rand
from collections import Counter

import numpy as np

import language


# =====================================BASIC LANGUAGE TESTING, NON SUPPLETIVE ALLOMORPHY============+===================
# Makes verbs where the endings rely on two phonological classes of the verbs
# In this case, it's verbs whose roots end in consonants and those whose roots end in vowels
# Consonant-ending roots add an "a" between the root's final consonant and the ending that follows
def non_suppletive_allomorphy(language_name="non_suppletive_allomorphy", num_train=1e6, num_test=5000):
    # Make num_train and num_test integers
    num_train = int(num_train)
    num_test = int(num_test)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # Create/load a base language
    mylang = create_language_base()

    # Set the inflection paradigms
    mylang.set_inflection_paradigms([
        ["verb", {
            ("sg", "1st", "/C_"): "-ame",
            ("sg", "2nd", "/C_"): "-aju",
            ("sg", "3rd", "/C_"): "-asi",
            ("pl", "1st", "/C_"): "-awe",
            ("pl", "2nd", "/C_"): "-ajal",
            ("pl", "3rd", "/C_"): "-adej",
            ("sg", "1st", "/V_"): "-me",
            ("sg", "2nd", "/V_"): "-ju",
            ("sg", "3rd", "/V_"): "-si",
            ("pl", "1st", "/V_"): "-we",
            ("pl", "2nd", "/V_"): "-jal",
            ("pl", "3rd", "/V_"): "-dej"
        }],
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }]
    ])

    # Generate 100 nouns specific to this language
    for amount, noun_property in [(600, "3rd")]:
        mylang.generate_words(num_words=amount, part_of_speech="noun", paradigm=noun_property)
    mylang.generate_words(num_words=700, part_of_speech="verb", paradigm="verb1")

    # Save the language
    mylang.dump_language(os.path.join("Languages", language_name))

    # Generate 10% more sentences than we need
    # We will sample test sentences from that set, and then remove them from the train sentences
    # Whenever we sample one, we remove all instances of it from the training sentences
    # There are three parameters:
    # 1. Grammaticality of the agreement (correct vs incorrect)
    # 2. Number of distractors (0 vs 1)
    # 3. Generalization (seen roots, unseen roots, unseen roots with one example before)

    # Define the incorrect paradigms (verbs conjugate incorrectly)
    # Class incorrect paradigms are caused by the correct suffix being attached to the wrong class or environment
    incorrect_paradigms_class = [
        ["verb", {
            ("sg", "1st", "/C_"): "-me",
            ("sg", "2nd", "/C_"): "-ju",
            ("sg", "3rd", "/C_"): "-si",
            ("pl", "1st", "/C_"): "-we",
            ("pl", "2nd", "/C_"): "-jal",
            ("pl", "3rd", "/C_"): "-dej",
            ("sg", "1st", "/V_"): "-ame",
            ("sg", "2nd", "/V_"): "-aju",
            ("sg", "3rd", "/V_"): "-asi",
            ("pl", "1st", "/V_"): "-awe",
            ("pl", "2nd", "/V_"): "-ajal",
            ("pl", "3rd", "/V_"): "-adej"
        }],
        # These aren't incorrect
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }],
        # We need to redefine determiner inflection
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }]
    ]

    # Shift incorrect paradigms are caused by the correct class being shifted by one, so number and person is wrong
    incorrect_paradigms_shift = [
        ["verb", {
            ("sg", "1st", "/C_"): "-dej",
            ("sg", "2nd", "/C_"): "-me",
            ("sg", "3rd", "/C_"): "-ju",
            ("pl", "1st", "/C_"): "-si",
            ("pl", "2nd", "/C_"): "-we",
            ("pl", "3rd", "/C_"): "-jal",
            ("sg", "1st", "/V_"): "-adej",
            ("sg", "2nd", "/V_"): "-ame",
            ("sg", "3rd", "/V_"): "-aju",
            ("pl", "1st", "/V_"): "-asi",
            ("pl", "2nd", "/V_"): "-awe",
            ("pl", "3rd", "/V_"): "-ajal"
        }],
        # These aren't incorrect
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }],
        # We need to redefine determiner inflection
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }]
    ]

    # Generate new unseen roots. These may repeat with eachother, but may not be in our current wordset
    unseen_roots = []
    # Keep making new roots not in mylang's word set until we reach num_test
    while len(unseen_roots) < num_test:
        new_verb_root = mylang.generate_words(1, "verb", "new", add_to_lexicon=False)[0]
        # These roots are guaranteed to not be in the word_set
        unseen_roots.append(new_verb_root)
    # We make unseen_roots into a dict since that's what generate_sentences requires
    unseen_roots = {"verb": unseen_roots}

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=int(num_train * 1.1), required_words=None)
    # We need a dictionary of sentence to sequence and a counter of sentences
    # The dictionary will help us ensure that they're unique
    # The counter will allow us to go back to the sentences from the mapping
    sentence_to_sequence = {sentences[i]: sequences[i] for i in range(len(sentences))}
    sentence_counts = Counter(sentences)

    # Iterate over every generalization type
    for generalization_type in ["seen_roots", "unseen_roots", "one_shot"]:
        print(f"Making test set for {generalization_type}")

        # If we're looking at sentences with seen roots, then we just need to sample from our generated sentences
        if generalization_type == "seen_roots":
            # Get our random sentences and their sequences
            random_sentences = rand.sample(list(sentence_to_sequence.keys()), k=num_test)
            random_sequences = [sentence_to_sequence.pop(random_sentence) for random_sentence in random_sentences]

            # This is the list of test sentences now
            # It's guaranteed to be unique, since all keys in sentence_to_sequence are unique
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = random_sentences
            ungrammatical_sentences_class = language.inflect(random_sequences, incorrect_paradigms_class,
                                                             mylang.phonemes)
            ungrammatical_sentences_shift = language.inflect(random_sequences, incorrect_paradigms_shift,
                                                             mylang.phonemes)

        # Now let's make sentences with unseen roots
        elif generalization_type == "unseen_roots":
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the list of test sentences now
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = sentences
            ungrammatical_sentences_class = language.inflect(sequences, incorrect_paradigms_class, mylang.phonemes)
            ungrammatical_sentences_shift = language.inflect(sequences, incorrect_paradigms_shift, mylang.phonemes)

        # Finally we make sentences in a one-shot setting
        else:
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the not yet list of test sentences
            # We need to find the verb for each of these sentences first
            # Then, we will generate an additional sentence with that verb.
            # From there, we will remake that sentence with an incorrect inflection
            prompt_sentences = sentences
            prompt_verbs = find_verbs_given_sequence(sequences)

            # Now we generate num_test sentences with these verbs
            grammatical_test_sentences = []
            # Iterate over each verb, and generate a random sentence
            # We'll store the test_sequences to make the ungrammatical test sentences
            test_sequences = []
            for verb in prompt_verbs:
                # Reformat the tagged verb for generate sentence, and set the verb's paradigm to "new"
                tagged_verb = {"verb": [(verb, "new")]}
                # Make a new sentence and sequence
                test_sentence, test_sequence = mylang.generate_sentences(num_sentences=1, required_words=tagged_verb)

                # generate_sentences returns a list for test_sentence and test_sequence, we only want the first element
                # The sentence is already in the final form, we can mark it as grammatical
                grammatical_test_sentences.append(test_sentence[0])
                test_sequences.append(test_sequence[0])
            # Now we remake the ungrammatical sentences with the ungrammatical paradigms
            ungrammatical_test_sentences_class = language.inflect(test_sequences, incorrect_paradigms_class,
                                                                  mylang.phonemes)
            ungrammatical_test_sentences_shift = language.inflect(test_sequences, incorrect_paradigms_shift,
                                                                  mylang.phonemes)

            # Now we should combine them!
            grammatical_sentences = [prompt_sentences[i] + ". " + grammatical_test_sentences[i]
                                     for i in range(num_test)]
            ungrammatical_sentences_class = [prompt_sentences[i] + ". " + ungrammatical_test_sentences_class[i]
                                             for i in range(num_test)]
            ungrammatical_sentences_shift = [prompt_sentences[i] + ". " + ungrammatical_test_sentences_shift[i]
                                             for i in range(num_test)]

        # Save these now
        language.save_sentences(sentences=grammatical_sentences,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_grammatical.txt"))
        language.save_sentences(sentences=ungrammatical_sentences_class,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_ungrammatical_class.txt"))
        language.save_sentences(sentences=ungrammatical_sentences_shift,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_ungrammatical_shift.txt"))

    # Save the training sentences
    # First, we make them full sentences again
    train_sentences = [item for item, count in sentence_counts.items() for _ in range(count)]
    # Just to make sure, we want to be sure that there are enough training sentences
    # If there are, we want to cut down the number of sentences to the right amount
    assert len(train_sentences) >= num_train
    random.shuffle(train_sentences)
    train_sentences = train_sentences[:num_train]
    # Then we want to incrementally make files with powers of 10, until we reach the train_num
    incremental_num_train = 10
    # Keep on making files
    while incremental_num_train <= num_train:
        # Save those sentences
        language.save_sentences(sentences=train_sentences[:incremental_num_train],
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      "train",
                                                      f"{incremental_num_train}_sentences.txt"))
        # Increment by a factor of 10
        incremental_num_train *= 10


# =====================================BASIC LANGUAGE TESTING, REGULAR PARADIGMS=================+======================
# Makes verbs of one regular paradigm
def regular_paradigms(language_name="one_regular_paradigm", num_train=1e6, num_test=5000):
    # Make num_train and num_test integers
    num_train = int(num_train)
    num_test = int(num_test)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # Create/load a base language
    mylang = create_language_base()

    # Set the inflection paradigms
    mylang.set_inflection_paradigms([
        ["verb", {
            ("sg", "1st"): "-me",
            ("sg", "2nd"): "-ju",
            ("sg", "3rd"): "-si",
            ("pl", "1st"): "-we",
            ("pl", "2nd"): "-jal",
            ("pl", "3rd"): "-dej"
        }],
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }]
    ])

    # Generate 100 nouns specific to this language
    for amount, noun_property in [(600, "3rd")]:
        mylang.generate_words(num_words=amount, part_of_speech="noun", paradigm=noun_property)
    mylang.generate_words(num_words=700, part_of_speech="verb", paradigm="verb1")

    # Save the language
    mylang.dump_language(os.path.join("Languages", language_name))

    # Generate 10% more sentences than we need
    # We will sample test sentences from that set, and then remove them from the train sentences
    # Whenever we sample one, we remove all instances of it from the training sentences
    # There are three parameters:
    # 1. Grammaticality of the agreement (correct vs incorrect)
    # 2. Number of distractors (0 vs 1)
    # 3. Generalization (seen roots, unseen roots, unseen roots with one example before)

    # Define the incorrect paradigms (verbs conjugate incorrectly)
    incorrect_paradigms = [
        ["verb", {
            ("sg", "1st"): "-dej",
            ("sg", "2nd"): "-me",
            ("sg", "3rd"): "-ju",
            ("pl", "1st"): "-si",
            ("pl", "2nd"): "-we",
            ("pl", "3rd"): "-jal"
        }],
        # These aren't incorrect
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }],
        # We need to redefine determiner inflection
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }]
    ]

    # Generate new unseen roots. These may repeat with eachother, but may not be in our current wordset
    unseen_roots = []
    # Keep making new roots not in mylang's word set until we reach num_test
    while len(unseen_roots) < num_test:
        new_verb_root = mylang.generate_words(1, "verb", "new", add_to_lexicon=False)[0]
        # These roots are guaranteed to not be in the word_set
        unseen_roots.append(new_verb_root)
    # We make unseen_roots into a dict since that's what generate_sentences requires
    unseen_roots = {"verb": unseen_roots}

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=int(num_train * 1.1), required_words=None)
    # We need a dictionary of sentence to sequence and a counter of sentences
    # The dictionary will help us ensure that they're unique
    # The counter will allow us to go back to the sentences from the mapping
    sentence_to_sequence = {sentences[i]: sequences[i] for i in range(len(sentences))}
    sentence_counts = Counter(sentences)

    # Iterate over every generalization type
    for generalization_type in ["seen_roots", "unseen_roots", "one_shot"]:
        print(f"Making test set for {generalization_type}")

        # If we're looking at sentences with seen roots, then we just need to sample from our generated sentences
        if generalization_type == "seen_roots":
            # Get our random sentences and their sequences
            random_sentences = rand.sample(list(sentence_to_sequence.keys()), k=num_test)
            random_sequences = [sentence_to_sequence.pop(random_sentence) for random_sentence in random_sentences]

            # This is the list of test sentences now
            # It's guaranteed to be unique, since all keys in sentence_to_sequence are unique
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = random_sentences
            ungrammatical_sentences = language.inflect(random_sequences, incorrect_paradigms, mylang.phonemes)

        # Now let's make sentences with unseen roots
        elif generalization_type == "unseen_roots":
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the list of test sentences now
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = sentences
            ungrammatical_sentences = language.inflect(sequences, incorrect_paradigms, mylang.phonemes)

        # Finally we make sentences in a one-shot setting
        else:
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the not yet list of test sentences
            # We need to find the verb for each of these sentences first
            # Then, we will generate an additional sentence with that verb.
            # From there, we will remake that sentence with an incorrect inflection
            prompt_sentences = sentences
            prompt_verbs = find_verbs_given_sequence(sequences)

            # Now we generate num_test sentences with these verbs
            grammatical_test_sentences = []
            # Iterate over each verb, and generate a random sentence
            # We'll store the test_sequences to make the ungrammatical test sentences
            test_sequences = []
            for verb in prompt_verbs:
                # Reformat the tagged verb for generate sentence, and set the verb's paradigm to "new"
                tagged_verb = {"verb": [(verb, "new")]}
                # Make a new sentence and sequence
                test_sentence, test_sequence = mylang.generate_sentences(num_sentences=1, required_words=tagged_verb)

                # generate_sentences returns a list for test_sentence and test_sequence, we only want the first element
                # The sentence is already in the final form, we can mark it as grammatical
                grammatical_test_sentences.append(test_sentence[0])
                test_sequences.append(test_sequence[0])
            # Now we remake the ungrammatical sentences with the ungrammatical paradigms
            ungrammatical_test_sentences = language.inflect(test_sequences, incorrect_paradigms, mylang.phonemes)

            # Now we should combine them!
            grammatical_sentences = [prompt_sentences[i] + ". " + grammatical_test_sentences[i]
                                     for i in range(num_test)]
            ungrammatical_sentences = [prompt_sentences[i] + ". " + ungrammatical_test_sentences[i]
                                       for i in range(num_test)]

        # Save these now
        language.save_sentences(sentences=grammatical_sentences,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_grammatical.txt"))
        language.save_sentences(sentences=ungrammatical_sentences,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_ungrammatical.txt"))

    # Save the training sentences
    # First, we make them full sentences again
    train_sentences = [item for item, count in sentence_counts.items() for _ in range(count)]
    # Just to make sure, we want to be sure that there are enough training sentences
    # If there are, we want to cut down the number of sentences to the right amount
    assert len(train_sentences) >= num_train
    random.shuffle(train_sentences)
    train_sentences = train_sentences[:num_train]
    # Then we want to incrementally make files with powers of 10, until we reach the train_num
    incremental_num_train = 10
    # Keep on making files
    while incremental_num_train <= num_train:
        # Save those sentences
        language.save_sentences(sentences=train_sentences[:incremental_num_train],
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      "train",
                                                      f"{incremental_num_train}_sentences.txt"))
        # Increment by a factor of 10
        incremental_num_train *= 10


# =====================================BASIC LANGUAGE TESTING, VERB CLASSES======================+======================
# Makes verbs of two classes, p1 and p2, with completely different paradigms
# The paradigms are not predictable by the base form of the verb
def two_verb_classes(language_name="two_verb_classes", num_train=1e6, num_test=5000):
    # Make num_train and num_test integers
    num_train = int(num_train)
    num_test = int(num_test)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # Create/load a base language
    mylang = create_language_base()

    # Set the inflection paradigms
    mylang.set_inflection_paradigms([
        ["verb", {
            ("sg", "1st", "p1"): "-me",
            ("sg", "2nd", "p1"): "-ju",
            ("sg", "3rd", "p1"): "-si",
            ("pl", "1st", "p1"): "-we",
            ("pl", "2nd", "p1"): "-jal",
            ("pl", "3rd", "p1"): "-dej",
            ("sg", "1st", "p2"): "-jo",
            ("sg", "2nd", "p2"): "-tu",
            ("sg", "3rd", "p2"): "-essi",
            ("pl", "1st", "p2"): "-noj",
            ("pl", "2nd", "p2"): "-voj",
            ("pl", "3rd", "p2"): "-loro"
        }],
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }]
    ])

    # Generate 100 nouns specific to this language
    for amount, noun_property in [(600, "3rd")]:
        mylang.generate_words(num_words=amount, part_of_speech="noun", paradigm=noun_property)
    # Generate 350 words from each paradigm with approximately equal probability
    for _ in range(350):
        mylang.generate_words(num_words=1, part_of_speech="verb", paradigm="p1")
        mylang.generate_words(num_words=1, part_of_speech="verb", paradigm="p2")

    # Save the language
    mylang.dump_language(os.path.join("Languages", language_name))

    # Generate 10% more sentences than we need
    # We will sample test sentences from that set, and then remove them from the train sentences
    # Whenever we sample one, we remove all instances of it from the training sentences
    # There are three parameters:
    # 1. Grammaticality of the agreement (correct vs incorrect)
    # 2. Number of distractors (0 vs 1)
    # 3. Generalization (seen roots, unseen roots, unseen roots with one example before)

    # Define the incorrect paradigms (verbs conjugate incorrectly)
    # Class incorrect paradigms are caused by the correct suffix being attached to the wrong class or environment
    incorrect_paradigms_class = [
        ["verb", {
            ("sg", "1st", "p1"): "-jo",
            ("sg", "2nd", "p1"): "-tu",
            ("sg", "3rd", "p1"): "-essi",
            ("pl", "1st", "p1"): "-noj",
            ("pl", "2nd", "p1"): "-voj",
            ("pl", "3rd", "p1"): "-loro",
            ("sg", "1st", "p2"): "-me",
            ("sg", "2nd", "p2"): "-ju",
            ("sg", "3rd", "p2"): "-si",
            ("pl", "1st", "p2"): "-we",
            ("pl", "2nd", "p2"): "-jal",
            ("pl", "3rd", "p2"): "-dej"
        }],
        # These aren't incorrect
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }],
        # We need to redefine determiner inflection
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }]
    ]

    # Shift incorrect paradigms are caused by the correct class being shifted by one, so number and person is wrong
    incorrect_paradigms_shift = [
        ["verb", {
            ("sg", "1st", "p1"): "-dej",
            ("sg", "2nd", "p1"): "-me",
            ("sg", "3rd", "p1"): "-ju",
            ("pl", "1st", "p1"): "-si",
            ("pl", "2nd", "p1"): "-we",
            ("pl", "3rd", "p1"): "-jal",
            ("sg", "1st", "p2"): "-loro",
            ("sg", "2nd", "p2"): "-jo",
            ("sg", "3rd", "p2"): "-tu",
            ("pl", "1st", "p2"): "-essi",
            ("pl", "2nd", "p2"): "-noj",
            ("pl", "3rd", "p2"): "-voj"
        }],
        # These aren't incorrect
        ["noun", {
            "sg": "-",
            "pl": "-ol"
        }],
        # We need to redefine determiner inflection
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }]
    ]

    # Generate new unseen roots. These may repeat with eachother, but may not be in our current wordset
    unseen_roots = []
    # Keep making new roots not in mylang's word set until we reach num_test
    while len(unseen_roots) < num_test:
        # Make a p1 verb
        new_verb_root = mylang.generate_words(1, "verb", "new.p1", add_to_lexicon=False)[0]
        # These roots are guaranteed to not be in the word_set
        unseen_roots.append(new_verb_root)

        # Do the same with a verb from p2
        new_verb_root = mylang.generate_words(1, "verb", "new.p2", add_to_lexicon=False)[0]
        unseen_roots.append(new_verb_root)
    # We make unseen_roots into a dict since that's what generate_sentences requires
    unseen_roots = {"verb": unseen_roots}

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=int(num_train * 1.1), required_words=None)
    # We need a dictionary of sentence to sequence and a counter of sentences
    # The dictionary will help us ensure that they're unique
    # The counter will allow us to go back to the sentences from the mapping
    sentence_to_sequence = {sentences[i]: sequences[i] for i in range(len(sentences))}
    sentence_counts = Counter(sentences)

    # Iterate over every generalization type
    for generalization_type in ["seen_roots", "unseen_roots", "one_shot"]:
        print(f"Making test set for {generalization_type}")

        # If we're looking at sentences with seen roots, then we just need to sample from our generated sentences
        if generalization_type == "seen_roots":
            # Get our random sentences and their sequences
            random_sentences = rand.sample(list(sentence_to_sequence.keys()), k=num_test)
            random_sequences = [sentence_to_sequence.pop(random_sentence) for random_sentence in random_sentences]

            # This is the list of test sentences now
            # It's guaranteed to be unique, since all keys in sentence_to_sequence are unique
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = random_sentences
            ungrammatical_sentences_class = language.inflect(random_sequences, incorrect_paradigms_class,
                                                             mylang.phonemes)
            ungrammatical_sentences_shift = language.inflect(random_sequences, incorrect_paradigms_shift,
                                                             mylang.phonemes)

        # Now let's make sentences with unseen roots
        elif generalization_type == "unseen_roots":
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the list of test sentences now
            # We need to make grammatical and ungrammatical test sentences now
            grammatical_sentences = sentences
            ungrammatical_sentences_class = language.inflect(sequences, incorrect_paradigms_class, mylang.phonemes)
            ungrammatical_sentences_shift = language.inflect(sequences, incorrect_paradigms_shift, mylang.phonemes)

        # Finally we make sentences in a one-shot setting
        else:
            # Now that we have our unseen verb roots, we can make sentences
            sentences, sequences = mylang.generate_sentences(num_sentences=num_test, required_words=unseen_roots)

            # This is the not yet list of test sentences
            # We need to find the verb for each of these sentences first
            # Then, we will generate an additional sentence with that verb.
            # From there, we will remake that sentence with an incorrect inflection
            prompt_sentences = sentences
            # Unlike the other two, we also want to check to see which class the verb belongs to
            prompt_verbs = find_verbs_given_sequence(sequences, ['p1', 'p2'])

            # Now we generate num_test sentences with these verbs
            grammatical_test_sentences = []
            # Iterate over each verb, and generate a random sentence
            # We'll store the test_sequences to make the ungrammatical test sentences
            test_sequences = []
            for verb, verb_class_list in prompt_verbs:
                # Make sure there's only one verb class that each verb belongs to, then get that class
                assert len(verb_class_list) == 1
                verb_class = verb_class_list[0]
                # Reformat the tagged verb for generate sentence, and set the verb's paradigm to "new"
                tagged_verb = {"verb": [(verb, f"new.{verb_class}")]}
                # Make a new sentence and sequence
                test_sentence, test_sequence = mylang.generate_sentences(num_sentences=1, required_words=tagged_verb)

                # generate_sentences returns a list for test_sentence and test_sequence, we only want the first element
                # The sentence is already in the final form, we can mark it as grammatical
                grammatical_test_sentences.append(test_sentence[0])
                test_sequences.append(test_sequence[0])
            # Now we remake the ungrammatical sentences with the ungrammatical paradigms
            ungrammatical_test_sentences_class = language.inflect(test_sequences, incorrect_paradigms_class,
                                                                  mylang.phonemes)
            ungrammatical_test_sentences_shift = language.inflect(test_sequences, incorrect_paradigms_shift,
                                                                  mylang.phonemes)

            # Now we should combine them!
            grammatical_sentences = [prompt_sentences[i] + ". " + grammatical_test_sentences[i]
                                     for i in range(num_test)]
            ungrammatical_sentences_class = [prompt_sentences[i] + ". " + ungrammatical_test_sentences_class[i]
                                             for i in range(num_test)]
            ungrammatical_sentences_shift = [prompt_sentences[i] + ". " + ungrammatical_test_sentences_shift[i]
                                             for i in range(num_test)]

        # Save these now
        language.save_sentences(sentences=grammatical_sentences,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_grammatical.txt"))
        language.save_sentences(sentences=ungrammatical_sentences_class,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_ungrammatical_class.txt"))
        language.save_sentences(sentences=ungrammatical_sentences_shift,
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      f"{num_test}_{generalization_type}_ungrammatical_shift.txt"))

    # Save the training sentences
    # First, we make them full sentences again
    train_sentences = [item for item, count in sentence_counts.items() for _ in range(count)]
    # Just to make sure, we want to be sure that there are enough training sentences
    # If there are, we want to cut down the number of sentences to the right amount
    assert len(train_sentences) >= num_train
    random.shuffle(train_sentences)
    train_sentences = train_sentences[:num_train]
    # Then we want to incrementally make files with powers of 10, until we reach the train_num
    incremental_num_train = 10
    # Keep on making files
    while incremental_num_train <= num_train:
        # Save those sentences
        language.save_sentences(sentences=train_sentences[:incremental_num_train],
                                filepath=os.path.join("Languages",
                                                      language_name,
                                                      "train",
                                                      f"{incremental_num_train}_sentences.txt"))
        # Increment by a factor of 10
        incremental_num_train *= 10


# =====================================GENERALLY HELPFUL METHODS========================================================

# Finds the number of distractor PPs given a new_agreed_lexeme_sequence
# This is what a sample new_agreed_lexeme_sequence looks like:
# [['', ['nom', '__hash__:1455983988560492', 'det', 'main_det', 'pl']],
#   ['fapuf', ['nom', '__hash__:1455983988560492', 'nouny', 'pl', 'noun', '3rd']],
#   ['ikjoku', ['', 'verb', 'verb1', 'pl', '3rd']]]
# Finds the number of prepositions between the first nominative noun and the first verb
# In my grammar (2024 Jan 17), there is always one nominative noun and one verb
def find_num_distractors(new_agreed_lexeme_sequence):
    # Keep track of the number of prepositions
    num_prepositions = -1

    # Start counting at the first noun (set the num_prepositions to 0)
    for lexeme in new_agreed_lexeme_sequence:
        # If we get to the first nominative noun, then we set the num_prepositions to 0
        if "nom" in lexeme[1] and "nouny" in lexeme[1]:
            num_prepositions = 0
        # If we get to the verb, then we stop counting and return the value
        if "verb" in lexeme[1]:
            # Sanity check: it should be non-negative
            assert num_prepositions >= 0
            return num_prepositions
        # If we get to a preposition, we increase the number of distractors by one
        if "prep" in lexeme[1]:
            num_prepositions += 1

    # We shouldn't get here, this is a sanity check
    raise Exception("Shouldn't get here")


# Finds the verbs given a list of sequences
# Returns just the verbs
# In my grammar (2024 Jan 17), there is always one verb. The behavior on sentences with more than one verb is undefined
# Check for properties is by default none, but may be a list of properties. Instead of being a list of the verb roots,
#   if you pass in check_for_properties, the output will be a list of tuples, where the first element if the verb root
#   and the second element is a containing all the properties that are both in check_for_properties and the verb.
def find_verbs_given_sequence(sequences, check_for_properties=None):
    # Store the verbs in a list
    verbs = []
    # For each sequence, find the lexical item tagged with "verb"
    for sequence in sequences:
        # Look at each word
        for lexical_item in sequence:
            # Look at the properties of each word
            if "verb" in lexical_item[1]:
                # If it's a verb, then we add the word itself to the verbs list
                root = lexical_item[0]
                # If we're checking to see that there are any additional properties, then check to see if they exist
                if check_for_properties:
                    overlapping_properties = list(set(check_for_properties) & set(lexical_item[1]) )
                    verbs.append((root, overlapping_properties))
                # Otherwise, just return the root
                else:
                    verbs.append(root)
    # And that's it!
    return verbs


def generate_and_save_sentences(lang, language_name, num_sentences, sentence_prefix, required_words=None):
    # Create the directory if it does not exist
    directory_path = os.path.join("Languages", language_name)
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs(os.path.join(directory_path, "train"), exist_ok=True)

    # Generate some sentences
    sentences, _ = lang.generate_sentences(num_sentences, required_words)
    rand.shuffle(sentences)

    # These are the sizes of the test
    training_sizes = np.logspace(1, 7, num=7, base=10, dtype=int)

    # Gradually increase the number of training sentences
    for training_set_index in range(len(training_sizes)):
        # The number of sentences we need is the training size, minus what's already in there
        # The number of sentences that's already in there is the previous training set index
        if training_set_index == 0:
            prev_num_training_examples = 0
        else:
            prev_num_training_examples = training_sizes[training_set_index - 1]
        # Get the number of sentences that we want to train the model on
        size_current_training_set = training_sizes[training_set_index] - prev_num_training_examples

        # Get that number of sentences uniquely
        training_set = sentences[prev_num_training_examples:size_current_training_set]

        # Save them
        language.save_sentences(sentences=training_set,
                                filepath=os.path.join(directory_path, "train",
                                                      f"{training_sizes[training_set_index]}_"
                                                      f"{sentence_prefix}_sentences.txt"))

    # Return the sentences you generate
    return sentences


# Creates a test language
def create_language_base():
    # Create a language
    mylang = language.Language()

    # Set the phonology of the language
    phonemes = {
        "C": ["p", "b", "t", "d", "k", "g", "m", "n", "f", "v", "s", "z", "h", "j", "w", "r", "l"],
        "V": ["a", "e", "i", "o", "u"]
    }
    mylang.set_phonemes(phonemes=phonemes)

    # Set the syllables of the language
    syllables = ["CVC", "CV", "VC"]
    mylang.set_syllables(syllables=syllables)

    # Set the syllable lambda
    mylang.set_syllable_lambda(0.8)

    # Set the parts of speech of the language
    parts_of_speech = ["noun", "verb", "adj", "prep", "det"]
    mylang.set_parts_of_speech(parts_of_speech=parts_of_speech)

    # Set the generation rules
    # Adj N (Prep Adj N) V Adj O (Prep Adj N)
    mylang.set_generation_rules({
        "S": [["sNP", "VP"], 1],  # Sentences generate subject NPs and VPs
        "VP": [["verb", "UnmarkedNP"], 0.7, ["verb"], 0.3],  # VPs generate verbs (and object NPs)
        "NP": [["det*nouny", "NOM"], 0.6, ["PRON"], 0.4],  # NPs can be a det NOM or a PRON
        "NOM": [["adj*nouny", "NOM"], 0.35, ["NoAdjNOM"], 0.65],  # NPs may take adjectives before the rest, recursive
        "NoAdjNOM": [["N", "PP*nom.__hash__"], 0.2, ["N"], 0.8],  # NoAdjNPs become nouns, or nouns with a PP
        "PP": [["prep*nouny", "UnmarkedNP"], 1],  # PPs always become prepositions followed by NPs
        "PRON": [["sgPRON"], 0.8, ["plPRON"], 0.2],  # Pronouns are singular or plural with the same probabilities as Ns
        "sgPRON": [["1stsgpron"], 0.45, ["2ndsgpron"], 0.2, ["3rdsgpron"], 0.25],  # Pronouns have number
        "plPRON": [["1stplpron"], 0.45, ["2ndplpron"], 0.2, ["3rdplpron"], 0.25],  # Pronouns have number
    })

    # Set independent probabilistic rules, e.g. pluralization, past tense
    mylang.set_unconditioned_rules({
        "sNP": [["UnmarkedNP"], "nom", 1],  # Subject NPs take the nominative
        "UnmarkedNP": [["NP"], "__hash__.nouny", 1],  # We want to make sure that words in the same NP can agree
        "N": [["noun"], "sg", 0.8, "pl", 0.2],  # Nouns may be singular or plural
    })

    # Set the agreement rules
    mylang.set_agreement_rules({
        "verb": [["nom", "nouny"], [["sg", "pl"], ["1st", "2nd", "3rd"]]],  # Verbs agree with nominative nouns
        "det": [["noun", "__hash__"], [["sg", "pl"]]]  # Determiners agree with their head nouns
    })

    # Generate 1 determiner. Different forms will come from inflections
    mylang.add_word(surface_form="", part_of_speech="det", paradigm="main_det")
    # Generate 6 pronouns, each with a different agreement
    for pers in ["1st", "2nd", "3rd"]:
        for num in ["sg", "pl"]:
            pronoun_pers_num = f"{pers}{num}pron"
            mylang.set_parts_of_speech([pronoun_pers_num])
            mylang.generate_words(num_words=1, part_of_speech=pronoun_pers_num, paradigm=f'pron.{pers}.{num}')
    # Generate 10 prepositions
    mylang.generate_words(num_words=10, part_of_speech="prep", paradigm='uninflected')
    # Generate 200 adjectives
    mylang.generate_words(num_words=200, part_of_speech="adj", paradigm='uninflected')

    # Set an inflection paradigm for determiners
    mylang.set_inflection_paradigms([
        ["det", {
            "sg": "-duh",
            "pl": "-di",
        }],
    ])

    # Return the language
    return mylang


if __name__ == "__main__":
    # Currently with sanity check settings
    # basic creates one regular paradigm
    # regular_paradigms()
    # verb_classes creates two regular paradigms, where the class of the verb is not predictable
    two_verb_classes()
    # non_suppletive_allomorphy creates one regular paradigm with regular CV allomorphy
    # non_suppletive_allomorphy()
