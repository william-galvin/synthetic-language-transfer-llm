import json
import math
import os
import random
import random as rand
from collections import Counter

import numpy as np

import language

# ===================================== FRISIAN ========================================================================
Frisian_POS = [
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


# Generate arbitrary amounts of Frisian sentences
def generate_frisian_data(language_name="frisian_synthetic", num_train=1e6):
    # Create a language
    mylang = language.Language()

    # Set the phonology of the language
    phonemes = {
        "L": ["p", "b", "t", "d", "k", "g", "m", "n", "f", "v", "s", "z", "h", "j", "w", "r", "l", "c", "x",
              "a", "e", "i", "o", "u", "â", "ê", "é", "y", "ô", "û", "ú"],
        "C": ["p", "b", "t", "d", "k", "g", "m", "n", "f", "v", "s", "z", "h", "j", "w", "r", "l", "c", "x"],
        "V": ["a", "e", "i", "o", "u", "â", "ê", "é", "y", "ô", "û", "ú"],
    }
    mylang.set_phonemes(phonemes=phonemes)

    # Set the parts of speech of the language
    parts_of_speech = [pos.lower() for pos in Frisian_POS]
    mylang.set_parts_of_speech(parts_of_speech=parts_of_speech)

    # Set the generation rules
    # Adj N (Prep Adj N) V Adj O (Prep Adj N)
    mylang.set_generation_rules({
        "S": [["sNP", "VP"], 1],  # Sentences generate subject NPs and VPs
        "VP": [["Untensedverb", "UnmarkedNP"], 0.7, ["Untensedverb"], 0.3],  # VPs generate verbs (and object NPs)
        "NP": [["det*nouny", "NOM"], 0.6, ["PRON"], 0.4],  # NPs can be a det NOM or a PRON
        "NOM": [["adj*nouny", "NOM"], 0.35, ["NoAdjNOM"], 0.65],  # NPs may take adjectives before the rest, recursive
        "NoAdjNOM": [["N", "PP*nom.__hash__"], 0.2, ["N"], 0.8],  # NoAdjNPs become nouns, or nouns with a PP
        "PP": [["adp*nouny", "UnmarkedNP"], 1],  # PPs always become prepositions followed by NPs
    })

    # Set independent probabilistic rules, e.g. pluralization, past tense
    mylang.set_unconditioned_rules({
        "sNP": [["UnmarkedNP"], "nom", 1],  # Subject NPs take the nominative
        "UnmarkedNP": [["NP"], "__hash__.nouny", 1],  # We want to make sure that words in the same NP can agree
        "N": [["NUMnoun"], "sg", 0.8, "pl", 0.2],  # Nouns may be singular or plural
        "NUMnoun": [["noun"], "def", 0.8, "indef", 0.2],  # Nouns may be definite or indefinite
        "Untensedverb": [["verb"], "prs", 0.8, "pst", 0.2],  # Verbs can take tense
        # Go through to get a fully specified pronoun
        "PRON": [["PERpron"], "1st", 0.2, "2nd", 0.1, "3rd", 0.7],  # Get the person of the pronoun
        "PERpron": [["NUMpron"], "sg", 0.7, "pl", 0.3],  # Get the number
        "NUMpron": [["REGISTERpron"], "pol", 0.7, "fam", 0.3],  # Get the register (polite, familiar)
        "REGISTERpron": [["pron"], "masc", 0.25, "fem", 0.25, "neut", 0.5]  # Get the gender
    })

    # Set the agreement rules
    mylang.set_agreement_rules({
        "verb": [["nom", "nouny"], [["sg", "pl"], ["1st", "2nd", "3rd"]]],  # Verbs agree with nominative nouns
        # Determiners agree with their head nouns in number, gender, and definiteness
        "det": [["noun", "__hash__"], [["sg", "pl"], ["common", "neuter"], ["def", "indef"]]],
        "adj": [["noun", "__hash__"], [["sg", "pl"], ["common", "neuter"], ["def", "indef"]]],
    })

    # Set the dictionary and set the pronouns to nothing, I already got rid of pron and det
    with open('../data/frisian_dict.json', 'r') as frisian_dict:
        mylang.set_dictionary(json.load(frisian_dict))
        # See if there's a better way to do this in the future

    # Set an inflection paradigm for pronoun
    mylang.set_inflection_paradigms([
        ["pron", {
            ("sg", "1st", "nom"): "-ik",
            ("sg", "1st", "*nom"): "-my",
            # Second person pronouns don't all distinguish between nominative and accusative
            ("sg", "2nd", "nom", "fam"): "-do",
            ("sg", "2nd", "*nom", "fam"): "-dy",
            ("sg", "2nd", "pol"): "-jo",
            # Third person singular pronouns have a gender distinction
            ("sg", "3rd", "nom", "masc"): "-hy",
            ("sg", "3rd", "*nom", "masc"): "-him",
            ("sg", "3rd", "nom", "fem"): "-sy",  # We use "sy" instead of "hya" since it's more modern
            ("sg", "3rd", "*nom", "fem"): "-har",
            # Third person singular neuter pronoun doesn't have a nom/acc distinction
            ("sg", "3rd", "neut"): "-it",
            ("pl", "1st", "nom"): "-wy",
            ("pl", "1st", "*nom"): "-ús",
            # Second person pronouns don't distinguish between nominative and accusative or register
            ("pl", "2nd"): "-jimme",
            ("pl", "3rd", "nom"): "-sy",  # We use "sy" instead of "hya" since it's more modern
            ("pl", "3rd", "*nom"): "-har"
        }],
        ["det", {
            ("sg", "common", "def"): "-de",
            ("sg", "neuter", "def"): "-it",
            ("pl", "def"): "-de",
            ("sg", "indef"): "-in",
            ("pl", "indef"): "-",
        }],
        ["noun", {
            "sg": "-",
            ("pl", "/eC_"): "-s",
            ("pl", "/eV_"): "-en",
            ("pl", "/*eL_"): "-en",
        }],
        ["verb", {
            # -je verbs, present
            ("sg", "1st", "/je_", "prs"): "-",
            ("sg", "2nd", "/je_", "prs"): "-st",
            ("sg", "3rd", "/je_", "prs"): "-t",
            ("pl", "/je_", "prs"): "-e",
            # -e verbs, present
            ("sg", "1st", "/*je_", "prs"): "-je",
            ("sg", "2nd", "/*je_", "prs"): "-est",
            ("sg", "3rd", "/*je_", "prs"): "-et",
            ("pl", "/*je_", "prs"): "-je",
            # -je verbs, past
            ("sg", "1st", "/je_", "pst"): "-e",
            ("sg", "2nd", "/je_", "pst"): "-est",
            ("sg", "3rd", "/je_", "pst"): "-et",
            ("pl", "/je_", "pst"): "-en",
            # -e verbs, past
            ("sg", "1st", "/*je_", "pst"): "-te",
            ("sg", "2nd", "/*je_", "pst"): "-test",
            ("sg", "3rd", "/*je_", "pst"): "-te",
            ("pl", "/*je_", "pst"): "-ten",
            # not -e verbs don't inflect, they shouldn't be there in theory
            "/*e_": "-"
        }],
        ["adj", {
            # Adjectives take "-e" always, except singular neuter indefinite
            # Just to simplify it for now (since singular neuter indefinite is very specific) we always take "-e"
            "sg": "-e",
            "pl": "-e"
        }]
    ])

    # Save the language
    mylang.dump_language(os.path.join("synthetic_datasets", language_name))

    # Make num_train and num_test integers
    num_train = int(num_train)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=num_train, required_words=None,
                                                     sampling_method="uniform", regenerate_exception_sentences=True)

    # Save these now
    for num_train_group in range(1, int(math.log10(num_train)) + 1):
        language.save_sentences(sentences=sentences[:10 ** (num_train_group + 1)],
                                filepath=os.path.join("synthetic_datasets",
                                                      language_name,
                                                      f"{10 ** (num_train_group + 1)}_train_sentences.txt"))


