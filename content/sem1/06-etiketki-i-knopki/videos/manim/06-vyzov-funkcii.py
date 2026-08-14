# -*- coding: utf-8 -*-
"""Вызов функций: руки для модели. Технический ролик Manim (ManimCE) для занятия 06.

Одна мысль: модель сама решает, что нужна функция «склад», формирует вызов, программа выполняет её
и возвращает реальный результат, модель отвечает по нему; без функции — «из головы», и это надо проверять.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 6 \
        06-vyzov-funkcii.py VyzovFunkcii
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


class VyzovFunkcii(Scene):
    def construct(self):
        self.zavyazka()
        self.model_reshaet()
        self.programma_vypolnyaet()
        self.otvet_modeli()
        self.without_function()
        self.final_message()

    # --- 1. Завязка: смена спрашивает, дежурный без кнопки (0–8 с) -----------
    def zavyazka(self):
        title = Text("ВЫЗОВ ФУНКЦИЙ: РУКИ ДЛЯ МОДЕЛИ", font_size=44,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        desk = RoundedRectangle(width=12.0, height=3.4, corner_radius=0.1,
                                fill_color=SWAMP, fill_opacity=1.0,
                                stroke_color=INK, stroke_width=8)
        desk.shift(DOWN * 1.4)
        lamp = Circle(radius=0.18, fill_color=PHOSPHOR, fill_opacity=1.0,
                      stroke_color=INK, stroke_width=4)
        lamp.next_to(desk, UP, buff=0.2)
        self.play(FadeIn(desk), FadeIn(lamp), run_time=1.0)

        q = bubble("КАКИЕ ПОЗИЦИИ ЕСТЬ НА СКЛАДЕ?", BEIGE, font_size=26)
        q.next_to(desk, DOWN, buff=0.4)
        self.play(FadeIn(q), run_time=1.0)

        ans = bubble("ЖИВОГО СПИСКА НЕТ", RUST, font_size=26)
        ans.next_to(q, DOWN, buff=0.3)
        self.play(FadeIn(ans), run_time=1.0)
        note = Text("СМЕНА СПРАШИВАЕТ · ДЕЖУРНЫЙ БЕЗ КНОПКИ", font_size=28,
                    color=BEIGE, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.0)

        self.play(FadeOut(q), FadeOut(ans), FadeOut(note), FadeOut(desk),
                  FadeOut(lamp), run_time=0.4)

    # --- 2. Модель решает: вызвать функцию (8–22 с) --------------------------
    def model_reshaet(self):
        model = RoundedRectangle(width=4.2, height=3.0, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.move_to(LEFT * 0.4)
        model_t = Text("МОДЕЛЬ", font_size=40, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(model), FadeIn(model_t), run_time=1.0)

        q = bubble("КАКИЕ ПОЗИЦИИ ЕСТЬ?", BEIGE, font_size=26)
        q.to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        self.play(FadeIn(q), run_time=0.8)
        arrow = Arrow(start=q.get_right(), end=model.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        vyzov = bubble("ФУНКЦИЯ: СКЛАД · tovar = «порошок стиральный»", OLIVE, font_size=22)
        vyzov.next_to(model, DOWN, buff=0.4)
        arrow2 = Arrow(start=model.get_bottom(), end=vyzov.get_top(),
                       color=PHOSPHOR, stroke_width=6, buff=0.15)
        self.play(GrowArrow(arrow2), FadeIn(vyzov), run_time=1.0)

        note = Text("МОДЕЛЬ РЕШАЕТ: ВЫЗВАТЬ ФУНКЦИЮ · ПРОВЕРЯЕТ ПОЗИЦИИ ПО ОДНОЙ", font_size=28,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.2)

        self.model_state = (model, model_t, vyzov)
        self.play(FadeOut(q), FadeOut(arrow), FadeOut(note), run_time=0.4)

    # --- 3. Программа выполняет функцию (22–38 с) ----------------------------
    def programma_vypolnyaet(self):
        model, model_t, vyzov = self.model_state

        script = RoundedRectangle(width=4.2, height=3.0, corner_radius=0.1,
                                  fill_color=DUST, fill_opacity=1.0,
                                  stroke_color=INK, stroke_width=8)
        script.to_edge(RIGHT, buff=1.2)
        script_t = Text("СКРИПТ", font_size=40, color=INK, weight=BOLD).move_to(script)
        self.play(FadeIn(script), FadeIn(script_t), run_time=1.0)

        arrow = Arrow(start=vyzov.get_right(), end=script.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        file = bubble("ФАЙЛ СКЛАДА\nsklad.csv", BEIGE, font_size=24)
        file.next_to(script, DOWN, buff=0.5)
        self.play(FadeIn(file), run_time=0.8)

        res = bubble("КАРТОЧКА: ПОРОШОК СТИРАЛЬНЫЙ · ЕСТЬ (14)", PHOSPHOR, font_size=22)
        res.next_to(file, DOWN, buff=0.3)
        self.play(FadeIn(res), run_time=1.0)

        note = Text("ФУНКЦИЮ ВЫПОЛНЯЕТ ПРОГРАММА (ЧИТАЕТ sklad.csv)", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.4)

        self.program_state = (script, script_t, file, res)
        self.play(FadeOut(arrow), FadeOut(note), run_time=0.4)

    # --- 4. Результат возвращается модели, модель отвечает (38–52 с) ---------
    def otvet_modeli(self):
        model, model_t, vyzov = self.model_state
        script, script_t, file, res = self.program_state

        arrow = Arrow(start=script.get_left(), end=model.get_right(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        self.play(res.animate.move_to(model.get_bottom() - DOWN * 1.6), run_time=1.0)

        ans = bubble("НА СКЛАДЕ: ПОРОШОК, СОДА, ЦЕМЕНТ", PHOSPHOR, font_size=24)
        ans.to_edge(LEFT, buff=1.2).shift(DOWN * 1.4)
        arrow2 = Arrow(start=model.get_bottom(), end=ans.get_top(),
                       color=PHOSPHOR, stroke_width=6, buff=0.15)
        self.play(GrowArrow(arrow2), FadeIn(ans), run_time=1.0)
        sub = Text("САХАРА НЕТ (ОСТАТОК 0)", font_size=22,
                   color=BEIGE, weight=BOLD)
        sub.next_to(ans, DOWN, buff=0.15)
        self.play(FadeIn(sub), run_time=0.8)

        note = Text("ОТВЕТ ПО РЕАЛЬНОМУ РЕЗУЛЬТАТУ", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.4)

        self.play(FadeOut(model), FadeOut(model_t), FadeOut(vyzov),
                  FadeOut(script), FadeOut(script_t), FadeOut(file),
                  FadeOut(res), FadeOut(ans), FadeOut(sub), FadeOut(arrow),
                  FadeOut(arrow2), FadeOut(note), run_time=0.4)

    # --- 5. Без функции — из головы (52–66 с) --------------------------------
    def without_function(self):
        model = RoundedRectangle(width=4.2, height=3.0, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.move_to(LEFT * 0.4)
        model_t = Text("МОДЕЛЬ", font_size=40, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(model), FadeIn(model_t), run_time=1.0)

        q = bubble("ВОПРОС БЕЗ ФУНКЦИИ", BEIGE, font_size=26)
        q.to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        self.play(FadeIn(q), run_time=0.8)
        arrow = Arrow(start=q.get_right(), end=model.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        ans = bubble("ПОРОШОК, СОДА, ЦЕМЕНТ, САХАР — ВСЁ ЕСТЬ", RUST, font_size=24)
        ans.next_to(model, DOWN, buff=0.4)
        self.play(FadeIn(ans), run_time=1.0)
        self.play(ans.animate.shift(UP * 0.25), run_time=0.6)
        self.play(ans.animate.shift(DOWN * 0.25), run_time=0.6)

        cross = Text("X", font_size=90, color=RUST, weight=BOLD)
        cross.next_to(ans, RIGHT, buff=0.6)
        self.play(FadeIn(cross), run_time=0.6)
        note = Text("БЕЗ ФУНКЦИИ — ИЗ ГОЛОВЫ: МОЖЕТ ПРИВРАТЬ", font_size=30,
                    color=RUST, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        check = Text("ПРОВЕРЯЙ!", font_size=28, color=BEIGE, weight=BOLD)
        check.next_to(note, UP, buff=0.15)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # --- 6. Вывод (66–76 с) --------------------------------------------------
    def final_message(self):
        main = Text("ФУНКЦИЯ — РУКИ МОДЕЛИ", font_size=46,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.5)
        sub = Text("ВЫЗВАЛ → РЕАЛЬНЫЙ РЕЗУЛЬТАТ → ОТВЕТ ПО ДЕЛУ", font_size=30,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
