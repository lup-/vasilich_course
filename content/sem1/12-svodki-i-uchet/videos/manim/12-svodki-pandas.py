# -*- coding: utf-8 -*-
"""Сводки pandas: как «перекручивается» таблица. Технический ролик Manim (ManimCE) для занятия 12, слайд 4.

Одна мысль: сводка — это «перекрутка» таблицы цепочкой словесных команд: читаем → смотрим → чистим →
фильтруем → группируем → считаем → проверяем. В конце цепочка складывается в одну формулу-вывод.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 12 \
        12-svodki-pandas.py SvodkiPandas
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


def make_table(rows, cols, header, colors=None):
    """Сетка ячеек rows×cols, первая строка — заголовок (люминофор)."""
    table = VGroup()
    for r in range(rows):
        row = VGroup()
        for c in range(cols):
            val = header if (r == 0 and c == 0) else ""
            col = PHOSPHOR if r == 0 else (colors if colors else BEIGE)
            if r == 0:
                col = PHOSPHOR
            row.add(cell(val, color=col))
        row.arrange(RIGHT, buff=0.0)
        table.add(row)
    table.arrange(DOWN, buff=0.0)
    return table


class SvodkiPandas(Scene):
    def construct(self):
        self.setup_sales_table()
        self.reading()
        self.cleaning()
        self.filtering()
        self.grouping()
        self.pivot()
        self.final_message()

    # --- 1. Завязка: журнал учёта (0–8 с) -------------------------------------
    def setup_sales_table(self):
        title = Text("УЧЁТ ЗАВОДА: ТАБЛИЦА ПРОДАЖ", font_size=40,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        headers = ["дата", "регион", "менеджер", "товар", "сумма"]
        data_rows = [
            ["янв", "Юг", "Петров", "глицерин", "53669"],
            ["янв", "Север", "Петров", "сода", "12490"],
            ["янв", "Центр", "Кладовщик", "глицерин", "7500"],
            ["фев", "Юг", "Петров", "порошок", "31130"],
            ["фев", "Север", "Сидоров", "глицерин", "47380"],
            ["мар", "Север", "Иванов", "глицерин", "54440"],
        ]
        rows, cols = len(data_rows) + 1, len(headers)
        table = make_table(rows, cols, None)
        # заполняем тексты
        for c, h in enumerate(headers):
            t = Text(h, font="DejaVu Sans", font_size=20, color=INK, weight=BOLD)
            t.move_to(table[0][c].get_center())
            table[0][c] = t
        for r, drow in enumerate(data_rows, start=1):
            for c, val in enumerate(drow):
                t = Text(val, font="DejaVu Sans", font_size=20, color=INK,
                         weight=BOLD)
                t.move_to(table[r][c].get_center())
                table[r][c] = t
        table.scale(0.9).move_to(ORIGIN)
        self.play(FadeIn(table), run_time=1.0)
        self.wait(1.5)

        note = Text("СВОДКА = «ПЕРЕКРУТКА» ТАБЛИЦЫ ПОД ВОПРОС",
                    font_size=28, color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(note), run_time=0.4)
        self.table = table
        self.play(FadeOut(title), run_time=0.4)

    # --- 2. Чтение (8–18 с) ---------------------------------------------------
    def reading(self):
        frame = RoundedRectangle(width=self.table.width + 0.4,
                                 height=self.table.height + 0.4,
                                 corner_radius=0.1, fill_color=PHOSPHOR,
                                 fill_opacity=0.0, stroke_color=PHOSPHOR,
                                 stroke_width=8)
        frame.move_to(self.table.get_center())
        label = bubble("DATAFRAME — ТАБЛИЦА С ИМЕНАМИ", SWAMP, font_size=26)
        label.next_to(frame, UP, buff=0.5)
        self.play(Create(frame), FadeIn(label), run_time=1.0)

        # подсветка столбцов по очереди
        for c in range(len(self.table[0])):
            col = VGroup(*[self.table[r][c] for r in range(len(self.table))])
            highlight = SurroundingRectangle(col, color=PHOSPHOR, buff=0.15,
                                             stroke_width=6)
            self.play(Create(highlight), run_time=0.5)
            self.wait(0.2)
            self.play(FadeOut(highlight), run_time=0.3)

        note = Text("ПРОЧИТАЛ → ПОСМОТРЕЛ: СТОЛБЦЫ · СТРОКИ · ТИПЫ",
                    font_size=28, color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(note), FadeOut(label), run_time=0.4)
        self.df_frame = frame

    # --- 3. Чистка (18–30 с) --------------------------------------------------
    def cleaning(self):
        label = bubble("ПОЧИСТИЛ: ДУБЛИКАТЫ ДОЛОЙ, ПРОПУСКИ — НУЛЯМИ", RUST,
                       font_size=26)
        label.next_to(self.df_frame, UP, buff=0.5)
        self.play(FadeIn(label), run_time=0.8)

        # дубликат: нижние две строки одинаковые — «сливаются» в одну
        last, prev = self.table[-1], self.table[-2]
        self.play(FadeOut(last, scale=0.5), run_time=0.8)
        self.play(prev.animate.set_opacity(1.0), run_time=0.3)
        dup_note = Text("ДУБЛИКАТЫ: 3 СТРОКИ → 1", font_size=24,
                        color=PHOSPHOR, weight=BOLD)
        dup_note.to_edge(RIGHT, buff=1.0)
        self.play(FadeIn(dup_note), run_time=0.6)

        # пропуск: одна ячейка «пустая» мигает ржавым и заполняется нулём
        empty_cell = self.table[1][4]
        for _ in range(3):
            self.play(empty_cell.animate.set_fill(RUST, opacity=0.6),
                      run_time=0.25)
            self.play(empty_cell.animate.set_fill(BEIGE, opacity=1.0),
                      run_time=0.25)
        zero = Text("0", font="DejaVu Sans", font_size=20, color=INK, weight=BOLD)
        zero.move_to(empty_cell.get_center())
        self.play(FadeIn(zero), run_time=0.4)
        miss_note = Text("ПРОПУСКИ В СУММЕ → НУЛЕМ", font_size=24,
                         color=BEIGE, weight=BOLD)
        miss_note.next_to(dup_note, DOWN, buff=0.5)
        self.play(FadeIn(miss_note), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(dup_note), FadeOut(miss_note), FadeOut(label),
                  run_time=0.4)

    # --- 4. Фильтрация (30–44 с) ----------------------------------------------
    def filtering(self):
        label = bubble("ОТФИЛЬТРОВАЛ: ТОЛЬКО НУЖНЫЕ СТРОКИ", OLIVE, font_size=26)
        label.next_to(self.df_frame, UP, buff=0.5)
        self.play(FadeIn(label), run_time=0.8)

        keep_regions = ["Север"]
        for r in range(1, len(self.table)):
            cell_region = self.table[r][1]
            region = cell_region.text if isinstance(cell_region, Text) else ""
            if region not in keep_regions:
                self.play(self.table[r].animate.set_opacity(0.18), run_time=0.4)
        self.wait(0.8)
        note = Text("ОСТАЛИСЬ СТРОКИ ТОЛЬКО ПРО «СЕВЕР»", font_size=28,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(note), FadeOut(label), run_time=0.4)

    # --- 5. Группировка (44–60 с) ---------------------------------------------
    def grouping(self):
        label = bubble("СГРУППИРОВАЛ → СУММА ПО КАЖДОМУ", SWAMP, font_size=26)
        label.next_to(self.df_frame, UP, buff=0.5)
        self.play(FadeIn(label), run_time=0.8)

        # регионы и их суммы (по текущей таблице после чистки/фильтра)
        groups = {"Север": 139310, "Юг": 84800, "Центр": 72330}
        stacks = VGroup()
        for name, total in groups.items():
            stack = VGroup()
            rect = RoundedRectangle(width=3.0, height=0.9, corner_radius=0.1,
                                    fill_color=OLIVE, fill_opacity=1.0,
                                    stroke_color=INK, stroke_width=6)
            t1 = Text(name.upper(), font="DejaVu Sans", font_size=24,
                      color=INK, weight=BOLD)
            t2 = Text(str(total), font="DejaVu Sans", font_size=22,
                      color=PHOSPHOR, weight=BOLD)
            t2.next_to(t1, DOWN, buff=0.15)
            v = VGroup(t1, t2)
            v.move_to(rect.get_center())
            stack.add(rect, v)
            stacks.add(stack)
        stacks.arrange(DOWN, buff=0.8).to_edge(RIGHT, buff=1.5)
        for s in stacks:
            self.play(FadeIn(s, shift=UP * 0.3), run_time=0.7)
            self.wait(0.3)

        sort_note = Text("ОТСОРТИРОВАЛ ПО УБЫВАНИЮ", font_size=24,
                         color=BEIGE, weight=BOLD)
        sort_note.next_to(stacks, DOWN, buff=0.6)
        self.play(FadeIn(sort_note), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(label), FadeOut(sort_note), run_time=0.4)
        self.group_stacks = stacks

    # --- 6. Сводная (60–78 с) -------------------------------------------------
    def pivot(self):
        label = bubble("СВОДНАЯ: РЕГИОНЫ × МЕСЯЦЫ", PHOSPHOR, font_size=26)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        # новая сетка: регионы в строках, месяцы в столбцах
        rows, cols = 4, 4
        grid = VGroup()
        heads = ["", "янв", "фев", "мар"]
        regions = ["Север", "Юг", "Центр"]
        values = [["52870", "47380", "54440"],
                  ["53669", "31130", "0"],
                  ["7500", "0", "54854"]]
        for r in range(rows):
            row = VGroup()
            for c in range(cols):
                if r == 0 and c == 0:
                    txt = ""
                elif r == 0:
                    txt = heads[c]
                elif c == 0:
                    txt = regions[r - 1]
                else:
                    txt = values[r - 1][c - 1]
                is_head = (r == 0 or c == 0)
                col = PHOSPHOR if is_head else BEIGE
                row.add(cell(txt, color=col))
            row.arrange(RIGHT, buff=0.0)
            grid.add(row)
        grid.arrange(DOWN, buff=0.0).scale(0.9)
        grid.move_to(LEFT * 2.2)
        self.play(FadeIn(grid), run_time=1.2)

        note = Text("СТРОКИ — РЕГИОНЫ, СТОЛБЦЫ — МЕСЯЦЫ, В ЯЧЕЙКАХ СУММЫ",
                    font_size=26, color=BEIGE, weight=BOLD)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(label), FadeOut(grid), FadeOut(note), run_time=0.4)

    # --- 7. Вывод (78–90 с) ---------------------------------------------------
    def final_message(self):
        steps = ["ЧИТАЕМ", "СМОТРИМ", "ЧИСТИМ", "ФИЛЬТРУЕМ",
                 "ГРУППИРУЕМ", "СЧИТАЕМ", "ПРОВЕРЯЕМ"]
        main = Text("СВОДКА =", font_size=44, color=PHOSPHOR, weight=BOLD)
        main.move_to(UP * 0.6)
        self.play(FadeIn(main), run_time=0.8)

        chips = VGroup()
        prev = None
        for step in steps:
            chip = bubble(step, OLIVE, font_size=24)
            if prev is None:
                chips.add(chip)
            else:
                chip.next_to(prev, RIGHT, buff=0.35)
                chips.add(chip)
            prev = chip
        chips.next_to(main, DOWN, buff=0.8).scale(0.9)
        for chip in chips:
            self.play(FadeIn(chip, shift=UP * 0.2), run_time=0.45)
        self.wait(2.0)

        check = Text("И ГЛАВНОЕ: ЧТО ПОСЧИТАЛ — ПЕРЕСЧИТАЙ!", font_size=32,
                     color=RUST, weight=BOLD)
        check.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(main), FadeOut(chips), FadeOut(check), run_time=0.5)
