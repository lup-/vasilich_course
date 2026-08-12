# 11. Автоматизация химических процессов

> Семестр: 2 · Курс: «Химия и ИИ» (course-05) · Время: ~2 часа

## Введение

Рутинные задачи — сбор данных, проверка наборов, отчёты — можно выполнять без ручного труда. В этой лекции объединяем всё из курса-04 (автоматизация, файлы, API) и курса-05 (RDKit, PubChem): строим конвейер «сырые данные → чистый набор → отчёт».

<!-- изображение (не скопировано): конвейер: файл → парсинг → проверка → обогащение из PubChem → таблица/отчёт -->

## Идея: конвейер данных в химии

Типичный рабочий процесс аналитика-хемоинформатика:

```
вход (список названий / SMILES / CSV / SDF)
   → нормализация (канонические SMILES)
   → проверка (RDKit, PAINS, Липински)
   → обогащение (свойства из RDKit + данные из PubChem)
   → сохранение (CSV/SDF) и отчёт
```

Каждый шаг — маленькая функция. Задача агента — собрать их в один скрипт, который обрабатывает весь набор без вмешательства.

## Собираем функции

```python
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def parse_and_validate(smiles_list):
    """Читаем SMILES, отбрасываем невалидные, возвращаем канонические."""
    valid = []
    for s in smiles_list:
        m = Chem.MolFromSmiles(s)
        if m is not None:
            valid.append(Chem.MolToSmiles(m))
    return valid

def add_properties(df, smiles_col="canonical_smiles"):
    """Считаем дескрипторы для каждой строки."""
    rows = []
    for s in df[smiles_col]:
        m = Chem.MolFromSmiles(s)
        rows.append({
            "MolWt": Descriptors.MolWt(m),
            "MolLogP": Descriptors.MolLogP(m),
            "TPSA": Descriptors.TPSA(m),
            "HBD": Descriptors.NumHDonors(m),
            "HBA": Descriptors.NumHAcceptors(m),
        })
    return df.join(pd.DataFrame(rows))

def lipinski_status(df):
    """Добавляем колонку о прохождении правила Липински."""
    ok = ((df["MolWt"] <= 500) & (df["MolLogP"] <= 5)
          & (df["HBD"] <= 5) & (df["HBA"] <= 10))
    df["lipinski_ok"] = ok
    return df
```

Итоговый скрипт — это последовательность:

```python
data = parse_and_validate(названия_или_smiles)
df = pd.DataFrame({"canonical_smiles": data})
df = add_properties(df)
df = lipinski_status(df)
df.to_csv("results.csv", index=False)
```

## Обогащение из PubChem: одна функция

```python
import requests
import time

def fetch_pubchem(smiles):
    """Возвращаем CID и InChIKey из PubChem по каноническому SMILES."""
    url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/"
           f"{smiles}/property/InChIKey/JSON")
    try:
        r = requests.get(url, timeout=15)
        if r.ok:
            p = r.json()["PropertyTable"]["Properties"][0]
            return p["CID"], p["InChIKey"]
    except Exception:
        pass
    return None, None

# для каждого SMILES
# cid, key = fetch_pubchem(s) ; time.sleep(0.3)  # вежливая пауза
```

Внимание: при большом количестве запросов делайте паузы и обрабатывайте ошибки (это API, а не локальный расчёт).

## Автоматический отчёт

Финальный шаг — отчёт, который можно показать коллеге:

```python
print("Всего молекул:", len(df))
print("Прошло Липински:", df["lipinski_ok"].sum())
print(df.groupby("lipinski_ok").agg({"MolWt": "mean", "MolLogP": "mean"}))
df["lipinski_ok"].value_counts().plot.bar()
```

Или сохранить таблицу в файл, который откроется в Excel (курс-04):

```python
df.to_excel("report.xlsx", index=False)
```

## Роль агента и ваша роль

Агент пишет код по вашему заданию, вы проверяете результат. Хорошее задание:

> «Собери скрипт-конвейер: на вход — CSV с колонкой SMILES. 1) Отбрось невалидные, 2) добавь дескрипторы, 3) добавь колонку “проходит Липински”, 4) для каждой молекулы получи CID и InChIKey из PubChem, 5) сохрани результат в results.csv и нарисуй гистограмму масс. Покажи код и объясни каждый шаг.»

Проверьте: не «завис» ли скрипт на ошибке, все ли колонки на месте, разумны ли числа.

## Что автоматизировать, а что нет

**Автоматизировать стоит** — повторяемые расчёты, стандартные проверки, сбор данных, формирование отчётов.

**Автоматизировать не стоит** — интерпретацию результатов и принятие решений: они всегда за человеком. Автоматизация ускоряет, но не заменяет экспертизу.

## Частые проблемы

| Проблема | Решение |
|---|---|
| Скрипт падает на одной строке | Обработка ошибок `try/except`, лог пропущенных |
| PubChem отвечает медленно | Паузы, таймауты, пакетные запросы |
| Результат «не бьётся» с ожиданием | Проверить промежуточные шаги: печатать количество на каждом этапе |
| Пустой файл на выходе | Проверить ввод: не пустой ли список, все ли SMILES валидны |
| Итоговые числа «слишком красивые» | Перепроверить через второй источник (курс-10) |

## Задание на дом

1. Соберите мини-конвейер: 10 молекул → очистка → дескрипторы → Липински → сохранение в results.csv.
2. Обогатите 3 молекулы данными PubChem (CID, InChIKey) в той же таблице.
3. Сделайте гистограмму масс и столбчатую диаграмму «прошло/не прошло Липински».
4. Сохраните итоговый отчёт в xlsx.
5. Пометьте в отчёте: какие значения — расчёты, а какие — факты из PubChem.

## Проверка знаний

- Назовите 5 шагов конвейера химических данных.
- Зачем нормализовывать SMILES перед анализом?
- Как вежливо работать с публичным API при массовой загрузке?
- Почему интерпретацию результатов не стоит автоматизировать?
- Что нужно проверить, если скрипт выдал «слишком красивые» числа?

## Продолжайте обучение

- PubChem PUG REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- Курс-04, лекция об автоматизации (n8n)
- TeachOpenCADD: https://github.com/volkamerlab/teachopencadd
