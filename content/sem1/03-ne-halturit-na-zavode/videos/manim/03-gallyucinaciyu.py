# -*- coding: utf-8 -*-
"""Уверенно, но неверно. Технический ролик Manim (ManimCE) для занятия 03.

Одна мысль: модель уверенно «дописывает» ответ токен за токеном по вероятностям —
продолжая вопрос, — и может уверенно выдумать факт, которого нет. Данные для ответа
модель берёт из текстов, на которых училась, а не из заводского архива. Проверка по архиву
не подтверждает → вывод ИИ — черновик.

Запуск (ManimCE, требуется установленный Manim; берём из .venv-manim):
    manim -r 1920,1080 --fps 30 03-gallyucinaciyu.py Gallyucinaciyu

Выход: videos/03-gallyucinaciyu.mp4 — подключается в `video_url` слайда (video_type: direct).
"""

from manim import *
from manim.constants import CapStyleType
import os
import random

PHOSPHOR = "#B6FF3C"
YELLOW   = "#FFC933"
SWAMP    = "#4A5D23"
RUST     = "#8C4A2F"
DUST     = "#8A8A7A"
BEIGE    = "#D8C9A3"
OLIVE    = "#556B2F"
INK      = "#111111"
WHITE    = "#FFFFFF"

FONT = "DejaVu Sans"
PIXEL_FONT = "Unifont"  # пиксельный (битмап) шрифт — есть кириллица

QUESTION = "СКОЛЬКО ТОНН ГЛИЦЕРИНА ОТГРУЗИЛ ЗАВОД 13 ФЕВРАЛЯ 2099 ГОДА?"


def bubble(text, color, font_size=28):
    t = Text(text, font=FONT, font_size=font_size, color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


def token_box(word, color, font_size=26, pad_x=0.26, pad_y=0.16):
    """Рамка-токен с текстом (словом) внутри."""
    label = Text(word, font=FONT, font_size=font_size, color=INK, weight=BOLD)
    rect = RoundedRectangle(width=label.width + 2 * pad_x, height=label.height + 2 * pad_y,
                            corner_radius=0.1, fill_color=color, fill_opacity=1.0,
                            stroke_color=INK, stroke_width=5)
    label.move_to(rect.get_center())
    return VGroup(rect, label)


def doc_icon(width=1.6, height=2.0, color=BEIGE, line_color=INK):
    """Значок документа: страница с несколькими строками текста."""
    page = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                            fill_color=color, fill_opacity=0.95,
                            stroke_color=line_color, stroke_width=5)
    lines = VGroup()
    for _ in range(4):
        ln = Rectangle(width=width * 0.62, height=0.12,
                       fill_color=line_color, fill_opacity=0.8, stroke_width=0)
        lines.add(ln)
    lines.arrange(DOWN, buff=0.26)
    lines.move_to(page.get_center()).shift(DOWN * 0.15)
    return VGroup(page, lines)


def doc_card(label, file_path, font_size=19, icon_scale=0.32):
    """Карточка документа: значок файла (SVG) + подпись в тёмной рамке."""
    icon = SVGMobject(file_path)
    icon.set_color(BEIGE)
    icon.scale(icon_scale)
    lbl = Text(label, font=FONT, font_size=font_size, color=BEIGE, weight=BOLD)
    content = VGroup(icon, lbl).arrange(RIGHT, buff=0.2)
    bg = RoundedRectangle(
        width=content.width + 0.45, height=content.height + 0.3,
        corner_radius=0.08, fill_color=INK, fill_opacity=0.92,
        stroke_color=BEIGE, stroke_width=3
    )
    content.move_to(bg.get_center())
    return VGroup(bg, content)


