"""Занятие 02, слайд 6. Технический ролик «Узкое горлышко против Матрицы Внимания»
Пример для генерации: Модели нужно закончить фразу: КЛЕЙ ДЛЯ ЦЕХА ИСПОРЧЕН. ВЫКИНУТЬ ___
Правильный ответ: КЛЕЙ. Но в тексте рядом стоит слово ЦЕХ.
Сцена 1: Архитектура RNN (Ошибка контекста)
Текст на экране: РЕКУРРЕНТНАЯ СЕТЬ (RNN): ПОТЕРЯ СМЫСЛА
Визуальный ряд:
Внизу выстраиваются токены: [КЛЕЙ], [ДЛЯ], [ЦЕХА], [ИСПОРЧЕН], [ВЫКИНУТЬ]. В конце пустой слот [ ? ].
Появляются блоки RNN. Токены проходят через них последовательно.
От слова [КЛЕЙ] тянется оранжевая стрелка памяти (hidden state). Проходя через слова [ДЛЯ], [ЦЕХА], она истончается.
По мере прохождения сами токены и их блоки RNN БЛЕКНУТ (выцветают, становятся серыми и прозрачными):
самые первые почти исчезают к концу фразы — видно, что модель «забывает» начало.
К моменту, когда алгоритм доходит до слова [ВЫКИНУТЬ], стрелка от слова КЛЕЙ превращается в жалкий, едва заметный пунктир —
модель забыла начало фразы.
Генерация результата: Блок пытается предсказать следующее слово. Из-за того, что КЛЕЙ забыт, модель опирается
на самое свежее существительное в памяти — ЦЕХА.
В пустом слоте печатается красный токен: [ЦЕХ].
Анимация ошибки: Появляется красная штамп-надпись: ОШИБКА: СИСТЕМА ПРЕДЛАГАЕТ ВЫКИНУТЬ ЦЕХ.
Сцена 2: Архитектура Трансформера (Спасение ситуации)
Текст на экране: ТРАНСФОРМЕР: МЕХАНИЗМ ВНИМАНИЯ (ATTENTION)
Визуальный ряд:
Появляется единый общий зелёный блок [БЛОК SELF-ATTENTION] — он охватывает ВСЕ токены сразу.
Те же токены [КЛЕЙ], [ДЛЯ], [ЦЕХА], [ИСПОРЧЕН], [ВЫКИНУТЬ], [ ? ] расставлены ПО КРУГУ внутри блока,
каждый подписан в своём боксе.
Между КАЖДОЙ парой токенов тянутся тонкие бледно-зелёные линии связи — каждое слово видит каждое (все пары, 15 рёбер).
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
BG_COLOR = "#1A2421"       # Тёмно-болотный (фон)
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
        title_rnn = Text("РЕКУРРЕНТНАЯ СЕТЬ (RNN): ПОТЕРЯ СМЫСЛА", color=RNN_COLOR, weight=BOLD, font_size=40)
        title_rnn.to_edge(UP)
        self.play(FadeIn(title_rnn))

        # Исходные слова
        words = ["КЛЕЙ", "ДЛЯ", "ЦЕХА", "ИСПОРЧЕН.", "ВЫКИНУТЬ", "?"]

        tokens = VGroup()
        for word in words:
            box = Rectangle(width=2.0, height=1.0, color=TEXT_COLOR, fill_opacity=0.1)
            txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=30)
            txt.move_to(box.get_center())
            tokens.add(VGroup(box, txt))

        tokens.arrange(RIGHT, buff=0.3)
        tokens.move_to(DOWN * 2)

        self.play(FadeIn(tokens), run_time=1.5)
        self.wait(1)

        # Блоки RNN
        rnn_blocks = VGroup()
        for i in range(len(words)):
            block = Square(side_length=1.2, color=RNN_COLOR, fill_opacity=0.2)
            lbl = Text("RNN", color=RNN_COLOR, weight=BOLD, font_size=24).move_to(block.get_center())
            rnn_blocks.add(VGroup(block, lbl))

        rnn_blocks.arrange(RIGHT, buff=1.1)
        rnn_blocks.move_to(UP * 0.5)

        # Анимация: последовательное прохождение (конвейер)
        h_arrows = VGroup()  # Горизонтальные стрелки (скрытое состояние)

        for i in range(len(words)):
            # Токен идет в блок
            v_arrow = Arrow(tokens[i].get_top(), rnn_blocks[i].get_bottom(), color=TEXT_COLOR, buff=0.1)
            self.play(FadeIn(rnn_blocks[i]), GrowArrow(v_arrow), run_time=0.5)

            # Передача скрытого состояния следующему блоку
            if i < len(words) - 1:
                start_pt = rnn_blocks[i].get_right()
                end_pt = rnn_blocks[i + 1].get_left()

                # Имитация потери памяти (истончение и прозрачность)
                thickness = max(1.0, 8.0 - i * 1.8)
                opacity = max(0.2, 1.0 - i * 0.2)

                h_arrow = Arrow(start_pt, end_pt, color=RNN_COLOR, buff=0.1)
                h_arrow.set_stroke(width=thickness, opacity=opacity)
                h_arrows.add(h_arrow)

                self.play(GrowArrow(h_arrow), run_time=0.5)

            # Старение: уже обработанные токены и их блоки блекнут (серые и прозрачные)
            if i >= 1:
                self.age_words(tokens, rnn_blocks, i)

        self.wait(1)

        # Генерация ошибки
        error_word = "ЦЕХ"
        error_box = Rectangle(width=2.0, height=1.0, color=ERROR_COLOR, fill_color=ERROR_COLOR, fill_opacity=0.3)
        error_txt = Text(error_word, color=ERROR_COLOR, weight=BOLD, font_size=32).move_to(error_box.get_center())
        error_token = VGroup(error_box, error_txt)
        error_token.move_to(tokens[-1].get_center())

        self.play(ReplacementTransform(tokens[-1], error_token))

        # Штамп с ошибкой
        stamp = Text("ОШИБКА: СИСТЕМА ПРЕДЛАГАЕТ ВЫКИНУТЬ ЦЕХ", color=ERROR_COLOR, weight=BOLD, font_size=42)
        stamp.set_stroke(color=BLACK, width=5, background=True)
        stamp.move_to(ORIGIN)

        self.play(FadeIn(stamp, scale=2.0), run_time=0.5)
        self.wait(2)

        # Очистка сцены 1
        self.play(FadeOut(VGroup(title_rnn, rnn_blocks, h_arrows, stamp, error_token)), run_time=1)
        self.play(FadeOut(tokens[:-1]))

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

        # Токены по кругу внутри блока (каждый подписан; «?» — сверху)
        radius = 2.9
        center = panel.get_center() + UP * 0.3
        positions = [
            center + RIGHT * (radius * np.sin(PI / 3)) + UP * (radius * np.cos(PI / 3)),   # 0 КЛЕЙ — верх-право
            center + RIGHT * (radius * np.sin(PI / 3)) + DOWN * (radius * np.cos(PI / 3)),  # 1 ДЛЯ — низ-право
            center + DOWN * radius,                                                         # 2 ЦЕХА — низ
            center + LEFT * (radius * np.sin(PI / 3)) + DOWN * (radius * np.cos(PI / 3)),   # 3 ИСПОРЧЕН. — низ-лево
            center + LEFT * (radius * np.sin(PI / 3)) + UP * (radius * np.cos(PI / 3)),     # 4 ВЫКИНУТЬ — верх-лево
            center + UP * radius,                                                           # 5 ? — верх
        ]

        tokens_tr = VGroup()
        for word, pos in zip(words, positions):
            box = Rectangle(width=2.0, height=1.0, color=TEXT_COLOR, fill_opacity=0.15)
            txt = Text(word, color=TEXT_COLOR, weight=BOLD, font_size=30).move_to(box.get_center())
            g = VGroup(box, txt).move_to(pos)
            tokens_tr.add(g)

        self.play(LaggedStart(*[FadeIn(t) for t in tokens_tr], lag_ratio=0.15), run_time=1.2)
        self.wait(0.5)

        # Все пары связаны: тонкие бледно-зелёные линии «каждый видит каждого» (15 рёбер)
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
        slot = tokens_tr[5]
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
            title_tr, tokens_tr[:-1], success_token, attention_block, all_links, arc_weak, arc_strong, subtitle
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

    def age_words(self, tokens, blocks, processed):
        """Блекнут уже обработанные токены и их RNN-блоки: чем старее — тем прозрачнее и серее."""
        anims = []
        for k in range(processed):
            age = processed - k  # 1 — обработан только что, больше — старее
            darkness = min(0.9, 0.15 + age * 0.25)
            anims.append(tokens[k].animate.fade(darkness))
            anims.append(blocks[k].animate.fade(darkness))
        self.play(*anims, run_time=0.4)