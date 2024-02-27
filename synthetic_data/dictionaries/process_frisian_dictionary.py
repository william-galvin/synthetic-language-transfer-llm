

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


if __name__ == "__main__":
    main()

