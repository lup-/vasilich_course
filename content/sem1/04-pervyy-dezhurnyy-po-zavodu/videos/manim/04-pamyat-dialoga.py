# -*- coding: utf-8 -*-
"""Память диалога и окно контекста. Технический ролик Manim (ManimCE) для занятия 04.

Одна мысль: модель «помнит» диалог, потому что вместе с новым сообщением в запрос
уходит вся история сообщений плюс системный промпт. Но у входа есть потолок —
окно контекста: что не влезло, выпадает, и модель «забывает» начало.

Сцена: слева — история чата столбиком, справа — модель (прямоугольник только
с контуром, без заливки). Сообщения, которые уйдут в запрос, обведены в истории
пунктирной рамкой — окном контекста. Как только появляется новое сообщение,
копии блоков из окна летят к модели и на полпути останавливаются; сверху у них
возникает «СИСТЕМНЫЙ ПРОМПТ», и вся стопка вместе въезжает в модель. Внутри
модели снизу пририсовывается ответ, блоки запроса исчезают, а ответ переезжает
в историю чата. Когда история перерастает окно — рамка съезжает вниз по одному
сообщению: выпадают ВОПРОС 1, ОТВЕТ 1, ВОПРОС 2, и модель их больше
не получает: начало забыто.

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

NUM_DASHES = 26        # фикс. число штрихов окна: рамка плавно пересчитывается

HIST_X  = -4.6         # центр колонки истории
TOP_Y   = 2.0          # y центра первого блока истории (чуть ниже верха модели)
SPACING = 0.62         # шаг между центрами блоков истории
STOP_X  = 0.0          # точка остановки копий на полпути к модели


def bubble(text, color, font_size=26, hpad=0.42, wpad=0.55):
    """Блок с закруглённой рамкой, чёрным контуром, надписью заглавными."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + wpad, height=t.height + hpad,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=5)
    v = VGroup(rect, t)
    v.text_str = text
    return v


def make_window(blocks):
    """Пунктирная рамка (окно контекста) вокруг набора блоков истории."""
    bb = VGroup(*blocks)
    rect = RoundedRectangle(width=bb.width + 0.65, height=bb.height + 0.55,
                            corner_radius=0.12, stroke_color=PHOSPHOR,
                            stroke_width=5)
    rect.move_to(bb.get_center())
    return DashedVMobject(rect, num_dashes=NUM_DASHES, dashed_ratio=0.55,
                          color=PHOSPHOR)


