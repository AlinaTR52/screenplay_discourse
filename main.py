import os
from pathlib import Path
from pdf_parser import extract_text
from text_cleaner import clean_text
from pos_tagger import process, to_lemma_text, to_tagged_text

UPLOAD = Path("upload")
ANTCONC = Path("for_antconc")
TAGGED = Path("tagged")


def run():
    os.makedirs(ANTCONC, exist_ok=True)
    os.makedirs(TAGGED, exist_ok=True)

    files = sorted(UPLOAD.glob("*.pdf"))
    if not files:
        print("Нет pdf файлов в upload/")
        return

    print(f"Файлов: {len(files)}\n")

    all_lemmas = []

    for f in files:
        print(f"[{f.name}]")
        raw = extract_text(f)
        cleaned = clean_text(raw)
        tagged = process(cleaned)

        lemma_text = to_lemma_text(tagged)
        all_lemmas.append(lemma_text)

        antconc_out = ANTCONC / f.with_suffix(".txt").name
        antconc_out.write_text(lemma_text, encoding="utf-8")

        tagged_out = TAGGED / f.with_suffix(".txt").name
        tagged_out.write_text(to_tagged_text(tagged), encoding="utf-8")

        print(f"  -> {antconc_out}")
        print(f"  -> {tagged_out} ({len(tagged)} токенов)\n")

    combined = ANTCONC / "corpus_all.txt"
    combined.write_text("\n".join(all_lemmas), encoding="utf-8")
    print(f"Общий корпус: {combined}")
    print("Готово")


if __name__ == "__main__":
    run()
