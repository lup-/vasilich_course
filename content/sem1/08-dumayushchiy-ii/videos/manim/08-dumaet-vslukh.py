# -*- coding: utf-8 -*-
"""Думает вслух. Технический ролик Manim (ManimCE) для занятия 08.

Одна мысль: попроси модель показать ход решения — расчёт точнее, чем ответ наобум.

Запуск:
    python -m manim render -ql --format mp4 --resolution 1920,1080 --fps 30 --seed 8 \
        08-dumaet-vslukh.py DumaetVslukh
"""

from manim import *

PHOSPHOR = "#B6FF3C"
SWAMP    = "#4A5D23"
RUST     = "#8C4A2F"
BEIGE    = "#D8C9A3"
OLIVE    = "#556B2F"
INK      = "#111111"


def bubble(text, color, font_size=28):
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


class DumaetVslukh(Scene):
    def construct(self):
        self.zavyazka()
        self.raschet()
        self.shag_za_shagom()
        self.sravnenie()
        self.final_message()

    def zavyazka(self):
        q = bubble("ХВАТИТ ЛИ ПОРОШКА ДО ПОСТАВКИ?", BEIGE, font_size=26)
        q.to_edge(UP, buff=1.0)
        self.play(FadeIn(q), run_time=0.8)

        bad = bubble("ХВАТИТ, С ЗАПАСОМ!", RUST, font_size=30)
        bad.move_to(ORIGIN)
        self.play(FadeIn(bad), run_time=0.8)
        self.wait(0.6)

        label = Text("БЕЗ РАССУЖДЕНИЙ → ОТВЕТ НАОБУМ", font_size=32,
                     color=RUST, weight=BOLD).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(label), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(q), FadeOut(bad), FadeOut(label), run_time=0.4)

    def raschet(self):
        title = Text("БУМАГА СКЛАДА", font_size=34, color=BEIGE,
                     weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        lines = [
            "17 МЕШКОВ × 25 КГ = 425 КГ",
            "12 КГ/ДЕНЬ × 6 ДНЕЙ × 3 НЕД = 216 КГ",
            "425 − 216 = 209 КГ",
        ]
        calc = VGroup()
        for line in lines:
            t = Text(line, font_size=28, color=INK, weight=BOLD)
            calc.add(t)
        calc.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(ORIGIN)

        for line in calc:
            self.play(FadeIn(line), run_time=0.7)
        self.wait(0.5)

        result = Text("ПО СЧЁТУ: ОСТАТОК 209 КГ", font_size=32,
                      color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(result), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(calc), FadeOut(result), run_time=0.4)

    def shag_za_shagom(self):
        prompt = bubble("ПОДУМАЙ ШАГ ЗА ШАГОМ", PHOSPHOR, font_size=26)
        prompt.to_edge(UP, buff=0.8)
        self.play(FadeIn(prompt), run_time=0.6)

        steps = [
            ("ШАГ 1", "17 × 25 = 425 КГ"),
            ("ШАГ 2", "12 × 6 × 3 = 216 КГ"),
            ("ШАГ 3", "425 − 216 = 209 КГ"),
        ]
        boxes = VGroup()
        for name, val in steps:
            b = VGroup(
                Text(name, font_size=24, color=OLIVE, weight=BOLD),
                Text(val, font_size=22, color=INK, weight=BOLD),
            ).arrange(DOWN, buff=0.2)
            box = RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1,
                                   fill_color=BEIGE, fill_opacity=0.2,
                                   stroke_color=INK, stroke_width=4)
            box.move_to(b.get_center())
            boxes.add(VGroup(box, b))
        boxes.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.3)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            a = Arrow(boxes[i].get_right(), boxes[i + 1].get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.15)
            arrows.add(a)

        for b in boxes:
            self.play(FadeIn(b), run_time=0.5)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.6)

        final = bubble("209 КГ", PHOSPHOR, font_size=30)
        final.next_to(boxes, DOWN, buff=0.6)
        sub = Text("ШАГ 1 · ШАГ 2 · ШАГ 3 → 209 КГ", font_size=26,
                   color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final), FadeIn(sub), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(prompt), FadeOut(boxes), FadeOut(arrows),
                  FadeOut(final), FadeOut(sub), run_time=0.4)

    def sravnenie(self):
        left_t = Text("НАОБУМ", font_size=30, color=RUST, weight=BOLD)
        left_b = bubble("ХВАТИТ, С ЗАПАСОМ!", RUST, font_size=22)
        left = VGroup(left_t, left_b).arrange(DOWN, buff=0.4)
        left.shift(LEFT * 3.5 + UP * 0.3)

        right_t = Text("ПО ШАГАМ", font_size=30, color=PHOSPHOR, weight=BOLD)
        right_b = bubble("209 КГ", PHOSPHOR, font_size=26)
        right = VGroup(right_t, right_b).arrange(DOWN, buff=0.4)
        right.shift(RIGHT * 3.5 + UP * 0.3)

        paper = bubble("ОСТАТОК: 209 КГ", BEIGE, font_size=24)
        paper.to_edge(DOWN, buff=1.2)
        check = Text("✓", font_size=56, color=PHOSPHOR, weight=BOLD)
        check.next_to(paper, RIGHT, buff=0.3)

        sub = Text("НАОБУМ — МИМО · ПО ШАГАМ — В ЯБЛОЧКО", font_size=24,
                   color=BEIGE, weight=BOLD).to_edge(UP, buff=0.5)
        arrow = Text("СВЕРЬ С БУМАГОЙ", font_size=26, color=BEIGE, weight=BOLD)
        arrow.next_to(right_b, DOWN, buff=0.5)

        self.play(FadeIn(left), FadeIn(right), FadeIn(sub), run_time=0.8)
        self.play(FadeIn(arrow), run_time=0.4)
        self.play(FadeIn(paper), FadeIn(check), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(left), FadeOut(right), FadeOut(sub),
                  FadeOut(arrow), FadeOut(paper), FadeOut(check), run_time=0.4)

    def final_message(self):
        main = Text("ПОПРОСИ ПОКАЗАТЬ ХОД РЕШЕНИЯ", font_size=38,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.4)
        sub = Text("ОТВЕТ ТОЧНЕЕ", font_size=40, color=BEIGE,
                   weight=BOLD).next_to(main, DOWN, buff=0.6)
        self.play(FadeIn(main), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
