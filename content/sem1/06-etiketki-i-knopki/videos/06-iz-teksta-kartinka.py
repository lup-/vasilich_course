# -*- coding: utf-8 -*-
"""Из текста — картинка. Технический ролик Manim (ManimCE) для занятия 06.

Одна мысль: картинка рождается из текста-промпта: промпт → модель изображений → картинка;
одинаковый промпт при повторе даёт похожую, но не ту же самую картинку; у генерации есть границы —
мета-промт (опасное не рисуем).

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 6 \
        06-iz-teksta-kartinka.py IzTekstaKartinka
"""

import random

from manim import *


PHOSPHOR = "#B6FF3C"   # кислотно-зелёный люминофор экранов
SWAMP    = "#4A5D23"   # болотный зелёный
RUST     = "#8C4A2F"   # ржавый
DUST     = "#8A8A7A"   # пыльный серый
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
INK      = "#111111"   # чёрный контур
PHOSPHOR_GOLD = "#FFD700"


def bubble(text, color, font_size=34):
    """Блок с закруглённой рамкой, чёрным контуром, надписью заглавными."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


def noise_cloud(center, radius_x=1.6, radius_y=1.1, n=90):
    """Пятно «шуна»: случайные точки внутри эллипса (детерминировано по seed)."""
    rnd = random.Random(config.seed if config.seed is not None else 6)
    dots = VGroup()
    for _ in range(n):
        x = rnd.uniform(-radius_x, radius_x)
        y = rnd.uniform(-radius_y, radius_y)
        if (x / radius_x) ** 2 + (y / radius_y) ** 2 > 1.0:
            continue
        d = Dot(radius=rnd.uniform(0.04, 0.10),
                fill_color=DUST if rnd.random() < 0.5 else OLIVE,
                fill_opacity=1.0, stroke_color=INK, stroke_width=2)
        d.move_to(center + RIGHT * x + UP * y)
        dots.add(d)
    return dots


def make_small_image(rgba, height=1.5):
    """Создает маленькое изображение из RGBA данных."""
    from PIL import Image
    import numpy as np
    im = Image.fromarray(rgba, mode="RGBA")
    m = ImageMobject(im)
    m.set_height(height)
    return m

    # --- 1. Промпт → модель изображений (0–8 с) ------------------------------
    def prompt_into_model(self):
        title = Text("ИЗ ТЕКСТА — КАРТИНКА", font_size=48, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        prompt = bubble("ЭТИКЕТКА СТИРАЛЬНОГО ПОРОШКА\n«ПОРОШОК-МАКС»…", BEIGE, font_size=26)
        prompt.to_edge(LEFT, buff=1.2).shift(DOWN * 0.3)
        self.play(FadeIn(prompt), run_time=1.0)

        model = RoundedRectangle(width=4.6, height=3.2, corner_radius=0.1,
                                 fill_color=SWAMP, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=8)
        model.to_edge(RIGHT, buff=1.4).shift(DOWN * 0.3)
        model_t = Text("МОДЕЛЬ\nИЗОБРАЖЕНИЙ", font_size=34, color=PHOSPHOR,
                       weight=BOLD).move_to(model)
        self.play(FadeIn(model), FadeIn(model_t), run_time=1.0)

        arrow = Arrow(start=prompt.get_right(), end=model.get_left(),
                      color=PHOSPHOR, stroke_width=6, buff=0.25)
        self.play(GrowArrow(arrow), run_time=0.8)

        # У-Net центр — место, куда приходит входная картинка
        unet_center = model.get_center() + DOWN * 0.2
        unet_dot = Dot(radius=0.3, color=PHOSPHOR).move_to(unet_center)
        self.play(FadeIn(unet_dot), run_time=0.5)

        note = Text("ПРОМПТ → МОДЕЛЬ ИЗОБРАЖЕНИЙ", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(prompt), FadeOut(arrow), FadeOut(note),
                  FadeOut(unet_dot), run_time=0.4)
        self.model = (model, model_t)

    # --- 2. Внутри модели: шум → картинка (8–22 с) ---------------------------
    def shum_to_kartinka(self):
        model, model_t = self.model

        inside = Text("ВНУТРИ:", font_size=28, color=BEIGE, weight=BOLD)
        inside.next_to(model, UP, buff=0.6)
        self.play(FadeIn(inside), run_time=0.5)

        center = model.get_center() + DOWN * 0.2
        cloud = noise_cloud(center)
        self.play(FadeIn(cloud, lag_ratio=0.05, run_time=1.0))

        shum = Text("ШУМ", font_size=26, color=DUST, weight=BOLD).next_to(cloud, UP, buff=0.3)
        self.play(FadeIn(shum), run_time=0.6)

        # Входная картинка появляется слева и движется к центру УНЕТ
        input_pic = RoundedRectangle(width=2.5, height=1.8, corner_radius=0.1,
                                      fill_color=PHOSPHOR, fill_opacity=1.0,
                                      stroke_color=INK, stroke_width=4)
        input_lbl = Text("ВХОДНАЯ КАРТИНКА", font_size=22, color=PHOSPHOR,
                          weight=BOLD)
        input_lbl.next_to(input_pic, DOWN, buff=0.1)
        input_pic.move_to(LEFT * 4.0)
        self.play(FadeIn(input_pic), FadeIn(input_lbl), run_time=0.5)

        # Анимация: входная картинка движется справа в центр УНЕТ
        self.play(input_pic.animate.move_to(center + RIGHT * 0.1 + UP * 0.1),
                  run_time=1.5)

        # Разделение входной картинки на две части
        # 1. "Выделенный шум" идет вниз и влево к рамке результата
        selected_noise = input_pic.copy()
        selected_noise.set_fill(DUST)
        self.play(selected_noise.animate.move_to(RIGHT * 4.2 + DOWN * 2.0),
                  run_time=1.0)
        selected_lbl = Text("ВЫДЕЛЕННЫЙ ШУМ", font_size=20, color=BEIGE, weight=BOLD)
        selected_lbl.next_to(selected_noise, DOWN, buff=0.1)
        self.play(FadeIn(selected_lbl), run_time=0.3)

        # 2. "Чистая" картинка идет наверх
        clean_img = input_pic.copy()
        clean_img.set_fill(PHOSPHOR)
        clean_img.move_to(RIGHT * 5.0 + UP * 2.0)
        clean_lbl = Text("ЧИСТАЯ КАРТИНКА", font_size=20, color=BEIGE, weight=BOLD)
        clean_lbl.next_to(clean_img, UP, buff=0.1)
        self.play(FadeIn(clean_img), FadeIn(clean_lbl), run_time=0.5)

        # Рамка "Результат при обучении" с эталонным шумом
        result_frame = RoundedRectangle(width=4.0, height=2.0, corner_radius=0.1,
                                        fill_color=BEIGE, fill_opacity=1.0,
                                        stroke_color=PHOSPHOR, stroke_width=6)
        result_frame.move_to(RIGHT * 5.0 + DOWN * 1.5)
        result_lbl = Text("РЕЗУЛЬТАТ ПРИ ОБУЧЕНИИ", font_size=28, color=PHOSPHOR,
                          weight=BOLD).next_to(result_frame, UP, buff=0.2)
        self.play(FadeIn(result_frame), FadeIn(result_lbl), run_time=0.5)

        # Эталонный шум внутри рамки
        ref_noise = noise_cloud(RIGHT * 5.0 + DOWN * 0.5, radius_x=1.2, radius_y=0.9, n=50)
        ref_lbl = Text("ЭТАЛОННЫЙ ШУМ", font_size=20, color=RUST, weight=BOLD)
        ref_lbl.next_to(ref_noise, DOWN, buff=0.1)
        self.play(FadeIn(ref_noise), FadeIn(ref_lbl), run_time=0.5)

        note = Text("ВНУТРИ: ШУМ → КАРТИНКА (УПРОЩЕНИЕ)", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(cloud), FadeOut(shum),
                  FadeOut(note), FadeOut(inside), FadeOut(model),
                  FadeOut(model_t), FadeOut(input_pic), FadeOut(input_lbl),
                  FadeOut(selected_noise), FadeOut(selected_lbl),
                  FadeOut(clean_img), FadeOut(clean_lbl),
                  FadeOut(ref_noise), FadeOut(ref_lbl),
                  FadeOut(result_frame), FadeOut(result_lbl), run_time=0.4)

    # --- 3. На выходе — этикетка (22–32 с) -----------------------------------
    def etiketa(self):
        model, model_t = self.model

        # Центр УНЕТ из предыдущего слайда
        unet_center = model.get_center() + DOWN * 0.2

        # Входная картинка появляется справа и движется к центру УНЕТ
        input_pic = RoundedRectangle(width=2.5, height=1.8, corner_radius=0.1,
                                      fill_color=PHOSPHOR, fill_opacity=1.0,
                                      stroke_color=INK, stroke_width=4)
        input_lbl = Text("ВХОДНАЯ КАРТИНКА", font_size=22, color=PHOSPHOR,
                          weight=BOLD)
        input_lbl.next_to(input_pic, DOWN, buff=0.1)
        input_pic.move_to(RIGHT * 4.0)
        self.play(FadeIn(input_pic), FadeIn(input_lbl), run_time=0.5)

        # Анимация: входная картинка движется влево к центру УНЕТ
        self.play(input_pic.animate.move_to(unet_center + RIGHT * 0.1 + UP * 0.1),
                  run_time=1.5)

        # Разделение на две части
        # 1. "Выделенный шум" идет вниз и влево
        selected_noise = input_pic.copy()
        selected_noise.set_fill(DUST)
        self.play(selected_noise.animate.move_to(RIGHT * 4.2 + DOWN * 2.0),
                  run_time=1.0)
        selected_lbl = Text("ВЫДЕЛЕННЫЙ ШУМ", font_size=20, color=BEIGE, weight=BOLD)
        selected_lbl.next_to(selected_noise, DOWN, buff=0.1)
        self.play(FadeIn(selected_lbl), run_time=0.3)

        # 2. "Чистая" картинка идет наверх
        clean_img = input_pic.copy()
        clean_img.set_fill(PHOSPHOR)
        clean_img.move_to(RIGHT * 5.0 + UP * 2.0)
        clean_lbl = Text("ЧИСТАЯ КАРТИНКА", font_size=20, color=BEIGE, weight=BOLD)
        clean_lbl.next_to(clean_img, UP, buff=0.1)
        self.play(FadeIn(clean_img), FadeIn(clean_lbl), run_time=0.5)

        # Этикетка на выходе
        e = RoundedRectangle(width=3.6, height=2.4, corner_radius=0.1,
                             fill_color=BEIGE, fill_opacity=1.0,
                             stroke_color=INK, stroke_width=8)
        e.move_to(LEFT * 0.4)
        name = Text("ПОРОШОК-МАКС", font_size=30, color=RUST, weight=BOLD)
        name.move_to(e.get_center() + UP * 0.5)
        band = RoundedRectangle(width=2.8, height=0.7, corner_radius=0.1,
                                fill_color=SWAMP, fill_opacity=1.0,
                                stroke_color=INK, stroke_width=4)
        band.move_to(e.get_center() - UP * 0.5)
        self.play(FadeIn(e), FadeIn(name), FadeIn(band), run_time=0.8)

        arrow = Arrow(start=LEFT * 4.0, end=e.get_left(), color=PHOSPHOR,
                      stroke_width=6, buff=0.2)
        out = Text("НА ВЫХОДЕ", font_size=26, color=BEIGE, weight=BOLD)
        out.next_to(arrow, UP, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(out), run_time=0.8)

        # "Чистая" картинка присоединяется к этикетке сверху
        self.play(clean_img.animate.move_to(e.get_center() + UP * 1.5),
                  clean_lbl.animate.move_to(e.get_center() + UP * 2.0),
                  run_time=0.8)

        note = Text("НА ВЫХОДЕ: КАРТИНКА-ЭТИКЕТКА", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.2)

        self.etiketa_group = (e, name, band, out, input_pic, input_lbl,
                              clean_img, clean_lbl, selected_noise, selected_lbl)
        self.play(FadeOut(arrow), FadeOut(note), run_time=0.4)

    # --- 4. Тот же промпт — картинка похожая, но другая (32–40 с) -------------
    def povtor(self):
        e, name, band, out = self.etiketa_group
        self.play(e.animate.shift(RIGHT * 3.2), name.animate.shift(RIGHT * 3.2),
                  band.animate.shift(RIGHT * 3.2), out.animate.shift(RIGHT * 3.2),
                  run_time=0.8)

        e2 = e.copy().shift(LEFT * 3.2)
        name2 = Text("ПОРОШОК-МАКС", font_size=34, color=RUST, weight=BOLD)
        name2.move_to(e2.get_center() + UP * 0.3)
        band2 = RoundedRectangle(width=3.0, height=0.9, corner_radius=0.1,
                                 fill_color=OLIVE, fill_opacity=1.0,
                                 stroke_color=INK, stroke_width=4)
        band2.move_to(e2.get_center() - UP * 0.6)
        self.play(FadeIn(e2), FadeIn(name2), FadeIn(band2), run_time=1.0)

        note = Text("ТОТ ЖЕ ПРОМПТ — КАРТИНКА ПОХОЖАЯ, НО ДРУГАЯ", font_size=30,
                    color=PHOSPHOR, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.2)

        self.play(FadeOut(e), FadeOut(name), FadeOut(band), FadeOut(out),
                  FadeOut(e2), FadeOut(name2), FadeOut(band2), FadeOut(note),
                  run_time=0.4)

    # --- 5. Вывод и границы (40–50 с) ----------------------------------------
    def final_message(self):
        main = Text("ИЗ ТЕКСТА — КАРТИНКА", font_size=46,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.5)
        sub = Text("МЕТА-ПРОМПТ ЗАДАЁТ ГРАНИЦЫ: ОПАСНОЕ НЕ РИСУЕМ", font_size=30,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
