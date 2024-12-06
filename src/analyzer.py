"""Python file to lemmatize the raw data.
"""

"""Script to lemmatize every text file.
Odycy is the selected parser and should be downloaded before hand.
"""
from pathlib import Path
import json
import spacy
from loguru import logger

nlp = spacy.load("grc_odycy_joint_trf")



replace_dict = {
    "μεθ'": "μετά",
    "μεθ’": "μετά",
    "μεθ´": "μετά",
    "μεθ᾽": "μετά",
    "κατ'": "κατά",
    "κατ’": "κατά",
    "κατ´": "κατά",
    "κατ᾽": "κατά",
    "καθ'": "κατά",
    "καθ’": "κατά",
    "καθ´": "κατά",
    "καθ᾽": "κατά",
    "παρ'": "παρά",
    "παρ’": "παρά",
    "παρ´": "παρά",
    "παρ᾽": "παρά",
    "ὑπ'": "ὑπό",
    "ὑπ’": "ὑπό",
    "ὑπ´": "ὑπό",
    "ὑπ᾽": "ὑπό",
    "ὑπʼ": "ὑπό",
    "ἵν'": "ἵνα",
    "ἵν’": "ἵνα",
    "ἵν´": "ἵνα",
    "ἵν᾽": "ἵνα",
    "ἀλλ'": "άλλὰ",
    "ἀλλ’": "άλλὰ",
    "ἀλλ´": "άλλὰ",
    "ἀλλ᾽": "άλλὰ",
    "δι'": "διὰ",
    "δι’": "διὰ",
    "δι´": "διὰ",
    "δι᾽": "διὰ",
    "ἀντ'": "ἀντί",
    "ἀντ’": "ἀντί",
    "ἀντ´": "ἀντί",
    "ἀντ᾽": "ἀντί",
    "ἀνθ'": "ἀντί",
    "ἀνθ’": "ἀντί",
    "ἀνθ´": "ἀντί",
    "ἀνθ᾽": "ἀντί",
    "ἐπ'": "ἐπί",
    "ἐπ’": "ἐπί",
    "ἐπ´": "ἐπί",
    "ἐπ᾽": "ἐπί",
    "ἐφ'": "ἐπί",
    "ἐφ’": "ἐπί",
    "ἐφ´": "ἐπί",
    "ἐφ᾽": "ἐπί"
}


def analyze(text_dict: dict[str, str]):
    """Analyze the content within the dictionary using GreCy"""
    lemmatized_dict = {}
    for chapter, content in text_dict.items():
        lemmatized_dict[chapter] = []
        doc = nlp(content)
        for token in doc:
            if token.text.lower() in replace_dict:
                # token.is_stop, token.pos_, token.morph, token.dep_, token.head
                lemmatized_dict[chapter].append({"lemma": replace_dict[token.text.lower()],
                                                 "raw": token.text,
                                                 "is_stop": token.is_stop,
                                                 "pos": token.pos_,
                                                 "morph": token.morph.to_dict(),
                                                 "dep": token.dep_,
                                                 "head": token.head.text})
            else:
                lemmatized_dict[chapter].append({"lemma": token.lemma_, 
                                                 "raw": token.text,
                                                 "is_stop": token.is_stop,
                                                 "pos": token.pos_,
                                                 "morph": token.morph.to_dict(),
                                                 "dep": token.dep_,
                                                 "head": token.head.text})
    return lemmatized_dict


if __name__ == "__main__":
    for file in Path("../data").rglob("*/*.json"):
        if "lemmatized" in str(file.parent):
            continue
        with open(file, "r") as f:
            text = json.load(f)
        logger.info(f"Lemmatizing {file}")
        lemmatized_text = analyze(text)
        with open(f"../data/lemmatized/{str(file.parent).split('/')[-1]}/{file.name}", "w") as f:
            json.dump(lemmatized_text, f, indent=4, ensure_ascii=False)