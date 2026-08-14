# -*- coding: utf-8 -*-
"""Как стучаться в чужие двери. Технический ролик Manim (ManimCE) для занятия 14.

Одна мысль: данные приходят из чужого API ящиком JSON; успех — по статусу; сверяй с источником.

Запуск:
    python -m manim render -ql --format mp4 --resolution 1920,1080 --fps 30 --seed 14 \
        14-rastvoritel-dlya-konkurentov-api.py ZhivyeDannyeApi
"""

from manim import *

PHOSPHOR = "#B6FF3C"
SWAMP    = "#4A5D23"
RUST     = "#8C4A2F"
BEIGE    = "#D8C9A3"
OLIVE    = "#556B2F"
INK      = "#111111"


def bubble(text, color, font_size=26):
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


class ZhivyeDannyeApi(Scene):
    def construct(self):
        self.zavyazka()
        self.zapros()
        self.statusy()
        self.json_v_tablicu()
        self.sverka()
        self.final_message()

    def zavyazka(self):
        laptop = RoundedRectangle(width=5.0, height=3.2, corner_radius=0.1,
                                  fill_color=SWAMP, fill_opacity=0.4,
                                  stroke_color=PHOSPHOR, stroke_width=6)
        laptop.shift(LEFT * 2.5)
        screen = RoundedRectangle(width=4.2, height=2.4, corner_radius=0.05,
                                  fill_color=INK, fill_opacity=0.8,
                                  stroke_color=BEIGE, stroke_width=3)
        screen.move_to(laptop.get_center() + UP * 0.2)
        door = RoundedRectangle(width=3.5, height=4.0, corner_radius=0.1,
                                fill_color=OLIVE, fill_opacity=0.5,
                                stroke_color=INK, stroke_width=6)
        door.shift(RIGHT * 3.5)
        door_t = Text("API", font_size=36, color=BEIGE, weight=BOLD)
        door_t.move_to(door.get_center())

        self.play(FadeIn(laptop), FadeIn(screen), FadeIn(door), FadeIn(door_t),
                  run_time=1.0)

        knock = Arrow(laptop.get_right(), door.get_left(), color=PHOSPHOR,
                      stroke_width=8, buff=0.3)
        self.play(GrowArrow(knock), run_time=0.8)

        label = Text("ЖИВЫЕ ДАННЫЕ: ИНТЕРНЕТ — ЕЩЁ ОДИН СКЛАД",
                     font_size=28, color=PHOSPHOR, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(label), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(laptop), FadeOut(screen), FadeOut(door), FadeOut(door_t),
                  FadeOut(knock), FadeOut(label), run_time=0.4)

    def zapros(self):
        url = Text("GET api.example.com/compound?name=acetone",
                   font_size=24, color=BEIGE, weight=BOLD).to_edge(UP, buff=1.0)
        self.play(FadeIn(url), run_time=0.6)

        client = bubble("НОУТБУК", SWAMP, font_size=22)
        client.to_edge(LEFT, buff=1.5)
        server = bubble("СЕРВЕР", OLIVE, font_size=22)
        server.to_edge(RIGHT, buff=1.5)
        self.play(FadeIn(client), FadeIn(server), run_time=0.5)

        arr = Arrow(client.get_right(), server.get_left(), color=PHOSPHOR,
                    stroke_width=8, buff=0.2)
        req = Text("ЗАПРОС", font_size=22, color=PHOSPHOR, weight=BOLD)
        req.next_to(arr, UP, buff=0.1)
        self.play(GrowArrow(arr), FadeIn(req), run_time=0.7)

        status = bubble("200 OK", PHOSPHOR, font_size=24)
        status.next_to(server, DOWN, buff=0.5)
        json_box = RoundedRectangle(width=3.0, height=2.0, corner_radius=0.1,
                                    fill_color=BEIGE, fill_opacity=0.3,
                                    stroke_color=INK, stroke_width=5)
        json_box.next_to(status, DOWN, buff=0.3)
        json_t = Text("{ JSON }", font_size=28, color=INK, weight=BOLD)
        json_t.move_to(json_box.get_center())
        arr2 = Arrow(server.get_bottom(), status.get_top(), color=BEIGE,
                     stroke_width=6, buff=0.15)
        self.play(GrowArrow(arr2), FadeIn(status), run_time=0.6)
        self.play(FadeIn(json_box), FadeIn(json_t), run_time=0.5)

        sub = Text("ЗАПРОС: URL + ПАРАМЕТРЫ → СТАТУС → JSON", font_size=26,
                   color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(url), FadeOut(client), FadeOut(server), FadeOut(arr),
                  FadeOut(req), FadeOut(arr2), FadeOut(status), FadeOut(json_box),
                  FadeOut(json_t), FadeOut(sub), run_time=0.4)

    def statusy(self):
        title = Text("КОДЫ ОТВЕТА", font_size=36, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        items = [
            ("200", "УСПЕХ", PHOSPHOR),
            ("404", "НЕТ ТАКОГО", RUST),
            ("401", "НЕТ ДОСТУПА", RUST),
            ("429", "ПОДОЖДИ", RUST),
        ]
        rows = VGroup()
        for code, desc, color in items:
            row = VGroup(
                bubble(code, color, font_size=22),
                Text(desc, font_size=24, color=INK, weight=BOLD),
            ).arrange(RIGHT, buff=0.5)
            rows.add(row)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(ORIGIN)

        for row in rows:
            self.play(FadeIn(row), run_time=0.4)
        self.wait(0.5)

        sub = Text("200 — УСПЕХ · 404 — НЕТ ТАКОГО · 429 — ПОДОЖДИ",
                   font_size=24, color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(title), FadeOut(rows), FadeOut(sub), run_time=0.4)

    def json_v_tablicu(self):
        box = RoundedRectangle(width=3.5, height=2.8, corner_radius=0.1,
                               fill_color=BEIGE, fill_opacity=0.25,
                               stroke_color=INK, stroke_width=6)
        box.to_edge(LEFT, buff=1.2)
        pairs = VGroup(
            Text("name: acetone", font_size=20, color=INK, weight=BOLD),
            Text("formula: C3H6O", font_size=20, color=INK, weight=BOLD),
            Text("mass: 58.08", font_size=20, color=INK, weight=BOLD),
            Text("smiles: CC(=O)C", font_size=20, color=INK, weight=BOLD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pairs.move_to(box.get_center())
        json_lbl = Text("{ JSON }", font_size=24, color=OLIVE, weight=BOLD)
        json_lbl.next_to(box, UP, buff=0.2)

        self.play(FadeIn(box), FadeIn(pairs), FadeIn(json_lbl), run_time=0.8)

        arrow = Arrow(box.get_right(), RIGHT * 1.5, color=PHOSPHOR,
                      stroke_width=8, buff=0.2)
        self.play(GrowArrow(arrow), run_time=0.5)

        headers = ["ПОЛЕ", "ЗНАЧЕНИЕ"]
        data = [("name", "acetone"), ("formula", "C3H6O"),
                ("mass", "58.08"), ("smiles", "CC(=O)C")]
        table_rows = VGroup()
        hdr = VGroup(*[Text(h, font_size=20, color=PHOSPHOR, weight=BOLD)
                        for h in headers]).arrange(RIGHT, buff=1.8)
        table_rows.add(hdr)
        for k, v in data:
            row = VGroup(
                Text(k, font_size=18, color=INK, weight=BOLD),
                Text(v, font_size=18, color=INK, weight=BOLD),
            ).arrange(RIGHT, buff=1.2)
            table_rows.add(row)
        table_rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        table_rows.next_to(arrow, RIGHT, buff=0.3)
        border = SurroundingRectangle(table_rows, color=INK, stroke_width=4,
                                      buff=0.2, corner_radius=0.1)
        self.play(FadeIn(table_rows), FadeIn(border), run_time=0.8)

        sub = Text("JSON → ТАБЛИЦА pandas", font_size=28, color=BEIGE,
                   weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(box), FadeOut(pairs), FadeOut(json_lbl),
                  FadeOut(arrow), FadeOut(table_rows), FadeOut(border),
                  FadeOut(sub), run_time=0.4)

    def sverka(self):
        our = bubble("ТАБЛИЦА: C3H6O", BEIGE, font_size=24)
        our.shift(LEFT * 2.5)
        truth = bubble("PUBCHEM: C3H6O", PHOSPHOR, font_size=24)
        truth.shift(RIGHT * 2.5)
        check = Text("✓", font_size=64, color=PHOSPHOR, weight=BOLD)
        check.move_to(ORIGIN + DOWN * 0.5)

        self.play(FadeIn(our), FadeIn(truth), run_time=0.6)
        arr1 = Arrow(our.get_bottom(), check.get_top(), color=BEIGE, stroke_width=5, buff=0.15)
        arr2 = Arrow(truth.get_bottom(), check.get_top(), color=BEIGE, stroke_width=5, buff=0.15)
        self.play(GrowArrow(arr1), GrowArrow(arr2), FadeIn(check), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(our), FadeOut(truth), FadeOut(check),
                  FadeOut(arr1), FadeOut(arr2), run_time=0.4)

    def final_message(self):
        main = Text("СВЕРЯЙ С ИСТОЧНИКОМ", font_size=42, color=PHOSPHOR,
                    weight=BOLD).move_to(UP * 0.4)
        sub = Text("НЕ ДОВЕРЯЙ ЧЕРТУ НА СЛОВО", font_size=34,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.6)
        self.play(FadeIn(main), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
