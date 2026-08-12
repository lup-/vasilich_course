#!/usr/bin/env python3
"""Расчёт эмбеддингов описаний мемов.

Читает catalog.parquet, эмбеддит колонку text локальной мультиязычной
моделью fastembed и сохраняет embeddings.npy + embeddings-meta.json.

Запуск:  python embed.py
"""

from __future__ import annotations

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
OUT_EMB = HERE / "embeddings.npy"
OUT_META = HERE / "embeddings-meta.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main() -> int:
    if not CATALOG.exists():
        print("Сначала запусти prepare.py (нет catalog.parquet)", file=sys.stderr)
        return 1

    df = pd.read_parquet(CATALOG)
    model = TextEmbedding(model_name=MODEL_NAME)
    vectors = np.asarray(
        list(model.embed(df["text"].tolist(), batch_size=64)), dtype=np.float32
    )
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    np.save(OUT_EMB, vectors)
    OUT_META.write_text(
        json.dumps(
            {"model": MODEL_NAME, "dim": int(vectors.shape[1]), "count": int(vectors.shape[0])},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Эмбеддинги: {OUT_EMB} {vectors.shape}")
    print(f"Мета: {OUT_META}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
