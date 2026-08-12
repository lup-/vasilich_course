# Начало работы с этим курсом

Мы очень рады, что вы начинаете этот курс и увидите, что вас вдохновит создать с помощью Генеративного ИИ!

Чтобы обеспечить ваш успех, на этой странице описаны шаги по настройке, технические требования и где можно получить помощь при необходимости.

## Шаги по настройке

Чтобы начать обучение на этом курсе, вам нужно выполнить следующие шаги.

### 1. Форкните этот репозиторий

[Сделайте форк всего репозитория](https://github.com/microsoft/generative-ai-for-beginners/fork?WT.mc_id=academic-105485-koreyst) в свой собственный аккаунт GitHub, чтобы иметь возможность изменять любой код и выполнять задания. Вы также можете [поставить звезду (🌟) этому репозиторию](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars?WT.mc_id=academic-105485-koreyst), чтобы проще было его находить и находить связанные репозитории.

### 2. Создайте codespace

Чтобы избежать проблем с зависимостями при запуске кода, мы рекомендуем запускать этот курс в [GitHub Codespaces](https://github.com/features/codespaces?WT.mc_id=academic-105485-koreyst).

В своём форке: **Code -> Codespaces -> New on main**

<!-- изображение (не скопировано): Диалоговое окно с кнопками для создания codespace -->

#### 2.1 Добавьте секрет

1. ⚙️ Иконка шестерёнки -> Command Pallete-> Codespaces : Управление пользовательскими секретами -> Добавить новый секрет.
2. Имя OPENAI_API_KEY, вставьте свой ключ, Сохранить.

### 3. Что дальше?

| Я хочу…             | Перейти к…                                                              |
|---------------------|-------------------------------------------------------------------------|
| Начать урок 1       | [`01-introduction-to-genai`](../01-introduction-to-genai/README.md)     |
| Работать оффлайн    | [`setup-local.md`](02-setup-local.md)                                   |
| Настроить провайдера LLM | [`providers.md`](03-providers.md)                                        |
| Познакомиться с другими учащимися | [Присоединиться к нашему Discord](https://aka.ms/genai-discord?WT.mc_id=academic-105485-koreyst)   |

## Устранение неполадок


| Симптом                                   | Решение                                                        |
|-------------------------------------------|-----------------------------------------------------------------|
| Сборка контейнера зависла > 10 мин       | **Codespaces ➜ «Пересобрать контейнер»**                      |
| `python: command not found`               | Терминал не прикрепился; нажмите **+** ➜ *bash*                |
| `401 Unauthorized` от OpenAI              | Неправильный / просроченный `OPENAI_API_KEY`                   |
| VS Code показывает «Dev container mounting…» | Обновите вкладку браузера — иногда Codespaces теряет соединение  |
| Отсутствует ядро блокнота                  | Меню блокнота ➜ **Kernel ▸ Выбрать ядро ▸ Python 3**           |

   Unix-подобные системы:

   ```bash
   touch .env
   ```

   Windows:

   ```cmd
   echo . > .env
   ```

3. **Отредактируйте файл `.env`**: Откройте файл `.env` в текстовом редакторе (например, VS Code, Notepad++ или любом другом). Добавьте следующие строки в файл, заменяя заполнители на ваши реальные конечные точки и ключи Microsoft Foundry Models (см. [`providers.md`](03-providers.md) для получения информации, как их получить):

   > **Примечание:** GitHub Models (и переменная `GITHUB_TOKEN`) будет закрыт в конце июля 2026 года. Вместо этого используйте [Microsoft Foundry Models](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst).

   ```env
   AZURE_INFERENCE_ENDPOINT=your_foundry_endpoint_here
   AZURE_INFERENCE_CREDENTIAL=your_foundry_api_key_here
   ```

4. **Сохраните файл**: Сохраните изменения и закройте текстовый редактор.

5. **Установите `python-dotenv`**: Если вы ещё не сделали этого, вам нужно установить пакет `python-dotenv`, чтобы загружать переменные окружения из файла `.env` в ваше Python-приложение. Его можно установить с помощью `pip`:

   ```bash
   pip install python-dotenv
   ```

6. **Загрузите переменные окружения в вашем Python-скрипте**: В вашем Python-скрипте воспользуйтесь пакетом `python-dotenv` для загрузки переменных из файла `.env`:

   ```python
   from dotenv import load_dotenv
   import os

   # Загрузить переменные окружения из файла .env
   load_dotenv()

   # Получить доступ к переменным Microsoft Foundry Models
   endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
   token = os.getenv("AZURE_INFERENCE_CREDENTIAL")

   print(endpoint)
   ```

Вот и всё! Вы успешно создали файл `.env`, добавили туда данные своей учётной записи Microsoft Foundry Models и загрузили их в своё Python-приложение.

## Как запускать локально на вашем компьютере

Для запуска кода локально на вашем компьютере потребуется установленная версия [Python](https://www.python.org/downloads/?WT.mc_id=academic-105485-koreyst).

Чтобы использовать репозиторий, нужно его клонировать:

```shell
git clone https://github.com/microsoft/generative-ai-for-beginners
cd generative-ai-for-beginners
```

Как только все загрузится, вы можете начать работать!

## Дополнительные шаги

### Установка Miniconda

[Miniconda](https://conda.io/en/latest/miniconda.html?WT.mc_id=academic-105485-koreyst) — это лёгкий установщик для установки [Conda](https://docs.conda.io/en/latest?WT.mc_id=academic-105485-koreyst), Python, а также некоторых пакетов.
Сам Conda — это менеджер пакетов, который упрощает настройку и переключение между разными Python [**виртуальными окружениями**](https://docs.python.org/3/tutorial/venv.html?WT.mc_id=academic-105485-koreyst) и пакетами. Также он полезен для установки пакетов, недоступных через `pip`.

Вы можете следовать [руководству установки MiniConda](https://docs.anaconda.com/free/miniconda/#quick-command-line-install?WT.mc_id=academic-105485-koreyst), чтобы настроить её.

После установки Miniconda нужно клонировать [репозиторий](https://github.com/microsoft/generative-ai-for-beginners/fork?WT.mc_id=academic-105485-koreyst) (если вы ещё этого не сделали)

Далее необходимо создать виртуальное окружение. Для этого с помощью Conda создайте новый файл окружения (_environment.yml_). Если вы используете Codespaces, создайте его в директории `.devcontainer`, то есть `.devcontainer/environment.yml`.

Заполните файл окружения следующим фрагментом:

```yml
name: <environment-name>
channels:
  - defaults
  - microsoft
dependencies:
  - python=<python-version>
  - openai
  - python-dotenv
  - pip
  - pip:
      - azure-ai-ml
```

Если у вас возникают ошибки при использовании conda, можно вручную установить Microsoft AI Libraries командой ниже в терминале.

```
conda install -c microsoft azure-ai-ml
```

Файл окружения задаёт необходимые зависимости. `<environment-name>` — имя вашего Conda-окружения, а `<python-version>` — используемая версия Python, например, `3` — последняя мажорная версия Python.

После этого создайте Conda-окружение, выполнив команды ниже в командной строке/терминале

```bash
conda env create --name ai4beg --file .devcontainer/environment.yml # Подпуть .devcontainer применяется только к установкам Codespace
conda activate ai4beg
```

Обратитесь к [руководству по управлению окружениями Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html?WT.mc_id=academic-105485-koreyst), если возникнут проблемы.

### Использование Visual Studio Code с расширением поддержки Python

Для этого курса мы рекомендуем использовать редактор [Visual Studio Code (VS Code)](https://code.visualstudio.com/?WT.mc_id=academic-105485-koreyst) с установленным [расширением поддержки Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python&WT.mc_id=academic-105485-koreyst). Однако это скорее рекомендация, а не обязательное требование.

> **Примечание**: Открыв репозиторий курса в VS Code, вы можете настроить проект внутри контейнера. Это возможно благодаря [специальной директории `.devcontainer`](https://code.visualstudio.com/docs/devcontainers/containers?itemName=ms-python.python&WT.mc_id=academic-105485-koreyst), которая находится в репозитории курса. Подробнее об этом далее.

> **Примечание**: После клонирования и открытия директории в VS Code он автоматически предложит установить расширение Python.

> **Примечание**: Если VS Code предложит открыть репозиторий в контейнере, отклоните запрос, чтобы использовать локально установленную версию Python.

### Использование Jupyter в браузере

Вы также можете работать над проектом через [среду Jupyter](https://jupyter.org?WT.mc_id=academic-105485-koreyst) прямо в браузере. И классический Jupyter, и [Jupyter Hub](https://jupyter.org/hub?WT.mc_id=academic-105485-koreyst) предоставляют удобную среду разработки с такими функциями, как автозаполнение, подсветка кода и так далее.

Чтобы запустить Jupyter локально, откройте терминал/командную строку, перейдите в папку с курсом и выполните:

```bash
jupyter notebook
```

или

```bash
jupyterhub
```

Это запустит экземпляр Jupyter, и URL для доступа к нему будет выведен в командной строке.

По переходу по ссылке вы увидите план курса и сможете открыть любой файл с расширением `*.ipynb`. Например `08-building-search-applications/python/oai-solution.ipynb`.

### Запуск в контейнере

Альтернативой настройке всего локально или на Codespace является использование [контейнера](../../../00-course-setup/<https:/en.wikipedia.org/wiki/Containerization_(computing)?WT.mc_id=academic-105485-koreyst>). Специальная папка `.devcontainer` в репозитории курса позволяет VS Code настроить проект внутри контейнера. За пределами Codespaces это потребует установки Docker и, честно говоря, немного усилий, поэтому мы рекомендуем этот путь только тем, кто уже работал с контейнерами.

Один из лучших способов обезопасить ваши API-ключи при использовании GitHub Codespaces — это использование Secrets в Codespace. Пожалуйста, ознакомьтесь с руководством по [управлению секретами в Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-secrets-for-your-codespaces?WT.mc_id=academic-105485-koreyst).


## Уроки и технические требования

Курс состоит из 6 концептуальных и 6 кодовых уроков.

Для кодовых уроков мы используем Azure OpenAI Service. Вам потребуется доступ к Azure OpenAI Service и API ключ для запуска кода. Вы можете подать заявку на доступ, [заполнив эту форму](https://azure.microsoft.com/products/ai-services/openai-service?WT.mc_id=academic-105485-koreyst).

Пока вы ждёте обработки заявки, в каждом кодовом уроке есть файл `README.md`, где вы можете просмотреть код и результаты.

## Использование Azure OpenAI Service впервые

Если вы впервые работаете с Azure OpenAI Service, пожалуйста, следуйте руководству по [созданию и развертыванию ресурса Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource?pivots=web-portal&WT.mc_id=academic-105485-koreyst)

## Использование OpenAI API впервые

Если вы впервые работаете с OpenAI API, пожалуйста, следуйте руководству по [созданию и использованию интерфейса](https://platform.openai.com/docs/quickstart?context=pythont&WT.mc_id=academic-105485-koreyst)

## Познакомьтесь с другими учащимися

Мы создали каналы в нашем официальном [Discord-сервере AI Community](https://aka.ms/genai-discord?WT.mc_id=academic-105485-koreyst) для общения с другими учащимися. Это отличный способ наладить связи с другими единомышленниками, предпринимателями, разработчиками, студентами и всеми, кто хочет развиваться в Генеративном ИИ.

<!-- изображение (не скопировано): Присоединиться к Discord-каналу (ссылка: https://aka.ms/genai-discord?WT.mc_id=academic-105485-koreyst) -->

Команда проекта также будет на этом Discord-сервере, чтобы помочь всем учащимся.

## Вклад в проект

Этот курс — инициатива с открытым исходным кодом. Если вы заметили области для улучшения или проблемы, пожалуйста, создайте [Pull Request](https://github.com/microsoft/generative-ai-for-beginners/pulls?WT.mc_id=academic-105485-koreyst) или зарегистрируйте [проблему на GitHub](https://github.com/microsoft/generative-ai-for-beginners/issues?WT.mc_id=academic-105485-koreyst).

Команда проекта будет отслеживать все вклады. Внесение вклада в открытое ПО — отличный способ построить карьеру в Генеративном ИИ.

Большинство вкладов требует согласия с Лицензионным соглашением с участником (CLA), в котором вы подтверждаете, что имеете право и фактически предоставляете нам права на использование вашего вклада. Подробнее смотрите на сайте [CLA, Contributor License Agreement](https://cla.microsoft.com?WT.mc_id=academic-105485-koreyst).

Важно: при переводе текста в этом репозитории, пожалуйста, не используйте машинный перевод. Мы будем проверять переводы через сообщество, поэтому участвуйте в переводе только на тех языках, которыми вы владеете профессионально.

При отправке pull request, CLA-бот автоматически определит, нужно ли вам предоставить CLA и отметит PR соответствующим образом (например, ярлыком, комментарием). Просто следуйте инструкциям бота. Это нужно сделать только один раз для всех репозиториев, использующих наш CLA.


Этот проект принял [Кодекс поведения Microsoft с открытым исходным кодом](https://opensource.microsoft.com/codeofconduct/?WT.mc_id=academic-105485-koreyst). Для получения дополнительной информации прочитайте Часто задаваемые вопросы о Кодексе поведения или свяжитесь с [Email opencode](opencode@microsoft.com) для любых дополнительных вопросов или комментариев.

## Давайте начнем

Теперь, когда вы выполнили необходимые шаги для завершения этого курса, давайте начнем с [введения в генеративный ИИ и LLM](../01-introduction-to-genai/README.md?WT.mc_id=academic-105485-koreyst).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->

---

# 01 Setup Cloud

# Облачная настройка ☁️ – GitHub Codespaces

**Используйте это руководство, если вы не хотите ничего устанавливать локально.**  
Codespaces предоставляет бесплатный экземпляр VS Code в браузере со всеми предустановленными зависимостями.

---

## 1.  Зачем нужен Codespaces?

| Преимущество | Что это значит для вас |
|-------------|----------------------|
| ✅ Никаких установок | Работает на Chromebook, iPad, школьных ПК… |
| ✅ Преднастроенный контейнер для разработки | Python 3, Node.js, .NET, Java уже внутри |
| ✅ Бесплатный лимит | Личные аккаунты получают **120 ядро-часов / 60 ГБ-часов в месяц** |

> 💡 **Совет**  
> Поддерживайте лимит в пределах, **останавливая** или **удаляя** неактивные codespaces  
> (Просмотр ▸ Command Palette ▸ *Codespaces: Stop Codespace*).

---

## 2.  Создать Codespace (одним кликом)

1. **Форкните** этот репозиторий (кнопка **Fork** вверху справа).  
2. В вашем форке нажмите **Code ▸ Codespaces ▸ Create codespace on main**.  
   <!-- изображение (не скопировано): Диалог с кнопками для создания codespace -->

✅ Откроется окно VS Code в браузере и запустится сборка контейнера для разработки.
Это займет **примерно 2 минуты** при первом запуске.

## 3. Добавьте ваш API-ключ (безопасный способ)

### Вариант A: Секреты Codespaces — Рекомендуется

1. ⚙️ Значок настроек -> Command Palette -> Codespaces : Manage user secret -> Add a new secret.
2. Имя: OPENAI_API_KEY
3. Значение: вставьте ваш ключ → Add secret

Вот и все — наш код автоматически его подхватит.

### Вариант B: файл .env (если он действительно нужен)

```bash
cp .env.copy .env
code .env         # заполните OPENAI_API_KEY=ваш_ключ_здесь
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->

---

# 02 Setup Local

# Локальная настройка 🖥️

**Используйте это руководство, если предпочитаете запускать всё на своём ноутбуке.**   
У вас есть два варианта: **(A) нативный Python + виртуальное окружение** или **(B) VS Code Dev Container с Docker**.  
Выберите любой, какой покажется проще — оба ведут к одним и тем же урокам.

## 1. Требования

| Инструмент           | Версия / Примечания                                                                  |
|----------------------|--------------------------------------------------------------------------------------|
| **Python**           | 3.10+ (скачайте с <https://python.org>)                                              |
| **Git**              | Последняя версия (входит в Xcode / Git для Windows / пакетный менеджер Linux)         |
| **VS Code**          | Опционально, но рекомендуется <https://code.visualstudio.com>                         |
| **Docker Desktop**   | *Только* для варианта B. Бесплатная установка: <https://docs.docker.com/desktop/>     |

> 💡 **Совет** – Проверьте инструменты в терминале:  
> `python --version`, `git --version`, `docker --version`, `code --version`  

## 2. Вариант А – Нативный Python (быстрее всего)

### Шаг 1 Клонируйте этот репозиторий

```bash
git clone https://github.com/<your-github>/generative-ai-for-beginners
cd generative-ai-for-beginners
```

### Шаг 2 Создайте и активируйте виртуальное окружение

```bash
python -m venv .venv          # сделать один
source .venv/bin/activate     # macOS / Linux
.\.venv\Scripts\activate      # Windows PowerShell
```

✅ Теперь приглашение командной строки должно начинаться с (.venv) — значит, вы в виртуальном окружении.

### Шаг 3 Установите зависимости

```bash
pip install -r requirements.txt
```

Перейдите к разделу 3 про [API ключи](#3-добавьте-свои-api-ключи)

## 2. Вариант B – VS Code Dev Container (Docker)

Мы подготовили этот репозиторий и курс с помощью [dev container](https://containers.dev?WT.mc_id=academic-105485-koreyst), который обеспечивает универсальную среду выполнения для разработки на Python3, .NET, Node.js и Java. Конфигурация описана в файле `devcontainer.json`, расположенном в папке `.devcontainer/` в корне репозитория.

>**Почему выбрать этот способ?**
>Среда полностью идентична Codespaces; отсутствует разбежка зависимостей.

### Шаг 0 Установите дополнительное ПО

Docker Desktop – проверьте, что команда ```docker --version``` работает.
Расширение VS Code Remote – Containers (ID: ms-vscode-remote.remote-containers).

### Шаг 1 Откройте репозиторий в VS Code

Файл ▸ Открыть папку…  → generative-ai-for-beginners

VS Code обнаружит `.devcontainer/` и покажет всплывающее окно.

### Шаг 2 Повторно открыть в контейнере

Нажмите «Reopen in Container». Docker собирает образ (≈ 3 минуты при первом запуске).
Когда появится приглашение терминала, вы внутри контейнера.

## 2. Вариант C – Miniconda

[Miniconda](https://conda.io/en/latest/miniconda.html?WT.mc_id=academic-105485-koreyst) — лёгкий установщик для [Conda](https://docs.conda.io/en/latest?WT.mc_id=academic-105485-koreyst), Python и нескольких пакетов.
Сам Conda — это менеджер пакетов, который облегчает создание и переключение между разными Python [виртуальными окружениями](https://docs.python.org/3/tutorial/venv.html?WT.mc_id=academic-105485-koreyst) и пакетами. Он также полезен для установки пакетов, отсутствующих в `pip`.

### Шаг 0 Установите Miniconda

Следуйте [инструкции по установке MiniConda](https://docs.anaconda.com/free/miniconda/#quick-command-line-install?WT.mc_id=academic-105485-koreyst).

```bash
conda --version
```

### Шаг 1 Создайте виртуальное окружение

Создайте файл окружения (*environment.yml*). Если вы работаете с Codespaces, создайте его внутри папки `.devcontainer`, то есть `.devcontainer/environment.yml`.

### Шаг 2 Заполните файл окружения

Добавьте следующий фрагмент в `environment.yml`

```yml
name: <environment-name>
channels:
 - defaults
 - microsoft
dependencies:
- python=<python-version>
- openai
- python-dotenv
- pip
- pip:
    - azure-ai-ml

```

### Шаг 3 Создайте окружение Conda

Выполните команды ниже в командной строке/терминале

```bash 
conda env create --name ai4beg --file .devcontainer/environment.yml # Подпуть .devcontainer применяется только к настройкам Codespace
conda activate ai4beg
```

Обратитесь к [руководству по окружениям Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html?WT.mc_id=academic-105485-koreyst), если возникнут проблемы.

## 2 Вариант D – Классический Jupyter / Jupyter Lab (в браузере)

> **Для кого это?**  
> Для тех, кто предпочитает классический интерфейс Jupyter или хочет запускать ноутбуки без VS Code.  

### Шаг 1 Убедитесь, что Jupyter установлен

Чтобы запустить Jupyter локально, откройте терминал/командную строку, перейдите в каталог курса и выполните:

```bash
jupyter notebook
```

или

```bash
jupyterhub
```

Запустится экземпляр Jupyter, URL для доступа к нему отобразится в окне командной строки.

После доступа по URL вы увидите структуру курса и сможете открыть любой файл `*.ipynb`. Например, `08-building-search-applications/python/oai-solution.ipynb`.

## 3. Добавьте свои API ключи

Важно хранить API ключи в безопасности при разработке любых приложений. Рекомендуем не сохранять ключи напрямую в коде. Выкладка этих данных в публичный репозиторий может привести к проблемам с безопасностью и нежелательным расходам, если ключи попадут к злоумышленникам.
Вот пошаговое руководство, как создать файл `.env` для Python и добавить ваши учетные данные Microsoft Foundry Models:

> **Примечание:** GitHub Models (и переменная `GITHUB_TOKEN`) будет закрыт в конце июля 2026. Это руководство использует [Microsoft Foundry Models](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst). Предпочитаете полностью офлайн? Смотрите [Foundry Local](https://foundrylocal.ai?WT.mc_id=academic-105485-koreyst).

1. **Перейдите в каталог проекта**: Откройте терминал или командную строку и перейдите в корневой каталог вашего проекта, где создадите файл `.env`.

   ```bash
   cd path/to/your/project
   ```

2. **Создайте файл `.env`**: Используйте любимый текстовый редактор для создания файла с именем `.env`. В командной строке можно использовать `touch` (на Unix) или `echo` (на Windows):

   На Unix-системах:

   ```bash
   touch .env
   ```

   На Windows:

   ```cmd
   echo . > .env
   ```

3. **Отредактируйте файл `.env`**: Откройте `.env` в текстовом редакторе (например, VS Code, Notepad++ или любом другом). Добавьте следующие строки, заменив заполнители на реальные данные вашего проекта Microsoft Foundry и API ключ:

   ```env
   AZURE_INFERENCE_ENDPOINT=your_foundry_endpoint_here
   AZURE_INFERENCE_CREDENTIAL=your_foundry_api_key_here
   ```

4. **Сохраните файл**: Сохраните изменения и закройте редактор.

5. **Установите `python-dotenv`**: Если ещё не сделали, установите пакет `python-dotenv`, чтобы загружать переменные окружения из файла `.env` в ваше Python-приложение. Установите через `pip`:

   ```bash
   pip install python-dotenv
   ```

6. **Загрузите переменные окружения в скрипте Python**: В вашем скрипте используйте пакет `python-dotenv`, чтобы загрузить переменные из `.env`:

   ```python
   from dotenv import load_dotenv
   import os

   # Загрузить переменные окружения из файла .env
   load_dotenv()

   # Получить доступ к переменным Microsoft Foundry Models
   endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
   token = os.getenv("AZURE_INFERENCE_CREDENTIAL")

   print(endpoint)
   ```

Вот и всё! Вы успешно создали `.env` файл, добавили учетные данные Microsoft Foundry Models и загрузили их в Python-приложение.

🔐 Никогда не коммитьте `.env` — он уже добавлен в `.gitignore`.
Полные инструкции от провайдера доступны в [`providers.md`](03-providers.md).

## 4. Что дальше?

| Я хочу…               | Перейти к…                                                             |
|-----------------------|------------------------------------------------------------------------|
| Начать урок 1          | [`01-introduction-to-genai`](../01-introduction-to-genai/README.md)    |
| Настроить провайдера LLM | [`providers.md`](03-providers.md)                                     |
| Познакомиться с другими учениками | [Присоединиться к нашему Discord](https://aka.ms/genai-discord?WT.mc_id=academic-105485-koreyst) |

## 5. Устранение неполадок

| Симптом                                   | Решение                                                         |
|-------------------------------------------|----------------------------------------------------------------|
| `python не найден`                        | Добавьте Python в PATH или перезапустите терминал после установки |
| `pip` не может собрать колёса (Windows)   | Выполните `pip install --upgrade pip setuptools wheel` и повторите попытку. |
| `ModuleNotFoundError: dotenv`             | Выполните `pip install -r requirements.txt` (окружение не установлено). |
| Сбой сборки Docker *No space left*        | Docker Desktop ▸ *Настройки* ▸ *Ресурсы* → увеличьте размер диска. |
| VS Code постоянно предлагает повторно открыть | Возможно, активны оба варианта; выберите один (venv **или** контейнер) |
| Ошибки OpenAI 401 / 429                    | Проверьте значение `OPENAI_API_KEY` / лимиты запросов.           |
| Ошибки при использовании Conda            | Установите библиотеки Microsoft AI через `conda install -c microsoft azure-ai-ml` |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->

---

# 03 Providers

# Выбор и настройка провайдера LLM 🔑

Задания **могут** быть настроены для работы с одной или несколькими развертками Больших Языковых Моделей (LLM) через поддерживаемого провайдера услуг, такого как OpenAI, Azure или Hugging Face. Они предоставляют _хостинг-эндпоинт_ (API), к которому мы можем получить программный доступ с нужными учетными данными (ключ API или токен). В этом курсе мы рассматриваем следующих провайдеров:

 - [OpenAI](https://platform.openai.com/docs/models?WT.mc_id=academic-105485-koreyst) с разнообразными моделями, включая основную серию GPT.
 - [Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/?WT.mc_id=academic-105485-koreyst) для моделей OpenAI с упором на корпоративную готовность
 - [Microsoft Foundry Models](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst) для одного эндпоинта и ключа API с доступом к сотням моделей от OpenAI, Meta, Mistral, Cohere, Microsoft и других (заменяет GitHub Models, который будет закрыт в конце июля 2026 года)
 - [Hugging Face](https://huggingface.co/docs/hub/index?WT.mc_id=academic-105485-koreyst) для моделей с открытым исходным кодом и сервера инференса
 - [Foundry Local](https://foundrylocal.ai?WT.mc_id=academic-105485-koreyst) или [Ollama](https://ollama.com/?WT.mc_id=academic-105485-koreyst), если вы предпочитаете запускать модели полностью офлайн на своем устройстве без необходимости облачной подписки

**Для этих упражнений вам понадобятся свои собственные аккаунты**. Задания необязательные, поэтому вы можете настроить одного, всех или ни одного из провайдеров по своему усмотрению. Немного советов по регистрации:

| Регистрация | Стоимость | Ключ API | Песочница | Комментарии |
|:---|:---|:---|:---|:---|
| [OpenAI](https://platform.openai.com/signup?WT.mc_id=academic-105485-koreyst)| [Цены](https://openai.com/pricing#language-models?WT.mc_id=academic-105485-koreyst)| [Проектные ключи](https://platform.openai.com/api-keys?WT.mc_id=academic-105485-koreyst) | [Веб без кода](https://platform.openai.com/playground?WT.mc_id=academic-105485-koreyst) | Доступно несколько моделей |
| [Azure](https://aka.ms/azure/free?WT.mc_id=academic-105485-koreyst)| [Цены](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/?WT.mc_id=academic-105485-koreyst)| [Быстрый старт SDK](https://learn.microsoft.com/azure/ai-services/openai/quickstart?WT.mc_id=academic-105485-koreyst)| [Быстрый старт Studio](https://learn.microsoft.com/azure/ai-services/openai/quickstart?WT.mc_id=academic-105485-koreyst) |  [Необходимо предварительное одобрение для доступа](https://learn.microsoft.com/azure/ai-services/openai/?WT.mc_id=academic-105485-koreyst)|
| [Microsoft Foundry](https://ai.azure.com?WT.mc_id=academic-105485-koreyst) | [Цены](https://azure.microsoft.com/pricing/details/ai-foundry/?WT.mc_id=academic-105485-koreyst) | [Страница обзора проекта](https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/overview?WT.mc_id=academic-105485-koreyst) | [Песочница Foundry](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst) | Доступен бесплатный уровень; один эндпоинт и ключ для множества провайдеров моделей |
| [Hugging Face](https://huggingface.co/join?WT.mc_id=academic-105485-koreyst) | [Цены](https://huggingface.co/pricing) | [Токены доступа](https://huggingface.co/docs/hub/security-tokens?WT.mc_id=academic-105485-koreyst) | [Hugging Chat](https://huggingface.co/chat/?WT.mc_id=academic-105485-koreyst)| [В Hugging Chat ограниченный набор моделей](https://huggingface.co/chat/models?WT.mc_id=academic-105485-koreyst) |
| [Foundry Local](https://foundrylocal.ai?WT.mc_id=academic-105485-koreyst) | Бесплатно (запускается на вашем устройстве) | Не требуется | [Локальный CLI/SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started?WT.mc_id=academic-105485-koreyst) | Полностью офлайн, совместимый с OpenAI эндпоинт |
| | | | | |

Следуйте указаниям ниже, чтобы _настроить_ этот репозиторий для работы с разными провайдерами. Задания, требующие определенного провайдера, будут иметь один из этих тегов в имени файла:

- `aoai` - требует Azure OpenAI эндпоинт и ключ
- `oai` - требует OpenAI эндпоинт и ключ
- `hf` - требует токен Hugging Face
- `githubmodels` - требует Microsoft Foundry Models эндпоинт, ключ (GitHub Models закрывается в конце июля 2026)

Вы можете настроить одного, всех или ни одного из провайдеров. Связанные задания просто выведут ошибку при отсутствии учетных данных.

## Создайте файл `.env`

Мы предполагаем, что вы уже прочитали вышеуказанные инструкции, зарегистрировались у нужного провайдера и получили необходимые данные для аутентификации (API_KEY или токен). В случае с Azure OpenAI предполагается, что у вас есть действующая развертка Azure OpenAI Service (эндпоинт) с хотя бы одной GPT моделью, развернутой для завершения чата.

Следующий шаг — настроить ваши **локальные переменные окружения** следующим образом:

1. Найдите в корневой папке файл `.env.copy`, который должен содержать такой текст:

   ```bash
   # Поставщик OpenAI
   OPENAI_API_KEY='<add your OpenAI API key here>'

   ## Azure OpenAI в Microsoft Foundry
   ## (Служба Azure OpenAI теперь является частью Microsoft Foundry: https://ai.azure.com)
   AZURE_OPENAI_API_VERSION='2024-10-21' # По умолчанию установлено! (текущая стабильная версия API)
   AZURE_OPENAI_API_KEY='<add your Foundry resource key here>'
   AZURE_OPENAI_ENDPOINT='<add your Foundry resource endpoint here, e.g. https://<resource-name>.openai.azure.com>'
   AZURE_OPENAI_DEPLOYMENT='<add your chat completion model deployment name here, e.g. gpt-4o-mini>'
   AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT='<add your embeddings model deployment name here, e.g. text-embedding-3-small>'

   ## Модели Microsoft Foundry (каталог моделей с несколькими поставщиками, заменяет модели GitHub, которые будут закрыты в конце июля 2026)
   AZURE_INFERENCE_ENDPOINT='<add your Microsoft Foundry project endpoint here>'
   AZURE_INFERENCE_CREDENTIAL='<add your Microsoft Foundry Models API key here>'

   ## Hugging Face
   HUGGING_FACE_API_KEY='<add your HuggingFace API or token here>'
   ```

2. Скопируйте этот файл в `.env` с помощью следующей команды. Этот файл _игнорируется git_, чтобы ваши секреты оставались в безопасности.

   ```bash
   cp .env.copy .env
   ```

3. Заполните значения (замените заполнители справа от `=`) как описано в следующем разделе.

4. (Опционально) Если вы используете GitHub Codespaces, у вас есть возможность сохранить переменные окружения как _секреты Codespaces_, связанные с этим репозиторием. В таком случае вам не нужно настраивать локальный файл .env. **Однако обратите внимание, что эта опция работает только для GitHub Codespaces.** Если вы используете Docker Desktop, файл .env все равно нужно будет настроить.

## Заполнение файла `.env`

Давайте быстро рассмотрим названия переменных, чтобы понять, что они означают:

| Переменная  | Описание  |
| :--- | :--- |
| HUGGING_FACE_API_KEY | Токен доступа пользователя, который вы настраиваете в своем профиле |
| OPENAI_API_KEY | Ключ авторизации для использования сервиса вне Azure OpenAI эндпоинтов |
| AZURE_OPENAI_API_KEY | Ключ авторизации для данного сервиса |
| AZURE_OPENAI_ENDPOINT | Развернутый эндпоинт для ресурса Azure OpenAI |
| AZURE_OPENAI_DEPLOYMENT | Эндпоинт развертки модели _генерации текста_ |
| AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT | Эндпоинт развертки модели _векторных эмбеддингов_ |
| AZURE_INFERENCE_ENDPOINT | Эндпоинт для вашего проекта Microsoft Foundry, используется для Microsoft Foundry Models |
| AZURE_INFERENCE_CREDENTIAL | Ключ API для вашего проекта Microsoft Foundry |
| | |

Примечание: Последние две переменные Azure OpenAI отражают модель по умолчанию для завершения чата (генерация текста) и векторного поиска (эмбеддинги) соответственно. Инструкции по их настройке будут даны в соответствующих заданиях.

## Настройка Azure OpenAI: через портал

> **Примечание:** Служба Azure OpenAI теперь является частью [Microsoft Foundry](https://ai.azure.com?WT.mc_id=academic-105485-koreyst). Ресурсы и развертки все еще отображаются в портале Azure, но ежедневное управление моделями (развертки, песочница, мониторинг) теперь происходит в портале Foundry вместо старого отдельного "Azure OpenAI Studio".

Значения эндпоинта и ключа Azure OpenAI можно найти в [портале Azure](https://portal.azure.com?WT.mc_id=academic-105485-koreyst), начнем с него.

1. Перейдите в [портал Azure](https://portal.azure.com?WT.mc_id=academic-105485-koreyst)
1. Нажмите на опцию **Keys and Endpoint** в боковом меню (слева).
1. Нажмите **Show Keys** — вы увидите: KEY 1, KEY 2 и Endpoint.
1. Используйте значение KEY 1 для AZURE_OPENAI_API_KEY
1. Используйте значение Endpoint для AZURE_OPENAI_ENDPOINT

Далее нам нужны эндпоинты конкретных моделей, которые мы развернули.

1. В боковом меню (слева) выберите опцию **Model deployments** для ресурса Azure OpenAI.
1. На странице перейдите по ссылке **Go to Microsoft Foundry portal** (или **Manage Deployments** в зависимости от типа ресурса)

Это приведет вас в портал Microsoft Foundry, где мы найдем другие необходимые значения, как описано ниже.

## Настройка Azure OpenAI: через портал Microsoft Foundry

1. Перейдите в [портал Microsoft Foundry](https://ai.azure.com?WT.mc_id=academic-105485-koreyst) **через ваш ресурс**, как описано выше.
1. Нажмите вкладку **Deployments** (боковая панель, слева), чтобы увидеть текущие развернутые модели.
1. Если нужная модель не развернута, используйте **Deploy model** для её развертывания из [каталога моделей](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst).
1. Вам понадобится модель _генерации текста_ — мы рекомендуем: **gpt-4o-mini**
1. Вам понадобится модель _векторных эмбеддингов_ — мы рекомендуем **text-embedding-3-small**

Теперь обновите переменные окружения, чтобы они отражали имя _Deployment_, которое вы использовали. Обычно это совпадает с именем модели, если вы явно не меняли его. Например, у вас может быть:

```bash
AZURE_OPENAI_DEPLOYMENT='gpt-4o-mini'
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT='text-embedding-3-small'
```

**Не забудьте сохранить файл .env после изменений**. Теперь вы можете закрыть файл и вернуться к инструкциям по запуску ноутбука.

## Настройка OpenAI: через профиль

Ваш ключ OpenAI API можно найти в вашем [аккаунте OpenAI](https://platform.openai.com/api-keys?WT.mc_id=academic-105485-koreyst). Если у вас его нет, вы можете зарегистрироваться и создать ключ API. После получения ключа используйте его для заполнения переменной `OPENAI_API_KEY` в файле `.env`.

## Настройка Hugging Face: через профиль

Ваш токен Hugging Face можно найти в вашем профиле в разделе [Access Tokens](https://huggingface.co/settings/tokens?WT.mc_id=academic-105485-koreyst). Не публикуйте и не делитесь им публично. Вместо этого создайте новый токен для использования в этом проекте и скопируйте его в файл `.env` в переменную `HUGGING_FACE_API_KEY`. _Примечание:_ технически это не ключ API, но используется для аутентификации, поэтому для удобства мы сохраняем это наименование.

## Настройка Microsoft Foundry Models: через портал

> **Примечание:** GitHub Models закрывается в конце июля 2026 года. Microsoft Foundry Models является прямой заменой с тем же каталогом моделей для бесплатного тестирования и поддержкой Azure AI Inference SDK / OpenAI SDK.

1. Перейдите на [Microsoft Foundry](https://ai.azure.com?WT.mc_id=academic-105485-koreyst) и создайте (или откройте) проект Foundry.
1. Просмотрите [каталог моделей](https://ai.azure.com/catalog/models?WT.mc_id=academic-105485-koreyst) и разверните модель, например `gpt-4o-mini`.
1. На странице **Обзор** проекта скопируйте **эндпоинт** и **ключ API**.
1. Используйте значение эндпоинта для `AZURE_INFERENCE_ENDPOINT` и ключ для `AZURE_INFERENCE_CREDENTIAL` в вашем файле `.env`.

## Офлайн / Локальные провайдеры

Если вы предпочитаете совсем не использовать облачную подписку, вы можете запускать совместимые открытые модели непосредственно на своем устройстве:

- **[Foundry Local](https://foundrylocal.ai?WT.mc_id=academic-105485-koreyst)** - локальное среда выполнения Microsoft. Она автоматически выбирает лучший провайдер выполнения (NPU, GPU или CPU) и предоставляет совместимый с OpenAI эндпоинт, что позволяет повторно использовать большую часть кода из этого курса с минимальными изменениями. Смотрите [документацию Foundry Local](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started?WT.mc_id=academic-105485-koreyst) для начала или установите с помощью `winget install Microsoft.FoundryLocal` (Windows) / `brew install microsoft/foundrylocal/foundrylocal` (macOS).
- **[Ollama](https://ollama.com/?WT.mc_id=academic-105485-koreyst)** - популярная альтернатива для локального запуска открытых моделей, таких как Llama, Phi, Mistral и Gemma.


Смотрите [Урок 19: Создание с помощью SLM](../19-slm/README.md?WT.mc_id=academic-105485-koreyst) для практических примеров использования обоих вариантов.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->