# Ссылки занятия 06 «Этикетки и кнопки»

## Теория (исходники курса — `prepared/`)

- `prepared/course-01-generative-ai/lectures/09-building-image-applications.md` — приложения для
  генерации изображений: промпты, размер, температура, мета-промты (база слайдов 2–6).
- `prepared/course-01-generative-ai/lectures/11-integrating-with-function-calling.md` — интеграция
  с внешними инструментами (в лекции — function calling): tools, описание инструмента, цикл вызова,
  токены и приватность (база слайдов 7–11, 14–15).
- `prepared/course-01-generative-ai/assignments/09-building-image-applications/` — практика по лекции 09
  (генерация изображений по промптам).
- `prepared/course-01-generative-ai/assignments/11-integrating-with-function-calling/` — практика
  по лекции 11 (вызов инструментов через API).

## Документация и инструменты

- https://openrouter.ai/collections/free-models — каталог бесплатных моделей OpenRouter (проверяем
  перед запуском, что слог `:free` ещё бесплатный; не все бесплатные модели поддерживают tools —
  сверяемся при сборке практики).
- https://openrouter.ai/docs — документация OpenRouter API (вызов моделей из кода, ключ в `.env`,
  function calling).
- https://openrouter.ai/docs/features/structured-outputs — structured outputs и tools (как передавать
  модели описание инструмента).
- https://opencode.ai/docs/ — документация opencode (установка, первый запуск — см. доп. инфо
  `opencode-ustanovka`).

## Генерация изображений (лекция 09)

- https://en.wikipedia.org/wiki/Diffusion_model — диффузионные модели (как устроена генерация
  изображений; в ролике показываем упрощение «шум → картинка»).
- https://www.assemblyai.com/blog/an-introduction-to-diffusion-models-for-machine-learning/ — введение
  в диффузионные модели по-человечески.
- https://huggingface.co/docs/diffusers/index — библиотека Diffusers (примеры генерации изображений
  из кода, бесплатные открытые модели).

## Function calling (лекция 11)

- https://platform.openai.com/docs/guides/function-calling — гайд по вызову инструментов (общий принцип:
  описание инструмента, решение модели, выполнение программой, ответ модели).
- https://en.wikipedia.org/wiki/Function_calling — обзор (для быстрого введения в тему).

## Этикетки (слайд 15)

- https://pollinations.ai/ — бесплатный публичный API генерации изображений без ключа (проверить,
  что жив на момент запуска; при необходимости подобрать альтернативу).
