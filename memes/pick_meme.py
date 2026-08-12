#!/usr/bin/env python3
"""Поиск мемов под контент по смыслу (векторный поиск по описаниям).

Пример:
    memes/pick_meme "не доверяй ИИ без проверки результата"
    memes/pick_meme "API-ключи в .env, приватность" --top 10
    memes/pick_meme "кот не хочет работать" --all --json

По умолчанию показывает только «чистые» мемы (is_clean=True).
--all включает помеченные (мат/оскорбления) — для ручного просмотра,
в контент курса их брать нельзя.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from fastembed import TextEmbedding

warnings.filterwarnings(
    "ignore", message=".*now uses mean pooling.*", category=UserWarning
)

HERE = Path(__file__).resolve().parent
CATALOG = HERE / "catalog.parquet"
EMBEDDINGS = HERE / "embeddings.npy"
META = HERE / "embeddings-meta.json"


def load_index() -> tuple[pd.DataFrame, np.ndarray, str]:
    if not CATALOG.exists() or not EMBEDDINGS.exists():
        print("Нет catalog.parquet/embeddings.npy — запусти prepare.py и embed.py", file=sys.stderr)
        raise SystemExit(1)
    df = pd.read_parquet(CATALOG)
    vec = np.load(EMBEDDINGS)
    model = META.read_text(encoding="utf-8")
    model = json.loads(model)["model"] if META.exists() else None
    if len(df) != vec.shape[0]:
        print("Каталог и эмбеддинги не совпадают по числу строк — перезапусти embed.py", file=sys.stderr)
        raise SystemExit(1)
    return df, vec, model or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main() -> int:
    ap = argparse.ArgumentParser(description="Подбор мемов под контент")
    ap.add_argument("query", help="что нужно проиллюстрировать (тема, настроение, контекст)")
    ap.add_argument("--top", type=int, default=5, help="сколько кандидатов вернуть (по умолчанию 5)")
    ap.add_argument("--all", action="store_true", help="включить мемы с флагом мата/оскорблений")
    ap.add_argument("--min-score", type=float, default=0.0, help="отсечка по косинусной близости (0..1)")
    ap.add_argument("--json", action="store_true", help="вывести результат в JSON (для агента)")
    args = ap.parse_args()

    df, vec, model = load_index()
    text_model = TextEmbedding(model_name=model)
    q = np.asarray(list(text_model.embed([args.query])), dtype=np.float32)[0]
    q = q / np.linalg.norm(q)

    scores = vec @ q
    df = df.assign(score=scores)
    if not args.all:
        df = df[df["is_clean"]]
    df = df[df["score"] >= args.min_score]
    top = df.sort_values("score", ascending=False).head(args.top)

    if top.empty:
        print("Ничего не нашлось — попробуй смягчить запрос или --all.")
        return 0

    if args.json:
        payload = [
            {
                "id": r.id,
                "score": round(float(r.score), 3),
                "is_clean": bool(r.is_clean),
                "path": r.path,
                "text": r.text,
            }
            for r in top.itertuples(index=False)
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f'Под запрос: "{args.query}"  (модель: {model})\n')
    for i, r in enumerate(top.itertuples(index=False), 1):
        badge = "" if r.is_clean else f" [флаг: {r.flag_reason}]"
        print(f"[{i}] {r.id}  score={r.score:.3f}  {r.path}{badge}")
        print(f"    {r.text}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
