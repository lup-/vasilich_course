# -*- coding: utf-8 -*-
"""Форматы данных: CSV, JSON, Excel. Технический ролик Manim (ManimCE) для занятия 11, слайд 4.

Одна мысль: у каждого формата свой язык — CSV «таблица в тексте», JSON «структура для машин»,
Excel «таблица с форматированием», а PDF — документ, а не таблица; формат подсказывает, как читать файл.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 11 \
        11-formaty-dannyh.py FormatyDannyh
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


class FormatyDannyh(Scene):
    def construct(self):
        self.archive_files()
        self.csv_format()
        self.json_format()
        self.excel_format()
        self.pdf_short()
        self.final_message()

    # --- 1. Архив: три файла трёх форматов (0–9 с) ----------------------------
    def archive_files(self):
        title = Text("АРХИВ ЗАВОДА: ФАЙЛЫ РАЗНЫХ ФОРМАТОВ", font_size=40,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        names = ["tovary-sklada.csv", "datchiki-ceh7.json", "ostatki-sklada.xlsx"]
        blocks = VGroup()
        for i, name in enumerate(names):
            b = bubble(name, BEIGE, font_size=26)
            if i == 0:
                blocks.add(b)
            else:
                b.next_to(blocks, RIGHT, buff=0.8)
                blocks.add(b)
        blocks.move_to(ORIGIN)
        for b in blocks:
            self.play(FadeIn(b), run_time=0.6)
        self.wait(1.2)

        note = Text("ЧТО ВНУТРИ — СМОТРИМ ПО ФОРМАТУ", font_size=28,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(note), run_time=0.4)
        self.file_blocks = blocks

    # --- 2. CSV — таблица в тексте (9–26 с) -----------------------------------
    def csv_format(self):
        self.play(FadeOut(self.file_blocks[1:]), run_time=0.4)

        label = bubble("CSV — ТАБЛИЦА В ТЕКСТЕ", SWAMP, font_size=30)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        sheet = RoundedRectangle(width=6.4, height=3.8, corner_radius=0.1,
                                 fill_color=BEIGE, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        sheet.to_edge(LEFT, buff=1.2)
        sheet_t = Text("sales.csv (блокнот)", font_size=24, color=INK,
                       weight=BOLD).next_to(sheet, UP, buff=0.3)
        rows = [
            "дата,регион,сумма",
            "2026-01-05,Москва,1500",
            "2026-01-05,СПб,900",
            "2026-01-12,Москва,2100",
        ]
        rows_v = VGroup(*[Text(r, font_size=22, color=INK, weight=BOLD)
                          for r in rows]).arrange(DOWN, buff=0.35)
        rows_v.move_to(sheet.get_center())
        header, data = rows_v[0], rows_v[1:]
        self.play(FadeIn(sheet), FadeIn(sheet_t), FadeIn(rows_v), run_time=1.0)

        comma_note = Text("СТРОКА = ЗАПИСЬ, ЗНАЧЕНИЯ ЧЕРЕЗ ЗАПЯТУЮ",
                          font_size=26, color=RUST, weight=BOLD)
        comma_note.to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        open_note = Text("ОТКРЫВАЕТСЯ ЛЮБЫМ ТЕКСТОВЫМ РЕДАКТОРОМ",
                         font_size=26, color=BEIGE, weight=BOLD)
        open_note.next_to(comma_note, DOWN, buff=0.6)
        self.play(FadeIn(comma_note), FadeIn(open_note), run_time=0.8)

        sep = Text("ВНИМАНИЕ: РАЗДЕЛИТЕЛЬ — `;` ИЛИ `,`", font_size=24,
                   color=PHOSPHOR, weight=BOLD)
        sep.next_to(open_note, DOWN, buff=0.6)
        self.play(FadeIn(sep), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(sheet), FadeOut(sheet_t), FadeOut(rows_v),
                  FadeOut(comma_note), FadeOut(open_note), FadeOut(sep),
                  FadeOut(self.file_blocks[0]), run_time=0.4)
        self.csv_label = label

    # --- 3. JSON — структура для машин (26–40 с) ------------------------------
    def json_format(self):
        self.play(FadeOut(self.csv_label), run_time=0.4)

        label = bubble("JSON — СТРУКТУРА ДЛЯ МАШИН", OLIVE, font_size=30)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        code = Code(
            code_string=(
                '[\n'
                '  {"sensor": "temp",\n'
                '   "time": "08:00",\n'
                '   "value": 23.4},\n'
                '  {"sensor": "vlag",\n'
                '   "value": 41.0}\n'
                ']'
            ),
            language="json",
            font_size=24,
            background="window",
            corner_radius=0.1,
        )
        code.to_edge(LEFT, buff=1.2)
        self.play(FadeIn(code, shift=UP * 0.3), run_time=1.0)

        kv = Text("ПАРЫ «КЛЮЧ: ЗНАЧЕНИЕ»", font_size=26, color=BEIGE, weight=BOLD)
        kv.to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        nest = Text("ВЛОЖЕННЫЕ ОБЪЕКТЫ И СПИСКИ", font_size=26, color=BEIGE,
                    weight=BOLD)
        nest.next_to(kv, DOWN, buff=0.6)
        api = Text("ОТВЕЧАЮТ ВЕБ-API", font_size=26, color=PHOSPHOR, weight=BOLD)
        api.next_to(nest, DOWN, buff=0.6)
        self.play(FadeIn(kv), FadeIn(nest), FadeIn(api), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(code), FadeOut(kv), FadeOut(nest), FadeOut(api),
                  run_time=0.4)
        self.json_label = label

    # --- 4. Excel — таблица с форматированием (40–55 с) -----------------------
    def excel_format(self):
        self.play(FadeOut(self.json_label), run_time=0.4)

        label = bubble("EXCEL — ТАБЛИЦА С ФОРМАТИРОВАНИЕМ", SWAMP, font_size=30)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        grid = VGroup()
        for r in range(3):
            row = VGroup(*[Square(side_length=0.7, fill_color=BEIGE,
                                  fill_opacity=1.0, stroke_color=INK,
                                  stroke_width=4) for _ in range(4)])
            row.arrange(RIGHT, buff=0.0)
            grid.add(row)
        grid.arrange(DOWN, buff=0.0).move_to(LEFT * 2.6)
        for cell in grid[0]:
            cell.set_fill(PHOSPHOR, opacity=0.35)
        self.play(FadeIn(grid), run_time=0.8)

        formula = Text("=СУММ(A1:A10)", font_size=24, color=INK, weight=BOLD)
        formula.next_to(grid, DOWN, buff=0.7)
        self.play(FadeIn(formula), run_time=0.8)

        tabs = VGroup(*[bubble(name, DUST, font_size=18)
                        for name in ["Остатки", "Поставки"]])
        tabs.arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.6)
        tabs[0].set_fill(PHOSPHOR, opacity=0.25)
        self.play(FadeIn(tabs), run_time=0.8)

        note = Text("ЛИСТЫ · ФОРМУЛЫ · ЦВЕТА · СТИЛИ", font_size=26,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(grid), FadeOut(formula), FadeOut(tabs), FadeOut(note),
                  run_time=0.4)
        self.excel_label = label

    # --- 5. PDF — документ, не таблица (55–65 с) ------------------------------
    def pdf_short(self):
        self.play(FadeOut(self.excel_label), run_time=0.4)

        label = bubble("PDF — ДОКУМЕНТ, НЕ ТАБЛИЦА", RUST, font_size=30)
        label.to_edge(UP)
        self.play(FadeIn(label), run_time=0.8)

        page = RoundedRectangle(width=4.4, height=5.6, corner_radius=0.1,
                                fill_color=BEIGE, fill_opacity=1.0,
                                stroke_color=INK, stroke_width=8)
        page.move_to(LEFT * 2.4)
        self.play(FadeIn(page), run_time=0.6)
        lines = VGroup()
        line_w = 3.2
        for i in range(6):
            y = page.get_center()[1] + 2.2 - i * 0.8
            lines.add(Line(LEFT * (line_w / 2), RIGHT * (line_w / 2),
                           color=DUST, stroke_width=5).move_to(
                [page.get_center()[0], y, 0]))
        self.play(FadeIn(lines), run_time=0.6)

        sealed = Text("СТРАНИЦЫ «ЗАПЕЧАТАНЫ»: ТЕКСТ И ТАБЛИЦЫ КАК КАРТИНКА",
                      font_size=24, color=RUST, weight=BOLD)
        sealed.to_edge(RIGHT, buff=0.8)
        next_l = Text("ИЗВЛЕКАТЬ ЦИФРЫ — ОТДЕЛЬНАЯ ИСТОРИЯ (ЗАНЯТИЕ 14)",
                      font_size=24, color=BEIGE, weight=BOLD)
        next_l.next_to(sealed, DOWN, buff=0.6)
        self.play(FadeIn(sealed), FadeIn(next_l), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(label), FadeOut(page), FadeOut(sealed), FadeOut(next_l),
                  run_time=0.4)

    # --- 6. Вывод (65–75 с) ---------------------------------------------------
    def final_message(self):
        main = Text("ФОРМАТ ПОДСКАЗЫВАЕТ, КАК ЧИТАТЬ ФАЙЛ", font_size=44,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.5)
        sub = Text("CSV — ТЕКСТ · JSON — СТРУКТУРА · EXCEL — ТАБЛИЦА С ФОРМАТОМ",
                   font_size=28, color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
