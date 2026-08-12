# 06. PubChem: база соединений и её API

> Семестр: 2 · Курс: «Химия и ИИ» (course-05) · Время: ~2–3 часа

## Введение

**PubChem** — крупнейшая бесплатная база данных о химических соединениях (под управлением NCBI/NIH). В ней — миллионы веществ: структуры, свойства, названия, ссылки на статьи. Это «Википедия молекул» + «API для автоматизации».

Для нас PubChem — главный источник правды: когда агент «что-то придумывает», мы сверяемся с PubChem. А когда нужно много данных — берём их оттуда автоматически через **PUG REST API**.

<!-- изображение (не скопировано): страница соединения в PubChem: структура, свойства, идентификаторы -->

## Как найти вещество на сайте

1. Откройте https://pubchem.ncbi.nlm.nih.gov/
2. Введите название (например, «aspirin»).
3. На странице соединения вы увидите:
   - структурную формулу;
   - брутто-формулу и массу;
   - InChI, SMILES, IUPAC-имя;
   - физико-химические свойства;
   - ссылки на литературу и связанные вещества.

Это ручной способ. Для автоматизации — API.

## PUG REST API: данные по ссылке

PUG REST — простой интерфейс: данные получаются прямо по URL. Формат:

```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/<домен>/<идентификатор>/<операция>/<выход>
```

Примеры (проверены):

**SMILES по названию:**
```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/CanonicalSMILES/TXT
→ CC(=O)OC1=CC=CC=C1C(=O)O
```

**Идентификатор (CID) по названию:**
```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/cids/TXT
→ 2244
```

**Свойства по CID (в JSON):**
```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula,MolecularWeight/JSON
```

Ключевые элементы URL:
- `name/aspirin` — ищем по названию;
- `cid/2244` — работаем по числовому ID;
- `property/MolecularFormula,MolecularWeight` — какие свойства;
- `/TXT` или `/JSON` — формат ответа.

## Получение данных из Python

```python
import requests

url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/CanonicalSMILES,InChI,InChIKey,MolecularFormula,MolecularWeight/JSON"
resp = requests.get(url)
data = resp.json()

props = data["PropertyTable"]["Properties"][0]
print(props["CanonicalSMILES"])
print(props["MolecularFormula"], props["MolecularWeight"])
print(props["InChIKey"])   # компактный «паспорт» молекулы
```

Как и в курсе-04, всё сводится к: запрос → JSON → таблица/использование.

## Превращаем ответ в таблицу для нескольких веществ

```python
import requests
import pandas as pd

compounds = ["aspirin", "ibuprofen", "paracetamol", "caffeine", "ethanol"]

rows = []
for name in compounds:
    url = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}"
           f"/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON")
    try:
        resp = requests.get(url)
        props = resp.json()["PropertyTable"]["Properties"][0]
        rows.append({"name": name, **props})
    except Exception as e:
        print("Ошибка для", name, e)

df = pd.DataFrame(rows)
df
```

Теперь у нас таблица: название, формула, масса, SMILES — всё из официального источника. Можно сортировать, фильтровать, рисовать графики (курс-04) и передавать в RDKit (курс-05).

## CID и InChIKey: зачем

- **CID** (PubChem CID) — числовой ID соединения: стабилен, удобен для ссылок и запросов.
- **InChIKey** — короткий (27 символов) «отпечаток» молекулы: если InChIKey совпадает — это одно и то же вещество. Удобно для дедупликации баз.

При работе лучше оперировать CID или InChIKey, а не названием: названия бывают синонимами, и одно название может соответствовать разным соединениям.

## Практика: проверка «придуманной» молекулы

Самый важный приём курса:

1. Агент назвал вещество или SMILES — вы не уверены.
2. Попросите агента (или сами) запросить PubChem по названию.
3. Сравните SMILES/свойства из PubChem с тем, что дал агент.

Запрос для агента:

> «Проверь по PubChem: каков официальный SMILES аспирина? Сравни с моим `CC(=O)OC1=CC=CC=C1C(=O)O`. Если совпадает — подтверди, если нет — покажи правильный. Также проверь молекулярную массу.»

## Частые проблемы

| Проблема | Решение |
|---|---|
| `404` — «такого нет» | Ошибка в названии; попробовать CID или поискать на сайте |
| `HTTPError 400` | Некорректный URL/параметры; проверить формат |
| Медленный ответ на много веществ | Добавить паузу между запросами, ограничить список |
| Одно название → несколько веществ | Уточнить, какой CID нужен; показать первые результаты |
| Русское название | PubChem понимает многие языки, но надёжнее английское имя |

## Задание на дом

1. Через API получите для 5 веществ: формулу, массу, SMILES, InChIKey. Соберите таблицу.
2. Проверьте: совпадают ли массы из PubChem с теми, что вы считали RDKit в задании лекции 04?
3. Для одного вещества получите данные по CID (найдите CID сначала по названию).
4. Попросите агента проверить SMILES аспирина из PubChem против вашего — совпадает ли.
5. Сохраните ноутбук.

## Проверка знаний

- Что такое PubChem и почему он считается «источником правды»?
- Что такое CID и InChIKey?
- Из каких частей состоит URL PUG REST API?
- Как получить SMILES по названию вещества?
- Как проверить, что агент «не придумал» молекулу?

## Продолжайте обучение

- PubChem: https://pubchem.ncbi.nlm.nih.gov/
- Документация PUG REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- TeachOpenCADD, талкториал T013 (данные из PubChem): https://github.com/volkamerlab/teachopencadd
