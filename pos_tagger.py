import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def tokenize(text):
    return re.findall(r"[а-яёА-ЯЁ]+-?[а-яёА-ЯЁ]*", text)


def process(text):
    tokens = tokenize(text)
    result = []
    for w in tokens:
        p = morph.parse(w)[0]
        tag = str(p.tag).replace(" ", "-").replace(",", "-")
        result.append((w, p.normal_form, tag))
    return result


def to_lemma_text(tagged):
    return " ".join(lemma for _, lemma, _ in tagged)


def to_tagged_text(tagged):
    return " ".join(f"{word}-{lemma}-{pos}" for word, lemma, pos in tagged)
