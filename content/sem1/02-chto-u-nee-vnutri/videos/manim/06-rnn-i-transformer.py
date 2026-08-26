"""Занятие 02, слайд 6. Технический ролик «Узкое горлышко против Матрицы Внимания»
Пример для генерации: Модели нужно закончить фразу: КЛЕЙ ДЛЯ ЦЕХА ИСПОРЧЕН. НУЖНО ВЫКИНУТЬ ___
Правильный ответ: КЛЕЙ. Но в тексте рядом стоит слово ЦЕХ.
Сцена 1: Архитектура RNN (Ошибка контекста)
Текст на экране: РАБОТА РЕКУРРЕНТНОЙ СЕТИ (RNN)
Визуальный ряд:
Внизу выстраиваются токены: [КЛЕЙ], [ДЛЯ], [ЦЕХА], [ИСПОРЧЕН], [.], [НУЖНО], [ВЫКИНУТЬ]. В конце пустой слот (без знака вопроса).
Над ними — единственный блок «ПАМЯТЬ». Блок по очереди подходит к каждому слову: слово влетает в блок
маленьким прямоугольничком-чипом и ложится нижним слотом, старые чипы поднимаются выше, а блок растёт
по необходимости. Пройденные слова ряда блекнут; самые первые исчезают, остальные сдвигаются на их место.
В памяти то же самое: старые чипы наверху постепенно выцветают, и когда чип стал почти прозрачным,
он улетает из памяти и исчезает — модель «забывает» начало фразы.
К моменту генерации в памяти отчётливо видны лишь свежие слова; призрак ЦЕХА — самое свежее существительное.
Генерация результата: Память встаёт над пустым слотом, из неё вниз тянется стрелка. Блок пытается предсказать
следующее слово. Из-за того, что КЛЕЙ забыт, модель опирается на самое свежее существительное в памяти — ЦЕХА.
Красный токен [ЦЕХ] появляется прямо в слоте: бокс заранее нужного размера, меняется только цвет и появляется слово.
Анимация ошибки: Появляется красный штамп «ОШИБКА: RNN ЗАБЫЛА ПРО КЛЕЙ, ПОМНИТ ЧТО ИСПОРЧЕН ЦЕХ.
ПРЕДЛАГАЕТ ВЫКИНУТЬ ЕГО» — он печатается по буквам и стоит справа от блока памяти,
с зазором в четверть ширины блока.
После печати — пауза на пару секунд.
Сцена 1Б: Проблемы архитектуры RNN (текстовый экран)
Заголовок: ПРОБЛЕМЫ АРХИТЕКТУРЫ RNN. Ниже две проблемы списком, по одной на строку:
1. Память быстро забывает слова, теряется внимание.
2. Медленная последовательная обработка слов.
Сцена 1В: Архитектура LSTM — память с воротами
Текст на экране: СЕТЬ LSTM: ПАМЯТЬ С ВОРОТАМИ.
Тот же ряд токенов и тот же блок «ПАМЯТЬ», но вокруг блока три ворота; вороты — в цвет памяти,
на едином зазоре от блока (входные ворота и ворота забывания шириной с блок, выходные — высотой
с блок), подписи вынесены за пределы блоков, а сами вороты соединены с памятью стрелками
(входные — к памяти, память — к воротам забывания и выходным). Стрелки создаются один раз,
никогда не исчезают и не пересоздаются: блок, ворота и стрелки движутся как единое целое,
зазоры между воротами и памятью постоянны.
Между словом и памятью — «ВХОДНЫЕ ВОРОТА»: чип подлетает к ним, ворота вспыхивают зелёным
(пропустить) или красным (отбросить). Точка и НУЖНО отбрасываются: чип падает вниз и гаснет.
Над памятью — «ВОРОТА ЗАБЫВАНИЯ»: при обработке ИСПОРЧЕН они удаляют из памяти ДЛЯ,
при НУЖНО — ЦЕХА (чип залетает в ворота, они вспыхивают зелёным, слово вылетает вверх растворяясь).
По ходу сцены трижды показываются карточки-пояснения: экран накрывается чёрным, печатается
заголовок (оранжевый) и поясняющий текст (бежевый); после паузы карточка исчезает, и сцена
продолжается ровно с места остановки. Моменты: 1) после залёта ДЛЯ во входные ворота (до зелёной
вспышки) — «ВХОДНЫЕ ВОРОТА»; 2) непосредственно перед перелётом ДЛЯ в ворота забывания —
«ВОРОТА ЗАБЫВАНИЯ»; 3) перед зелёной вспышкой выходных ворот — «ВЫХОДНЫЕ ВОРОТА». Чипы в памяти не выцветают — слова
держатся ярко, пока ворота явно не удалят ненужное; КЛЕЙ сохраняется до конца.
Справа от памяти — «ВЫХОДНЫЕ ВОРОТА». В конце блок встаёт над пустым слотом, из стопки в выходные
ворота перелетают важные для генерации слова (КЛЕЙ, ИСПОРЧЕН), ворота вспыхивают зелёным, из них
в слот спускается угловая зелёная стрелка — и в слоте появляется зелёный токен [КЛЕЙ]. Вместо штампа ошибки — зелёный текст (печатается по буквам):
«LSTM ЧАСТИЧНО РЕШИЛА ПРОБЛЕМУ ПАМЯТИ. НО ОБРАБОТКА ВСЁ ЕЩЁ ПОСЛЕДОВАТЕЛЬНАЯ».
Сцена 1Г: Проблемы архитектуры LSTM (текстовый экран)
Заголовок: ПРОБЛЕМЫ АРХИТЕКТУРЫ LSTM. Первый пункт зачёркнут линией и притушен (проблема решена),
второй остаётся: 2. Медленная последовательная обработка слов.
Затем переход к сцене про трансформеры.
Сцена 2: Трансформер — круг внимания и эмбеддинг контекста
Текст на экране: ТРАНСФОРМЕР: МЕХАНИЗМ ВНИМАНИЯ.
Визуальный ряд:
Внизу, справа налево, едут токены предложения (как в сценах RNN/LSTM): лишние слова
уходят за левый край экрана. Примерно на середине пути из токенов начинают отделяться
копии слов (мелким шрифтом, как чипы; в ленте остаются) и по ОБЩЕЙ спиральной
траектории — сначала влево, затем по часовой стрелке с закруткой вокруг центра —
занимают шесть слотов: «поездом», с одинаковой скоростью; КЛЕЙ проходит по
окружности дальше всех (почти полный оборот), ВЫКИНУТЬ сходит раньше прочих.
ЦЕХА встаёт ровно справа («правая точка»-хаб). Рядом с каждым словом появляется
зелёная точка.
Между всеми точками растут зелёные линии связи (все пары): соседние узлы соединяются
дугами по окружности, вместе они образуют круг; дальние хорды слегка изогнуты
наружу. 3 случайные связи усилены: толще, ярче и с большим выгибом. Затем толщина
и яркость линий меняются по весам внимания: чем важнее пара, тем жирнее линия; на
значимых связях появляются числовые подписи весов (вес 0.53 у пары ИСПОРЧЕН–НУЖНО
смещён внутрь круга).
Ближе к кругу (чуть правее ЦЕХА, центр выровнен
с его точкой) появляется блок «Эмбеддинг контекста»; лента всё это время продолжает
ехать, «?» останавливается ровно под блоком.
По ходу сцены — две длинные карточки-пояснения с медленным набором текста и долгой
паузой: «Слой внимания» (после весов, до блока) и «Эмбеддинг контекста» (в момент,
когда копии точек въезжают в блок). Заголовки карточек печатаются в 3 раза быстрее.
Анимация агрегации: точки остаются в узлах, а их копии едут по линиям к правой
точке круга (чем сильнее связь, тем раньше и тем ярче едет копия); соседние узлы —
по дуге кольца, дальние — по изогнутой хорде. От правой точки
одна общая горизонтальная линия ведёт в блок эмбеддинга. Все копии въезжают в блок —
блок вспыхивает зелёным, от него вниз идёт ровно вертикальная зелёная стрелка
к пустому слоту «?», и в слоте появляется уверенный зелёный токен [КЛЕЙ].
Финальный текстовый слайд: список крупных сетей, построенных на трансформерах
(ChatGPT, Claude, Gemini, DeepSeek, Llama, Mistral, Grok).

Запуск (ManimCE, требуется установленный Manim):
    manim -r 1920,1080 --fps 30 06-rnn-i-transformer.py RNNvsTransformer

Выход: videos/06-rnn-i-transformer.mp4 — подключается в `video_url` слайда 6
(video_type: direct).
"""

