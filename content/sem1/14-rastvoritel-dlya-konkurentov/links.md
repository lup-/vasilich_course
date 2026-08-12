# Ссылки занятия 14 «Растворитель для конкурентов»

## Теория (исходники курса — `prepared/`)

- `prepared/course-04-work-with-data/lectures/07-web-apis.md` — Веб-API: запросы, JSON, статусы, ключи (база слайдов 3–4).
- `prepared/course-04-work-with-data/lectures/08-pdf-extraction.md` — Извлечение текста и таблиц из PDF: PyMuPDF (база слайда 7).
- `prepared/course-04-work-with-data/assignments/04-api/` — задание 04 «Данные из API» (`task.md` + `assignment.ipynb`).
- `prepared/course-04-work-with-data/assignments/05-pdf/` — задание 05 «Извлечение данных из PDF» (`task.md` + `assignment.ipynb`).
- `prepared/course-05-chemistry-ai/lectures/06-pubchem-api.md` — PubChem PUG REST как «источник правды» (база слайда 5).

## Веб-API

- Библиотека requests для Python: https://requests.readthedocs.io/
- Open-Meteo — погода бесплатно, без ключа (пример лекции 07): https://open-meteo.com
- ExchangeRate API — курсы валют без ключа: https://www.exchangerate-api.com

## PubChem (химическая база)

- PubChem — поиск веществ: https://pubchem.ncbi.nlm.nih.gov/
- Документация PUG REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- Пример запроса (свойства по названию):
  https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/acetone/property/MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey/JSON

## Научные API

- CrossRef — реестр DOI и цитирований, REST API: https://api.crossref.org/
  - Гайд по REST API CrossRef: https://www.crossref.org/documentation/rest-api/
- OpenAlex — открытая база публикаций: https://openalex.org/
  - Документация OpenAlex API: https://docs.openalex.org/

## PDF (PyMuPDF)

- PyMuPDF — документация: https://pymupdf.readthedocs.io/en/latest/
- PyMuPDF4LLM (PDF → Markdown для ИИ): https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html
- Рецепты извлечения текста: https://pymupdf.readthedocs.io/en/latest/recipes-text.html

## Практика через агента

- opencode — локальный ИИ-агент (описываешь задачу словами, агент пишет и запускает код):
  https://opencode.ai/docs/ (установка и настройка — [в доп. инфо](@opencode-ustanovka))
- Каталог бесплатных моделей OpenRouter (проверяем перед запуском, что слог `:free` ещё бесплатный):
  https://openrouter.ai/collections/free-models
