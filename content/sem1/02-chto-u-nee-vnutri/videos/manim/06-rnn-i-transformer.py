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
Сцена 2: Архитектура Трансформера (Спасение ситуации)
Текст на экране: ТРАНСФОРМЕР: МЕХАНИЗМ ВНИМАНИЯ (ATTENTION)
Визуальный ряд:
Появляется единый общий зелёный блок [БЛОК SELF-ATTENTION] — он охватывает ВСЕ токены сразу.
Те же токены [КЛЕЙ], [ДЛЯ], [ЦЕХА], [ИСПОРЧЕН], [.], [НУЖНО], [ВЫКИНУТЬ], [ ? ] расставлены ПО КРУГУ внутри блока,
каждый подписан в своём боксе.
Между КАЖДОЙ парой токенов тянутся тонкие бледно-зелёные линии связи — каждое слово видит каждое (все пары, 28 рёбер).
Анимация Внимания: Начинаем генерировать ответ для слота [ ? ]. Выделяются две дуги:
тоненькая бледно-серая дуга к слову [ЦЕХА] и жирная, пульсирующая кислотно-зеленая дуга к слову [КЛЕЙ].
(Модель понимает: испорчен именно клей, значит выкидываем его).
Генерация результата: В пустом слоте уверенно печатается зелёный токен: [КЛЕЙ].
Надпись: КАЖДОЕ СЛОВО ВИДИТ ВСЕ ОСТАЛЬНЫЕ. КОНТЕКСТ НЕ ТЕРЯЕТСЯ.
Сцена 3: Итог
Визуальный ряд:
Зелёные дуги связей масштабируются, заполняя экран красивой нейросетевой паутиной.
Финальный текст в центре: НА ТРАНСФОРМЕРАХ СТОЯТ ВСЕ СОВРЕМЕННЫЕ ЯЗЫКОВЫЕ МОДЕЛИ (LLM).

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

        # --- СЦЕНА 2: Трансформер и Внимание ---

        title_tr = Text("ТРАНСФОРМЕР: МЕХАНИЗМ ВНИМАНИЯ", color=ATTN_COLOR, weight=BOLD, font_size=40)
        title_tr.to_edge(UP)
        self.play(FadeIn(title_tr))

        # Общий зелёный блок на ВСЕ токены
        panel = RoundedRectangle(
            width=13.5, height=8.5, corner_radius=0.5,
            color=ATTN_COLOR, fill_color=PANEL_COLOR, fill_opacity=0.6
        )
        panel.move_to(DOWN * 0.3)
        panel_lbl = Text("БЛОК SELF-ATTENTION (ПАРАЛЛЕЛЬНО)", color=ATTN_COLOR, weight=BOLD, font_size=32)
        panel_lbl.move_to(panel.get_top() + DOWN * 0.5)

        attention_block = VGroup(panel, panel_lbl)
        self.play(FadeIn(attention_block))

        # Токены по кругу внутри блока (каждый подписан; «?» — сверху,
        # дальше по часовой: КЛЕЙ, ДЛЯ, ЦЕХА, ., ИСПОРЧЕН, НУЖНО, ВЫКИНУТЬ)
        radius = 2.9
        center = panel.get_center() + UP * 0.3
        step_angle = PI / 4
        angles = [PI / 2 - (k + 1) * step_angle for k in range(7)] + [PI / 2]
        positions = [
            center + radius * np.array([np.cos(a), np.sin(a), 0.0])
            for a in angles
        ]

        tokens_tr = VGroup()
        for word, pos in zip(words, positions):
            box = Rectangle(width=2.0, height=1.0, color=TEXT_COLOR, fill_opacity=0.15)
            txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=30).move_to(box.get_center())
            g = VGroup(box, txt).move_to(pos)
            tokens_tr.add(g)

        self.play(LaggedStart(*[FadeIn(t) for t in tokens_tr], lag_ratio=0.15), run_time=1.2)
        self.wait(0.5)

        # Все пары связаны: тонкие бледно-зелёные линии «каждый видит каждого» (28 рёбер)
        all_links = VGroup()
        for i in range(len(tokens_tr)):
            for j in range(i + 1, len(tokens_tr)):
                line = Line(
                    tokens_tr[i].get_center(), tokens_tr[j].get_center(),
                    color=ATTN_COLOR, stroke_width=1.5, stroke_opacity=0.15
                )
                all_links.add(line)

        self.play(Create(all_links, lag_ratio=0.02), run_time=1.5)
        self.wait(0.5)

        # Анимация внимания: две дуги от слота «?»
        slot = tokens_tr[7]
        arc_weak = CurvedArrow(
            start_point=slot.get_center(),
            end_point=tokens_tr[2].get_center(),  # ЦЕХА
            angle=-PI / 4,
            color=GRAY,
            stroke_width=2
        )
        arc_strong = CurvedArrow(
            start_point=slot.get_center(),
            end_point=tokens_tr[0].get_center(),  # КЛЕЙ
            angle=-PI / 5,
            color=ATTN_COLOR,
            stroke_width=9
        )
        self.play(Create(arc_weak), Create(arc_strong), run_time=0.8)
        self.play(Indicate(arc_strong, color=ATTN_COLOR, scale_factor=1.15), run_time=1)

        # Генерация правильного ответа
        success_word = "КЛЕЙ"
        success_box = Rectangle(width=2.0, height=1.0, color=ATTN_COLOR, fill_color=ATTN_COLOR, fill_opacity=0.3)
        success_txt = Text(success_word, color=ATTN_COLOR, weight=BOLD, font_size=32).move_to(success_box.get_center())
        success_token = VGroup(success_box, success_txt)
        success_token.move_to(slot.get_center())

        self.play(ReplacementTransform(slot, success_token))

        # Вывод
        subtitle = Text("КАЖДОЕ СЛОВО ВИДИТ ВСЕ ОСТАЛЬНЫЕ. КОНТЕКСТ НЕ ТЕРЯЕТСЯ.", color=TEXT_COLOR, weight=BOLD, font_size=32)
        subtitle.next_to(attention_block, DOWN, buff=0.6)
        self.play(Write(subtitle))
        self.wait(2.5)

        # Очистка сцены 2
        self.play(FadeOut(VGroup(
            title_tr, tokens_tr, success_token, attention_block, all_links, arc_weak, arc_strong, subtitle
        )))

        # --- СЦЕНА 3: Финал (Сеть и Бум ИИ) ---

        # Рисуем паутину внимания
        dots = VGroup()
        for i in range(12):
            angle = i * (2 * PI / 12)
            dot = Dot(radius=0.1, color=ATTN_COLOR).move_to(RIGHT * 3.5 * np.cos(angle) + UP * 3.5 * np.sin(angle))
            dots.add(dot)

        lines = VGroup()
        for i in range(len(dots)):
            for j in range(i + 1, len(dots)):
                line = Line(dots[i].get_center(), dots[j].get_center(), color=ATTN_COLOR, stroke_opacity=0.15)
                lines.add(line)

        self.play(FadeIn(dots), Create(lines, run_time=2, lag_ratio=0.01))

        # Финальный текст
        final_text = Text(
            "НА ТРАНСФОРМЕРАХ СТОЯТ ВСЕ\nСОВРЕМЕННЫЕ ЯЗЫКОВЫЕ МОДЕЛИ (LLM)",
            color=TEXT_COLOR,
            weight=BOLD,
            font_size=48
        )
        final_text.set_stroke(color=BLACK, width=8, background=True)  # Чёрная обводка для читаемости поверх линий

        self.play(Write(final_text), run_time=1.5)

        # Эффект пульсации
        self.play(final_text.animate.scale(1.05), run_time=1, rate_func=there_and_back)
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

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
                )
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
              title_color=RNN_COLOR, body_color=TEXT_COLOR):
        """Карточка-пояснение: экран накрывается чёрным, печатаются заголовок и текст;
        после паузы всё исчезает и сцена продолжается ровно с места остановки."""
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
        self.play(LaggedStart(*[FadeIn(g) for g in t_glyphs], lag_ratio=0.06), run_time=1.2)
        b_glyphs = body_card.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in b_glyphs], lag_ratio=0.04), run_time=1.8)
        # нормализуем сцену: разрозненные глифы прочь, тексты целиком на сцену
        self.remove(*t_glyphs, *b_glyphs)
        self.add(title_card)
        self.add(body_card)
        self.wait(2)
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

        # Зелёная угловая стрелка: из выходных ворот вниз и влево — в слот слова
        corner_pt = np.array([out_box.get_center()[0], tokens[-1].get_center()[1], 0.0])
        gen_v = Line(out_box.get_bottom(), corner_pt, color=ATTN_COLOR, stroke_width=6)
        gen_h = Arrow(
            corner_pt, tokens[-1].get_right() + RIGHT * 0.06,
            color=ATTN_COLOR, stroke_width=6, buff=0.0,
        )
        self.play(Create(gen_v), GrowArrow(gen_h), run_time=0.6)

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

        # Выходные ворота собрали важное — вспышка и верный ответ зелёным
        self.play(Indicate(out_box, color=ATTN_COLOR, scale_factor=1.06), run_time=0.6)

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