class PamyatDialoga(Scene):
    def construct(self):
        self.blocks = []          # блоки истории в колонке (в порядке сверху вниз)
        self.window = None        # пунктирная рамка окна контекста
        self.win_label = None     # подпись «ОКНО КОНТЕКСТА»
        self.budget = None        # плашка «≈ 2000 ТОКЕНОВ»
        self.model = None         # контур модели
        self.fallen_cap = None    # плашка о выпавших сообщениях

        self.draw_scene()
        self.request_1()
        self.request_2()
        self.request_3()
        self.final_message()

    # --- Оформление сцены ------------------------------------------------
    def draw_scene(self):
        title = Text("ПАМЯТЬ ДИАЛОГА", font_size=56, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.8)

        # Модель справа: прямоугольник без заливки, только контур
        self.model = RoundedRectangle(width=3.4, height=4.75, corner_radius=0.1,
                                      fill_opacity=0.0, stroke_color=PHOSPHOR,
                                      stroke_width=8)
        self.model.move_to((4.3, 0.0, 0))
        model_t = Text("МОДЕЛЬ", font_size=28, color=PHOSPHOR,
                       weight=BOLD).move_to(self.model.get_center()
                                            + DOWN * 2.07)

        # Подпись истории слева — на уровне надписи «МОДЕЛЬ» в правом столбце
        hist_header = Text("ИСТОРИЯ ДИАЛОГА", font_size=28, color=PHOSPHOR,
                           weight=BOLD)
        hist_header.move_to((HIST_X, model_t.get_center()[1], 0))

        cap1 = Text("ОТВЕЧАЕТ ТОЛЬКО НА ТО,", font_size=16, color=BEIGE,
                    weight=BOLD)
        cap2 = Text("ЧТО В ЗАПРОСЕ", font_size=16, color=BEIGE, weight=BOLD)
        model_cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.08)
        model_cap.next_to(self.model, DOWN, buff=0.35)
        model_cap.shift(DOWN * 0.17)
        self.play(FadeIn(self.model), FadeIn(model_t), FadeIn(hist_header),
                  FadeIn(model_cap), run_time=1.0)
        self.wait(1.2)

    # --- История и окно контекста ----------------------------------------
    def place_in_history(self, text, color):
        """Новый блок вниз колонки истории; возвращает блок."""
        b = bubble(text, color, font_size=22, hpad=0.3, wpad=0.45)
        y = TOP_Y - len(self.blocks) * SPACING
        b.move_to((HIST_X, y, 0))
        self.blocks.append(b)
        return b

    def set_window(self, blocks, with_labels=False):
        """Пересчитать пунктирную рамку вокруг обводимых блоков.

        Подписи «ОКНО КОНТЕКСТА» и «≈ 2000 ТОКЕНОВ» появляются и двигаются
        только вместе, одним кадром (with_labels создаёт их одновременно)."""
        new_win = make_window(blocks)
        animations = []
        if self.window is None:
            self.window = new_win
            animations.append(FadeIn(self.window))
        else:
            animations.append(Transform(self.window, new_win))

        if with_labels and self.win_label is None:
            self.win_label = Text("ОКНО КОНТЕКСТА", font_size=12,
                                  color=PHOSPHOR, weight=BOLD).rotate(-PI / 2)
            self.win_label.next_to(new_win, RIGHT, buff=0.1)
            self.win_label.set_y(new_win.get_center()[1])
            self.budget = Text("≈ 2000 ТОКЕНОВ", font_size=12,
                               color=PHOSPHOR, weight=BOLD).rotate(-PI / 2)
            self.budget.next_to(new_win, LEFT, buff=0.1)
            self.budget.set_y(new_win.get_center()[1])
            animations.append(FadeIn(self.win_label))
            animations.append(FadeIn(self.budget))
        elif self.win_label is not None:
            animations.append(self.win_label.animate.next_to(new_win, RIGHT,
                                                             buff=0.1)
                              .set_y(new_win.get_center()[1]))
            animations.append(self.budget.animate.next_to(new_win, LEFT,
                                                          buff=0.1)
                              .set_y(new_win.get_center()[1]))
        self.play(*animations, run_time=0.7)

    # --- Один цикл «запрос → ответ» ---------------------------------------
    def send_request(self, window_blocks, answer_text, hint=None):
        """Копии блоков окна летят к модели, промпт сверху, ответ в историю."""
        copies = VGroup(*[b.copy() for b in window_blocks])
        stop = (STOP_X, self.model.get_center()[1], 0)
        self.play(copies.animate.move_to(stop), run_time=1.4)

        sys_p = bubble("СИСТЕМНЫЙ ПРОМПТ", OLIVE, font_size=20)
        sys_p.next_to(copies, UP, buff=0.22)
        self.play(FadeIn(sys_p), run_time=0.8)

        if hint:
            lines = [l.strip() for l in hint.split("\n")]
            lab = VGroup(*[Text(l, font_size=20, color=BEIGE, weight=BOLD)
                           for l in lines])
            lab.arrange(DOWN, buff=0.08)
            lab.next_to(sys_p, UP, buff=0.22)
            self.play(FadeIn(lab), run_time=0.6)
            self.wait(1.2)
            self.play(FadeOut(lab), run_time=0.4)
        else:
            self.wait(1.0)

        stack = VGroup(sys_p, copies)
        self.play(stack.animate.scale(0.72).move_to(self.model.get_center()
                                                    + UP * 0.8), run_time=1.4)

        ans = bubble(answer_text, PHOSPHOR, font_size=22, hpad=0.3, wpad=0.45)
        ans.move_to(self.model.get_center() + DOWN * 1.15)
        self.play(FadeIn(ans), run_time=0.8)
        self.wait(0.8)

        self.play(FadeOut(sys_p), FadeOut(copies), run_time=0.5)

        y = TOP_Y - len(self.blocks) * SPACING
        self.play(ans.animate.move_to((HIST_X, y, 0)), run_time=1.2)
        self.blocks.append(ans)

    def dim_block(self, block):
        """Выпавшее из окна сообщение: приглушить и чуть выдавить вверх.
        Текст выпавшего блока — обычный (не жирный), приглушённого цвета."""
        rect, text = block
        faded = Text(block.text_str, font="DejaVu Sans",
                     font_size=text.font_size, color=DUST,
                     weight=NORMAL).move_to(text.get_center() + UP * 0.1)
        self.play(FadeOut(text), rect.animate.shift(UP * 0.1)
                  .set_stroke(RUST, width=6).set_fill(RUST, opacity=0.4),
                  run_time=0.8)
        self.add(faded)

    def show_fallen(self, text, wait_time=2.5):
        """Пояснение о выпавших сообщениях: по центру, в несколько строк,
        с паузой на чтение; после паузы само гаснет."""
        if self.fallen_cap is not None:
            self.remove(self.fallen_cap)
        lines = [l.strip() for l in text.split("\n")]
        cap = VGroup(*[Text(l, font_size=22, color=RUST, weight=BOLD)
                       for l in lines])
        cap.arrange(DOWN, buff=0.12)
        cap.move_to(ORIGIN)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(wait_time)
        self.play(FadeOut(cap), run_time=0.4)
        self.fallen_cap = cap

    # --- Части сценария ---------------------------------------------------
    def request_1(self):
        q1 = self.place_in_history("ВОПРОС 1", BEIGE)
        self.play(FadeIn(q1), run_time=0.7)
        self.set_window(self.blocks)
        self.wait(0.8)
        self.send_request(self.blocks, "ОТВЕТ 1")
        self.set_window(self.blocks)
        self.wait(0.8)

    def request_2(self):
        q2 = self.place_in_history("ВОПРОС 2", BEIGE)
        self.play(FadeIn(q2), run_time=0.7)
        self.set_window(self.blocks)
        self.wait(0.6)
        self.send_request(self.blocks, "ОТВЕТ 2")

        # ОТВЕТ 2 в истории: ВОПРОС 1 выпадает, окно сокращается до О1-В2-О2,
        # вместе с окном впервые появляются обе подписи (они остаются
        # по центру окна контекста)
        self.dim_block(self.blocks[0])
        self.set_window(self.blocks[1:4], with_labels=True)
        self.show_fallen("ВОПРОС 1 ВЫПАЛ ИЗ ОКНА —\nКОНТЕКСТ КОНЕЧЕН")

    def request_3(self):
        q3 = self.place_in_history("ВОПРОС 3", BEIGE)
        self.play(FadeIn(q3), run_time=0.7)

        # Как только появился ВОПРОС 3 — ОТВЕТ 1 выпадает, окно = В2-О2-В3
        self.dim_block(self.blocks[1])
        window_blocks = self.blocks[2:5]
        self.set_window(window_blocks)
        self.show_fallen("ВОПРОС 1 И ОТВЕТ 1\nВЫПАЛИ — НАЧАЛО ЗАБЫТО")

        # В запрос уходит только то, что в окне: ВОПРОС 2, ОТВЕТ 2, ВОПРОС 3
        self.send_request(window_blocks, "ОТВЕТ 3",
                          hint="В ЗАПРОС УХОДИТ ТОЛЬКО ТО,\n"
                               "ЧТО ВЛЕЗЛО В ОКНО КОНТЕКСТА")

        # ОТВЕТ 3 в истории: ВОПРОС 2 тоже выпадает, окно = О2-В3-О3
        self.dim_block(self.blocks[2])
        self.set_window(self.blocks[3:6])
        self.show_fallen("ВОПРОС 1, ОТВЕТ 1\nИ ВОПРОС 2 ВЫПАЛИ —\n"
                         "НАЧАЛО ЗАБЫТО")

    # --- Вывод ------------------------------------------------------------
    def final_message(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        main = VGroup(
            Text("ПАМЯТЬ = ИСТОРИЯ В ЗАПРОСЕ,", font_size=52,
                 color=PHOSPHOR, weight=BOLD),
            Text("НО ОКНО КОНЕЧНО", font_size=52, color=PHOSPHOR,
                 weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        main.move_to(UP * 0.4)
        self.play(FadeIn(main), run_time=1.0)
        self.wait(2.0)

        sub = VGroup(
            Text("СТАРЫЕ СООБЩЕНИЯ ВЫПАДАЮТ ·", font_size=34,
                 color=BEIGE, weight=BOLD),
            Text("ТОКЕНЫ — ДЕНЬГИ", font_size=34, color=BEIGE,
                 weight=BOLD),
        ).arrange(DOWN, buff=0.1)
        sub.next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