# ===================================== OCCITAN ========================================================================
# Generate arbitrary amounts of Frisian sentences
def generate_occitan_data(language_name="occitan_synthetic", num_train=1e6):
    # Get the dictionary:
    with open('../scripts/occitan_dict.json', 'r') as file:
        occitan_dict = json.load(file)

    # Create a language
    mylang = language.Language()

    # Set the phonology of the language
    phonemes = {
        "C": ["p", "b", "t", "d", "k", "g", "m", "n", "f", "v", "s", "z", "h", "j", "w", "r", "l", "c", "x"],
        "V": ["a", "e", "i", "o", "u", "â", "ê", "é", "y", "ô", "û", "ú"],
    }
    mylang.set_phonemes(phonemes=phonemes)

    # Set the parts of speech of the language
    parts_of_speech = list(occitan_dict.keys() )
    mylang.set_parts_of_speech(parts_of_speech=parts_of_speech)

    # Set the generation rules
    # Adj N (Prep Adj N) V Adj O (Prep Adj N)
    mylang.set_generation_rules({
        "S": [["sNP", "VP"], 1],  # Sentences generate subject NPs and VPs
        # VPs may have an object, which precedes the verb if it's a pronoun and follows it otherwise
        "VP": [["Untensedverb", "ObjDetNom"], 0.5, ["Untensedverb"], 0.2, ["ObjPron", "Untensedverb"], 0.3],
        "DetNom": [['det', "NOM"], 1],  # DetNoms can become det noms
        "NP": [["det*nouny", "NOM"], 0.6, ["PRON"], 0.4],  # NPs can be a det NOM or a PRON
        "NOM": [["NOM", "adj*nouny"], 0.35, ["NoAdjNOM"], 0.65],  # NPs may take adjectives before the rest, recursive
        "NoAdjNOM": [["N", "PP*nom.__hash__"], 0.2, ["N"], 0.8],  # NoAdjNPs become nouns, or nouns with a PP
        "PP": [["prep*nouny", "UnmarkedNP"], 1],  # PPs always become prepositions followed by NPs
    })

    # Set independent probabilistic rules, e.g. pluralization, past tense
    mylang.set_unconditioned_rules({
        "sNP": [["UnmarkedNP"], "nom", 1],  # Subject NPs take the nominative
        "ObjDetNom": [["DetNom"], "__hash__.acc.nouny", 1],  # Object things are accusative
        "ObjPron": [["PRON"], "acc.nouny", 1],  # Object things are accusative
        "UnmarkedNP": [["NP"], "__hash__.nouny", 1],  # We want to make sure that words in the same NP can agree
        "N": [["NUMnoun"], "sg", 0.8, "pl", 0.2],  # Nouns may be singular or plural
        "NUMnoun": [["noun"], "def", 0.8, "indef", 0.2],  # Nouns may be definite or indefinite
        "Untensedverb": [["verb"], "prs", 0.4, "impfv", 0.2, "pret", 0.2, "fut", 0.2],  # Verbs can take tense
        # # Go through to get a fully specified pronoun
        "PRON": [["PERpron"], "1st", 0.2, "2nd", 0.1, "3rd", 0.7],  # Get the person of the pronoun
        "PERpron": [["NUMpron"], "sg", 0.7, "pl", 0.3],  # Get the number
        "NUMpron": [["pron"], "masc", 0.25, "fem", 0.25, "neut", 0.5]  # Get the gender
    })

    # Set the agreement rules
    mylang.set_agreement_rules({
        "verb": [["nom", "nouny"], [["sg", "pl"], ["1st", "2nd", "3rd"]]],  # Verbs agree with nominative nouns
        # Determiners agree with their head nouns in number, gender, and definiteness
        "det": [["noun", "__hash__"], [["sg", "pl"], ["masculine", "feminine"], ["def", "indef"]]],
        "adj": [["noun", "__hash__"], [["sg", "pl"], ["masculine", "feminine"], ["def", "indef"]]],
    })

    # Set the dictionary
    mylang.set_dictionary(occitan_dict)

    # Set an inflection paradigm for pronoun
    mylang.set_inflection_paradigms([
        ["pron", {
            ("sg", "1st", "nom"): "-ièu",
            ("sg", "1st", "*nom"): "-me",
            ("sg", "2nd", "nom"): "-tu",  # No formality since it's not well documented
            ("sg", "2nd", "*nom"): "-te",
            # Third person singular and all plural pronouns have a gender distinction
            ("sg", "3rd", "nom", "masc"): "-el",
            ("sg", "3rd", "*nom", "masc"): "lo",
            ("sg", "3rd", "nom", "fem"): "-ela",
            ("sg", "3rd", "*nom", "fem"): "-la",
            ("sg", "3rd", "nom", "neut"): "-el",
            ("sg", "3rd", "*nom", "neut"): "-o",
            ("pl", "1st", "nom", "*fem"): "-nosautres",  # We do this to increase the change of a plural masc
            ("pl", "1st", "nom", "fem"): "-nosautras",
            ("pl", "1st", "*nom"): "-nos",
            ("pl", "2nd", "nom", "*fem"): "-vosautres",  # We do this to increase the change of a plural masc
            ("pl", "2nd", "nom", "fem"): "-vosautras",
            ("pl", "2nd", "*nom"): "-vos",
            ("pl", "3rd", "nom", "*fem"): "-eles",  # We do this to increase the change of a plural masc
            ("pl", "3rd", "nom", "fem"): "-elas",
            ("pl", "3rd", "*nom", "*fem"): "-los",  # We do this to increase the change of a plural masc
            ("pl", "3rd", "*nom", "fem"): "-las",
        }],
        ["det", {
            ("sg", "masculine", "def"): "-lo",
            ("sg", "feminine", "def"): "-la",
            ("pl", "masculine", "def"): "-los",
            ("pl", "feminine", "def"): "-las",
            ("sg", "masculine", "indef"): "-un",
            ("sg", "feminine", "indef"): "-una",
            ("pl", "indef"): "-de",  # Plural indefinites look the same
        }],
        ["noun", {
            "sg": "-",
            ("pl", "/s_"): "-es",
            ("pl", "/*s_"): "-s",
        }],
        ["verb", {
            # Group 1, -ar, prs
            ("sg", "1st", "ar", "prs"): "-i",
            ("sg", "2nd", "ar", "prs"): "-as",
            ("sg", "3rd", "ar", "prs"): "-a",
            ("pl", "1st", "ar", "prs"): "-am",
            ("pl", "2nd", "ar", "prs"): "-atz",
            ("pl", "3rd", "ar", "prs"): "-an",
            # Group 1, -ar, impfv
            ("sg", "1st", "ar", "impfv"): "-avi",
            ("sg", "2nd", "ar", "impfv"): "-avas",
            ("sg", "3rd", "ar", "impfv"): "-ava",
            ("pl", "1st", "ar", "impfv"): "-àvem",
            ("pl", "2nd", "ar", "impfv"): "-àvetz",
            ("pl", "3rd", "ar", "impfv"): "-avan",
            # Group 1, -ar, pret
            ("sg", "1st", "ar", "pret"): "-èri",
            ("sg", "2nd", "ar", "pret"): "-ères",
            ("sg", "3rd", "ar", "pret"): "-èt",
            ("pl", "1st", "ar", "pret"): "-èrem",
            ("pl", "2nd", "ar", "pret"): "-èretz",
            ("pl", "3rd", "ar", "pret"): "-èron",
            # Group 1, -ar, fut
            ("sg", "1st", "ar", "fut"): "-arai",
            ("sg", "2nd", "ar", "fut"): "-aràs",
            ("sg", "3rd", "ar", "fut"): "-arà",
            ("pl", "1st", "ar", "fut"): "-arem",
            ("pl", "2nd", "ar", "fut"): "-aretz",
            ("pl", "3rd", "ar", "fut"): "-àn",
            # Group 2 no suffix, -er, prs
            ("sg", "1st", "ir", "prs"): "-issi",
            ("sg", "2nd", "ir", "prs"): "-isses",
            ("sg", "3rd", "ir", "prs"): "-ís",
            ("pl", "1st", "ir", "prs"): "-issèm",
            ("pl", "2nd", "ir", "prs"): "-issètz",
            ("pl", "3rd", "ir", "prs"): "-isson",
            # Group 2 no suffix, -er, impfv
            ("sg", "1st", "ir", "impfv"): "-issiái",
            ("sg", "2nd", "ir", "impfv"): "-issiás",
            ("sg", "3rd", "ir", "impfv"): "-issiá",
            ("pl", "1st", "ir", "impfv"): "-issiam",
            ("pl", "2nd", "ir", "impfv"): "-issiatz",
            ("pl", "3rd", "ir", "impfv"): "-issián",
            # Group 2 no suffix, -er, pret
            ("sg", "1st", "ir", "pret"): "-iguèri",
            ("sg", "2nd", "ir", "pret"): "-iguères",
            ("sg", "3rd", "ir", "pret"): "-iguèt",
            ("pl", "1st", "ir", "pret"): "-iguèrem",
            ("pl", "2nd", "ir", "pret"): "-iguèretz",
            ("pl", "3rd", "ir", "pret"): "-iguèron",
            # Group 2 no suffix, -er, fut
            ("sg", "1st", "ir", "fut"): "-irai",
            ("sg", "2nd", "ir", "fut"): "-iràs",
            ("sg", "3rd", "ir", "fut"): "-irà",
            ("pl", "1st", "ir", "fut"): "-irem",
            ("pl", "2nd", "ir", "fut"): "-iretz",
            ("pl", "3rd", "ir", "fut"): "-iràn",
            # Group 3, -re, prs
            ("sg", "1st", "re", "prs"): "-i",
            ("sg", "2nd", "re", "prs"): "-es",
            ("sg", "3rd", "re", "prs"): "-",
            ("pl", "1st", "re", "prs"): "-èm",
            ("pl", "2nd", "re", "prs"): "-ètz",
            ("pl", "3rd", "re", "prs"): "-on",
            # Group 3, -re, impfv
            ("sg", "1st", "re", "impfv"): "-iái",
            ("sg", "2nd", "re", "impfv"): "-iás",
            ("sg", "3rd", "re", "impfv"): "-iá",
            ("pl", "1st", "re", "impfv"): "-iam",
            ("pl", "2nd", "re", "impfv"): "-iatz",
            ("pl", "3rd", "re", "impfv"): "-ián",
            # Group 3, -re, pret
            ("sg", "1st", "re", "pret"): "-èri",
            ("sg", "2nd", "re", "pret"): "-ères",
            ("sg", "3rd", "re", "pret"): "-èt",
            ("pl", "1st", "re", "pret"): "-èrem",
            ("pl", "2nd", "re", "pret"): "-èretz",
            ("pl", "3rd", "re", "pret"): "-èron",
            # Group 3, -re, fut
            ("sg", "1st", "re", "fut"): "-rai",
            ("sg", "2nd", "re", "fut"): "-ràs",
            ("sg", "3rd", "re", "fut"): "-rà",
            ("pl", "1st", "re", "fut"): "-rem",
            ("pl", "2nd", "re", "fut"): "-retz",
            ("pl", "3rd", "re", "fut"): "-ràn",
            # Group 3, -er, prs
            ("sg", "1st", "er", "prs"): "-i",
            ("sg", "2nd", "er", "prs"): "-es",
            ("sg", "3rd", "er", "prs"): "-",
            ("pl", "1st", "er", "prs"): "-èm",
            ("pl", "2nd", "er", "prs"): "-ètz",
            ("pl", "3rd", "er", "prs"): "-on",
            # Group 3, -er, impfv
            ("sg", "1st", "er", "impfv"): "-iái",
            ("sg", "2nd", "er", "impfv"): "-iás",
            ("sg", "3rd", "er", "impfv"): "-iá",
            ("pl", "1st", "er", "impfv"): "-iam",
            ("pl", "2nd", "er", "impfv"): "-iatz",
            ("pl", "3rd", "er", "impfv"): "-ián",
            # Group 3, -er, pret
            ("sg", "1st", "er", "pret"): "-èri",
            ("sg", "2nd", "er", "pret"): "-ères",
            ("sg", "3rd", "er", "pret"): "-èt",
            ("pl", "1st", "er", "pret"): "-èrem",
            ("pl", "2nd", "er", "pret"): "-èretz",
            ("pl", "3rd", "er", "pret"): "-èron",
            # Group 3, -er, fut
            ("sg", "1st", "er", "fut"): "-rai",
            ("sg", "2nd", "er", "fut"): "-ràs",
            ("sg", "3rd", "er", "fut"): "-rà",
            ("pl", "1st", "er", "fut"): "-rem",
            ("pl", "2nd", "er", "fut"): "-retz",
            ("pl", "3rd", "er", "fut"): "-ràn",
        }],
        # Adjective inflection is quite simple, first add -a if it's feminine, and -s if it's plural
        ["adj", {
            "feminine": "-a",
            "masculine": "-"
        }],
        ["adj", {
            "sg": "-",
            "pl": "-s"
        }]
    ])

    # Save the language
    mylang.dump_language(os.path.join("synthetic_datasets", language_name))

    # Make num_train and num_test integers
    num_train = int(num_train)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=num_train, required_words=None,
                                                     sampling_method="uniform", regenerate_exception_sentences=True)

    # Save these now
    for num_train_group in range(1, int(math.log10(num_train)) + 1):
        language.save_sentences(sentences=sentences[:10 ** (num_train_group + 1)],
                                filepath=os.path.join("synthetic_datasets",
                                                      language_name,
                                                      f"{10 ** (num_train_group + 1)}_train_sentences.txt"))


