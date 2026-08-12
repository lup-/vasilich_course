#!/usr/bin/env python3
"""Подготовка датасета мемов для поиска.

- читает train-00000-of-00001.parquet
- присваивает стабильные id (m00000, m00001, ...)
- извлекает картинки в images/{id}.jpg
- помечает «грязные» мемы (мат/оскорбления) колонкой is_clean и flag_reason
- сохраняет catalog.parquet (id, path, text, is_clean, flag_reason)

Запуск:  python prepare.py
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import pandas as pd
from PIL import Image

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "train-00000-of-00001.parquet"
CATALOG = HERE / "catalog.parquet"
IMAGES_DIR = HERE / "images"

FLAG_REASONS: list[tuple[str, re.Pattern]] = [
    (
        "мат",
        re.compile(
            r"\b(?:"
            r"бл[яэ]"
            r"|ху[йеяёюи]"
            r"|хер[ноль*аеёи]?"
            r"|пизд"
            r"|залуп"
            r"|шлюх"
            r"|курв"
            r"|гандон"
            r"|член(?!ораздельн)"
            r"|хул[и]"
            r"|проститут"
            r"|[её]б"
            r"|ъ[её]б"
            r"|за[её]б|на[её]б|вы[её]б|у[её]б|до[её]б|про[её]б"
            r"|объ[её]б|отъ[её]б|подъ[её]б|разъ[её]б|съ[её]б"
            r"|долбо[её]б|оху"
            r"|сру|срёт|засра|насра|обосра|сран|сра[лть]|срака|срач"
            r"|говн"
            r"|муда|мудил|мудозвон"
            r"|выбл"
            r"|твар"
            r"|пидор|пидр|педрил"
            r"|\b(?:"
            r"fuc[kt]ing?|motherfuck(?:er|ing)?|shit|bitch(?:ing|es)?"
            r"|asshole|dick|cunt|bastard|whore|slut|prick|wanker|twat|douche"
            r")\b"
            r")"
        ),
    ),
    (
        "оскорбление",
        re.compile(r"\b(?:дебил|даун|чмо|лох|придурок|идиот|тупо[йаы])"),
    ),
    (
        "национализм",
        re.compile(r"\b(?:жидо|чурк|хач|нигг|черномаз|узкоглаз|хохо[л])"),
    ),
]


def normalize_text(raw: str) -> str:
    return re.sub(r"\s+", " ", raw).strip()


def classify(text: str) -> tuple[bool, str]:
    reasons = [name for name, pat in FLAG_REASONS if pat.search(text)]
    return (not reasons, ",".join(reasons))


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.exists():
        print(f"Файл не найден: {source}", file=sys.stderr)
        return 1

    df = pd.read_parquet(source)
    required = {"image", "text"}
    if not required.issubset(df.columns):
        print(f"Ожидались колонки {required}, есть: {list(df.columns)}", file=sys.stderr)
        return 1

    df = df.drop_duplicates(subset="text").reset_index(drop=True)
    df["text"] = df["text"].fillna("").map(normalize_text)
    df = df[df["text"].str.len() >= 20].reset_index(drop=True)

    df["id"] = [f"m{i:05d}" for i in range(len(df))]
    df["path"] = "images/" + df["id"] + ".jpg"
    df["text_len"] = df["text"].str.len()

    clean_flags = df["text"].str.lower().map(lambda s: classify(s))
    df["is_clean"] = clean_flags.str[0]
    df["flag_reason"] = clean_flags.str[1]

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    bad = 0
    for row in df.itertuples(index=False):
        try:
            img = Image.open(io.BytesIO(row.image["bytes"]))
            if img.format not in ("JPEG", "PNG", "WEBP"):
                raise ValueError(f"неожиданный формат {img.format}")
            img.convert("RGB").save(IMAGES_DIR / f"{row.id}.jpg", "JPEG", quality=90)
        except Exception as exc:  # noqa: BLE001
            bad += 1
            print(f"Ошибка картинки {row.id}: {exc}", file=sys.stderr)

    out = df[["id", "path", "text", "text_len", "is_clean", "flag_reason"]]
    out.to_parquet(CATALOG, index=False)

    clean_n = int(out["is_clean"].sum())
    print(f"Мемов после подготовки: {len(out)} (чистых: {clean_n}, с флагом: {len(out) - clean_n})")
    print(f"Ошибок картинок: {bad}")
    print(f"Каталог: {CATALOG}")
    print(f"Картинки: {IMAGES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
