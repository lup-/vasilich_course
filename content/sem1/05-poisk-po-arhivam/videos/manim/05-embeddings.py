# -*- coding: utf-8 -*-
"""Эмбеддинги: смысл в числах. Технический ролик Manim (ManimCE) для занятия 05.

Одна мысль: слова текста становятся точками, близкие по смыслу (используемые вместе) — рядом;
у точек появляются координаты — каждая точка вектор, а всё облако слов — индекс эмбеддингов;
слово «ПОРОШОК» — вектор из начала координат с числами.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 5 \
        05-embeddings.py Embeddings
"""

from manim import *


PHOSPHOR = "#B6FF3C"   # кислотно-зелёный люминофор экранов
SWAMP    = "#4A5D23"   # болотный зелёный
RUST     = "#8C4A2F"   # ржавый
DUST     = "#8A8A7A"   # пыльный серый
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
INK      = "#111111"   # чёрный контур


def bubble(text, color, font_size=34):
    """Блок с закруглённой рамкой, чёрным контуром, надписью заглавными."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


class Embeddings(Scene):
    def construct(self):
        self.word_cloud()
        self.axes_appear()
        self.index_reveal()
        self.vector_numbers()
        self.final_message()

    # --- 1. Облако слов: слова → точки (0–12 с) ------------------------------
    def word_cloud(self):
        title = Text("ЭМБЕДДИНГИ", font_size=56, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        sub = Text("СМЫСЛ В ЧИСЛАХ", font_size=30, color=BEIGE,
                   weight=BOLD).next_to(title, DOWN)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        # Слова появляются вразброс, потом превращаются в точки
        words = [
            ("ПОРОШОК", UP * 2.0 + LEFT * 1.0),
            ("МОЮЩЕЕ СРЕДСТВО", DOWN * 1.9 + RIGHT * 0.6),
            ("СТИРАЛЬНАЯ МАШИНА", UP * 0.5 + RIGHT * 3.9),
            ("НАКЛАДНАЯ", DOWN * 0.2 + LEFT * 4.2),
            ("СКЛАД", UP * 2.4 + RIGHT * 3.1),
            ("ПРИКАЗ", DOWN * 2.2 + LEFT * 3.1),
        ]
        paired = []
        for label, pos in words:
            b = bubble(label, BEIGE, font_size=24)
            b.move_to(pos)
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.35)
            paired.append((label, b))
        self.wait(0.4)

        # Близкие по смыслу (используются вместе) ложатся рядом — два «облака»
        cluster = {
            "ПОРОШОК": LEFT * 3.4 + UP * 0.6,
            "МОЮЩЕЕ СРЕДСТВО": LEFT * 3.4 + DOWN * 0.8,
            "СТИРАЛЬНАЯ МАШИНА": LEFT * 3.4 + UP * 1.9,
            "НАКЛАДНАЯ": RIGHT * 3.4 + UP * 0.6,
            "СКЛАД": RIGHT * 3.4 + DOWN * 0.8,
            "ПРИКАЗ": RIGHT * 3.4 + UP * 1.9,
        }
        dots = VGroup()
        labels = {}
        for label, b in paired:
            target = cluster[label]
            d = Dot(radius=0.17, fill_color=PHOSPHOR, fill_opacity=1.0,
                    stroke_color=INK, stroke_width=4).move_to(target)
            self.play(Transform(b, d), run_time=0.6)
            dots.add(d)
            wl = Text(label, font_size=19, color=BEIGE, weight=BOLD)
            wl.next_to(d, DOWN, buff=0.15)
            self.play(FadeIn(wl), run_time=0.25)
            labels[label] = wl
            if label == "ПОРОШОК":
                self.poroshok = d
        self.dots = dots
        self.labels = labels

        note = Text("СЛОВА → ТОЧКИ", font_size=32, color=PHOSPHOR,
                    weight=BOLD).to_edge(DOWN, buff=1.1)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(0.8)
        note2 = Text("БЛИЗКИЕ ПО СМЫСЛУ — РЯДОМ (ИХ ИСПОЛЬЗУЮТ ВМЕСТЕ)",
                     font_size=28, color=BEIGE, weight=BOLD)
        note2.next_to(note, UP, buff=0.3)
        self.play(FadeIn(note2), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(note), FadeOut(note2), run_time=0.4)

    # --- 2. Оси: у точек есть координаты (12–19 с) ---------------------------
    def axes_appear(self):
        origin = ORIGIN + DOWN * 0.4
        x_axis = Arrow(start=origin, end=origin + RIGHT * 6.4,
                       color=DUST, stroke_width=6)
        y_axis = Arrow(start=origin, end=origin + UP * 3.4,
                       color=DUST, stroke_width=6)
        x_lab = Text("ОСЬ 1", font_size=24, color=DUST, weight=BOLD)
        x_lab.next_to(x_axis.get_end(), DOWN, buff=0.2)
        y_lab = Text("ОСЬ 2", font_size=24, color=DUST, weight=BOLD)
        y_lab.next_to(y_axis.get_end(), RIGHT, buff=0.15)
        self.play(GrowArrow(x_axis), GrowArrow(y_axis), run_time=1.2)
        self.play(FadeIn(x_lab), FadeIn(y_lab), run_time=0.5)
        self.wait(1.2)

        note = Text("ТЕПЕРЬ У ТОЧЕК ЕСТЬ КООРДИНАТЫ", font_size=32,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(3.0)
        self.play(FadeOut(note), run_time=0.4)

        self.origin = origin
        self.axes = (x_axis, y_axis, x_lab, y_lab)

    # --- 3. Облако слов = индекс эмбеддингов (19–27 с) -----------------------
    def index_reveal(self):
        box = RoundedRectangle(width=10.0, height=4.4, corner_radius=0.1,
                               stroke_color=PHOSPHOR, stroke_width=6)
        box.move_to(UP * 0.7)
        self.play(Create(box), run_time=1.0)
        label = Text("ИНДЕКС ЭМБЕДДИНГОВ", font_size=30, color=PHOSPHOR,
                     weight=BOLD).next_to(box, UP, buff=0.25)
        note = Text("КАЖДАЯ ТОЧКА — ВЕКТОР", font_size=28, color=BEIGE,
                    weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(label), FadeIn(note), run_time=0.8)
        self.play(*[Flash(d, color=PHOSPHOR, line_length=0.3, num_lines=8)
                    for d in self.dots], run_time=1.0)
        note2 = Text("ОБЛАКО СЛОВ = ИНДЕКС ЭМБЕДДИНГОВ", font_size=28,
                     color=PHOSPHOR, weight=BOLD)
        note2.next_to(note, UP, buff=0.3)
        self.play(FadeIn(note2), run_time=0.6)
        self.wait(1.2)

        all_vectors = Text("ВСЕ СЛОВА СТАЛИ ВЕКТОРАМИ", font_size=28,
                           color=BEIGE, weight=BOLD)
        all_vectors.next_to(note2, UP, buff=0.3)
        self.play(FadeIn(all_vectors), run_time=0.6)
        self.wait(2.2)
        self.play(FadeOut(note), FadeOut(note2), FadeOut(all_vectors),
                  FadeOut(label), run_time=0.4)

    # --- 4. Вектор из начала координат + числа (27–35 с) ---------------------
    def vector_numbers(self):
        x_axis, y_axis, x_lab, y_lab = self.axes
        self.play(FadeOut(x_axis), FadeOut(y_axis), FadeOut(x_lab),
                  FadeOut(y_lab), run_time=0.4)

        vec = Arrow(start=self.origin, end=self.poroshok.get_center(),
                    buff=0.15, color=PHOSPHOR, stroke_width=8)
        self.play(GrowArrow(vec), run_time=1.2)

        nums = Text("[0.41, -0.87, 0.12, 0.76, …]", font_size=28,
                    color=PHOSPHOR, weight=BOLD)
        nums.next_to(self.poroshok, UP + RIGHT * 0.3, buff=0.25)
        self.play(FadeIn(nums), run_time=0.8)
        self.wait(1.0)

        note = Text("СЛОВО = ВЕКТОР ЧИСЕЛ (ЭМБЕДДИНГ)", font_size=30,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(3.6)
        self.play(FadeOut(vec), FadeOut(nums), FadeOut(note), run_time=0.4)

    # --- 5. Вывод (35–44 с) --------------------------------------------------
    def final_message(self):
        self.play(FadeOut(self.mobjects), run_time=0.4)

        main = Text("БЛИЗКИЙ СМЫСЛ — БЛИЗКИЕ ВЕКТОРЫ", font_size=48,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.4)
        self.play(FadeIn(main), run_time=1.0)
        self.wait(2.8)

        sub = Text("ОБЛАКО СЛОВ = ИНДЕКС ЭМБЕДДИНГОВ",
                   font_size=30, color=BEIGE, weight=BOLD)
        sub.next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(2.8)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