# ===================================== YORUBA =========================================================================
# Generate arbitrary amounts of Yoruba sentences
def generate_cebuano_data(language_name="cebuano_synthetic", num_train=1e6):
    # Create a language
    mylang = language.Language()

    # Set the phonology of the language
    phonemes = {
    }
    mylang.set_phonemes(phonemes=phonemes)

    # Get the dictionary:
    with open('../data/cebuano_dict.json', 'r') as file:
        cebuano_dict = json.load(file)

    # Set the parts of speech of the language
    parts_of_speech = list(cebuano_dict.keys() )
    mylang.set_parts_of_speech(parts_of_speech=parts_of_speech)

    # Set the generation rules
    # Adj N (Prep Adj N) V Adj O (Prep Adj N)
    mylang.set_generation_rules({
        "S": [["VSO"], 0.7, ["VS"], 0.3],  # Verbs come first
        # Choose the type of trigger
        "VSO": [["AgentVSOOb"], 0.4, ["PatientVSOOb"], 0.2, ["CircumstantialVSO"], 0.2, ["InstrumentVSO"], 0.2],
        "VS": [["AgentVSO", "DirN"], 1],
        # Agent formation
        "AgentVSOOb": [["AgentVSO"], 0.7, ["AgentVSO", "OblN"], 0.3],
        "AgentVSO": [["Vagent", "DirN", "AccN"], 0.7, ],
        # Patient formation
        "PatientVSOOb": [["PatientVSO"], 0.7, ["PatientVSO", "OblN"], 0.3],
        "PatientVSO": [["Vpatient", "ErgN", "DirN"], 0.7, ],
        # Circumstantial formation
        "CircumstantialVSO": [["Vcircum", "ErgN", "DirN", "AccN"], 1],
        # Instrumental formation
        "InstrumentVSO": [["Vinstr", "ErgN", "DirN", "AccN"], 1],
        # Now go through and mark the particles
        "MarkedOblN": [["Oblparticle", "NOM"], 0.7, ["PRON"], 0.3],
        "MarkedDirN": [["Dirparticle", "NOM"], 0.7, ["DIRPRON"], 0.3],
        "MarkedAccN": [["Accparticle", "NOM"], 0.7, ["PRON"], 0.3],
        "MarkedErgN": [["Ergparticle", "NOM"], 0.7, ["PRON"], 0.3],
        # Name or noun?
        "NOM": [["PreAdjPremarkedNoun"], 0.9, ["Name"], 0.1],
        # Adjectives
        "PreAdjPremarkedNoun": [["PremarkedNoun"], 0.7, ["adj", "linker", "PremarkedNoun"], 0.3]
    })

    # Set independent probabilistic rules, e.g. pluralization, past tense
    mylang.set_unconditioned_rules({
        # Mark everything with a hash
        "OblN": [["MarkedOblN"], "__hash__", 1],
        "DirN": [["MarkedDirN"], "__hash__", 1],
        "AccN": [["MarkedAccN"], "__hash__", 1],
        "ErgN": [["MarkedErgN"], "__hash__", 1],
        # Nouns and names take different properties
        "PremarkedNoun": [["Noun"], "general.nouny", 1],
        "Name": [["name"], "personal.def.nouny.sg", 1],
        # Verbs with different purposes
        "Vagent": [["verb"], "agentinfl", 1],
        "Vpatient": [["verb"], "patientinfl", 1],
        "Vcircum": [["verb"], "circuminfl", 1],
        "Vinstr": [["verb"], "instrinfl", 1],
        # Types of particle
        "Oblparticle": [["particle"], "oblique", 1],
        "Dirparticle": [["particle"], "direct", 1],
        "Accparticle": [["particle"], "indirect", 1],
        "Ergparticle": [["particle"], "indirect", 1],  # ergative and accusative look the same
        # "sNP": [["UnmarkedNP"], "nom", 1],  # Subject NPs take the nominative
        # "UnmarkedNP": [["NP"], "__hash__.nouny", 1],  # We want to make sure that words in the same NP can agree
        "Noun": [["NUMnoun"], "sg", 0.8, "pl", 0.2],  # Nouns may be singular or plural
        "NUMnoun": [["noun"], "def", 0.8, "indef", 0.2],  # Nouns may be definite or indefinite
        # "Untensedverb": [["verb"], "prs", 0.8, "pst", 0.2],  # Verbs can take tense
        # # Go through to get a fully specified pronoun
        # "PRON": [["PERpron"], "1st", 0.2, "2nd", 0.1, "3rd", 0.7],  # Get the person of the pronoun
        # "PERpron": [["NUMpron"], "sg", 0.7, "pl", 0.3],  # Get the number
        # "NUMpron": [["REGISTERpron"], "pol", 0.7, "fam", 0.3],  # Get the register (polite, familiar)
        # "REGISTERpron": [["pron"], "masc", 0.25, "fem", 0.25, "neut", 0.5]  # Get the gender
        "DIRPRON": [["PRON"], "dir", 1],  # Some pronouns can be direct
        "PRON": [["pron"], "1sg", 0.15, "2sg", 0.1, "3sg", 0.25,
                 "1plincl", 0.10, "1plexcl", 0.10, "2pl", 0.05, "3pl", 0.25]
    })

    # Set the agreement rules
    mylang.set_agreement_rules({
        # "verb": [["nom", "nouny"], [["sg", "pl"], ["1st", "2nd", "3rd"]]],  # Verbs agree with nominative nouns
        # # Determiners agree with their head nouns in number, gender, and definiteness
        "particle": [["nouny", "__hash__"], [["sg", "pl"], ["def", "indef"], ["general", "personal"]]],
        # "adj": [["noun", "__hash__"], [["sg", "pl"], ["common", "neuter"], ["def", "indef"]]],
    })

    # Set the dictionary
    mylang.set_dictionary(cebuano_dict)

    # Set an inflection paradigm for pronoun
    mylang.set_inflection_paradigms([
        ['particle', {
            # We mark plurality here
            # Direct General
            ("direct", "sg", "def", "general"): "-ang",
            ("direct", "sg", "indef", "general"): "-ing",
            ("direct", "pl", "def", "general"): "-ang mga",
            ("direct", "pl", "indef", "general"): "-ing mga",
            # Direct Personal
            ("direct", "sg", "personal"): "-si",  # no definiteness distinction
            ("direct", "pl", "personal"): "-silá ni",  # no definiteness distinction
            # Indirect Personal
            ("indirect", "sg", "personal"): "-ni",  # no definiteness distinction
            ("indirect", "pl", "personal"): "-nilá ni",  # no definiteness distinction
            # Oblique Personal
            ("oblique", "sg", "personal"): "-kang",  # no definiteness distinction
            ("oblique", "pl", "personal"): "-ila ni",  # no definiteness distinction
            # Non-direct General
            ("*direct", "sg", "def", "general"): "-sa",
            ("*direct", "sg", "indef", "general"): "-og",
            ("*direct", "pl", "def", "general"): "-sa mga",
            ("*direct", "pl", "indef", "general"): "-og mga",
        }],
        ['verb', {
            "agentinfl": "mo-",
            "patientinfl": "-on",
            "circuminfl": "-an",
            "instrinfl": "i-"
        }],
        ["pron", {
            # We only use the full forms
            ("direct", "1sg"): "-akó",
            ("direct", "1plincl"): "-kamí",
            ("direct", "1plexcl"): "-kitá",
            ("direct", "2sg"): "-ikáw",
            ("direct", "2pl"): "-kamó",
            ("direct", "3sg"): "-siyá",
            ("direct", "3pl"): "-silá",
            # I'm really not sure this is how it works tbh, but I don't have time to fix it
            ("*direct", "1sg"): "-kanakò",
            ("*direct", "1plincl"): "-kanamò",
            ("*direct", "1plexcl"): "-kanatò",
            ("*direct", "2sg"): "-kanimo",
            ("*direct", "2pl"): "-kaninyo",
            ("*direct", "3sg"): "-kaniya",
            ("*direct", "3pl"): "-kanila",
        }],
    ])

    # Save the language
    mylang.dump_language(os.path.join("synthetic_datasets", language_name))

    # Make num_train and num_test integers
    num_train = int(num_train)
    # num_train should be a power of 10 and that it's at least 10 sentences
    assert math.log10(num_train) % 1 == 0 and num_train >= 10

    # We start by generating many sentences
    sentences, sequences = mylang.generate_sentences(num_sentences=num_train, required_words=None,
                                                     sampling_method="uniform", regenerate_exception_sentences=True)

    # Save these now
    for num_train_group in range(1, int(math.log10(num_train)) + 1):
        language.save_sentences(sentences=sentences[:10 ** (num_train_group + 1)],
                                filepath=os.path.join("synthetic_datasets",
                                                      language_name,
                                                      f"{10 ** (num_train_group + 1)}_train_sentences.txt"))


# =====================================GENERALLY HELPFUL METHODS========================================================

# I'm not deleting this, but we don't need to use it
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
                    overlapping_properties = list(set(check_for_properties) & set(lexical_item[1]))
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
    parts_of_speech = ["noun", "verb", "adj", "prep", "det", "name"]
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
    # generate_frisian_data(num_train=1000)
    # generate_occitan_data(num_train=1000)
    generate_cebuano_data(num_train=1000)
