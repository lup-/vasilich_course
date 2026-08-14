# -*- coding: utf-8 -*-
"""RAG: дежурный ищет в архиве. Технический ролик Manim (ManimCE) для занятия 05.

Одна мысль: чтобы модель отвечала по документам, вопрос вместе с найденными в архиве чанками
отдают модели: RAG = вопрос + документы из архива → ответ по источникам, который можно проверить.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 5 \
        05-rag.py RagArkhyv
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


class RagArkhyv(Scene):
    def construct(self):
        self.smena()
        self.query_search()
        self.top3()
        self.generation()
        self.without_archive()
        self.final_message()

    # --- 1. Завязка: дежурный без архива (0–9 с) ----------------------------
    def smena(self):
        title = Text("RAG: ДЕЖУРНЫЙ ИЩЕТ В АРХИВЕ", font_size=48, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        desk = RoundedRectangle(width=14.0, height=4.2, corner_radius=0.1,
                                fill_color=SWAMP, fill_opacity=1.0,
                                stroke_color=INK, stroke_width=8)
        desk.shift(DOWN * 1.6)
        lamp = Circle(radius=0.18, fill_color=PHOSPHOR, fill_opacity=1.0,
                      stroke_color=INK, stroke_width=4)
        lamp.next_to(desk, UP, buff=0.2)
        self.play(FadeIn(desk), FadeIn(lamp), run_time=1.0)

        q = bubble("СКОЛЬКО ПОРОШКА ЗАКАЗАТЬ?", BEIGE, font_size=28)
        q.next_to(desk, DOWN, buff=0.4)
        self.play(FadeIn(q), run_time=1.0)
        self.wait(0.8)

        ans = bubble("ЦИФР НЕТ. АРХИВ НЕ СМОТРЕЛ.", RUST, font_size=26)
        ans.next_to(q, DOWN, buff=0.3)
        self.play(FadeIn(ans), run_time=1.0)
        note = Text("ДЕЖУРНЫЙ БЕЗ АРХИВА: ИЗ ГОЛОВЫ", font_size=28,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(q), FadeOut(ans), FadeOut(note), FadeOut(desk),
                  FadeOut(lamp), run_time=0.4)

    # --- 2. Вопрос → поиск в индексе (9–21 с) --------------------------------
    def query_search(self):
        q = bubble("СКОЛЬКО ПОРОШКА?", BEIGE, font_size=30)
        q.to_edge(LEFT, buff=1.4).shift(UP * 0.4)
        self.play(FadeIn(q), run_time=0.8)

        qv = Dot(radius=0.22, fill_color=PHOSPHOR, fill_opacity=1.0,
                 stroke_color=INK, stroke_width=4)
        qv.next_to(q, RIGHT, buff=0.7)
        label = Text("ВЕКТОР ВОПРОСА", font_size=22, color=BEIGE,
                     weight=BOLD).next_to(qv, UP, buff=0.15)
        self.play(FadeIn(qv), FadeIn(label), run_time=0.8)

        box = RoundedRectangle(width=6.2, height=4.4, corner_radius=0.1,
                               stroke_color=PHOSPHOR, stroke_width=6)
        box.to_edge(RIGHT, buff=1.2).shift(UP * 0.2)
        box_t = Text("ИНДЕКС АРХИВА", font_size=32, color=PHOSPHOR,
                     weight=BOLD).next_to(box, UP, buff=0.2)
        self.play(Create(box), FadeIn(box_t), run_time=1.0)

        dots = VGroup()
        for x in (-1.5, 0.0, 1.5):
            for y in (0.8, 0.0, -0.8):
                d = Dot(radius=0.12, fill_color=DUST, fill_opacity=1.0,
                        stroke_color=INK, stroke_width=3)
                d.move_to(box.get_center() + RIGHT * x + UP * y)
                dots.add(d)
        self.play(FadeIn(dots, lag_ratio=0.05, run_time=1.0))

        arrow = Arrow(start=qv.get_right(), end=box.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)
        note = Text("ВОПРОС → ЭМБЕДДИНГ → ПОИСК В ИНДЕКСЕ", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.2)

        self.rag_state = (q, qv, label, box, box_t, dots)
        self.play(FadeOut(note), FadeOut(arrow), run_time=0.4)

    # --- 3. Топ-3 чанка (21–33 с) --------------------------------------------
    def top3(self):
        q, qv, label, box, box_t, dots = self.rag_state
        self.play(FadeOut(q), FadeOut(label), run_time=0.3)

        top = [dots[0], dots[4], dots[7]]
        for d in top:
            d.set_fill(PHOSPHOR, opacity=1.0)
            d.set_stroke(INK, width=5)
        self.play(*[Flash(d, color=PHOSPHOR, line_length=0.4, num_lines=8)
                    for d in top], run_time=1.0)

        chunks = VGroup()
        for name, i in (("НАКЛАДНАЯ", 0), ("ИНСТРУКЦИЯ", 1), ("ПРИКАЗ", 2)):
            c = bubble("ЧАНК: " + name, OLIVE if i % 2 == 0 else DUST, font_size=22)
            c.move_to(box.get_center() + RIGHT * (i - 1) * 2.6 + UP * 0.6)
            chunks.add(c)
        self.play(FadeIn(chunks, shift=UP * 0.5), run_time=1.2)

        note = Text("ТОП-3 САМЫХ БЛИЗКИХ ЧАНКА", font_size=32, color=PHOSPHOR,
                    weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.0)

        self.rag_top = (qv, box, box_t, dots, chunks)
        self.play(FadeOut(note), FadeOut(box), FadeOut(box_t), FadeOut(dots),
                  FadeOut(chunks), run_time=0.4)

    # --- 4. Расширенная генерация (33–47 с) ----------------------------------
    def generation(self):
        model = RoundedRectangle(width=4.4, height=3.0, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.move_to(LEFT * 0.4)
        model_t = Text("МОДЕЛЬ", font_size=40, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(model), FadeIn(model_t), run_time=1.0)

        ctx = bubble("КОНТЕКСТ + ВОПРОС", BEIGE, font_size=26)
        ctx.to_edge(LEFT, buff=1.0).shift(UP * 0.6)
        self.play(FadeIn(ctx), run_time=0.8)
        arrow = Arrow(start=ctx.get_right(), end=model.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        ans = bubble("12 УЙДЁТ · ЕСТЬ 14 → 2 ОСТАНЕТСЯ", PHOSPHOR, font_size=24)
        ans.next_to(model, DOWN, buff=0.4)
        arrow2 = Arrow(start=model.get_bottom(), end=ans.get_top(),
                       color=PHOSPHOR, stroke_width=6, buff=0.15)
        self.play(GrowArrow(arrow2), FadeIn(ans), run_time=1.0)

        note = Text("RAG (Retrieval-Augmented Generation): ВОПРОС + ДОКУМЕНТЫ → ОТВЕТ ПО ИСТОЧНИКАМ", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        note2 = Text("НЕ ВЫДУМЫВАЕТ — ЧИТАЕТ АРХИВ", font_size=26, color=BEIGE,
                     weight=BOLD).next_to(note, UP, buff=0.15)
        self.play(FadeIn(note2), run_time=0.8)
        self.wait(1.4)

        self.play(FadeOut(ctx), FadeOut(ans), FadeOut(note), FadeOut(note2),
                  FadeOut(arrow), FadeOut(arrow2), FadeOut(model),
                  FadeOut(model_t), run_time=0.4)

    # --- 5. Без архива — из головы (47–60 с) ---------------------------------
    def without_archive(self):
        model = RoundedRectangle(width=4.4, height=3.0, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.move_to(LEFT * 0.4)
        model_t = Text("МОДЕЛЬ", font_size=40, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(model), FadeIn(model_t), run_time=1.0)

        q = bubble("ВОПРОС БЕЗ КОНТЕКСТА", BEIGE, font_size=26)
        q.to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        self.play(FadeIn(q), run_time=0.8)
        arrow = Arrow(start=q.get_right(), end=model.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        ans = bubble("МЕШКОВ СОРОК, НЕБОСЬ", RUST, font_size=28)
        ans.next_to(model, DOWN, buff=0.4)
        self.play(FadeIn(ans), run_time=1.0)
        self.play(ans.animate.shift(UP * 0.25), run_time=0.6)
        self.play(ans.animate.shift(DOWN * 0.25), run_time=0.6)

        cross = Text("X", font_size=90, color=RUST, weight=BOLD)
        cross.next_to(ans, RIGHT, buff=0.6)
        self.play(FadeIn(cross), run_time=0.6)
        note = Text("БЕЗ АРХИВА — ИЗ ГОЛОВЫ: МОЖЕТ ПРИВРАТЬ", font_size=30,
                    color=RUST, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        check = Text("ПРОВЕРЯЙ!", font_size=28, color=BEIGE, weight=BOLD)
        check.next_to(note, UP, buff=0.15)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # --- 6. Вывод (60–74 с) --------------------------------------------------
    def final_message(self):
        main = Text("RAG = ВОПРОС + ДОКУМЕНТЫ ИЗ АРХИВА", font_size=44,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.4)
        sub = Text("→ ОТВЕТ ПО ИСТОЧНИКАМ, КОТОРЫЙ МОЖНО ПРОВЕРИТЬ", font_size=30,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
