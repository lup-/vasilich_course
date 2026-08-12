# -*- coding: utf-8 -*-
"""Что значат числа в эмбеддинге. Технический ролик Manim (ManimCE) для занятия 05.

Одна мысль: координата вектора — «как будто» признак (упрощение), а на деле каждая координата —
смесь признаков: что именно значит число, мы не знаем, поэтому сходство считают по всему вектору.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 5 \
        05-chisla.py Chisla
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


class Chisla(Scene):
    def construct(self):
        self.vector_coordinate()
        self.axis_science()
        self.axis_veshestvo()
        self.honest()
        self.many_numbers()

    # --- 1. Координата-признак (0–11 с) --------------------------------------
    def vector_coordinate(self):
        word = bubble("ПОРОШОК", BEIGE, font_size=36)
        word.to_edge(LEFT, buff=2.0).shift(UP * 0.4)

        emb = RoundedRectangle(width=4.6, height=3.0, corner_radius=0.1,
                               fill_color=SWAMP, fill_opacity=1.0,
                               stroke_color=INK, stroke_width=8)
        emb.shift(RIGHT * 1.2)
        emb_t = Text("ЭМБЕДДИНГ", font_size=36, color=PHOSPHOR,
                     weight=BOLD).move_to(emb)
        self.play(FadeIn(word), FadeIn(emb), FadeIn(emb_t), run_time=1.0)

        arrow = Arrow(start=word.get_right(), end=emb.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.wait(0.4)

        chunks = [Text(t, font="DejaVu Sans", font_size=30, color=DUST,
                       weight=BOLD)
                  for t in ["0.41", ",", "-0.87", ",", "0.12", ",", "0.76", ",", "…"]]
        chunks[0].set_color(PHOSPHOR)
        row = VGroup(*chunks).arrange(RIGHT, buff=0.18)
        row.next_to(emb, DOWN, buff=0.5)
        self.play(FadeIn(row, lag_ratio=0.1), run_time=1.0)

        hl = RoundedRectangle(width=chunks[0].width + 0.4,
                              height=chunks[0].height + 0.4,
                              corner_radius=0.1, stroke_color=PHOSPHOR,
                              stroke_width=5).move_to(chunks[0].get_center())
        lab = Text("ЧИСЛО №1", font_size=30, color=PHOSPHOR, weight=BOLD)
        lab.next_to(hl, UP, buff=0.3)
        self.play(Create(hl), FadeIn(lab), run_time=1.0)
        self.wait(0.8)

        note = Text("КАЖДОЕ ЧИСЛО — КООРДИНАТА-ПРИЗНАК (УПРОЩЕНИЕ)", font_size=30,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(word), FadeOut(arrow), FadeOut(emb), FadeOut(emb_t),
                  FadeOut(row), FadeOut(hl), FadeOut(lab), FadeOut(note),
                  run_time=0.4)

    # --- Псевдо-3D «угол пространства» с тремя осями ------------------------
    def pseudo3d_space(self, highlight):
        """Три оси из одной точки (изометрия); highlight: 'x' | 'y' | 'z'."""
        O = LEFT * 2.8 + DOWN * 0.7
        X = RIGHT * 4.4
        Y = RIGHT * 1.7 + UP * 0.9
        Z = UP * 2.5
        floor = Polygon(O, O + X, O + X + Y, O + Y,
                        fill_color=SWAMP, fill_opacity=0.5,
                        stroke_color=INK, stroke_width=6)
        ends = {'x': O + X, 'y': O + Y, 'z': O + Z}
        lines = VGroup()
        for name, end in ends.items():
            active = name == highlight
            lines.add(Line(O, end,
                           stroke_color=PHOSPHOR if active else DUST,
                           stroke_width=9 if active else 5))
        label_pos = {'x': O + X + DOWN * 0.35 + RIGHT * 0.15,
                     'y': O + Y + RIGHT * 0.6 + UP * 0.3,
                     'z': O + Z + RIGHT * 0.3}[highlight]
        label = Text("ЧИСЛО №" + {"x": "1", "y": "2", "z": "3"}[highlight],
                     font_size=32, color=PHOSPHOR, weight=BOLD).move_to(label_pos)
        group = VGroup(floor, lines)
        return group, label, O, X, Y, Z

    # --- 2. Ось «научность» (11–20 с) ----------------------------------------
    def axis_science(self):
        title = Text("ЧИСЛО №1: НАУЧНЫЕ СЛОВА БЛИЗКО, ВАЛЕНКИ — ДАЛЕКО",
                     font_size=34, color=BEIGE, weight=BOLD).to_edge(UP)
        group, label, O, X, Y, Z = self.pseudo3d_space('x')
        self.play(FadeIn(title), FadeIn(group), FadeIn(label), run_time=1.0)

        near1 = bubble("ФОРМУЛА", OLIVE, font_size=26)
        near2 = bubble("ТЕОРЕМА", OLIVE, font_size=26)
        near3 = bubble("РАСЧЁТ", OLIVE, font_size=26)
        far1 = bubble("ВАЛЕНКИ", DUST, font_size=26)
        near1.move_to(O + X + UP * 0.4)
        near2.move_to(O + X + LEFT * 1.8 + UP * 0.15)
        near3.move_to(O + X + LEFT * 3.2 + UP * 0.75)
        far1.move_to(O + UP * 0.25 + RIGHT * 0.2)
        self.play(FadeIn(near1), FadeIn(near2), FadeIn(near3),
                  FadeIn(far1), run_time=1.0)
        self.play(Indicate(near1, color=PHOSPHOR), Indicate(near2, color=PHOSPHOR),
                  Indicate(near3, color=PHOSPHOR), run_time=1.0)
        self.wait(0.8)

        note = Text("У ПОХОЖИХ ПО СМЫСЛУ — ПОХОЖИЕ ЧИСЛА", font_size=32,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(group), FadeOut(label),
                  FadeOut(near1), FadeOut(near2), FadeOut(near3),
                  FadeOut(far1), FadeOut(note), run_time=0.4)

    # --- 3. Ось «вещество» (20–29 с) -----------------------------------------
    def axis_veshestvo(self):
        title = Text("ЧИСЛО №2: ВЕЩЕСТВА БЛИЗКО, НАКЛАДНАЯ — ДАЛЕКО",
                     font_size=34, color=BEIGE, weight=BOLD).to_edge(UP)
        group, label, O, X, Y, Z = self.pseudo3d_space('y')
        self.play(FadeIn(title), FadeIn(group), FadeIn(label), run_time=1.0)

        near1 = bubble("ПОРОШОК", OLIVE, font_size=26)
        near2 = bubble("СОДА", OLIVE, font_size=26)
        near3 = bubble("КИСЛОТА", OLIVE, font_size=26)
        far1 = bubble("НАКЛАДНАЯ", DUST, font_size=26)
        near1.move_to(O + Y + UP * 0.3)
        near2.move_to(O + Y + DOWN * 0.5 + LEFT * 0.2)
        near3.move_to(O + Y + UP * 0.8 + RIGHT * 0.5)
        far1.move_to(O + RIGHT * 0.3 + DOWN * 0.15)
        self.play(FadeIn(near1), FadeIn(near2), FadeIn(near3),
                  FadeIn(far1), run_time=1.0)
        self.play(Indicate(near1, color=PHOSPHOR), Indicate(near2, color=PHOSPHOR),
                  Indicate(near3, color=PHOSPHOR), run_time=1.0)
        self.wait(0.8)

        note = Text("ДРУГОЕ ЧИСЛО — ДРУГОЙ ПРИЗНАК", font_size=32,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(group), FadeOut(label),
                  FadeOut(near1), FadeOut(near2), FadeOut(near3),
                  FadeOut(far1), FadeOut(note), run_time=0.4)

    # --- 4. Честный кадр: числа = смесь признаков (29–38 с) -----------------
    def honest(self):
        main = Text("ЧТО ТОЧНО ЗНАЧИТ КАЖДОЕ ЧИСЛО — МЫ НЕ ЗНАЕМ",
                    font_size=40, color=PHOSPHOR, weight=BOLD).move_to(UP * 0.4)
        line2 = Text("ЭТО СМЕСЬ ПРИЗНАКОВ: НАУЧНОСТЬ · ЦВЕТ · ГЛЯНЦЕВОСТЬ",
                     font_size=30, color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.7)
        line3 = Text("СМЫСЛ РАЗМАЗАН ПО ВСЕМ ЧИСЛАМ СРАЗУ",
                     font_size=30, color=BEIGE, weight=BOLD).next_to(line2, DOWN, buff=0.4)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(line2), FadeIn(line3), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(main), FadeOut(line2), FadeOut(line3), run_time=0.4)

    # --- 5. Много чисел: многомерное пространство (38–46 с) -----------------
    def many_numbers(self):
        title = Text("У СЛОВА СОТНИ ЧИСЕЛ", font_size=40, color=PHOSPHOR,
                     weight=BOLD).move_to(UP * 0.5)
        vec = Text("[0.41, -0.87, 0.12, 0.76, -0.33, 0.58, 0.02, -0.19, … × 384]",
                   font_size=28, color=PHOSPHOR, weight=BOLD).next_to(title, DOWN, buff=0.8)
        sub = Text("ТОЧКА В МНОГОМЕРНОМ ПРОСТРАНСТВЕ СМЫСЛА", font_size=32,
                   color=BEIGE, weight=BOLD).next_to(vec, DOWN, buff=0.8)
        note = Text("У НАШЕЙ МОДЕЛИ — 384 ЧИСЛА", font_size=30, color=PHOSPHOR,
                    weight=BOLD).next_to(sub, DOWN, buff=0.5)
        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(vec), run_time=1.0)
        self.play(FadeIn(sub), FadeIn(note), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(vec), FadeOut(sub), FadeOut(note),
                  run_time=0.4)
