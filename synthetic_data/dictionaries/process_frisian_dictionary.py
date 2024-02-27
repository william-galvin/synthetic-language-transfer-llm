

def main():
    # TODO
    # Please take the file called raw_frisian_dictionary.txt and process it
    # https://github.com/ukn-ubi/frysk/blob/master/frysk-english.txt
    # Here's the file
    # The output should be a json file that looks as follows:
    """
    {
        "verb": [
            "foo", "bar", "baz", ...
        ],
        "noun": [
            {
                "fem": [
                    "femnoun1", "femnoun2", ...
                ],
                "masc": [
                    "mascnoun1", "mascnoun2", ...
                ]
            }
        ],
        "adj": [...],
        "adv": [...]
    }
    """
    # The inflectional paradigms will map each lexeme to a series of inflections
    """
    {
        'word1': {
            'Ger.verb': 'foo',
            'Past.verb': 'bar', 
            'Present.verb': 'baz'
        }, 
        'word2': {
            'singular.noun': 'example',
            'plural.noun': 'examples'
        }
    }
    """
    # For example, for
    # wyfke	wyfke	[Islemma.yes Number.Sing, Pos.NOUN]	true	true	vifkə
    # ûnderskriuwe	ûnderskreauste	[Person.2 Number.Sing Tense.Past, Pos.VERB]	true	false	undrskrøˑsə
    # We would get something like this:
    """
        {
        'wyfke': {
            'sg.noun': 'wyfke',
            'pl.noun': 'wyfken'
        }, 
        'ûnderskriuwe': {
            '2nd.sg.pst.verb': 'ûnderskreauste',
        }
    }
    """


if __name__ == "__main__":
    main()

