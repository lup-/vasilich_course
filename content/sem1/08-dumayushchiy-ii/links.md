# Ссылки занятия 08 «Думающий ИИ»

## Теория (исходники курса — `prepared/`, раздел `15-intermediate`)

- `prepared/course-02-learn-prompting/lectures/15-intermediate/chain_of_thought/chain_of_thought.md` —
  Chain of Thought: примеры с расписанным решением (база слайдов 2, 3, 4, 5).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/zero_shot_cot/zero_shot_cot.md` —
  Zero-shot CoT: фраза «подумай шаг за шагом» (база слайдов 6, 7, 8).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/least_to_most/least_to_most.md` —
  Least-to-Most: разбиение на подзадачи (база слайда 9).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/self_consistency/self_consistency.md` —
  Self-Consistency: несколько прогонов, большинство (база слайдов 10, 11).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/long_form_content/long_form_content.md` —
  работа с длинным текстом: сжать, разбить, собрать (база слайда 12).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/generated_knowledge/generated_knowledge.md` —
  сгенерированное знание: сначала факты, потом ответ (дополнительно; упоминается в доп. инфо).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/revisiting_roles/revisiting_roles.md` —
  роли в современных моделях (дополнительно).
- `prepared/course-02-learn-prompting/lectures/15-intermediate/whats_in_a_prompt/whats_in_a_prompt.md` —
  формат примеров в промпте (дополнительно к CoT-примерам).

## Документация и инструменты

- https://openrouter.ai/collections/free-models — каталог бесплатных моделей OpenRouter (проверяем
  перед запуском, что `nvidia/nemotron-3-super-120b-a12b:free` ещё бесплатный и не снят).
- https://openrouter.ai/docs — документация OpenRouter API (вызов моделей из кода, ключ в `.env`).
- https://opencode.ai/docs/ — документация opencode (установка, первый запуск — см. доп. инфо
  `opencode-ustanovka` из занятий 05–06).

## Оригинальные лекции Learn Prompting (по желанию)

- https://learnprompting.org/docs/intermediate/chain_of_thought — Chain of Thought.
- https://learnprompting.org/docs/intermediate/zero_shot_chain_of_thought — Zero-shot CoT.
- https://learnprompting.org/docs/intermediate/least_to_most — Least-to-Most.
- https://learnprompting.org/docs/intermediate/self_consistency — Self-Consistency.
- https://learnprompting.org/docs/intermediate/dealing_with_long_form_content — длинные тексты.
- https://github.com/trigaten/Learn_Prompting — репозиторий Learn Prompting (русский перевод — в `prepared/`).

## Статьи (оригинальные работы)

- Wei J. et al. «Chain-of-Thought Prompting Elicits Reasoning in Large Language Models» (2022) —
  https://arxiv.org/abs/2201.11903 — CoT.
- Kojima T. et al. «Large Language Models are Zero-Shot Reasoners» (2022) —
  https://arxiv.org/abs/2205.11916 — zero-shot CoT.
- Wang X. et al. «Self-Consistency Improves Chain of Thought Reasoning in Language Models» (2022) —
  https://arxiv.org/abs/2203.11171 — self-consistency.
- Zhou D. et al. «Least-to-Most Prompting Enables Complex Reasoning in Large Language Models» (2022) —
  https://arxiv.org/abs/2205.10625 — least-to-most.
