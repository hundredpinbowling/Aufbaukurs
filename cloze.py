#!/usr/bin/env python3


import re
with open(r'deck.json', 'r') as file:

    # Reading the content of the file
    # using the read() function and storing
    # them in a new variable
    data = file.read()

    # cards = re.finditer(r"fields\": \[(.*)\]", data)
    regex = re.compile(r"\"fields\": \[(.*?)\]", re.MULTILINE | re.DOTALL)
    cards = re.finditer(regex, data)
    for card in cards:
        # print(card)
        fields = card.group(1).split(",")
        if len(fields) == 6:
            main_sentence = fields[0]
            verb = main_sentence.split(" ")[-1]
            if "<" in verb:
                verb = verb[:verb.index("<")]
            if "\"" in verb:
                verb = verb[:verb.index("\"")]

            if verb != "":

                replaced_sentence = main_sentence.replace(verb, "___")

                fields[5] = replaced_sentence

                new_substring = ",".join(fields)
                new_substring = f"\"fields\": [{new_substring}\n]"
                data = data.replace(card.group(0), new_substring)

                # print(verb)
                # print(replaced_sentence)


    with open(r'deck2.json', 'w') as file:

        # Writing the replaced data in our
        # text file
        file.write(data)