import os
import numpy as np
from manim import *

# === ПАЛИТРА И СТИЛЬ (Завод «БытХимИскИнДеталь») ===
BG_COLOR = "#000000"       # Чёрный (фон)
TEXT_COLOR = "#E6D5B8"     # Пыльно-бежевый (основной текст)
RNN_COLOR = "#D95C14"      # Ржаво-оранжевый (RNN и ошибки)
ATTN_COLOR = "#39FF14"     # Кислотно-зелёный (Трансформеры и Внимание)
ERROR_COLOR = "#FF3333"    # Красный (ошибка)
PANEL_COLOR = "#2F3E33"    # Тёмно-оливковый (блоки и панели)

config.background_color = BG_COLOR
config.seed = 42  # Детерминизм


class RNNvsTransformer(Scene):
    def construct(self):
        # --- СЦЕНА 1: RNN и потеря смысла ---

        # Заголовок
        title_rnn = Text("РАБОТА РЕКУРРЕНТНОЙ СЕТИ (RNN)", color=RNN_COLOR, weight=BOLD, font_size=40)
        title_rnn.to_edge(UP)
        self.play(FadeIn(title_rnn))

        # Исходные слова (точка и «нужно» — отдельные токены; слот — пустой бокс
        # размера ERR_W: в него на месте превратится токен-ошибка)
        ERR_W = 1.5
        words = ["КЛЕЙ", "ДЛЯ", "ЦЕХА", "ИСПОРЧЕН", ".", "НУЖНО", "ВЫКИНУТЬ", "?"]

        tokens = VGroup()
        for word in words:
            if word == "?":  # пустой слот: бокс без знака вопроса
                box = Rectangle(width=ERR_W, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                tokens.add(VGroup(box))
            else:
                txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=28)
                box = Rectangle(width=txt.width + 0.5, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                txt.move_to(box.get_center())
                tokens.add(VGroup(box, txt))

        tokens.arrange(RIGHT, buff=0.25)
        if tokens.width > 13.5:  # страховка: ряд не шире кадра
            tokens.scale_to_fit_width(13.5)
        tokens.move_to(DOWN * 2)

        self.play(FadeIn(tokens), run_time=1.5)
        self.wait(1)

        # Единственный блок «ПАМЯТЬ» (скрытое состояние вместо цепочки RNN-блоков)
        CHIP_H, PITCH, PAD = 0.34, 0.42, 0.12
        MAX_AGE = 6  # сколько шагов чип живёт в памяти; ЦЕХА должен дожить до предсказания

        memory_box = Rectangle(width=1.5, height=1.2, color=RNN_COLOR, fill_opacity=0.2)
        memory_lbl = Text("ПАМЯТЬ", color=RNN_COLOR, weight=BOLD, font_size=26)
        memory_lbl.next_to(memory_box, UP, buff=0.18)
        memory = VGroup(memory_box, memory_lbl)
        memory.move_to(tokens[0].get_top() + UP * 2.0)
        self.play(FadeIn(memory), run_time=0.7)

        # Чипы-слова внутри памяти: новый ложится нижним слотом, старые поднимаются,
        # самые старые наверху выцветают и улетают. Группа едет вместе с блоком.
        stack_grp = VGroup()
        chips = []  # [0] — самый старый, [-1] — самый новый
        ages = []

        def needed_height(n):
            """Высота блока, необходимая для n чипов."""
            return max(1.2, 2 * PAD + (n - 1) * PITCH + CHIP_H)

        def label_target(box_h):
            """Позиция подписи над верхом блока высотой box_h (низ блока на месте)."""
            cx = memory_box.get_center()[0]
            top_y = memory_box.get_bottom()[1] + box_h
            return np.array([cx, top_y + 0.18 + memory_lbl.height / 2, 0.0])

        def box_resize_anims(h_target, w_target):
            """Анимации растяжения бокса: низ и центр X остаются на месте."""
            fx = w_target / memory_box.width
            fy = h_target / memory_box.height
            if abs(fx - 1) < 1e-6 and abs(fy - 1) < 1e-6:
                return []
            anim = memory_box.animate
            if abs(fx - 1) >= 1e-6:
                anim = anim.stretch_about_point(fx, 0, memory_box.get_center())
            if abs(fy - 1) >= 1e-6:
                anim = anim.stretch_about_point(fy, 1, memory_box.get_bottom())
            return [anim]

        def move_memory(target_center, run_time=0.5):
            """Блок памяти и стопка внутри него движутся как одно целое."""
            delta = target_center - memory.get_center()
            self.play(
                memory.animate.shift(delta),
                stack_grp.animate.shift(delta),
                run_time=run_time,
            )

        def make_chip(word):
            chip_txt = Text(word, color=RNN_COLOR, weight=BOLD, font_size=18)
            chip_box = Rectangle(width=chip_txt.width + 0.22, height=CHIP_H, color=RNN_COLOR, fill_opacity=0.25)
            chip_txt.move_to(chip_box.get_center())
            return VGroup(chip_box, chip_txt)

        def stack_width_target(extra_chip=None):
            """Ширина блока под самый широкий чип (плюс поля)."""
            widths = [c.width + 0.4 for c in chips]
            if extra_chip is not None:
                widths.append(extra_chip.width + 0.4)
            return max([1.5] + widths)

        for i in range(len(words) - 1):  # КЛЕЙ ... ВЫКИНУТЬ
            if i > 0:
                move_memory(tokens[i].get_top() + UP * 2.0)

            # Стрелочка от слова к памяти — только на время передачи
            v_arrow = Arrow(tokens[i].get_top(), memory_box.get_bottom(), color=TEXT_COLOR, buff=0.1)
            self.play(GrowArrow(v_arrow), run_time=0.3)

            # Слово-чип влетает в память нижним слотом, уменьшаясь до размера чипа;
            # блок сразу растёт по необходимости (вширь и вверх)
            chip = make_chip(words[i])
            s0 = max(1.0, min(2.9, tokens[i][0].width * 0.85 / chip.width))
            chip.move_to(tokens[i].get_center()).scale(s0)
            h_target = needed_height(len(chips) + 1)
            w_target = stack_width_target(chip)
            slot_y = memory_box.get_bottom()[1] + PAD + CHIP_H / 2
            # Всё одновременно: старые чипы сдвигаются вверх и тускнеют, освобождая
            # нижний слот, новый чип влетает прямо на это место; блок растёт,
            # подпись следует за верхом, стрелка гаснет
            anims = [
                chip.animate.move_to(
                    np.array([memory_box.get_center()[0], slot_y, 0.0])
                ).scale(1 / s0),
                *box_resize_anims(h_target, w_target),
                memory_lbl.animate.move_to(label_target(h_target)),
                FadeOut(v_arrow),
            ]
            anims += [c.animate.shift(UP * PITCH).fade(0.25) for c in chips]
            self.play(*anims, run_time=0.7)
            stack_grp.add(chip)
            chips.append(chip)
            ages.append(0)

            # Старение ряда: пройденные слова блекнут; самые первые исчезают,
            # остальные сдвигаются на их место (память и стопка едут вместе с ними)
            anims = []
            if i >= 2:
                step = tokens[i - 2][0].width + 0.25  # ширина убираемого токена + отступ
                anims.append(FadeOut(tokens[i - 2]))
                anims.append(tokens[i - 1].animate.set_opacity(0.45).shift(LEFT * step))
                anims.append(tokens[i].animate.set_opacity(0.75).shift(LEFT * step))
                anims += [t.animate.shift(LEFT * step) for t in tokens[i + 1:]]
                anims.append(memory.animate.shift(LEFT * step))
                anims.append(stack_grp.animate.shift(LEFT * step))
            elif i == 1:
                anims.append(tokens[0].animate.set_opacity(0.45))
                anims.append(tokens[1].animate.set_opacity(0.75))
            else:
                anims.append(tokens[0].animate.set_opacity(0.75))
            self.play(*anims, run_time=0.5)

            # Самый старый чип совсем выцвел — улетает из памяти и исчезает
            for k in range(len(ages)):
                ages[k] += 1
            if ages and ages[0] >= MAX_AGE:
                old = chips.pop(0)
                ages.pop(0)
                stack_grp.remove(old)
                h_shrunk = needed_height(len(chips))
                w_shrunk = stack_width_target()
                anims = [old.animate.shift(RIGHT * 1.1 + UP * 0.9).set_opacity(0)]
                anims += box_resize_anims(h_shrunk, w_shrunk)
                anims.append(memory_lbl.animate.move_to(label_target(h_shrunk)))
                self.play(*anims, run_time=0.6)
                self.remove(old)

        self.wait(1)

        # Память встаёт над пустым слотом — как над остальными словами
        move_memory(tokens[-1].get_top() + UP * 2.0)

        # Генерация ошибки: стрелка вниз от памяти к слоту
        pred_arrow = Arrow(memory_box.get_bottom(), tokens[-1].get_top(), color=RNN_COLOR, buff=0.1)
        self.play(GrowArrow(pred_arrow), run_time=0.5)

        # Слот сразу нужного размера: слово появляется на месте, меняется только цвет
        error_word = "ЦЕХ"
        error_box = Rectangle(width=ERR_W, height=1.0, color=ERROR_COLOR, fill_color=ERROR_COLOR, fill_opacity=0.3)
        error_txt = Text(error_word, color=ERROR_COLOR, weight=BOLD, font_size=28).move_to(error_box.get_center())
        error_token = VGroup(error_box, error_txt)
        error_token.move_to(tokens[-1].get_center())

        self.play(ReplacementTransform(tokens[-1], error_token))

        # Штамп с ошибкой — компактный, без обводки, чуть заходит на блок памяти;
        # появляется печатанием по буквам
        stamp = Text(
            "ОШИБКА:\nRNN ЗАБЫЛА ПРО КЛЕЙ,\nПОМНИТ ЧТО ИСПОРЧЕН ЦЕХ.\nПРЕДЛАГАЕТ ВЫКИНУТЬ ЕГО",
            color=ERROR_COLOR,
            weight=BOLD,
            font_size=30,
        )
        stamp.move_to(UP * 0.2)
        # зазор между правой гранью блока памяти и текстом — четверть ширины блока
        target_left = memory_box.get_right()[0] + 0.25 * memory_box.width
        stamp.shift(RIGHT * (target_left - stamp.get_left()[0]))
        if stamp.get_right()[0] > config.frame_x_radius - 0.2:  # страховка от выезда за кадр
            stamp.set_right(config.frame_x_radius - 0.2)

        glyphs = stamp.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in glyphs], lag_ratio=0.05), run_time=2.5)
        self.wait(2)

        # Очистка сцены 1: всё, что осталось на экране, гаснет одновременно
        # (уже ушедшие слова не возвращаются — они просто удалены со сцены)
        leftover_tokens = VGroup(tokens[len(words) - 3], tokens[len(words) - 2])  # НУЖНО, ВЫКИНУТЬ
        self.play(
            FadeOut(VGroup(title_rnn, memory, stack_grp, pred_arrow, stamp, error_token, leftover_tokens)),
            run_time=1,
        )
        # страховка: всё уже прозрачно — снимаем со сцены любые «двойные» корни
        self.clear()

        # --- СЦЕНА 1Б: Проблемы архитектуры RNN (текстовый экран) ---
        self._problems_scene("ПРОБЛЕМЫ АРХИТЕКТУРЫ RNN")

        # --- СЦЕНА 1В: Архитектура LSTM — память с воротами ---
        self._lstm_scene()

        # --- СЦЕНА 1Г: Проблемы архитектуры LSTM (проблема памяти решена) ---
        self._problems_scene("ПРОБЛЕМЫ АРХИТЕКТУРЫ LSTM", cross_first=True)

        # --- СЦЕНА 2: Трансформер — круг внимания и эмбеддинг контекста ---
        self._attention_scene()

    def _problems_scene(self, title_text, cross_first=False):
        """Текстовый экран «Проблемы архитектуры …» (сцены 1Б и 1Г).

        cross_first=True — первый пункт зачёркивается линиями и притушается
        (для LSTM: проблема памяти решена воротами).
        """
        # Первый пункт разбит на строки отдельными Text — чтобы получить точные
        # границы строк для линий-зачёркивания
        item1_lines = VGroup(
            Text("1. ПАМЯТЬ БЫСТРО ЗАБЫВАЕТ СЛОВА,", color=TEXT_COLOR, weight=BOLD, font_size=34),
            Text("ТЕРЯЕТСЯ ВНИМАНИЕ.", color=TEXT_COLOR, weight=BOLD, font_size=34),
        )
        item1_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        problem_items = VGroup(
            item1_lines,
            Text(
                "2. МЕДЛЕННАЯ ПОСЛЕДОВАТЕЛЬНАЯ\nОБРАБОТКА СЛОВ",
                color=TEXT_COLOR, weight=BOLD, font_size=34,
            ),
        )
        problem_items.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        problem_items.move_to(DOWN * 0.8)

        title_prob = Text(title_text, color=RNN_COLOR, weight=BOLD, font_size=40)
        title_prob.next_to(problem_items, UP, buff=0.7)

        self.play(FadeIn(title_prob))
        self.play(Write(item1_lines), run_time=1.5)
        self.wait(0.8)

        strikes = VGroup()
        if cross_first:
            strikes = VGroup(*[
                Line(
                    line.get_corner(DL) + LEFT * 0.12,
                    line.get_corner(DR) + RIGHT * 0.12,
                    color=TEXT_COLOR, stroke_width=6,
                ).shift(UP * line.get_height() * 0.5)  # поднять на полстроки
                for line in item1_lines
            ])
            self.play(Create(strikes), item1_lines.animate.set_opacity(0.35), run_time=0.8)

        self.play(Write(problem_items[1]), run_time=1.5)
        self.wait(2)

        # Очистка: каждый зарегистрированный корень гаснет своим FadeOut
        self.play(
            FadeOut(title_prob),
            FadeOut(item1_lines),
            FadeOut(problem_items[1]),
            *[FadeOut(s) for s in strikes],
            run_time=1,
        )

    def _card(self, title_text, body_text,
              title_color=RNN_COLOR, body_color=TEXT_COLOR, hold=2.0,
              title_time=1.2, body_time=1.8):
        """Карточка-пояснение: экран накрывается чёрным, заголовок и текст
        печатаются по глифам (title_time/body_time — скорость набора);
        после паузы (hold секунд) всё исчезает и сцена продолжается с места остановки."""
        overlay = Rectangle(
            width=config.frame_width + 0.2,
            height=config.frame_height + 0.2,
            stroke_width=0, fill_color=BLACK, fill_opacity=1,
        )
        title_card = Text(title_text, color=title_color, weight=BOLD, font_size=40)
        body_card = Text(body_text, color=body_color, font_size=30)
        VGroup(title_card, body_card).arrange(DOWN, buff=0.6)

        self.play(FadeIn(overlay), run_time=0.3)
        t_glyphs = title_card.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in t_glyphs], lag_ratio=0.06), run_time=title_time)
        b_glyphs = body_card.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in b_glyphs], lag_ratio=0.04), run_time=body_time)
        # нормализуем сцену: разрозненные глифы прочь, тексты целиком на сцену
        self.remove(*t_glyphs, *b_glyphs)
        self.add(title_card)
        self.add(body_card)
        self.wait(hold)
        self.play(FadeOut(overlay), FadeOut(title_card), FadeOut(body_card), run_time=0.7)

    def _lstm_scene(self):
        """Сцена 1В: архитектура LSTM — память под контролем ворот."""
        title_lstm = Text("СЕТЬ LSTM: ПАМЯТЬ С ВОРОТАМИ", color=RNN_COLOR, weight=BOLD, font_size=40)
        title_lstm.to_edge(UP)
        self.play(FadeIn(title_lstm))

        ERR_W = 1.5
        words = ["КЛЕЙ", "ДЛЯ", "ЦЕХА", "ИСПОРЧЕН", ".", "НУЖНО", "ВЫКИНУТЬ", "?"]
        DISCARD = {".", "НУЖНО"}                          # входные ворота отбрасывают
        FORGET_AT = {"ИСПОРЧЕН": "ДЛЯ", "НУЖНО": "ЦЕХА"}  # ворота забывания удаляют

        tokens = VGroup()
        for word in words:
            if word == "?":  # пустой слот: бокс без знака вопроса
                box = Rectangle(width=ERR_W, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                tokens.add(VGroup(box))
            else:
                txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=28)
                box = Rectangle(width=txt.width + 0.5, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                txt.move_to(box.get_center())
                tokens.add(VGroup(box, txt))

        tokens.arrange(RIGHT, buff=0.25)
        if tokens.width > 13.5:  # страховка: ряд не шире кадра
            tokens.scale_to_fit_width(13.5)
        tokens.move_to(DOWN * 2)

        self.play(FadeIn(tokens), run_time=1.5)
        self.wait(0.5)

        # --- Юнит LSTM: блок памяти и три ворота вокруг него ---
        CHIP_H, PITCH, PAD = 0.34, 0.42, 0.12
        GAP = 0.35      # единый зазор между памятью и любыми воротами (= длина коннекторов)
        GATE_H = 0.45   # одинаковая высота входных ворот и ворот забывания
        OUT_W = 2.1     # своя ширина выходных ворот

        memory_box = Rectangle(width=1.5, height=1.2, color=RNN_COLOR, fill_opacity=0.2)

        # Ворота в цвет памяти, без закруглений; входные/забывания — шириной с блок,
        # выходные — высотой с блок (подстраиваются при каждом изменении блока)
        input_box = Rectangle(width=1.5, height=GATE_H, color=RNN_COLOR, fill_opacity=0.2)
        input_lbl = Text("ВХОДНЫЕ ВОРОТА", color=TEXT_COLOR, font_size=12)
        input_gate = VGroup(input_box, input_lbl)

        forget_box = Rectangle(width=1.5, height=GATE_H, color=RNN_COLOR, fill_opacity=0.2)
        forget_lbl = Text("ВОРОТА ЗАБЫВАНИЯ", color=TEXT_COLOR, font_size=12)
        forget_gate = VGroup(forget_box, forget_lbl)

        out_box = Rectangle(width=OUT_W, height=1.2, color=RNN_COLOR, fill_opacity=0.2)
        out_lbl = Text("ВЫХОДНЫЕ ВОРОТА", color=TEXT_COLOR, font_size=12)
        out_gate = VGroup(out_box, out_lbl)

        memory_box.move_to(tokens[0].get_top() + UP * 2.0)
        # вороты выровнены по блоку памяти на едином зазоре
        input_box.next_to(memory_box, DOWN, buff=GAP)
        forget_box.next_to(memory_box, UP, buff=GAP)
        out_box.next_to(memory_box, RIGHT, buff=GAP)
        # подписи ворот — снаружи блоков
        input_lbl.next_to(input_box, LEFT, buff=0.12)
        forget_lbl.next_to(forget_box, UP, buff=0.08)
        out_lbl.next_to(out_box, UP, buff=0.08)

        unit = VGroup(memory_box, input_gate, forget_gate, out_gate)

        # --- Стрелки ворота <-> память: создаются один раз и живут до конца сцены.
        # Зазоры между блоком и воротами постоянны, поэтому при изменении размера
        # стрелки не пересоздаются, а сдвигаются целиком вместе с гранями ---
        conn_style = dict(color=RNN_COLOR, stroke_width=4, buff=0.04, tip_length=0.16)
        conns = {
            "input": Arrow(input_box.get_top(), memory_box.get_bottom(), **conn_style),
            "forget": Arrow(memory_box.get_top(), forget_box.get_bottom(), **conn_style),
            "out": Arrow(
                np.array([memory_box.get_right()[0], memory_box.get_center()[1], 0.0]),
                out_box.get_left(),
                **conn_style,
            ),
        }
        unit.add(*conns.values())

        stack_grp = VGroup()
        chips = []      # [0] — самый старый (нижний слот)
        chip_words = []

        self.play(FadeIn(unit), run_time=0.8)

        def needed_height(n):
            """Высота блока, необходимая для n чипов."""
            return max(1.2, 2 * PAD + (n - 1) * PITCH + CHIP_H)

        def box_resize_anims(h_target, w_target):
            """Растяжение бокса: низ и центр X остаются на месте."""
            fx = w_target / memory_box.width
            fy = h_target / memory_box.height
            if abs(fx - 1) < 1e-6 and abs(fy - 1) < 1e-6:
                return []
            anim = memory_box.animate
            if abs(fx - 1) >= 1e-6:
                anim = anim.stretch_about_point(fx, 0, memory_box.get_center())
            if abs(fy - 1) >= 1e-6:
                anim = anim.stretch_about_point(fy, 1, memory_box.get_bottom())
            return [anim]

        def seg(p0, p1, b=0.04):
            """Концы отрезка с отступом от граней — как у стрелок при создании."""
            p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
            d = (p1 - p0) / np.linalg.norm(p1 - p0)
            return p0 + d * b, p1 - d * b

        def follow_anims(h_target, w_target):
            """Вороты, подписи и стрелки ставятся в АБСОЛЮТНЫЕ целевые позиции,
            вычисленные из целевого размера блока: зазор GAP до всех ворот постоянен,
            накопленных смещений не бывает. Стрелки те же — не пересоздаются."""
            cx = memory_box.get_center()[0]
            bot = memory_box.get_bottom()[1]
            cy = bot + h_target / 2          # середина высоты целевого блока
            rx = cx + w_target / 2           # правая грань целевого блока
            anims = []
            # входные ворота: шириной с блок, верх на GAP ниже низа блока
            anims.append(
                input_box.animate.stretch_to_fit_width(w_target)
                .move_to([cx, bot - GAP - GATE_H / 2, 0.0])
            )
            anims.append(input_lbl.animate.move_to([
                cx - w_target / 2 - 0.12 - input_lbl.width / 2,
                input_box.get_center()[1],
                0.0,
            ]))
            # ворота забывания: шириной с блок, низ на GAP выше верха блока
            anims.append(
                forget_box.animate.stretch_to_fit_width(w_target)
                .move_to([cx, bot + h_target + GAP + GATE_H / 2, 0.0])
            )
            anims.append(forget_lbl.animate.move_to([
                cx,
                bot + h_target + GAP + GATE_H + 0.08 + forget_lbl.height / 2,
                0.0,
            ]))
            # выходные ворота: ширина OUT_W, высота с блок, левая грань на GAP правее
            anims.append(
                out_box.animate.stretch_to_fit_width(OUT_W)
                .stretch_to_fit_height(h_target)
                .move_to([rx + GAP + OUT_W / 2, cy, 0.0])
            )
            anims.append(out_lbl.animate.move_to([
                rx + GAP + OUT_W / 2,
                bot + h_target + 0.08 + out_lbl.height / 2,
                0.0,
            ]))
            # вечные стрелки: те же объекты, концы приклеиваются к новым граням
            anims.append(conns["forget"].animate.put_start_and_end_on(
                *seg([cx, bot + h_target, 0.0], [cx, bot + h_target + GAP, 0.0])
            ))
            anims.append(conns["out"].animate.put_start_and_end_on(
                *seg([rx, cy, 0.0], [rx + GAP, cy, 0.0])
            ))
            return anims

        def move_unit(target_center, run_time=0.5):
            """Юнит целиком (блок, подпись, ворота) и стопка едут как одно целое."""
            delta = target_center - memory_box.get_center()
            self.play(
                unit.animate.shift(delta),
                stack_grp.animate.shift(delta),
                run_time=run_time,
            )

        def make_chip(word):
            chip_txt = Text(word, color=RNN_COLOR, weight=BOLD, font_size=18)
            chip_box = Rectangle(width=chip_txt.width + 0.22, height=CHIP_H,
                                 color=RNN_COLOR, fill_opacity=0.25)
            chip_txt.move_to(chip_box.get_center())
            return VGroup(chip_box, chip_txt)

        def stack_width_target(extra_chip=None):
            """Ширина блока под самый широкий чип (плюс поля)."""
            widths = [c.width + 0.4 for c in chips]
            if extra_chip is not None:
                widths.append(extra_chip.width + 0.4)
            return max([1.5] + widths)

        for i in range(len(words) - 1):  # КЛЕЙ ... ВЫКИНУТЬ
            word = words[i]
            if i > 0:
                move_unit(tokens[i].get_top() + UP * 2.0)

            # Стрелка от слова к входным воротам
            v_arrow = Arrow(tokens[i].get_top(), input_box.get_bottom(), color=TEXT_COLOR, buff=0.08)
            self.play(GrowArrow(v_arrow), run_time=0.3)

            # Чип подлетает к входным воротам, те «решают» его судьбу
            chip = make_chip(word)
            s0 = max(1.0, min(2.9, tokens[i][0].width * 0.85 / chip.width))
            chip.move_to(tokens[i].get_center()).scale(s0)
            mid_scale = max(0.55, s0 * 0.65)
            self.play(
                chip.animate.move_to(input_box.get_center()).scale(mid_scale / s0),
                run_time=0.35,
            )

            if word == "ДЛЯ":
                # карточка-пояснение: слово уже во входных воротах, вспышки ещё не было
                self._card(
                    "ВХОДНЫЕ ВОРОТА",
                    "Решают, какую новую информацию нужно добавить в память,\n"
                    "а какую нужно пропустить",
                )

            if word in DISCARD:
                # Красная вспышка — слово не пропущено: чип падает вниз и гаснет
                self.play(Indicate(input_box, color=ERROR_COLOR, scale_factor=1.06), run_time=0.45)
                self.play(
                    chip.animate.move_to(tokens[i].get_top() + UP * 0.3).set_opacity(0),
                    FadeOut(v_arrow),
                    run_time=0.5,
                )
                self.remove(chip)
            else:
                # Зелёная вспышка — слово проходит в память нижним слотом; старые
                # чипы поднимаются (не выцветая!), блок растёт — всё одним движением
                self.play(Indicate(input_box, color=ATTN_COLOR, scale_factor=1.06), run_time=0.3)
                h_target = needed_height(len(chips) + 1)
                w_target = stack_width_target(chip)
                slot_y = memory_box.get_bottom()[1] + PAD + CHIP_H / 2
                anims = [
                    chip.animate.move_to(
                        np.array([memory_box.get_center()[0], slot_y, 0.0])
                    ).scale(1 / mid_scale),
                    *box_resize_anims(h_target, w_target),
                    *follow_anims(h_target, w_target),
                    FadeOut(v_arrow),
                ]
                anims += [c.animate.shift(UP * PITCH) for c in chips]
                self.play(*anims, run_time=0.7)
                stack_grp.add(chip)
                chips.append(chip)
                chip_words.append(word)

            # Старение ряда: пройденные слова блекнут; самые первые исчезают,
            # остальные сдвигаются на их место (юнит и стопка едут вместе с ними)
            anims = []
            if i >= 2:
                step = tokens[i - 2][0].width + 0.25  # ширина убираемого токена + отступ
                anims.append(FadeOut(tokens[i - 2]))
                anims.append(tokens[i - 1].animate.set_opacity(0.45).shift(LEFT * step))
                anims.append(tokens[i].animate.set_opacity(0.75).shift(LEFT * step))
                anims += [t.animate.shift(LEFT * step) for t in tokens[i + 1:]]
                anims.append(unit.animate.shift(LEFT * step))
                anims.append(stack_grp.animate.shift(LEFT * step))
            elif i == 1:
                anims.append(tokens[0].animate.set_opacity(0.45))
                anims.append(tokens[1].animate.set_opacity(0.75))
            else:
                anims.append(tokens[0].animate.set_opacity(0.75))
            self.play(*anims, run_time=0.5)

            # Ворота забывания: чип залетает в ворота, те мигают зелёным,
            # затем слово вылетает вверх, растворяясь
            if word in FORGET_AT:
                k = chip_words.index(FORGET_AT[word])
                old = chips.pop(k)
                chip_words.pop(k)
                stack_grp.remove(old)
                if FORGET_AT[word] == "ДЛЯ":
                    # карточка-пояснение: непосредственно перед перелётом чипа в ворота
                    self._card(
                        "ВОРОТА ЗАБЫВАНИЯ",
                        "Смотрят на новое слово и прошлую память.\n"
                        "Решают, какую информацию пора выбросить",
                    )
                self.play(old.animate.move_to(forget_box.get_center()), run_time=0.4)
                self.play(Indicate(forget_box, color=ATTN_COLOR, scale_factor=1.06), run_time=0.45)

                h_shrunk = needed_height(len(chips))
                w_shrunk = stack_width_target()
                anims = [
                    old.animate.move_to(forget_box.get_top() + UP * 0.6).set_opacity(0),
                    *box_resize_anims(h_shrunk, w_shrunk),
                    *follow_anims(h_shrunk, w_shrunk),
                ]
                # чипы над жертвой опускаются на освободившееся место
                for j, c in enumerate(chips):
                    target_y = memory_box.get_bottom()[1] + PAD + CHIP_H / 2 + j * PITCH
                    dy = target_y - c.get_center()[1]
                    if abs(dy) > 1e-3:
                        anims.append(c.animate.shift(UP * dy))
                self.play(*anims, run_time=0.7)
                self.remove(old)

        self.wait(0.8)

        # --- Генерация: юнит встаёт над пустым слотом ---
        move_unit(tokens[-1].get_top() + UP * 2.0)

        # Важные для генерации слова выходят из памяти в выходные ворота
        important = {"КЛЕЙ", "ИСПОРЧЕН"}
        flying = [(c, w) for c, w in zip(chips, chip_words) if w in important]
        remaining = [(c, w) for c, w in zip(chips, chip_words) if w not in important]
        chips = [c for c, w in remaining]
        chip_words = [w for c, w in remaining]

        out_chips = VGroup()
        anims = []
        for idx, (c, w) in enumerate(flying):
            target = np.array([
                out_box.get_center()[0],
                out_box.get_top()[1] - 0.62 - idx * PITCH,
                0.0,
            ])
            anims.append(c.animate.move_to(target))
            stack_grp.remove(c)
            out_chips.add(c)
        h_final = needed_height(len(chips))
        anims += box_resize_anims(h_final, stack_width_target())
        anims += follow_anims(h_final, stack_width_target())
        for j, c in enumerate(chips):
            target_y = memory_box.get_bottom()[1] + PAD + CHIP_H / 2 + j * PITCH
            anims.append(c.animate.move_to(np.array([memory_box.get_center()[0], target_y, 0.0])))
        self.play(*anims, run_time=0.8)

        # Карточка-пояснение: перед зелёной вспышкой выходных ворот
        self._card(
            "ВЫХОДНЫЕ ВОРОТА",
            "Решают, какая информация из памяти нужна прямо сейчас\n"
            "для предсказания следующего слова",
        )

        # Выходные ворота собрали важное — вспышка зелёным
        self.play(Indicate(out_box, color=ATTN_COLOR, scale_factor=1.06), run_time=0.6)

        # --- Зелёная угловая стрелка: из выходных ворот вниз и влево — в слот слова ---
        # Рисуем ПОСЛЕ вспышки выходных ворот
        corner_pt = np.array([out_box.get_center()[0], tokens[-1].get_center()[1], 0.0])
        gen_v = Line(out_box.get_bottom(), corner_pt, color=ATTN_COLOR, stroke_width=6)
        gen_h = Arrow(
            corner_pt, tokens[-1].get_right() + RIGHT * 0.06,
            color=ATTN_COLOR, stroke_width=6, buff=0.0,
        )
        self.play(Create(gen_v), GrowArrow(gen_h), run_time=0.6)

        success_box = Rectangle(width=ERR_W, height=1.0, color=ATTN_COLOR,
                                fill_color=ATTN_COLOR, fill_opacity=0.3)
        success_txt = Text("КЛЕЙ", color=ATTN_COLOR, weight=BOLD, font_size=28).move_to(success_box.get_center())
        success_token = VGroup(success_box, success_txt)
        success_token.move_to(tokens[-1].get_center())

        self.play(ReplacementTransform(tokens[-1], success_token))
        self.wait(0.5)

        # Вместо штампа ошибки — зелёный итог печатанием по буквам
        summary = Text(
            "LSTM ЧАСТИЧНО РЕШИЛА ПРОБЛЕМУ ПАМЯТИ.\nНО ОБРАБОТКА ВСЁ ЕЩЁ ПОСЛЕДОВАТЕЛЬНАЯ",
            color=ATTN_COLOR, weight=BOLD, font_size=30,
        )
        summary.to_edge(DOWN, buff=0.35)

        glyphs = summary.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in glyphs], lag_ratio=0.04), run_time=2.5)
        # нормализуем сцену: разрозненные глифы прочь, текст целиком на сцену
        self.remove(*glyphs)
        self.add(summary)
        self.wait(2)

        # Очистка: всё, что осталось на экране, гаснет одновременно
        self.play(
            FadeOut(title_lstm),
            FadeOut(unit),
            FadeOut(stack_grp),
            *[FadeOut(c) for c in out_chips],
            FadeOut(gen_v),
            FadeOut(gen_h),
            FadeOut(success_token),
            FadeOut(summary),
            FadeOut(tokens[len(words) - 3]),  # НУЖНО
            FadeOut(tokens[len(words) - 2]),  # ВЫКИНУТЬ
            run_time=1,
        )
        # страховка: всё уже прозрачно — снимаем со сцены любые «двойные» корни,
        # чтобы чипы (например, ВЫКИНУТЬ) не оставались висеть над следующим экраном
        self.clear()

    def _attention_scene(self):
        """Сцена 2: трансформер — лента токенов, круг внимания, эмбеддинг контекста.

        Токены едут справа налево (лишние уходят за левый край). Примерно на 2/3
        пути слова (кроме «.» и «?») отделяются копиями без чипов и по часовой
        стрелке рассаживаются по кругу; рядом вспыхивают зелёные точки. Между
        точками растут связи, толщина и яркость — по весам внимания, значимые
        подписаны числами (вес 0.53 — внутрь круга). 3 случайные связи усилены:
        толще, ярче, хорды с большим выгибом. Справа появляется блок
        «Эмбеддинг контекста»; копии точек едут по своим связям к правой точке
        круга (хаб) — соседние по дуге кольца, дальние по изогнутой хорде,
        усиленные — с большим выгибом; от хаба одна линия в блок, блок загорается
        зелёным — и в пустом слоте «?» появляется зелёный токен [КЛЕЙ].
        Финал: слайд со списком крупных сетей на трансформерах.
        """
        title_tr = Text("ТРАНСФОРМЕР: МЕХАНИЗМ ВНИМАНИЯ", color=ATTN_COLOR,
                        weight=BOLD, font_size=40)
        title_tr.to_edge(UP)
        self.play(FadeIn(title_tr), run_time=0.7)

        words = ["КЛЕЙ", "ДЛЯ", "ЦЕХА", "ИСПОРЧЕН", ".", "НУЖНО", "ВЫКИНУТЬ", "?"]
        ERR_W = 1.5
        LANE_Y = -2.0          # уровень ленты (как в сценах RNN/LSTM)
        TRIGGER_FRAC = 0.55    # доля пути ряда до отделений (при большем прокате
                               # до блока 2/3 уводят КЛЕЙ за край кадра)

        # Круг: 6 слов без «.», слоты через 60°. Общая спираль слов закручивается
        # по часовой и посещает слоты в обратном порядке предложения, поэтому
        # КЛЕЙ встаёт внизу-слева (самый длинный путь), ВЫКИНУТЬ — слева (короткий).
        # ЦЕХА остаётся ровно справа (угол 0°) — это «правая точка»-хаб.
        circle_words = ["КЛЕЙ", "ДЛЯ", "ЦЕХА", "ИСПОРЧЕН", "НУЖНО", "ВЫКИНУТЬ"]
        importance = [0.90, 0.10, 0.20, 0.70, 0.40, 0.35]
        HUB = 2  # индекс ЦЕХА

        CIRCLE_C = np.array([-1.6, 0.60, 0.0])  # круг сжат и поднят: целиком помещается
        R = 1.70                                # между заголовком (сверху) и лентой (снизу)

        def slot_angle(k):
            return (-120 + k * 60) * DEGREES

        def slot_dot_pos(k):
            return CIRCLE_C + R * np.array([np.cos(slot_angle(k)), np.sin(slot_angle(k)), 0.0])

        RW = R + 0.34  # радиус посадки слов на кольце (до ручной досадки)

        # Ручная досадка слов у слотов: КЛЕЙ и ДЛЯ сдвинуты вдоль кольца вверх
        # от своей дуги (не перекрывая свои точки), ВЫКИНУТЬ отъехал левее точки,
        # ЦЕХА поднялся над стволом-стрелкой
        WORD_OFF = {
            0: np.array([-0.39, 0.225, 0.0]),  # КЛЕЙ
            1: np.array([0.39, 0.225, 0.0]),   # ДЛЯ
            2: np.array([0.28, 0.30, 0.0]),    # ЦЕХА
            3: np.array([0.00, 0.00, 0.0]),    # ИСПОРЧЕН
            4: np.array([0.00, 0.00, 0.0]),    # НУЖНО
            5: np.array([-0.70, 0.00, 0.0]),   # ВЫКИНУТЬ
        }

        def slot_word_pos(k):
            u = np.array([np.cos(slot_angle(k)), np.sin(slot_angle(k)), 0.0])
            return CIRCLE_C + RW * u + WORD_OFF[k]

        def weight(i, j):
            return round(np.sqrt(importance[i] * importance[j]), 2)

        # Блок эмбеддинга: правее слова ЦЕХА, центр выровнен с точкой ЦЕХА
        # по высоте — ствол-стрелка ложится ровно горизонтально
        BLOCK_POS = np.array([2.39, 0.60, 0.0])

        # --- Лента токенов: как в LSTM, стартует прижатой к правому краю ---
        tokens = VGroup()
        for word in words:
            if word == "?":  # пустой слот: бокс без знака вопроса
                box = Rectangle(width=ERR_W, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                tokens.add(VGroup(box))
            else:
                txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=28)
                box = Rectangle(width=txt.width + 0.5, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
                txt.move_to(box.get_center())
                tokens.add(VGroup(box, txt))
        tokens.arrange(RIGHT, buff=0.25)
        if tokens.width > 13.5:
            tokens.scale_to_fit_width(13.5)
        # старт: правый край ряда за экраном, головные слова уже видны
        # (стартовый вид ряда фиксирован и не зависит от позиции блока);
        # финиш: центр «?» ровно под блоком эмбеддинга
        q_start_x = 10.5
        tokens.shift(np.array([q_start_x, LANE_Y, 0.0]) - tokens[7].get_center())
        total_scroll = tokens[7].get_center()[0] - BLOCK_POS[0]
        scrolled = [0.0]

        def lane_shift(frac):
            """Очередной бит прокрутки ленты влево (доля полного пути)."""
            scrolled[0] += frac
            return tokens.animate.shift(LEFT * total_scroll * frac)

        self.play(lane_shift(0.20), run_time=1.1)

        # --- Отделение слов: ОДНА общая спиральная траектория («поезд» слов) ---
        # к этому моменту лента прошла ровно 2/3 своего пути
        self.play(lane_shift(TRIGGER_FRAC - 0.20), run_time=0.8)

        TH_IN, TH_OUT = 235.0, -120.0  # вход в закрутку и финал (слот КЛЕЙ), по часовой
        N_A, N_B = 140, 520            # сэмплов: прямой участок и спираль

        def spiral_point(theta_deg):
            """Точка спирали: радиус плавно сходит с выпуклости на радиус кольца."""
            s = (theta_deg - TH_OUT) / (TH_IN - TH_OUT)
            rr = RW + 0.16 * (s ** 1.2)
            aa = theta_deg * DEGREES
            return CIRCLE_C + rr * np.array([np.cos(aa), np.sin(aa), 0.0])

        S_APPR = np.array([8.4, -1.5, 0.0])  # старт общего пути: справа, чуть выше ленты
        E_APPR = spiral_point(TH_IN)         # точка входа в закрутку (слева-снизу круга)
        path_pts = (
            [S_APPR + (E_APPR - S_APPR) * (i / (N_A - 1)) for i in range(N_A)]
            + [spiral_point(TH_IN + (TH_OUT - TH_IN) * ((i + 1) / N_B)) for i in range(N_B)]
        )

        def rail_for(k, start_pt):
            """Общий путь для слова k: от его позиции на ленте до своего слота —
            сначала влево по общему прямому участку, затем по часовой спирали;
            для слов с ручной досадкой — короткий доводящий хвост."""
            th_k = -120 + 60 * k
            i_end = N_A - 1 + round(N_B * (TH_IN - th_k) / (TH_IN - TH_OUT))
            frac = (S_APPR[0] - start_pt[0]) / (S_APPR[0] - E_APPR[0])
            i_in = int(round(min(1.0, max(0.0, frac)) * (N_A - 1)))
            pts_k = [start_pt] + path_pts[i_in : i_end + 1]
            off = WORD_OFF[k]
            if np.any(off):
                base = path_pts[i_end]
                pts_k += [base + off * (t / 8.0) for t in range(1, 9)]
            rail = VMobject()
            rail.set_points_as_corners(pts_k)
            return rail, len(pts_k)

        word_copies = []
        detach_anims = []
        dim_anims = []
        rails = []
        lens = []
        for k, word in enumerate(circle_words):
            idx = words.index(word)
            start = tokens[idx].get_center()
            copy = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=18)  # как чипы
            copy.move_to(start)
            word_copies.append(copy)
            self.add(copy)
            rail, n_pts = rail_for(k, start)
            rails.append(rail)
            lens.append(n_pts)
            dim_anims += [m.animate.set_opacity(0.3) for m in tokens[idx]]
        n_max = max(lens)
        for k, copy in enumerate(word_copies):
            # одинаковая скорость у всех — время пропорционально длине пути:
            # слова едут «поездом», КЛЕЙ наматывает по окружности дальше всех
            detach_anims.append(MoveAlongPath(
                copy, rails[k], rate_func=linear,
                run_time=3.0 * lens[k] / n_max,
            ))
        self.play(*detach_anims, *dim_anims, lane_shift(0.11))

        # --- Зелёные точки на круге ---
        dots = VGroup()
        for k in range(len(circle_words)):
            dots.add(Dot(radius=0.085, color=ATTN_COLOR).move_to(slot_dot_pos(k)))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.12),
                  lane_shift(0.08),
                  run_time=0.9)

        # --- Связи всех со всеми, затем толщина и подписи весов ---
        # Соседние узлы — дугами по окружности (образуют круг); дальние — хорды с изгибом наружу.
        # 3 случайные связи усилены: толще, ярче, и хорды — с большим выгибом.
        links = VGroup()
        link_w = {}
        n_words = len(circle_words)

        def is_adjacent(i, j):
            return j - i == 1 or (i == 0 and j == n_words - 1)

        # Сначала собираем все пары, чтобы детерминированно выбрать 3 для усиления
        all_pairs = [(i, j) for i in range(n_words) for j in range(i + 1, n_words)]
        rng = np.random.default_rng(42)
        boost_pair_idx = set(rng.choice(len(all_pairs), size=3, replace=False).tolist())
        # какие пары с хабом усилены — для траекторий копий
        boosted_hub_pairs = set()
        for idx in boost_pair_idx:
            i, j = all_pairs[idx]
            if i == HUB or j == HUB:
                boosted_hub_pairs.add((min(i, j), max(i, j)))

        for idx, (i, j) in enumerate(all_pairs):
            w = weight(i, j)
            boosted = idx in boost_pair_idx
            if is_adjacent(i, j):
                # соседние — дуги по кольцу (60°); усиление только толщиной/яркостью
                a0 = slot_angle(j) if (i == 0 and j == n_words - 1) else slot_angle(i)
                line = Arc(radius=R, start_angle=a0, angle=60 * DEGREES,
                           arc_center=CIRCLE_C, color=ATTN_COLOR,
                           stroke_width=1.5, stroke_opacity=0.25)
            else:
                # хорда — изогнутая дуга, выгнутая наружу круга
                a, b = slot_dot_pos(i), slot_dot_pos(j)
                mid = (a + b) / 2
                d = b - a
                left_n = np.array([-d[1], d[0], 0.0])  # нормаль влево от хорды
                sign = 1.0 if np.dot(mid - CIRCLE_C, left_n) > 0 else -1.0
                # усиленные — с большим выгибом
                angle_mag = 0.45 if boosted else 0.22
                line = ArcBetweenPoints(a, b, angle=sign * angle_mag,
                                        color=ATTN_COLOR,
                                        stroke_width=1.5, stroke_opacity=0.25)
            links.add(line)
            link_w[line] = w
        self.play(Create(links, lag_ratio=0.03),
                  lane_shift(0.07),
                  run_time=1.0)

        thick_anims = []
        for idx, (line, w) in enumerate(link_w.items()):
            boosted = idx in boost_pair_idx
            extra = 6 if boosted else 0
            thick_anims.append(line.animate.set_stroke(
                width=2 + 11 * w + extra,
                opacity=min(0.95, 0.25 + 0.55 * w + (0.18 if extra else 0))))
        labels = VGroup()
        for i in range(n_words):
            for j in range(i + 1, n_words):
                w = weight(i, j)
                if w < 0.40:
                    continue
                if is_adjacent(i, j):
                    # подпись дуги — снаружи кольца на середине дуги
                    # ИСКЛЮЧЕНИЕ: вес 0.53 (ИСПОРЧЕН–НУЖНО) — внутрь круга
                    if i == 0 and j == n_words - 1:
                        m = slot_angle(j) + 30 * DEGREES
                    else:
                        m = slot_angle(i) + 30 * DEGREES
                    # 0.53 — пара (3,4) ИСПОРЧЕН–НУЖНО: внутрь круга
                    if abs(w - 0.53) < 1e-9:
                        rad = R - 0.42
                    else:
                        rad = R + 0.17
                    pos = CIRCLE_C + rad * np.array([np.cos(m), np.sin(m), 0.0])
                else:
                    a, b = slot_dot_pos(i), slot_dot_pos(j)
                    mid = (a + b) / 2
                    chord = b - a
                    perp = np.array([-chord[1], chord[0], 0.0])
                    perp /= np.linalg.norm(perp)
                    if np.dot(mid - CIRCLE_C, perp) < 0:
                        perp = -perp  # наружу круга, поверх лёгкого изгиба хорды
                    pos = mid + perp * 0.26
                lbl = Text(f"{w:.2f}", color=ATTN_COLOR, font_size=18)
                lbl.move_to(pos)
                labels.add(lbl)
        self.play(*thick_anims, FadeIn(labels),
                  lane_shift(0.05),
                  run_time=1.0)

        # --- Карточка «Слой внимания»: связи нарисованы, блока ещё нет ---
        self._card(
            "Слой внимания",
            "Это аналитический центр. Здесь слова «общаются»\n"
            "друг с другом. Каждое слово смотрит на все\n"
            "остальные слова в контексте и решает, какие из\n"
            "них важны для понимания смысла. Слово «клей»\n"
            "посмотрит на слово «выкинуть» или «нужно», чтобы\n"
            "понять свое точное значение. Таких центров в\n"
            "модели могут быть десятки или даже сотни.",
            title_color=ATTN_COLOR, hold=3.5,
            title_time=2.1, body_time=13.6,
        )

        # --- Блок «Эмбеддинг контекста» справа ---
        block_box = Rectangle(width=2.4, height=1.3, color=ATTN_COLOR,
                              fill_color=PANEL_COLOR, fill_opacity=0.5)
        block_lbl = Text("ЭМБЕДДИНГ\nКОНТЕКСТА", color=ATTN_COLOR, weight=BOLD,
                         font_size=22).move_to(block_box.get_center())
        block_grp = VGroup(block_box, block_lbl).move_to(BLOCK_POS)
        self.play(FadeIn(block_grp),
                  lane_shift(1.0 - scrolled[0]),  # финальный бит: «?» точно под блоком
                  run_time=0.8)

        # --- Копии точек едут по связям к правой точке (хабу) ---
        # Сами точки остаются в узлах; по линиям отправляются их копии.
        # Каскад: чем сильнее связь с хабом, тем раньше копия отправляется
        # и тем она ярче — яркость наследуется от толщины линии связи.
        hub_pos = slot_dot_pos(HUB)
        order = sorted(
            (k for k in range(len(circle_words)) if k != HUB),
            key=lambda k: -weight(k, HUB),
        )
        w_max = max(weight(k, HUB) for k in order)

        def ride_path(k):
            """Траектория копии: ровно по своей нарисованной связи к хабу —
            соседний узел по дуге кольца, дальний по изогнутой хорде.
            Для усиленных связей — с большим выгибом (0.45 вместо 0.22)."""
            a = dots[k].get_center()
            if is_adjacent(min(k, HUB), max(k, HUB)):
                alpha = slot_angle(k)
                delta = ((slot_angle(HUB) - alpha + PI) % TAU) - PI
                return Arc(radius=R, start_angle=alpha, angle=delta,
                           arc_center=CIRCLE_C)
            mid = (a + hub_pos) / 2
            d = hub_pos - a
            left_n = np.array([-d[1], d[0], 0.0])
            sign = 1.0 if np.dot(mid - CIRCLE_C, left_n) > 0 else -1.0
            boosted = (min(k, HUB), max(k, HUB)) in boosted_hub_pairs
            angle_mag = 0.45 if boosted else 0.22
            return ArcBetweenPoints(a, hub_pos, angle=sign * angle_mag)

        riders = VGroup()
        for k in range(len(circle_words)):
            d = Dot(radius=0.085, color=ATTN_COLOR).move_to(dots[k].get_center())
            d.set_z_index(5)
            if k != HUB:
                d.set_opacity(0.35 + 0.65 * (weight(k, HUB) / w_max))
            riders.add(d)
        self.add(riders)
        self.play(
            LaggedStart(
                *[MoveAlongPath(riders[k], ride_path(k),
                                rate_func=smooth) for k in order],
                lag_ratio=0.25,
            ),
            run_time=1.6,
        )

        # --- От хаба одна общая линия в блок; все копии уезжают по ней ---
        trunk = Arrow(hub_pos, block_box.get_left() + LEFT * 0.04,
                      color=ATTN_COLOR, stroke_width=6, buff=0.0, tip_length=0.2)
        self.play(GrowArrow(trunk), run_time=0.45)
        absorb_anims = [
            d.animate.move_to(block_box.get_center()).scale(0.3).set_opacity(0)
            for d in riders
        ]
        self.play(*absorb_anims, run_time=0.8)

        # --- Карточка «Эмбеддинг контекста»: копии точек въехали в блок ---
        self._card(
            "Эмбеддинг контекста",
            "Отражает смысл конкретного слова с учетом всех\n"
            "окружающих его слов. Например, для слова «плата»\n"
            "он будет совершенно разным в сочетаниях\n"
            "«материнская плата» и «заработная плата». Проходя\n"
            "через каждый этаж с трансформером, он все больше\n"
            "уточняется, впитывая в себя дополнительные\n"
            "значения. И на самом последнем этаже он содержит\n"
            "в себе смысл вообще всего текста. Именно его модель\n"
            "и использует, чтобы предсказать следующее слово.",
            title_color=ATTN_COLOR, hold=4,
            title_time=2.1, body_time=15.2,
        )

        # --- Блок загорается зелёным ---
        self.play(
            Indicate(block_box, color=ATTN_COLOR, scale_factor=1.06),
            block_box.animate.set_fill(PANEL_COLOR, opacity=0.75),
            run_time=0.7,
        )

        # --- Зелёная стрелка к пустой коробочке и токен [КЛЕЙ] ---
        q_token = tokens[7]
        gen_arrow = Arrow(
            block_box.get_bottom(), q_token.get_top() + UP * 0.06,
            color=ATTN_COLOR, stroke_width=6, buff=0.0, tip_length=0.2,
        )
        self.play(Create(gen_arrow), run_time=0.5)

        success_box = Rectangle(width=q_token[0].width, height=1.0,
                                color=ATTN_COLOR, fill_color=ATTN_COLOR, fill_opacity=0.3)
        success_txt = Text("КЛЕЙ", color=ATTN_COLOR, weight=BOLD, font_size=28)
        success_txt.move_to(success_box.get_center())
        success_token = VGroup(success_box, success_txt)
        success_token.move_to(q_token.get_center())

        self.play(ReplacementTransform(q_token, success_token), run_time=0.7)
        self.wait(1.2)

        # --- Очистка сцены трансформера: всё гаснет перед финальным слайдом ---
        self.play(
            FadeOut(title_tr),
            FadeOut(tokens),
            FadeOut(VGroup(*word_copies)),
            FadeOut(dots),
            FadeOut(riders),
            FadeOut(links),
            FadeOut(labels),
            FadeOut(block_grp),
            FadeOut(trunk),
            FadeOut(gen_arrow),
            FadeOut(success_token),
            run_time=1,
        )
        self.wait(0.3)

        # --- Финальный слайд (отдельная сцена на тёмном фоне): крупные сети на трансформерах ---
        final_title = Text("НА ТРАНСФОРМЕРАХ СТОЯТ", color=ATTN_COLOR,
                           weight=BOLD, font_size=40).to_edge(UP)
        models = [
            "ChatGPT / GPT-4o (OpenAI)",
            "Claude / Sonnet / Opus (Anthropic)",
            "Gemini (Google)",
            "DeepSeek (DeepSeek AI)",
            "Llama (Meta)",
            "Mistral (Mistral AI)",
            "Grok (xAI)",
        ]
        final_items = VGroup(*[
            Text(f"▸ {m}", color=TEXT_COLOR, font_size=28)
            for m in models
        ])
        final_items.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        final_items.next_to(final_title, DOWN, buff=0.8)
        final_group = VGroup(final_title, final_items)

        self.play(FadeIn(final_title), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.3)
                                for item in final_items], lag_ratio=0.15),
                  run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(final_group), run_time=0.6)
        self.clear()