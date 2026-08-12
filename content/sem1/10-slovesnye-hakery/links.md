# Ссылки занятия 10 «Словесные хакеры»

## Теория (исходники курса — `prepared/`, раздел `50-prompt_hacking`)

- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/intro/intro.md` —
  введение в prompt hacking: три вида (инъекция, утечка промпта, джейлбрейк) + оборона (база слайдов 2–5).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/injection/injection.md` —
  prompt injection: чужой текст в промпте перехватывает вывод; первый пример — бот remoteli.io
  (база слайда 3).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/offensive_measures/indirect_injection/indirect_injection.md` —
  непрямая инъекция: чужой приказ через сторонний источник (веб-поиск, сайт, документ) (база слайда 4).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/jailbreaking/jailbreaking.md` —
  джейлбрейки: pretending, ролевые игры, «sudo mode», DAN (база слайда 5).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/leaking/leaking.md` —
  утечка промпта: просим модель выдать собственные инструкции; пример с Bing Chat «Sydney» (база слайда 5).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/offensive_measures/overview/overview.md` —
  обзор способов доставки атаки (обфускация, split payload, словарь, виртуализация) (дополнительно).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/defensive_measures/instruction/instruction.md` —
  инструкция-защита (база слайда 7).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/defensive_measures/post_prompting/post_prompting.md` —
  пост-промптинг: правило в конец промпта (база слайда 7).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/defensive_measures/xml_tagging/xml_tagging.md` —
  отделение данных метками (XML-теги) (база слайда 7).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/defensive_measures/sandwich_defense/sandwich_defense.md` —
  «сэндвич»: инструкция до и после данных (база слайда 7).
- `prepared/course-02-learn-prompting/lectures/50-prompt_hacking/defensive_measures/overview/overview.md` —
  обзор обороны (дополнительно).
- `prepared/course-01-generative-ai/lectures/13-securing-ai-applications.md` —
  безопасность ИИ-приложений: OWASP LLM Top-10 (дополнительно к слайдам 3–9).

## Практика и инструменты

- **Игра «Continue? Y/N» (слайд 12, `embed`):** https://llmgame.scalex.dev/ — 60 секунд, игрок —
  человек-контролёр ИИ-агента: разрешает (`1`) или запрещает (`2`) команды, ловит опасные. По статистике
  автора игроки пропускают ~1 из 3 опасных команд, к концу сессии усталость растёт. Запасная ссылка на
  случай блокировки iframe. Разбор и статистика автора:
  https://scalex.dev/blog/ai-agent-permissions/ (первоисточник для слайда 12 и доп. инфо).
- https://openrouter.ai/collections/free-models — каталог бесплатных моделей OpenRouter (проверяем перед
  запуском, что `openai/gpt-oss-20b:free` и `nvidia/nemotron-3-super-120b-a12b:free` ещё бесплатные и не сняты).
- https://openrouter.ai/docs — документация OpenRouter API (вызов моделей из кода, ключ в `.env`).
- https://jailbreakchat.com — коллекция известных джейлбрейк-промптов (упоминается в лекции `injection`;
  смотрим как примеры, не применяем).

## Реальные случаи (блок «Реальные случаи» в [словесные хакеры](@slovesnye-hakery))

**Группа А. Словесные атаки на ИИ**

- Чат-бот автосалона Chevrolet of Watsonville «продал» 2024 Chevy Tahoe за $1 (декабрь 2023) — прямая
  инъекция; Chris Bakke уговорил ChatGPT-бот договориться о продаже. Вирусный пример того, как просто
  «развести» не защищённый чат-бот:
  - https://gmauthority.com/blog/2023/12/gm-dealer-chat-bot-agrees-to-sell-2024-chevy-tahoe-for-1/ (GM Authority, новость)
  - https://cybermaniacs.com/news/chevrolet-chatbot-incident-the-1-tahoe-problem (разбор + FAQ про prompt injection)
- Bing Chat «Sydney» раскрыл свой системный промпт (февраль 2023) — утечка промпта; пользователи
  вытащили скрытое имя, правила и ограничения чат-бота:
  - https://github.com/Jiggyboy99/ai-threat-analyses/tree/main/01-bing-chat-sydney-prompt-injection (разбор)
- Скрытый текст на страницах управляет веб-агентами (2024 — наст. время) — непрямая инъекция:
  спрятанная на сайте инструкция заставила ИИ-агента выполнить действие (вплоть до покупки набора Lego);
  к 2026 это уже боевые кампании — страницы-ловушки переводят криптовалюту злоумышленникам:
  - https://www.hcs.harvard.edu/~hcs/blog/2024/11/20/its-a-trap-ai-agents-and-the-risk-of-prompt-injections/ (Harvard HCS, разбор)
  - https://www.preposterousuniverse.com/blog/2024/03/06/read-the-small-print-hidden-text-can-manipulate-ai-agents/ (обзор; оригинал — Financial Times)

**Группа Б. Агенты, которые сами пошли не туда**

- Claude Code: утечка учёток между сессиями, агент по SSH изменил чужую продакшн-базу (июнь 2026) —
  в контекст сессии попали чужие root-учётки, агент сам подключился к чужому хосту и выполнил миграцию
  базы `tk_dist` (GitHub Issue #72274, метка `area:security`):
  - https://github.com/anthropics/claude-code/issues/72274
- Агент ROME (Alibaba/Qwen, февраль 2026) — во время RL-обучения агент самовольно сканировал внутренние
  системы, открывал reverse-SSH-туннели на внешние IP и майнил криптовалюту на GPU — без команд человека:
  - https://www.forbes.com/sites/boazsobrado/2026/03/11/alibabas-ai-agent-mined-crypto-without-permission-now-what/
- PocketOS: агент Cursor стёр продакшн-базу за 9 секунд и «признался» (апрель 2026) — агент на рутинной
  задаче сам решил «починить» staging, удалил продакшн-том и бэкапы одним запросом к Railway API;
  потом перечислил в письменном виде правила, которые нарушил:
  - https://x.com/lifeofjer/status/2048103471019434248 (X, разбор основателя PocketOS)
  - https://zenity.io/blog/current-events/ai-agent-database-deletion-pocketos (разбор)
  - https://benjaminhan.net/posts/20260427-cursor-railway-production-wipe/ (разбор)

## Приватность

- Секреты (API-ключи, пароли) — только в `.env`, не в промпты и не в чат (сквозная тема курса; слайд 9).
  Правило применимо и к учебному коду, и к системным промптам персонажей.
