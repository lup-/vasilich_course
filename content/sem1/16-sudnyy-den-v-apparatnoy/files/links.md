# Ссылки и источники занятия 16

> Внешние ресурсы и материалы курса. Реальные и проверенные на момент сборки.

## Научные и веб-API (живые данные)

- PubChem PUG REST — идентификация веществ (формула, масса, SMILES):
  https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- Конкретные вещества из протокола (снапшоты лежат в `files/dannye/`):
  - Ацетон, CID 180 — https://pubchem.ncbi.nlm.nih.gov/compound/180
  - Этилацетат, CID 8857 — https://pubchem.ncbi.nlm.nih.gov/compound/8857
  - Ксилол, CID 7235 — https://pubchem.ncbi.nlm.nih.gov/compound/7235
- CrossRef REST API (поиск публикаций) — https://api.crossref.org/
- OpenAlex (научная графомания) — https://docs.openalex.org/

## Работа с данными (Python)

- pandas — https://pandas.pydata.org/docs/
- openpyxl (чтение/запись Excel) — https://openpyxl.readthedocs.io/
- ReportLab (генерация PDF) — https://docs.reportlab.com/
- PyMuPDF (извлечение текста/таблиц из PDF) — https://pymupdf.readthedocs.io/
- Matplotlib / Plotly (графики для дирекции) — https://matplotlib.org/, https://plotly.com/python/

## Безопасность и защита

- Занятие 10 «Словесные хакеры» (памятка-защита) — `../10-slovesnye-hakery/`
- OWASP: Prompt Injection — https://owasp.org/www-community/attacks/Prompt_Injection
- Курс-02, `defensive_measures`: инструкция-защита, метки, пост-проверка

## Материалы курса

- Курс-04, лекция 12 (финальный проект, экономика/оценка) — `prepared/course-04-work-with-data/lectures/12-final-project.md`
- Задание 06 (итоговый проект) — `prepared/course-04-work-with-data/assignments/06-final-project/task.md`
- План занятий — `plan-zanyatiy.md` (занятие 16)
- База доп-чтения — `content/sem1/extra/` (особ. `slovesnye-hakery`, `kachestvo-dannyh`, `razbor-arhiva`, `opencode-ustanovka`)

## Приватность

- Ключи API — только в `.env`, не в код и не в чат (см. занятие 14, `14-rastvoritel-dlya-konkurentov`).
- Бесплатные снапшоты в `files/dannye/` уже не требуют ключей — можно учиться офлайн.
