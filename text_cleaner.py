import re

# паттерны для очистки сценарного текста
PATTERNS = [
    (r"^\s*\d+\s*$", ""),                          # номера страниц
    (r"^\s*(\d+[.)]\s*|[-•●▪]\s*)", ""),            # списки
    (r"\(.*?\)", ""),                                # ремарки в скобках
    (r"^\s*(INT\.|EXT\.|ИНТ\.|НАТ\.|ИНТЕРЬЕР|ЭКСТЕРЬЕР|НАПЛЫВ|ЗАТЕМНЕНИЕ|ТИТР).*$", ""),
    (r"^\s*[A-ZА-ЯЁ]{2,}[\s.]*$", ""),             # имена персонажей
]


def clean_text(raw):
    text = raw
    for pattern, repl in PATTERNS:
        flags = re.MULTILINE | re.IGNORECASE if "INT" in pattern else re.MULTILINE
        text = re.sub(pattern, repl, text, flags=flags)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
