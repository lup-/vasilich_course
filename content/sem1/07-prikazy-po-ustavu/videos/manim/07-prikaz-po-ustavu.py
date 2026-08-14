# -*- coding: utf-8 -*-
"""Приказ по уставу. Технический ролик Manim (ManimCE) для занятия 07.

Одна мысль: промпт — приказ по уставу (роль + задача + контекст + примеры);
без устава — ответ «как попало», по уставу — по делу.

Запуск:
    python -m manim render -ql --format mp4 --resolution 1920,1080 --fps 30 --seed 7 \
        07-prikaz-po-ustavu.py PrikazPoUstavu
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


class PrikazPoUstavu(Scene):
    def construct(self):
        self.zavyazka()
        self.blank()
        self.otvet_po_delu()
        self.sravnenie()
        self.final_message()

    def zavyazka(self):
        q = bubble("ГДЕ ЛЕЖИТ ПОРОШОК?", BEIGE, font_size=30)
        q.to_edge(UP, buff=1.2)
        self.play(FadeIn(q), run_time=0.8)

        bad = bubble("ВОТ ВАМ СТИХИ ПРО ПОРОШОК", RUST, font_size=26)
        bad.move_to(ORIGIN)
        self.play(FadeIn(bad), run_time=0.8)
        self.wait(0.8)

        label = Text("ПРИКАЗ КАК ПОПАЛО → ОТВЕТ КАК ПОПАЛО", font_size=32,
                     color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(label), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(q), FadeOut(bad), FadeOut(label), run_time=0.4)

    def blank(self):
        header = Text("ПРИКАЗ ПО УСТАВУ", font_size=40, color=PHOSPHOR,
                      weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(header), run_time=0.6)

        form = RoundedRectangle(width=10.0, height=5.5, corner_radius=0.15,
                                fill_color=BEIGE, fill_opacity=0.15,
                                stroke_color=INK, stroke_width=6)
        form.move_to(DOWN * 0.2)
        self.play(FadeIn(form), run_time=0.5)

        fields = [
            ("РОЛЬ", "ДЕЖУРНЫЙ СКЛАДА"),
            ("ЗАДАЧА", "СКАЖИ, ГДЕ ЛЕЖИТ ПОРОШОК"),
            ("КОНТЕКСТ", "СМЕНА, СКЛАД 3"),
            ("ПРИМЕРЫ", "ПОРОШОК-МАКС → СЕКЦИЯ B"),
        ]
        rows = VGroup()
        for name, val in fields:
            row = VGroup(
                Text(name + ":", font_size=26, color=OLIVE, weight=BOLD),
                Text(val, font_size=24, color=INK, weight=BOLD),
            ).arrange(RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(form.get_center())

        for row in rows:
            self.play(FadeIn(row), run_time=0.7)
        self.wait(0.8)

        sub = Text("РОЛЬ · ЗАДАЧА · КОНТЕКСТ · ПРИМЕРЫ", font_size=28,
                   color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(header), FadeOut(form), FadeOut(rows),
                  FadeOut(sub), run_time=0.4)

    def otvet_po_delu(self):
        order = bubble("ПРИКАЗ ПО УСТАВУ", OLIVE, font_size=24)
        order.to_edge(LEFT, buff=1.5)
        arrow = Arrow(order.get_right(), RIGHT * 0.5, color=PHOSPHOR,
                      stroke_width=8, buff=0.2)
        model = RoundedRectangle(width=3.5, height=2.5, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=0.5,
                                 stroke_color=PHOSPHOR, stroke_width=6)
        model.next_to(arrow, RIGHT, buff=0.2)
        model_t = Text("МОДЕЛЬ", font_size=22, color=BEIGE, weight=BOLD)
        model_t.move_to(model.get_center())
        self.play(FadeIn(order), GrowArrow(arrow), FadeIn(model), FadeIn(model_t),
                  run_time=1.0)

        ans = bubble("ПОРОШОК-МАКС: СКЛАД 3, СЕКЦИЯ B", PHOSPHOR, font_size=24)
        ans.next_to(model, RIGHT, buff=0.8)
        self.play(FadeIn(ans), run_time=0.8)

        label = Text("ПО УСТАВУ → ОТВЕТ ПО ДЕЛУ", font_size=32,
                     color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(label), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(order), FadeOut(arrow), FadeOut(model), FadeOut(model_t),
                  FadeOut(ans), FadeOut(label), run_time=0.4)

    def sravnenie(self):
        left_t = Text("БЕЗ УСТАВА", font_size=30, color=RUST, weight=BOLD)
        left_b = bubble("СТИХИ ПРО ПОРОШОК", RUST, font_size=22)
        left = VGroup(left_t, left_b).arrange(DOWN, buff=0.4)
        left.shift(LEFT * 3.2)

        right_t = Text("ПО УСТАВУ", font_size=30, color=PHOSPHOR, weight=BOLD)
        right_b = bubble("СКЛАД 3, СЕКЦИЯ B", PHOSPHOR, font_size=22)
        right = VGroup(right_t, right_b).arrange(DOWN, buff=0.4)
        right.shift(RIGHT * 3.2)

        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        self.wait(0.8)

        check = Text("ПРОВЕРЯЙ", font_size=34, color=BEIGE, weight=BOLD)
        check.to_edge(DOWN, buff=1.0)
        arr = Arrow(left_b.get_bottom(), check.get_top(), color=BEIGE,
                    stroke_width=6, buff=0.2)
        arr2 = Arrow(right_b.get_bottom(), check.get_top(), color=BEIGE,
                     stroke_width=6, buff=0.2)
        sub = Text("БЕЗ УСТАВА — КАК ПОПАЛО · ПО УСТАВУ — ПО ДЕЛУ",
                   font_size=24, color=BEIGE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(sub), GrowArrow(arr), GrowArrow(arr2), FadeIn(check),
                  run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(left), FadeOut(right), FadeOut(sub),
                  FadeOut(arr), FadeOut(arr2), FadeOut(check), run_time=0.4)

    def final_message(self):
        main = Text("ПРИКАЗ ПО УСТАВУ =", font_size=40, color=PHOSPHOR,
                    weight=BOLD).move_to(UP * 0.6)
        sub = Text("РОЛЬ + ЗАДАЧА + КОНТЕКСТ + ПРИМЕРЫ", font_size=34,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.6)
        self.play(FadeIn(main), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
