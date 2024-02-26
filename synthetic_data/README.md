# README

README.md, language.py, and generator.py are all copied from https://github.com/Alessioryan/SyntheticLanguageDataGenerator on Feb 25, 2024. 

When using the generator, you need to define the following parameters for the language:
```python
# 1. CREATE A LANGUAGE BASE. 
import language
# Create/load a base language
mylang = language.Language()

# 2. IF YOU'RE GENERATING WORDS, TODO (WE'RE NOT DOING THIS FOR NOW)

# 3. SET THE PARTS OF SPEECH FOR YOUR LANGUAGE
# Set the parts of speech of the language
parts_of_speech = ["noun", "verb", "adj", "prep", "det"]
mylang.set_parts_of_speech(parts_of_speech=parts_of_speech)

# 4. SET THE GENERATION RULES
mylang.set_generation_rules({
    # The left side describes the initial state. All sentences start generating from the "S" state.    
    # Set sentence generation rules according to CFGs
    # The format of a rule is "A": [["B", "C*p", "..."], x, ["D"], y, ...]
    #   A is the input state
    #   B, C, ... are the outputs states
    #       C*p means that the property p will be removed from C
    #   x is the probability of the rule taking place
    #   D is another output state that takes place with probability y
    # An example is "S": [["sN", "VP"], 1]
    #   This means sentence goes to subject noun and verb phrase with probability 1
    # Another example is "VP": [["verb", "oN"], 0.7, ["verb"], 0.3]
    #   This means verb phrases take an object noun with probability 0.7
    # The probabilities must sum to 1, but this isn't checked
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

# 5. SET THE UNCONDITIONED RULES
# Set independent probabilistic rules, e.g. pluralization, past tense
# These rules are non-branching and simply add a feature to the state
mylang.set_unconditioned_rules({
    # Sets sentence generation rules for individual words that are not conditioned by other words
    # The format of a rule is "A": [["a"], "p1", x, "p2", y, ...]
    #   A is the input state
    #   a is the output state, it must be wrapped in a list
    #   x is the probability of a having property p1, y is the probability of having property p2
    # An example is "sN": [["noun"], "sing", 0.8, "pl", 0.2]
    #   This means that subject nouns map to nouns, with the feature singular with probability 0.8 and plural with 0.2
    "sNP": [["UnmarkedNP"], "nom", 1],  # Subject NPs take the nominative
    "UnmarkedNP": [["NP"], "__hash__.nouny", 1],  # We want to make sure that words in the same NP can agree
    "N": [["noun"], "sg", 0.8, "pl", 0.2],  # Nouns may be singular or plural
})

# 6. SET THE AGREEMENT RULES
# These rules 
mylang.set_agreement_rules({
    # Sets the agreement rules for words with a property or terminal
    # The format of a rule is "t": [["p1", "p2", ...], [["q1", "q2", ...], ["r1", ...], ...]]
    #   t is the property or terminal that takes the agreement affixes
    #   p1, p2, ... are the agreement properties that a word that t agrees with must have to trigger agreement
    #       There must be exactly one word with ALL the properties that are needed to trigger agreement
    #       Otherwise, an error is raised
    #   ["q1", "q2", ...] is a set of properties that determine feature q
    #       The word that satisfies the agreement properties must have exactly one of the features in q
    #       Otherwise, an error is raised
    #   ["r1", ...], ... are other sets of properties that determine other features
    # An example is "verb": [["nom", "noun"], [["sg", "pl"], ["1st", "2nd", "3rd"]]]
    #   This means that verbs must agree with a word that has the property nominative and noun
    #   Then, the verb agrees with that word, taking either the property singular or plural, and 1st, 2nd, or 3rd
    # The agreement rules don't dictate the inflections, just what words agree with what
    # FOR NOW, WORDS CAN ONLY AGREE WITH ONE OTHER WORD. POTENTIALLY CHANGE THIS LATER.
    "verb": [["nom", "nouny"], [["sg", "pl"], ["1st", "2nd", "3rd"]]],  # Verbs agree with nominative nouns
    "det": [["noun", "__hash__"], [["sg", "pl"]]]  # Determiners agree with their head nouns
})

# 7. IMPORT THE LEXICON
# TODO

# 8. SET THE INFLECTION PARADIGM
mylang.set_inflection_paradigms([
    # Define an inflection pattern for a given paradigm
    # The format of a rule is ["w", {("p1", "p2", ...): "-s1", ("q1", ...): "-s2", ...}]
    #   w is the property of the word that triggers a check for whether this word inflects for this rule
    #   ("p1", "p2", ...) is a tuple of properties that result in inflection being triggered
    #       There must be exactly one tuple that triggers inflection for a given word
    #       Otherwise, an error is raised
    #   -s1 is a suffix that is appended to the word if the properties that trigger inflection are met
    #       Prefixes (pref-) and circumfixes (cir-cum) are also supported
    #   ("q1", ...): "-s2" is another tuple of properties that triggers inflection with suffix "-s2"
    # If we call ["w", {("p1", "p2", ...): "-s1", ("q1", ...): "-s2", ...}] R1, the format of the input is [R1, R2, ...]
    #   The rules apply in order
    #   If you're adding a single inflection paradigm, wrap the rule in a list
    # An example for one rule is ["noun", {"sg": "-", "pl": "-ol"}]
    #   For this rule, we see that nouns must agree with either singular of plural. If they agree with none or both,
    #       an error is thrown
    #   Whichever feature it agrees with results in that suffix getting added. The singular is unmarked while the
    #       plural takes the suffix "-ol"
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

# 9. SAVE THE LANGUAGE
# Save the language
import os
mylang.dump_language(os.path.join("Languages", "example_language") )
```
