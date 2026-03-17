import xml.etree.ElementTree as ET
from pathlib import Path

xml_path = Path("assets/annot.opcorpora.xml")
out_lemmas = Path("assets/annot.opcorpora_lemmas.txt")
out_tagged = Path("assets/annot.opcorpora_tagged.txt")


def tag_name(e):
    t = e.tag
    return t.split("}")[-1] if "}" in t else t


def parse_token(tok):
    w = tok.get("text", "")
    lemma = w
    grams = []
    for node in tok.iter():
        if tag_name(node) != "l":
            continue
        lemma = node.get("t", w)
        for g in node.iter():
            if tag_name(g) == "g":
                grams.append(g.get("v", ""))
        break
    if grams and grams[0] == "PNCT":
        return None
    tag = "-".join(grams) if grams else "UNKN"
    return lemma, f"{w}-{lemma}-{tag}"


if __name__ == "__main__":
    if not xml_path.exists():
        print("файл не найден:", xml_path)
        raise SystemExit(1)

    lemmas = []
    tagged = []

    for _, elem in ET.iterparse(xml_path, events=("end",)):
        if tag_name(elem) != "sentence":
            continue
        sl, st = [], []
        for node in elem.iter():
            if tag_name(node) != "token":
                continue
            res = parse_token(node)
            if res:
                l, t = res
                sl.append(l)
                st.append(t)
        if sl:
            lemmas.append(" ".join(sl))
            tagged.append(" ".join(st))
        elem.clear()

    out_lemmas.write_text("\n".join(lemmas), encoding="utf-8")
    out_tagged.write_text("\n".join(tagged), encoding="utf-8")
    n = sum(len(s.split()) for s in tagged)
    print("предложений:", len(lemmas), "токенов:", n)
    print(out_lemmas, out_tagged)