class Gallyucinaciyu(Scene):
    def construct(self):
        self.zavyazka()
        self.generaciya()
        self.uverennyj_otvet()
        self.otkuda_dannye()
        self.proverka_arhiva()
        self.final_message()

    # --- 1. Завязка -------------------------------------------------------
    def zavyazka(self):
        title = Text("УВЕРЕННО, НО НЕВЕРНО", font_size=66, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.8)

        screen = Rectangle(width=12.0, height=3.6, fill_color=WHITE,
                           fill_opacity=1.0, stroke_width=0)
        screen.shift(DOWN * 0.2)
        q = VGroup(
            Text("СКОЛЬКО ТОНН ГЛИЦЕРИНА ОТГРУЗИЛ", font=PIXEL_FONT,
                 font_size=40, color=INK),
            Text("ЗАВОД 13 ФЕВРАЛЯ 2099 ГОДА?", font=PIXEL_FONT,
                 font_size=40, color=INK),
        )
        q.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        q.move_to(screen.get_center())
        if q.width > screen.width - 1.0:
            q.scale_to_fit_width(screen.width - 1.0)
        # прижать блок к левому краю «текстового поля» с отступом
        q.shift(LEFT * (screen.width / 2 - 0.5 - q.width / 2))
        self.play(FadeIn(screen), run_time=0.5)
        self.play(Write(q), run_time=1.6)
        self.wait(1.2)
        self.play(FadeOut(title), run_time=0.3)
        self.screen = screen
        self.q = q

    # --- 2. Генерация: токен за токеном (продолжение вопроса) ---------------
    def generaciya(self):
        self.play(FadeOut(self.q), FadeOut(self.screen), run_time=0.4)

        note = Text("МОДЕЛЬ ДОПИСЫВАЕТ ОТВЕТ ТОКЕН ЗА ТОКЕНОМ",
                     font_size=28, color=PHOSPHOR, weight=BOLD).to_edge(UP, buff=0.4)
        q_label = Text(QUESTION, font_size=20, color=BEIGE, weight=BOLD).move_to(UP * 2.4)
        self.play(FadeIn(note), FadeIn(q_label), run_time=0.6)

        # модель продолжает вопрос: показываем 2-3 последних слова вопроса
        # как начало цепочки токенов, к которым она дописывает ответ
        prompt_tail = ["ФЕВРАЛЯ", " 2099", " ГОДА?"]
        seq = VGroup()
        seq.add(token_box("…", BEIGE, font_size=26))
        for w in prompt_tail:
            seq.add(token_box(w, BEIGE, font_size=26))
        seq.arrange(RIGHT, buff=0.12)
        seq.move_to(DOWN * 2.8)
        self.play(FadeIn(seq, lag_ratio=0.2), run_time=0.9)

        # шаги генерации: слово-токен + кандидаты с вероятностями
        steps = [
            ("137",     [("137", 0.90), ("128", 0.06), (" 95", 0.04)]),
            (" ТОНН",   [(" ТОНН", 0.85), (" КГ", 0.08), (" Л", 0.05)]),
            (", НАКЛ",  [(", НАКЛ", 0.80), (", НАК", 0.10), (", А", 0.06)]),
            ("АДНАЯ",   [("АДНАЯ", 0.78), ("АДН", 0.12), ("А", 0.06)]),
            (" №88-90", [(" №88-90", 0.70), (" №77", 0.15), (" №12", 0.10)]),
        ]

        panel_title = Text("выбираем следующий токен", font_size=24,
                           color=BEIGE).move_to(UP * 1.9)
        self.play(FadeIn(panel_title), run_time=0.5)

        for word, cands in steps:
            cand_group = VGroup()
            for cw, prob in cands:
                box = token_box(cw, BEIGE, font_size=24)
                pct = Text(f"{int(prob * 100)}%", font=FONT, font_size=24,
                           color=PHOSPHOR, weight=BOLD)
                cand_group.add(VGroup(box, pct).arrange(RIGHT, buff=0.4))
            cand_group.arrange(DOWN, buff=0.25).move_to(UP * 0.1)
            self.play(FadeIn(cand_group, lag_ratio=0.1), run_time=0.9)

            chosen_row = cand_group[0]
            chosen_rect = chosen_row[0][0]
            self.play(
                chosen_rect.animate.set_stroke(PHOSPHOR, width=8),
                chosen_row.animate.scale(1.06),
                run_time=0.3,
            )
            self.wait(0.2)

            new_box = token_box(word, PHOSPHOR, font_size=26)
            new_box.move_to(chosen_row.get_center())
            self.play(new_box.animate.move_to(seq.get_right() + RIGHT * 0.45))
            seq.add(new_box)
            seq.arrange(RIGHT, buff=0.12)
            if seq.width > config.frame_width - 1.5:
                seq.scale_to_fit_width(config.frame_width - 1.5)
            seq.move_to(DOWN * 2.8)
            self.play(seq.animate)
            self.play(FadeOut(cand_group), run_time=0.35)
            self.wait(0.25)

        self.play(FadeOut(panel_title), run_time=0.3)

        self.play(FadeOut(note), FadeOut(q_label), run_time=0.4)
        self.seq = seq

    # --- 3. Уверенный ответ ------------------------------------------------
    def uverennyj_otvet(self):
        ans = bubble("137 ТОНН, НАКЛАДНАЯ №88-90", PHOSPHOR, font_size=26)
        ans.move_to(UP * 0.6)
        conf = Text("УВЕРЕННОСТЬ: 98%", font_size=34, color=RUST, weight=BOLD)
        conf.next_to(ans, DOWN, buff=0.6)
        label = Text("УВЕРЕННО: 137 ТОНН, НАКЛАДНАЯ №88-90", font_size=24,
                     color=BEIGE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(label), FadeIn(ans),
                  *[FadeOut(t) for t in self.seq], run_time=0.8)
        self.play(FadeIn(conf), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(label), FadeOut(ans), FadeOut(conf), run_time=0.4)

    # --- 4. Откуда данные? ------------------------------------------------
    def otkuda_dannye(self):
        title = Text("ОТКУДА ДАННЫЕ?", font_size=42, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP, buff=0.6)
        sub = Text("ИЗ ТЕКСТОВ, НА КОТОРЫХ УЧИЛАСЬ МОДЕЛЬ", font_size=28,
                   color=BEIGE, weight=BOLD).next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        icons_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "_shared", "assets", "icons")
        school_path = os.path.join(icons_dir, "school.svg")
        file_path = os.path.join(icons_dir, "file-text.svg")

        # Иконка модели (академическая шапочка — обучение)
        model_pos = RIGHT * 2.2 + DOWN * 0.5
        school = SVGMobject(school_path)
        school.set_color(PHOSPHOR)
        school.scale(0.65)
        school.move_to(model_pos)

        mlabel = Text("МОДЕЛЬ", font=FONT, font_size=22, color=PHOSPHOR, weight=BOLD)
        mlabel.next_to(school, DOWN, buff=0.25)

        self.play(FadeIn(school, scale=0.5), FadeIn(mlabel), run_time=0.5)

        sources = [
            "ФОРУМЫ ПЛОСКОЗЕМЕЛЬЩИКОВ",
            "ИНСТРУКЦИЯ К ПЫЛЕСОСУ",
            "ГОРОСКОП НА 2099 ГОД",
            "КОММЕНТАРИИ НА WB",
            "СТАТЬИ ИЗ ВИКИПЕДИИ",
            "ПРЕПРИНТЫ ARXIV.ORG",
            "УЧЕБНЫЕ КУРСЫ 1С",
        ]

        spawn_pos = LEFT * 3.4 + DOWN * 0.5

        for src in sources:
            card = doc_card(src, file_path)
            card.move_to(spawn_pos)
            self.play(FadeIn(card, shift=RIGHT * 0.3), run_time=0.35)
            self.wait(0.55)

            # Полёт к иконке модели со сжатием
            self.play(
                card.animate.move_to(school.get_center()).scale(0.2),
                FadeOut(card, run_time=0.4),
                run_time=0.4
            )

            # Поглощение: модель растёт, подпись сдвигается
            t_school = school.copy().scale(1.15)
            t_label = mlabel.copy().next_to(t_school, DOWN, buff=0.25)
            self.play(
                Transform(school, t_school),
                Transform(mlabel, t_label),
                run_time=0.25
            )
            self.wait(0.5)

        self.wait(1.2)

        # Модель «обучилась»: сдвигаем иконку с подписью в центр
        target_center = DOWN * 0.4
        shift_vec = target_center - VGroup(school, mlabel).get_center()
        self.play(
            school.animate.shift(shift_vec),
            mlabel.animate.shift(shift_vec),
            run_time=0.6
        )

        # Смена значка на лампочку и подписи на «уверенный» ответ
        bulb = SVGMobject(os.path.join(icons_dir, "bulb.svg"))
        bulb.set_color(YELLOW)
        bulb.scale(1.6)
        bulb.move_to(school.get_center())
        ans_label = Text("137 ТОНН, НАКЛАДНАЯ №88-90!", font=FONT, font_size=26,
                         color=PHOSPHOR, weight=BOLD).next_to(bulb, DOWN, buff=0.3)
        self.play(
            FadeOut(school), FadeOut(mlabel),
            FadeIn(bulb, scale=0.3), FadeIn(ans_label),
            run_time=0.6
        )
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(sub), FadeOut(bulb), FadeOut(ans_label),
                  run_time=0.4)

    # --- 5. Проверка по архиву (циклическое сканирование стопки) ----------
    def proverka_arhiva(self):
        title = Text("НО НЕ ИЗ АРХИВОВ ЗАВОДА!", font_size=36, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP, buff=0.5)
        subtitle = Text("ПОИСК ПО АРХИВАМ ЗАВОДА...", font_size=24, color=BEIGE,
                        weight=BOLD).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.6)

        icons_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                                 "_shared", "assets", "icons")
        file_path = os.path.join(icons_dir, "file-text.svg")

        # номера накладных: №БХИИД-(ММ)-(НННННН), детерминированный генератор
        rng = random.Random(88)
        nums = [f"№БХИИД-{rng.randint(1, 12):02d}-{rng.randint(0, 999999):06d}"
                for _ in range(9)]

        # центр стопки (центр масс) остаётся на месте при любом числе карточек
        center = DOWN * 0.1
        offset = RIGHT * 0.22 + UP * 0.22
        n_cards = 5

        def card_pos(i):
            return center + offset * (i - (n_cards - 1) / 2)

        docs = []
        for i in range(n_cards):
            d = doc_card(nums[i], file_path, font_size=20)
            d.move_to(card_pos(i))
            docs.append(d)
        self.play(FadeIn(VGroup(*docs), lag_ratio=0.1), run_time=0.8)

        # цикл: верхний документ исчезает, остальные сдвигаются вперёд,
        # сзади появляется новый — и так по кругу
        for k in range(4):
            self.play(FadeOut(docs[0], run_time=0.35))
            docs.pop(0)
            anims = []
            for i, d in enumerate(docs):
                anims.append(d.animate.move_to(card_pos(i)))
            new = doc_card(nums[5 + k], file_path, font_size=20)
            new.move_to(card_pos(len(docs)))
            docs.append(new)
            anims.append(FadeIn(new, run_time=0.35))
            self.play(*anims, run_time=0.5)
            self.wait(0.2)

        empty = Text("НАКЛАДНОЙ №88-90 — НЕ СУЩЕСТВУЕТ!", font_size=30, color=RUST,
                     weight=BOLD).move_to(DOWN * 0.2)
        cross = Text("✗", font_size=72, color=RUST, weight=BOLD)
        cross.next_to(empty, RIGHT, buff=0.3)
        self.play(FadeOut(VGroup(*docs)), run_time=0.4)
        self.play(FadeIn(empty), FadeIn(cross), run_time=0.6)
        self.wait(3.0)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(empty), FadeOut(cross),
                  run_time=0.4)

    # --- 6. Вывод ---------------------------------------------------------
    def final_message(self):
        pre = Text("УВЕРЕННО ", font_size=46, color=PHOSPHOR, weight=BOLD)
        post = Text(" ПРАВИЛЬНО", font_size=46, color=PHOSPHOR, weight=BOLD)
        eq = Text("=", font_size=46, color=PHOSPHOR, weight=BOLD)
        strike = Line(
            eq.get_corner(UR) + LEFT * 0.15 * eq.width + UP * 0.12 * eq.height,
            eq.get_corner(DL) + RIGHT * 0.15 * eq.width + DOWN * 0.12 * eq.height,
            stroke_color=PHOSPHOR, stroke_width=6,
        )
        strike.stroke_cap_style = CapStyleType.ROUND
        neq = VGroup(eq, strike)
        main = VGroup(pre, neq, post).arrange(RIGHT, buff=0).move_to(UP * 0.5)
        sub = Text("ВЫВОД ИИ — ЧЕРНОВИК. ПРОВЕРЯЙ", font_size=32,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.7)
        self.play(FadeIn(main), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(3.0)
