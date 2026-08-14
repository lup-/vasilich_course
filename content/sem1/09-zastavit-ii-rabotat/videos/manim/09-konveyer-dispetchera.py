"""
Набросок ролика «Конвейер диспетчера» (занятие 09, слайд 12).

СТАТУС: не отрендерен, это скелет сценария. Доделать по _shared/video-guide.md перед рендером.

Мысль ролика (одна): дежурный отвечает только по документу из базы знаний;
если ответа в документе нет — честно говорит «не знаю», а не выдумывает.

Стиль: палитра comic-style.md (болотный/ржавый/пыльный + кислотно-зелёный люминофор),
чёрный контур, надписи ЗАГЛАВНЫМИ рубленым шрифтом. 1920x1080, 30 fps, ~60 с, seed=9.

Кадры (~60 с):
  1. (0-8с)   Завязка: вопрос смены «КАК ПРИНЯТЬ ПАРТИЮ ГЛИЦЕРИНА?». Слева стопка
              «БАЗА ЗНАНИЙ», справа иконка диспетчера.
  2. (8-22с)  Шаг 1: «ПОИСК ПО СМЫСЛУ» -> из стопки выезжает лист «ИНСТРУКЦИЯ: ПРИЁМКА СЫРЬЯ».
  3. (22-38с) Шаг 2: сборка промпта: блоки «РОЛЬ» + «КОНТЕКСТ [лист]» + «ВОПРОС».
  4. (38-52с) Шаг 3: ответ по фактам листа; вопрос «СЕГОДНЯ ДОЖДЬ?» -> «НЕ ЗНАЮ, В БАЗЕ НЕТ»
              (зелёная галочка) против «ВЫДУМАЛ» (красный крест).
  5. (52-60с) Вывод: «ОТВЕЧАЙ ТОЛЬКО ПО СВОИМ ДОКУМЕНТАМ».
"""
from manim import *

# Палитра (в духе `comic-style.md`): болотный/ржавый/пыльный + люминофор.
PHOSPHOR = "#b8ff2f"   # кислотно-зелёный
BOLOT    = "#5c6b3c"   # болотный зелёный
RZHAV    = "#8a5a3a"   # ржавый
PYLYA    = "#6f6a60"   # пыльный серый
INK      = "#111111"   # чёрный контур
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
FON      = "#2a2d28"   # фон сцены

config.background_color = FON
config.frame_rate = 30


def bubble(text, color, font_size=30):
    """Блок с закруглённой рамкой, надписью заглавными и чёрным контуром."""
    t = Text(text, font="DejaVu Sans", font_size=font_size, color=INK, weight=BOLD)
    rect = RoundedRectangle(
        width=t.width + 0.7,
        height=t.height + 0.5,
        corner_radius=0.15,
        fill_color=color,
        fill_opacity=1.0,
        stroke_color=INK,
        stroke_width=6,
    )
    return VGroup(rect, t)


