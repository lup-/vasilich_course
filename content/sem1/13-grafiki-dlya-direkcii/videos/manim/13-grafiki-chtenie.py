# -*- coding: utf-8 -*-
"""Как читать график: от сырой таблицы до визуального понимания. Технический ролик Manim (ManimCE) для занятия 13, слайд 4.

Одна мысль: цифры в таблице спрятаны — график их «достаёт»; тип графика выбирается под вопрос, а результат всегда сверяют с таблицей.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 13 \
        13-grafiki-chtenie.py GrafikiChtenie
"""

from manim import *


PHOSPHOR = "#B6FF3C"   # кислотно-зелёный люминофор экранов
SWAMP    = "#4A5D23"   # болотный зелёный
RUST     = "#8C4A2F"   # ржавый
DUST     = "#8A8A7A"   # пыльный серый
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
INK      = "#111111"   # чёрный контур


def bubble(text, color, font_size=26):
    """Блок с закруглённой рамкой, чёрным контуром, надписью заглавными."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


def cell(text, color=BEIGE, width=1.9, height=0.8):
    """Ячейка таблицы: прямоугольник с чёрным контуром и текстом."""
    t = Text(text, font="DejaVu Sans", font_size=20, color=INK, weight=BOLD)
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.05,
                            fill_color=color, fill_opacity=1.0,
                            stroke_color=INK, stroke_width=4)
    t.move_to(rect.get_center())
    return VGroup(rect, t)


class GrafikiChtenie(Scene):
    def construct(self):
        self.setup_table()
        self.questions_and_types()
        self.line_chart_anim()
        self.bar_and_pie_anim()
        self.plotly_interactive_anim()
        self.final_verification()

    # --- 1. Завязка: таблица скрывает цифры (0–10 с) ---------------------------
    def setup_table(self):
        title = Text("ТАБЛИЦА СДОХЛА: ЦИФРЫ СПРЯТАНЫ", font_size=38,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        headers = ["дата", "регион", "менеджер", "товар", "сумма"]
        rows_data = [
            ["2025-01", "Юг", "Петров", "глицерин", "53669"],
            ["2025-01", "Север", "Петров", "сода", "12490"],
            ["2025-01", "Центр", "Кладовщик", "глицерин", "7500"],
            ["2025-02", "Центр", "Петров", "глицерин", "54854"],
            ["2025-02", "Север", "Сидоров", "глицерин", "47380"],
        ]

        table = VGroup()
        for r in range(6):
            row = VGroup()
            for c in range(5):
                txt = headers[c] if r == 0 else rows_data[r - 1][c]
                col = PHOSPHOR if r == 0 else BEIGE
                row.add(cell(txt, color=col))
            row.arrange(RIGHT, buff=0.0)
            table.add(row)
        table.arrange(DOWN, buff=0.0).scale(0.85).move_to(ORIGIN)

        self.play(FadeIn(table), run_time=1.0)

        # Рамка-«взгляд» хаотично бегает по ячейкам
        eye_frame = SurroundingRectangle(table[1][4], color=RUST, stroke_width=6)
        self.play(Create(eye_frame), run_time=0.4)
        self.play(eye_frame.animate.move_to(table[3][1]), run_time=0.5)
        self.play(eye_frame.animate.move_to(table[4][4]), run_time=0.5)
        self.play(FadeOut(eye_frame), run_time=0.3)

        note = Text("ГЛАЗУ ТРУДНО СРАВНИВАТЬ СОТНИ ЧИСЕЛ", font_size=28,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(note), FadeOut(title), run_time=0.4)
        self.table = table

    # --- 2. Тип графика = Вопрос (10–24 с) ------------------------------------
    def questions_and_types(self):
        label = bubble("ТИП ГРАФИКА = ВОПРОС К ДАННЫМ", SWAMP, font_size=28)
        label.to_edge(UP)
        self.play(FadeOut(self.table), FadeIn(label), run_time=0.8)

        q1 = Text("1. КАК МЕНЯЛОСЬ ВО ВРЕМЕНИ?  →  ЛИНИЯ", font_size=24, color=PHOSPHOR, weight=BOLD)
        q2 = Text("2. КТО БОЛЬШЕ / МЕНЬШЕ?     →  СТОЛБЦЫ", font_size=24, color=BEIGE, weight=BOLD)
        q3 = Text("3. КАКИЕ ДОЛИ ОТ ЦЕЛОГО?     →  КРУГ", font_size=24, color=BEIGE, weight=BOLD)
        q4 = Text("4. КАК РАСПРЕДЕЛЕНО?         →  ГИСТОГРАММА", font_size=24, color=BEIGE, weight=BOLD)

        q_group = VGroup(q1, q2, q3, q4).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        q_group.move_to(ORIGIN)

        for q in q_group:
            self.play(FadeIn(q, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(1.5)
        self.play(FadeOut(q_group), FadeOut(label), run_time=0.5)

    # --- 3. Линейный график (24–42 с) ----------------------------------------
    def line_chart_anim(self):
        label = bubble("ПРОДАЖИ ПО МЕСЯЦАМ: ПРОВАЛ В ЯНВАРЕ, ПИК В МАЕ", PHOSPHOR, font_size=24)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        axes = Axes(
            x_range=[1, 12, 1],
            y_range=[50, 150, 25],
            x_length=9,
            y_length=4.5,
            axis_config={"color": DUST, "stroke_width": 4},
        ).move_to(DOWN * 0.3)

        x_labs = Text("ЯНВ  ФЕВ  МАР  АПР  МАЙ  ИЮН  ИЮЛ  АВГ  СЕН  ОКТ  НОЯ  ДЕК",
                      font_size=18, color=BEIGE, weight=BOLD)
        x_labs.next_to(axes.x_axis, DOWN, buff=0.2)

        self.play(Create(axes), FadeIn(x_labs), run_time=1.0)

        # Данные по месяцам (в тыс.)
        monthly_pts = [73.6, 133.3, 107.6, 86.3, 133.5, 117.1, 74.7, 116.8, 91.1, 120.1, 97.2, 111.2]
        coords = [axes.c2p(m, val) for m, val in enumerate(monthly_pts, start=1)]

        dots = VGroup(*[Dot(point=pt, color=PHOSPHOR, radius=0.08) for pt in coords])
        line = VMobject(color=PHOSPHOR, stroke_width=5)
        line.set_points_as_corners(coords)

        self.play(Create(dots), run_time=1.0)
        self.play(Create(line), run_time=1.5)

        # Выделение провала (январь) и пика (май)
        jan_highlight = Circle(radius=0.3, color=RUST, stroke_width=6).move_to(coords[0])
        may_highlight = Circle(radius=0.3, color=PHOSPHOR, stroke_width=6).move_to(coords[4])

        txt_jan = Text("ПРОВАЛ: 73.6К", font_size=20, color=RUST, weight=BOLD).next_to(jan_highlight, DOWN)
        txt_may = Text("ПИК: 133.5К", font_size=20, color=PHOSPHOR, weight=BOLD).next_to(may_highlight, UP)

        self.play(Create(jan_highlight), FadeIn(txt_jan), run_time=0.8)
        self.play(Create(may_highlight), FadeIn(txt_may), run_time=0.8)

        self.wait(2.0)
        self.play(FadeOut(axes), FadeOut(x_labs), FadeOut(dots), FadeOut(line),
                  FadeOut(jan_highlight), FadeOut(may_highlight), FadeOut(txt_jan),
                  FadeOut(txt_may), FadeOut(label), run_time=0.5)

    # --- 4. Столбцы + Круговая (42–60 с) --------------------------------------
    def bar_and_pie_anim(self):
        label = bubble("ЦЕНТР ЛИДИРУЕТ, ЮГ ОТСТАЁТ", SWAMP, font_size=26)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        # Левая часть: Столбчатая
        bar_center = RoundedRectangle(width=1.2, height=3.5, corner_radius=0.05, fill_color=PHOSPHOR, fill_opacity=1.0, stroke_color=INK, stroke_width=4)
        bar_north  = RoundedRectangle(width=1.2, height=2.9, corner_radius=0.05, fill_color=OLIVE, fill_opacity=1.0, stroke_color=INK, stroke_width=4)
        bar_south  = RoundedRectangle(width=1.2, height=2.6, corner_radius=0.05, fill_color=RUST, fill_opacity=1.0, stroke_color=INK, stroke_width=4)

        bars = VGroup(bar_center, bar_north, bar_south).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        bars.move_to(LEFT * 3.0 + DOWN * 0.5)

        t_c = Text("ЦЕНТР\n486К", font_size=18, color=INK, weight=BOLD).move_to(bar_center)
        t_n = Text("СЕВЕР\n402К", font_size=18, color=INK, weight=BOLD).move_to(bar_north)
        t_s = Text("ЮГ\n373К", font_size=18, color=INK, weight=BOLD).move_to(bar_south)

        bars_group = VGroup(bars, t_c, t_n, t_s)

        # Правая часть: Круговая
        pie = Sector(radius=1.8, start_angle=0, angle=TAU * 0.385, color=PHOSPHOR, stroke_width=4, stroke_color=INK)
        pie2 = Sector(radius=1.8, start_angle=TAU * 0.385, angle=TAU * 0.319, color=OLIVE, stroke_width=4, stroke_color=INK)
        pie3 = Sector(radius=1.8, start_angle=TAU * (0.385 + 0.319), angle=TAU * 0.296, color=RUST, stroke_width=4, stroke_color=INK)

        pie_group = VGroup(pie, pie2, pie3).move_to(RIGHT * 3.0 + DOWN * 0.5)

        self.play(FadeIn(bars_group, shift=UP * 0.3), FadeIn(pie_group, scale=0.8), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(bars_group), FadeOut(pie_group), FadeOut(label), run_time=0.5)

    # --- 5. Plotly Интерактив (60–76 с) ---------------------------------------
    def plotly_interactive_anim(self):
        label = bubble("PLOTLY: НАВЕДИ КУРСОР И УВИДЬ ТОЧНОЕ ЧИСЛО", PHOSPHOR, font_size=24)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        # Эмуляция окна браузера Plotly
        browser_rect = RoundedRectangle(width=10, height=5, corner_radius=0.2, fill_color=DUST, fill_opacity=0.3, stroke_color=BEIGE, stroke_width=4)
        browser_rect.move_to(DOWN * 0.2)

        curve = FunctionGraph(lambda x: 0.5 * np.sin(2 * x) + 0.2 * np.cos(5 * x), x_range=[-4, 4], color=PHOSPHOR, stroke_width=5)
        curve.move_to(browser_rect.get_center())

        self.play(Create(browser_rect), Create(curve), run_time=1.0)

        # Анимация наведения курсора
        cursor = Arrow(start=RIGHT*2 + DOWN*2, end=RIGHT*0.5 + UP*0.3, color=RUST, buff=0, stroke_width=6)
        tooltip = bubble("МАЙ 2025: 133,503 РУБ.", BEIGE, font_size=20)
        tooltip.next_to(cursor.get_end(), UP + RIGHT)

        self.play(Create(cursor), FadeIn(tooltip), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(browser_rect), FadeOut(curve), FadeOut(cursor), FadeOut(tooltip), FadeOut(label), run_time=0.5)

    # --- 6. Финальная сверка с таблицей (76–90 с) ----------------------------
    def final_verification(self):
        main_title = Text("ГРАФИК — ОТВЕТ, НО СВЕРЯЙ С ТАБЛИЦЕЙ!", font_size=36, color=RUST, weight=BOLD)
        main_title.move_to(UP * 1.5)

        chip1 = bubble("1. ВЫБЕРИ ВОПРОС", OLIVE, font_size=22)
        chip2 = bubble("2. ПОСТРОЙ ГРАФИК", OLIVE, font_size=22)
        chip3 = bubble("3. ОФОРМИ ОСИ", OLIVE, font_size=22)
        chip4 = bubble("4. СВЕРЬ С ТАБЛИЦЕЙ!", RUST, font_size=22)

        chips = VGroup(chip1, chip2, chip3, chip4).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)

        self.play(FadeIn(main_title), run_time=0.8)
        for c in chips:
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.4)

        self.wait(2.0)

        final_note = Text("НЕ ДОВЕРЯЙ КРАСИВОЙ КАРТИНКЕ БЕЗ ПРОВЕРКИ ЧИСЕЛ!", font_size=28, color=PHOSPHOR, weight=BOLD)
        final_note.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(final_note), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(main_title), FadeOut(chips), FadeOut(final_note), run_time=0.5)
