# Ссылки занятия 05 «Поиск по архивам»

## Теория (исходники курса — `prepared/`)

- `prepared/course-01-generative-ai/lectures/08-building-search-applications.md` — поисковые приложения:
  семантический поиск, текстовые эмбеддинги, индекс эмбеддингов, косинусное сходство (база слайдов 2–4).
- `prepared/course-01-generative-ai/lectures/15-rag-and-vector-databases.md` — RAG и векторные базы:
  база знаний, чанки, извлечение, расширенная генерация, зачем RAG (база слайдов 8–10).
- `prepared/course-01-generative-ai/assignments/08-building-search-applications/` — практика по лекции 08:
  `oai-solution.ipynb` / `oai-assignment.ipynb` (семантический поиск по индексу эмбеддингов).
- `prepared/course-01-generative-ai/assignments/15-rag-and-vector-databases/` — практика по лекции 15:
  `notebook-rag-vector-databases.ipynb` (создание базы знаний → эмбеддинги → извлечение → сборка ответа).

## Документация и инструменты

- https://openrouter.ai/collections/free-models — каталог бесплатных моделей OpenRouter (проверяем
  перед запуском, что слог `:free` ещё бесплатный). Эмбеддинг-моделей на OpenRouter нет — эмбеддинги
  считаем локально.
- https://www.sbert.net/ — документация `sentence-transformers` (локальные эмбеддинги, без ключей).
- https://huggingface.co/intfloat/multilingual-e5-small — модель эмбеддингов `intfloat/multilingual-e5-small`
  (бесплатная, локальная, поддерживает русский; ~470 МБ при первом запуске).
- https://scikit-learn.org/stable/modules/neighbors.html — `sklearn.neighbors.NearestNeighbors`
  (поиск ближайших соседей для индекса).
- https://en.wikipedia.org/wiki/Cosine_similarity — косинусное сходство (метрика близости векторов).
- https://openrouter.ai/docs — документация OpenRouter API (вызов моделей из кода, ключ в `.env`).

## RAG (лекция 15)

- https://arxiv.org/abs/2005.11401 — оригинальная статья RAG «Retrieval-Augmented Generation
  for Knowledge-Intensive NLP Tasks».
- https://en.wikipedia.org/wiki/Retrieval-augmented_generation — обзор RAG (схема, применение).

## Готовые RAG-сервисы по документам (слайд 10)

> Перед использованием проверяем, что ссылки живые и бесплатные тарифы на месте.

- https://notebook.google.com — NotebookLM (Google): «блокнот» с источниками, ответ с цитатами-ссылками,
  бесплатный тариф, звуковой обзор документов.
- https://github.com/Open-Notebook/Open-Notebook — Open Notebook: сервис с открытым исходным кодом
  (можно пользоваться как готовым или поставить себе и запускать локально).
- https://www.chatpdf.com — ChatPDF: разбор одного PDF (статья, договор).