def make_sheet(width=3.6, height=2.1, fill=BEIGE):
    """Прямоугольный лист-документ с рамкой."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=INK,
        stroke_width=6,
    )


def check_mark():
    """Зелёная галочка (VGroup линий)."""
    a = Line(LEFT * 0.25 + UP * 0.05, LEFT * 0.05 + DOWN * 0.15,
             color=PHOSPHOR, stroke_width=12)
    b = Line(LEFT * 0.05 + DOWN * 0.15, RIGHT * 0.25 + UP * 0.15,
             color=PHOSPHOR, stroke_width=12)
    return VGroup(a, b)


def cross_mark():
    """Красный крест (VGroup линий)."""
    a = Line(LEFT * 0.25 + UP * 0.25, RIGHT * 0.25 + DOWN * 0.25,
             color=RZHAV, stroke_width=12)
    b = Line(RIGHT * 0.25 + UP * 0.25, LEFT * 0.25 + DOWN * 0.25,
             color=RZHAV, stroke_width=12)
    return VGroup(a, b)


class KonveyerDispetchera(Scene):
    def construct(self):
        # --- Служебные цвета из comic-style.md ---
        # Cвета нужно задать в начале (примерно):
        #   BOLOT = "#5c6b3c"; RZHAV = "#8a5a3a"; PYLYA = "#6f6a60"
        #   OGLAS = "#30383a"; LYUM = "#b8ff2f"; FON = "#2a2d28"
        # --- Кадр 1: завязка (0-8 с) ---
        q = Text(
            "КАК ПРИНЯТЬ ПАРТИЮ ГЛИЦЕРИНА?",
            font_size=34,
            color=PHOSPHOR,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(FadeIn(q), run_time=0.9)

        # Слева: «БАЗА ЗНАНИЙ»
        stack_bg = RoundedRectangle(
            width=5.0,
            height=4.3,
            corner_radius=0.1,
            fill_color=BOLOT,
            fill_opacity=0.15,
            stroke_color=PHOSPHOR,
            stroke_width=6,
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.15)
        self.play(Create(stack_bg), run_time=0.8)

        sheets = []
        for i in range(4):
            s = make_sheet(width=3.6, height=2.1, fill=BEIGE)
            s.move_to(stack_bg.get_center() + LEFT * 0.25 + UP * (1.05 - i * 0.25) + RIGHT * i * 0.06)
            sheets.append(s)

        self.play(FadeIn(VGroup(*sheets)), run_time=0.9)
        base_label = Text("БАЗА ЗНАНИЙ", font_size=26, color=BEIGE, weight=BOLD)
        base_label.next_to(stack_bg, DOWN, buff=0.25)
        self.play(FadeIn(base_label), run_time=0.8)

        # Справа: «ДИСПЕТЧЕР»
        disp = RoundedRectangle(
            width=4.0,
            height=4.0,
            corner_radius=0.1,
            fill_color=BOLOT,
            fill_opacity=0.35,
            stroke_color=PHOSPHOR,
            stroke_width=8,
        ).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.15)
        disp_t = Text("ДИСПЕТЧЕР", font_size=30, color=PHOSPHOR, weight=BOLD).move_to(disp)
        ekran = RoundedRectangle(
            width=2.0,
            height=1.2,
            corner_radius=0.08,
            fill_color=PYLYA,
            fill_opacity=0.45,
            stroke_color=INK,
            stroke_width=4,
        ).move_to(disp.get_center() + DOWN * 0.4)
        antenna = Line(disp.get_top() + UP * 0.1, disp.get_top() + UP * 0.75, color=PHOSPHOR, stroke_width=6)
        self.play(FadeIn(disp), FadeIn(disp_t), run_time=0.9)
        self.play(FadeIn(ekran), Create(antenna), run_time=0.7)
        self.wait(0.4)

        top_sheet = sheets[0]

        # --- Кадр 2: шаг 1 — поиск по смыслу (8-22 с) ---
        step1 = Text("ШАГ 1: НАЙТИ ДОКУМЕНТ ПО СМЫСЛУ", font_size=26, color=PHOSPHOR, weight=BOLD)
        step1.to_edge(UP, buff=0.3)
        self.play(Transform(q, step1), run_time=0.5)

        instr_title = Text("ИНСТРУКЦИЯ: ПРИЁМКА СЫРЬЯ", font_size=20, color=PHOSPHOR, weight=BOLD)
        instr_title.move_to(top_sheet.get_center() + UP * 0.35)
        self.play(top_sheet.animate.scale(1.12).shift(RIGHT * 0.3 + UP * 0.15), run_time=1.0)
        self.play(FadeIn(instr_title), run_time=0.7)
        self.wait(0.3)

        # --- Кадр 3: шаг 2 — сборка промпта (22-38 с) ---
        step2 = Text(
            "ШАГ 2: СОБРАТЬ ПРОМПТ: РОЛЬ + КОНТЕКСТ + ВОПРОС",
            font_size=22,
            color=BEIGE,
            weight=BOLD,
        )
        step2.to_edge(UP, buff=0.3)
        self.play(FadeIn(step2), run_time=0.6)

        role_box = bubble("РОЛЬ: ДЕЖУРНЫЙ", OLIVE, font_size=22)
        ctx_box = bubble("КОНТЕКСТ", BOLOT, font_size=22)
        q_box = bubble("ВОПРОС", BEIGE, font_size=22)
        row = VGroup(role_box, ctx_box, q_box).arrange(RIGHT, buff=0.7).move_to(UP * 1.7)
        self.play(FadeIn(row), run_time=0.8)

        mini = top_sheet.copy().scale(0.45)
        mini.move_to(ctx_box[0].get_center())
        self.play(FadeIn(mini), run_time=0.6)

        q2 = Text("СЕГОДНЯ ДОЖДЬ?", font_size=22, color=INK, weight=BOLD)
        q2.move_to(q_box[1].get_center())
        self.play(FadeIn(q2), run_time=0.5)
        self.wait(0.4)

        # --- Кадр 4: шаг 3 — ответ по фактам (38-52 с) ---
        step3 = Text(
            "ШАГ 3: ОТВЕТ ТОЛЬКО ПО ДОКУМЕНТУ",
            font_size=22,
            color=PHOSPHOR,
            weight=BOLD,
        ).to_edge(UP, buff=0.3)
        self.play(FadeOut(step2), FadeIn(step3), run_time=0.5)

        resp_left = bubble("НЕ ЗНАЮ, В БАЗЕ НЕТ", BOLOT, font_size=22)
        resp_right = bubble("ВЫДУМАЛ", RZHAV, font_size=22)
        resp_left.move_to(LEFT * 2.7 + DOWN * 0.55)
        resp_right.move_to(RIGHT * 1.5 + DOWN * 0.55)
        self.play(FadeIn(resp_left), FadeIn(resp_right), run_time=0.7)

        chk = check_mark().scale(0.95).move_to(resp_left.get_center() + RIGHT * 1.35)
        xmk = cross_mark().scale(0.95).move_to(resp_right.get_center() + RIGHT * 1.25)
        self.play(FadeIn(chk), FadeIn(xmk), run_time=0.4)

        facts = VGroup(
            Text("ФАКТЫ — только из листа.", font_size=18, color=INK, weight=BOLD),
            Text("ЕСЛИ НЕТ В ЛИСТЕ — НЕ ПРИДУМЫВАЕМ.", font_size=18, color=INK, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        facts.move_to(mini.get_center() + DOWN * 0.15)
        self.play(FadeIn(facts), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(facts), run_time=0.3)

        # --- Кадр 5: вывод (52-60 с) ---
        self.play(FadeOut(q2), FadeOut(mini), FadeOut(instr_title), FadeOut(chk), FadeOut(xmk), run_time=0.4)
        self.play(FadeOut(resp_right), run_time=0.3)

        final = Text(
            "ОТВЕЧАЙ ТОЛЬКО ПО СВОИМ ДОКУМЕНТАМ",
            font_size=34,
            color=PHOSPHOR,
            weight=BOLD,
        ).move_to(ORIGIN + DOWN * 0.25)
        self.play(FadeOut(step3), run_time=0.2)
        self.play(FadeIn(final), run_time=0.9)
        self.wait(2.0)
