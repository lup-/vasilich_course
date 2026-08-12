# Ссылки занятия 02. «Что у неё внутри»

## Лекции курса-01 (основной источник теории)

- Введение в генеративный ИИ и LLM — `prepared/course-01-generative-ai/lectures/01-introduction-to-genai.md`
  (токенизация, предсказание следующего токена, температура, «Проверка знаний»)
  - Видео-версия (оригинал Microsoft): https://youtu.be/lFXQkBvEe0o
- Изучение и сравнение различных LLM — `prepared/course-01-generative-ai/lectures/02-exploring-and-comparing-different-llms.md`
  (ландшафт моделей: размер, цена, контекст, открытые vs проприетарные; выбор модели под задачу)
  - Видео-версия (оригинал Microsoft): https://youtu.be/KIRUeDKscfI

## «Заглянуть внутрь»: интерактивные инструменты

Ссылки здесь — запасной вариант: tiktokenizer и TokenProbe встроены в занятие прямо в embed-слайдах 5 и 9.
Работают в браузере, без установки.

- **tiktokenizer** — токенизатор вживую: вставь текст, увидишь, как он разбивается на токены и какие
  у них ID. Выбирая шаблон `gpt-4o`, увидишь служебные токены `<|im_start|>`, `<|im_sep|>`, `<|im_end|>`
  (embed-слайд 5; упоминается в слайде 7):
  https://tiktokenizer.vercel.app
- **TokenProbe** (Колумбийский университет) — как модель «читает» текст токен за токеном: вероятности
  на каждом шаге, альтернативные токены, настройки температуры и top-k
  (embed-слайд 9; упоминается в слайде 8):
  https://tokenprobe.cs.columbia.edu
- **LLM Visualization** (bbycroft) — вся «начинка» модели: эмбеддинги токенов, слои внимания, выбор
  следующего токена по вероятностям (слайд 8, ссылка):
  https://bbycroft.net/llm
- **How LLMs Work — Visual Deep Dive** (по лекции Карпати) — большой наглядный разбор: данные →
  токенизация (BPE) → обучение → инференс и сэмплинг → постобучение (SFT, RLHF) → формат разговора
  со служебными токенами (`Conversation Token Format`):
  https://ynarwal.github.io/how-llms-work/

## Сравнение и выбор моделей

- **OpenRouter** — агрегатор моделей, удобен для сравнения маленьких и больших моделей на одной задаче
  (см. занятие 1): https://openrouter.ai
- **OpenRouter — бесплатные модели** (каталог, что сейчас бесплатно и не снято): 
  https://openrouter.ai/collections/free-models
- **Hugging Face** — каталог открытых моделей: https://huggingface.co/models

## Репозиторий курса-01 (исходник)

- https://github.com/microsoft/generative-ai-for-beginners

## Ролик занятия

- Программа-сценарий Manim-ролика «Токенизация: текст в числа» — `videos/manim/03-tokenizaciya.py`
  (запуск и описание — `videos/README.md`).
