# -*- coding: utf-8 -*-
"""Память диалога и окно контекста. Технический ролик Manim (ManimCE) для занятия 04.

Одна мысль: модель «помнит» диалог, потому что вместе с новым сообщением в запрос
уходит вся история сообщений плюс системный промпт. Но у входа есть потолок —
окно контекста: что не влезло, выпадает, и модель «забывает» начало.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 4 \
        04-pamyat-dialoga.py PamyatDialoga
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


class PamyatDialoga(Scene):
    def construct(self):
        self.section_title()
        self.first_request()
        self.answer_in_history()
        self.memory_works()
        self.context_window()
        self.final_message()

    # --- 1. Завязка: пульт дежурного (0–8 с) --------------------------------
    def section_title(self):
        title = Text("ПАМЯТЬ ДИАЛОГА", font_size=60, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        sub = Text("ДЕЖУРНЫЙ ПО ЦЕХУ НА ПУЛЬТЕ", font_size=34, color=BEIGE,
                   weight=BOLD).next_to(title, DOWN)
        self.play(FadeIn(title), FadeIn(sub), run_time=1.0)

        # Пульт дежурного: болотная панель со стрелочными индикаторами
        desk = RoundedRectangle(width=14.0, height=4.2, corner_radius=0.1,
                                fill_color=SWAMP, fill_opacity=1.0,
                                stroke_color=INK, stroke_width=8)
        desk.shift(DOWN * 1.6)
        lamp = Circle(radius=0.18, fill_color=PHOSPHOR, fill_opacity=1.0,
                      stroke_color=INK, stroke_width=4)
        lamp.next_to(desk, UP, buff=0.2)
        dial = Arc(radius=0.7, start_angle=PI, angle=PI, color=BEIGE,
                   stroke_width=5).next_to(desk, DOWN, buff=0.3)
        self.play(FadeIn(desk), FadeIn(lamp), FadeIn(dial), run_time=1.0)

        msg = bubble("СМЕНА СПРАШИВАЕТ", PHOSPHOR, font_size=30)
        msg.next_to(dial, DOWN, buff=0.4)
        self.play(FadeIn(msg), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(msg), FadeOut(desk), FadeOut(lamp), FadeOut(dial),
                  run_time=0.5)

    # --- 2. Первый запрос (8–22 с) -----------------------------------------
    def first_request(self):
        instr = bubble("ИНСТРУКЦИЯ", OLIVE, font_size=30)
        instr.to_edge(UP, buff=0.9)
        instr.shift(LEFT * 4.6)
        instr_sub = Text("(СИСТЕМНЫЙ ПРОМПТ)", font_size=24, color=BEIGE,
                         weight=BOLD).next_to(instr, DOWN, buff=0.15)
        model = RoundedRectangle(width=4.4, height=3.4, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.shift(RIGHT * 3.4)
        model_t = Text("МОДЕЛЬ", font_size=44, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(instr), FadeIn(instr_sub), FadeIn(model),
                  FadeIn(model_t), run_time=1.0)

        # Инструкция всегда идёт первой: ИНСТРУКЦИЯ → МОДЕЛЬ
        a_instr = Arrow(start=instr.get_bottom(), end=model.get_top(),
                        color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(a_instr), run_time=1.0)
        self.wait(1.0)

        # Вопрос 1 от смены
        q1 = bubble("ВОПРОС 1: СКОЛЬКО ВОДЫ В СТИРКУ?", BEIGE, font_size=28)
        q1.shift(LEFT * 5.2).align_to(model, UP).shift(UP * 0.2)
        label_q = Text("ЗАПРОС 1", font_size=28, color=PHOSPHOR,
                       weight=BOLD).next_to(q1, UP, buff=0.2)
        self.play(FadeIn(q1), FadeIn(label_q), run_time=1.0)

        # Вопрос и инструкция уходят в модель
        self.play(q1.animate.move_to(model.get_center()),
                  label_q.animate.move_to(model.get_center()),
                  run_time=1.5)
        self.wait(1.0)

        # Ответ из модели
        a1 = bubble("ОТВЕТ 1", PHOSPHOR, font_size=30)
        a1.next_to(model, RIGHT, buff=1.0).shift(UP * 0.6)
        arrow_out = Arrow(start=model.get_right(), end=a1.get_left(),
                          color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(FadeOut(q1), FadeOut(label_q), run_time=0.4)
        self.play(GrowArrow(arrow_out), FadeIn(a1), run_time=1.0)
        self.wait(1.5)

        self.first_state = (instr, instr_sub, a_instr, model, model_t,
                            arrow_out, a1)

    # --- 3. Ответ в истории (22–38 с) --------------------------------------
    def answer_in_history(self):
        instr, instr_sub, a_instr, model, model_t, arrow_out, a1 = self.first_state

        # История диалога: стопка сообщений внизу справа
        hist = bubble("ИСТОРИЯ ДИАЛОГА", DUST, font_size=28)
        hist.to_edge(DOWN, buff=0.9).shift(RIGHT * 3.4)
        hdr = Text("ИСТОРИЯ: ОТВЕТ 1", font_size=26, color=BEIGE,
                   weight=BOLD).next_to(hist, DOWN, buff=0.15)
        self.play(FadeIn(hist), FadeIn(hdr), run_time=1.0)

        # ОТВЕТ 1 ложится в историю
        self.play(a1.animate.next_to(hist, UP, buff=0.3),
                  arrow_out.animate.set_opacity(0.3), run_time=1.0)
        self.wait(0.8)

        # Вопрос 2
        q2 = bubble("ВОПРОС 2", BEIGE, font_size=28)
        q2.shift(LEFT * 5.2).align_to(model, UP).shift(UP * 0.2)
        self.play(FadeIn(q2), run_time=0.8)

        # Вся история + вопрос 2 собираются в один запрос к модели
        req = VGroup(instr.copy(), q2.copy(), a1.copy())
        req.sort(lambda m: (m.get_x(), m.get_y()))
        req.move_to(model.get_center())
        label = Text("ЗАПРОС 2 = ИНСТРУКЦИЯ + ВОПРОС 1 + ОТВЕТ 1 + ВОПРОС 2",
                     font_size=26, color=PHOSPHOR, weight=BOLD)
        label.next_to(model, DOWN, buff=0.6)
        self.play(Indicate(q2, color=PHOSPHOR), run_time=1.0)
        self.play(FadeIn(label), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(label), FadeOut(q2), run_time=0.5)

        # Ответ 2
        a2 = bubble("ОТВЕТ 2", PHOSPHOR, font_size=30)
        a2.next_to(model, RIGHT, buff=1.0).shift(DOWN * 0.2)
        self.play(GrowArrow(arrow_out), FadeIn(a2), run_time=1.0)
        self.play(a2.animate.next_to(hist, UP, buff=0.3), run_time=1.0)
        self.play(FadeOut(hdr), run_time=0.4)
        hdr2 = Text("ИСТОРИЯ: ОТВЕТ 1, ОТВЕТ 2", font_size=26, color=BEIGE,
                    weight=BOLD).next_to(hist, DOWN, buff=0.15)
        self.play(FadeIn(hdr2), run_time=1.0)
        self.wait(1.5)

        self.second_state = (instr, instr_sub, a_instr, model, model_t,
                             arrow_out, a1, a2, hist, hdr2)

    # --- 4. Память работает (38–52 с) --------------------------------------
    def memory_works(self):
        (instr, instr_sub, a_instr, model, model_t, arrow_out,
         a1, a2, hist, hdr2) = self.second_state

        # Вопрос 3 ссылается на начало разговора
        q3 = bubble("ВОПРОС 3: А ЧЕГО Я В НАЧАЛЕ СПРАШИВАЛ?", BEIGE, font_size=28)
        q3.shift(LEFT * 5.2).align_to(model, UP).shift(UP * 0.2)
        self.play(FadeIn(q3), run_time=0.8)
        self.play(Indicate(q3, color=PHOSPHOR), run_time=1.0)

        self.play(q3.animate.move_to(model.get_center()), run_time=1.2)
        self.play(FadeOut(q3), run_time=0.4)

        # Модель отвечает, опираясь на историю
        a3 = bubble("ОТВЕТ 3: ПРО ВОДУ ДЛЯ СТИРКИ, МОЛОДЁЖЬ", PHOSPHOR,
                    font_size=26)
        a3.next_to(model, RIGHT, buff=1.0).shift(DOWN * 0.6)
        self.play(GrowArrow(arrow_out), FadeIn(a3), run_time=1.0)
        self.wait(1.5)

        note = Text("ПОМНИТ, ПОТОМУ ЧТО ИСТОРИЯ В ЗАПРОСЕ", font_size=34,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(1.5)

        self.final_state = (instr, instr_sub, a_instr, model, model_t,
                            arrow_out, a1, a2, a3, hist, hdr2, note)

    # --- 5. Окно контекста (52–70 с) ---------------------------------------
    def context_window(self):
        (instr, instr_sub, a_instr, model, model_t, arrow_out,
         a1, a2, a3, hist, hdr2, note) = self.final_state

        self.play(FadeOut(note), run_time=0.4)

        # Окно контекста: пунктирная рамка «входа» слева от модели
        window = DashedVMobject(
            RoundedRectangle(width=7.4, height=4.6, corner_radius=0.1,
                             stroke_color=PHOSPHOR, stroke_width=5))
        window.move_to(model.get_center() + LEFT * 3.4)
        wlabel = Text("ОКНО КОНТЕКСТА", font_size=32, color=PHOSPHOR,
                      weight=BOLD).next_to(window, UP, buff=0.2)
        budget = Text("≈ 2000 ТОКЕНОВ", font_size=26, color=BEIGE,
                      weight=BOLD).next_to(wlabel, UP, buff=0.1)
        self.play(FadeIn(window), FadeIn(wlabel), FadeIn(budget), run_time=1.0)

        # Стопка входа заполняет окно: инструкция + сообщения
        items = [("ИНСТРУКЦИЯ", OLIVE), ("ВОПРОС 1", BEIGE), ("ОТВЕТ 1", DUST),
                 ("ВОПРОС 2", BEIGE), ("ОТВЕТ 2", DUST), ("ВОПРОС 3", BEIGE),
                 ("ОТВЕТ 3", DUST)]
        placed = VGroup()
        top = window.get_top() + DOWN * 0.55
        for i, (label, color) in enumerate(items):
            box = bubble(label, color, font_size=24)
            box.move_to(top + DOWN * (i * 0.40))
            self.play(FadeIn(box), run_time=0.28)
            placed.add(box)
        self.wait(1.0)

        # Окно полное: новое сообщение не влезает — старейшее выпадает
        q4 = bubble("ВОПРОС 4 (НОВЫЙ)", BEIGE, font_size=24)
        q4.move_to(window.get_bottom() + UP * 0.5)
        self.play(FadeIn(q4), run_time=0.5)

        oldest = placed[1]  # старейшее сообщение смены: ВОПРОС 1
        ghost = oldest.copy().set_color(RUST)
        ghost.move_to(oldest.get_center())
        self.play(ghost.animate.shift(DOWN * 3.2).set_opacity(0.0),
                  oldest.animate.set_fill(RUST, opacity=0.5),
                  run_time=1.2)
        fallen = bubble("ВЫПАЛО ИЗ ОКНА: МОДЕЛЬ ЗАБЫЛА НАЧАЛО", RUST, font_size=24)
        fallen.next_to(window, DOWN, buff=0.3)
        self.play(FadeIn(fallen), run_time=0.8)

        note2 = Text("КОНТЕКСТ КОНЕЧЕН: СТАРЫЕ СООБЩЕНИЯ ВЫПАДАЮТ", font_size=32,
                     color=RUST, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note2), run_time=1.0)
        self.wait(1.5)

    # --- 6. Вывод (70–88 с) ------------------------------------------------
    def final_message(self):
        self.play(FadeOut(self.mobjects), run_time=0.4)

        main = Text("ПАМЯТЬ = ИСТОРИЯ В ЗАПРОСЕ, НО ОКНО КОНЕЧНО", font_size=52,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.4)
        self.play(FadeIn(main), run_time=1.0)
        self.wait(2.0)

        sub = Text("СТАРЫЕ СООБЩЕНИЯ ВЫПАДАЮТ · ТОКЕНЫ — ДЕНЬГИ", font_size=34,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
