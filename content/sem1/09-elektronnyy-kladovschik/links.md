# Ссылки занятия 09 «Электронный кладовщик»

## Теория (исходники курса — `prepared/`, раздел `11-basic_applications`)

- `prepared/course-02-learn-prompting/lectures/11-basic_applications/writing_emails/writing_emails.md` — письма-ответы: тон, структура, объём (база слайдов 4, 5 — два письма-ответа ХимСнабу и СодаТресту).
- `prepared/course-02-learn-prompting/lectures/11-basic_applications/summarize/summarize.md` — сводки и чек-листы: как сжать инструкцию в чек-лист п.1.1–1.6 (база слайда 7).
- `prepared/course-02-learn-prompting/lectures/11-basic_applications/table_generation/table_generation.md` — структурирование сырого текста в таблицу (база слайда 6 — накладная простынёй + заказ из системы → сверочная таблица, контраст с pandas в з.11–12).
- `prepared/course-02-learn-prompting/lectures/11-basic_applications/introduction/introduction.md` — вводная по прикладным применениям.

## Практика (исходники курса — `prepared/`, раздел `assignments/applied_prompting`)

- `prepared/course-02-learn-prompting/assignments/applied_prompting/build_chatbot_from_kb.md` — документы в промпте: роль + START CONTEXT/END CONTEXT + задача → ответ по документам (база слайдов 7 и 12 — кладовщик по инструкции, заказ + накладная + инструкция). Контраст с RAG занятия 5 (много доков через вектора) — здесь три коротких документа целиком.
- `prepared/course-02-learn-prompting/assignments/applied_prompting/build_chatgpt.md` — как устроен чат-бот: промпт с историей диалога, формат «User:/Chatbot:» (дополнительно, для понимания контекста).
- `prepared/course-02-learn-prompting/assignments/applied_prompting/short_response.md` — короткие ответы и развёртывание по шагам (дополнительно к слайду 6).

## Связь с другими занятиями завода

- Занятие 05 «Поиск по архивам: по смыслу, а не по словам» — RAG на много документов (эмбеддинги, топ-3 чанка) vs занятие 09 — три коротких документа в промпте (инструкция, заказ, накладная влезают в окно). Вместе — два режима работы с документами.
- Занятия 11–12 «Разбираем архив / Сводки и учёт» — там таблицы уже готовые и их считает код pandas; здесь сверочную таблицу из бумаг (заказ + накладная) собирает LLM. Дополняют друг друга, не дублируют.

## Документация и инструменты

- https://openrouter.ai/collections/free-models — каталог бесплатных моделей OpenRouter (проверяем перед запуском, что `nvidia/nemotron-3-super-120b-a12b:free` ещё бесплатный и не снят).
- https://openrouter.ai/docs — документация OpenRouter API (вызов моделей из кода, ключ в `.env`).
- https://opencode.ai/docs/ — документация opencode (установка, первый запуск — см. доп. инфо `opencode-ustanovka` из занятий 05–06).

## Оригинальные лекции Learn Prompting (по желанию)

- https://learnprompting.org/docs/basic_applications/writing_emails — письма.
- https://learnprompting.org/docs/basic_applications/summarizing — сводки.
- https://learnprompting.org/docs/basic_applications/table_generation — таблицы.
- https://learnprompting.org/docs/applied_prompting/build_chatbot_from_kb — документы в промпте (как кладовщик).
- https://learnprompting.org/docs/applied_prompting/build_chatgpt — как собрать свой ChatGPT.
- https://github.com/trigaten/Learn_Prompting — репозиторий Learn Prompting (русский перевод — в `prepared/`).
