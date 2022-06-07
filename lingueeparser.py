#!/usr/bin/env python3

import requests
import csv


def linguee(word):
    api_root = "https://linguee-api-v2.herokuapp.com/api/v2"
    params = {"query": word, "src": "de", "dst": "en"}
    translations = requests.get(f"{api_root}/translations", params= params)
    external_sources = requests.get(f"{api_root}/external_sources", params= params)


    json = translations.json()

    # print(json)
    if not json or type(json) is dict:
        new_trans = ""
        examples = ""
    else:
        trans_rows = [trans_row for lemma in json for trans_row in lemma['translations']]

        new_trans = "\n".join([row['text'] for row in trans_rows])
        examples = "\n".join([f"{ex['src']} -> {ex['dst']}" for row in trans_rows for ex in row['examples']])

    json = external_sources.json()


    if not json or type(json) is dict:
        external_examples = ""
    else:
        external_examples = "\n".join([f"{row['src']} -> {row['dst']}"  for row in external_sources.json()][:5])

    # print(new_trans, examples)

    return new_trans, examples + external_examples

# Verb,Präposition,Fall,Quelle,Beispielsatz,Extra,auf Englisch

linguee("danken für")
linguee("fürchten um")
linguee("riechen nach")

new_lines = []
with open('feste-präpositionen.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile)
    def add_linguee(row):
        verb, prep, case, source, example, extra, eng = row

        if not verb:
            return row
        print(f"Doing verb {verb} {prep}")

        new_trans, examples = linguee(f"{verb} {prep}")


        print(f"got examples {examples}")

        return [verb, prep, case, source, example + examples, extra, eng + new_trans]





    old_lines = list(reader)
    new_lines = [old_lines[0]] + [add_linguee(row) for row in old_lines[1:]]

    print(new_lines)
with open('linguee-prep.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for row in new_lines:
        spamwriter.writerow(row)
