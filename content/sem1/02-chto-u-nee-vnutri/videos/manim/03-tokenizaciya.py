"""Занятие 02, слайд 3. Технический ролик «Фраза → токены → дополнение» (ManimCE).

Что показывает (одна мысль): модель читает текст по кусочкам и дополняет его дальше —
токен за токеном.
  1. Фраза «Без труда не вытащишь и рыбку из пруда» (поговорка бабушки Алисы) нарезается
     на токены, каждый получает свой ID — модель видит только числа.
  2. Токен — целое слово, часть слова или знак препинания (пример: «вытащишь» → «выта» + «щишь»).
  3. Затем модель циклически дополняет текст: в блоках токенов — номера (ID), слова под ними
     подписями; в панели выбора кандидаты тоже показаны номерами с процентами. Модель выбирает
     следующий токен по вероятностям — « рыбку», « из», « пруда», «.» — так «пишется» продолжение.
  3.5. Пояснение: почему модель оперирует числами, а не словами напрямую (однозначность,
      универсальность словаря, вероятность ID, обратное восстановление слова).
  4. Параметр «температура»: при низкой — всегда самый вероятный токен (ответы одинаковые),
     при высокой — разброс, ответы живее.

Запуск (ManimCE, требуется установленный Manim):
    manim -r 1920,1080 --fps 30 03-tokenizaciya.py Tokenizaciya

Выход: videos/03-tokenizaciya.mp4 — подключается в `video_url` слайда 3 (video_type: direct).
"""

from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#141A14"

LUMINOFOR = "#7CFC00"
BOLOTO = "#4A5D3A"
RZHAVYI = "#8A5A33"
PYL = "#B8A98A"
BEGEZ = "#D8CBAC"
OLIVA = "#3E4A2F"
CHERN = "#1A1A1A"
FONT = "DejaVu Sans"

PHRASE_TOKENS = [
    ("Без", 12834),
    (" труда", 5021),
    (" не", 610),
    (" выта", 2100),
    ("щишь", 1742),
    (" и", 516),
    (" рыбку", 29012),
    (" из", 398),
    (" пруда", 48444),
    (".", 13),
]

TOKEN_COLORS = [
    BOLOTO, RZHAVYI, PYL, RZHAVYI, RZHAVYI, OLIVA,
    RZHAVYI, PYL, BOLOTO, OLIVA,
]

# Первая строка: «Без труда не выта щишь и», вторая: «рыбку из пруда.»
ROW_BREAK = 6

GIVEN_TOKENS = PHRASE_TOKENS[:ROW_BREAK]
NEXT_STEPS = [
    {
        "token": (" рыбку", 29012),
        "candidates": [(" рыбку", 29012, 0.87), (" лодку", 77155, 0.06), (" всё", 9053, 0.04)],
    },
    {
        "token": (" из", 398),
        "candidates": [(" из", 398, 0.92), (" на", 4421, 0.03), (" для", 8810, 0.02)],
    },
    {
        "token": (" пруда", 48444),
        "candidates": [(" пруда", 48444, 0.90), (" озера", 33120, 0.05), (" реки", 20145, 0.02)],
    },
    {
        "token": (".", 13),
        "candidates": [(".", 13, 0.94), ("!", 9, 0.03), ("…", 772, 0.02)],
    },
]


def token_box(token, color, font_size=36, pad_x=0.28, pad_y=0.18):
    """Рамка подгоняется под текст — слова не вылезают за края."""
    label = Text(token, font=FONT, color=WHITE, weight=BOLD, font_size=font_size)
    rect = RoundedRectangle(
        corner_radius=0.1,
        width=label.width + 2 * pad_x,
        height=label.height + 2 * pad_y,
        stroke_color=CHERN,
        stroke_width=5,
        fill_color=color,
        fill_opacity=1.0,
    )
    label.move_to(rect.get_center())
    return VGroup(rect, label)


def token_chip(tid, word, color, id_size=32, word_size=17, pad_x=0.22, pad_y=0.18):
    """Чип токена: номер (ID) внутри рамки, слово — подпись снизу."""
    num = Text(str(tid), font=FONT, color=WHITE, weight=BOLD, font_size=id_size)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=num.width + 2 * pad_x,
        height=num.height + 2 * pad_y,
        stroke_color=CHERN,
        stroke_width=5,
        fill_color=color,
        fill_opacity=1.0,
    )
    num.move_to(box.get_center())
    cap = Text(word, font=FONT, color=PYL, font_size=word_size)
    cap.next_to(box, DOWN, buff=0.08)
    return VGroup(box, num, cap)


def tokens_in_rows(token_color_pairs, break_at=ROW_BREAK, font_size=34, row_gap=0.35):
    """Собирает токены в одну или две строки; возвращает группу и плоский список боксов."""
    boxes = [
        token_box(tok, color, font_size=font_size)
        for (tok, _), color in token_color_pairs
    ]
    row1 = VGroup(*boxes[:break_at])
    row1.arrange(RIGHT, buff=0.12)
    if len(boxes) <= break_at:
        return VGroup(row1), boxes
    row2 = VGroup(*boxes[break_at:])
    row2.arrange(RIGHT, buff=0.12)
    row2.align_to(row1, LEFT)
    rows = VGroup(row1, row2).arrange(DOWN, buff=row_gap, aligned_edge=LEFT)
    return rows, boxes


def clear_screen(scene, run_time=0.5):
    """Убирает всё со сцены одним кадром — без «хвостов» вроде второй строки токенов."""
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=run_time)
        scene.remove(*scene.mobjects)


class Tokenizaciya(Scene):
    def construct(self):
        # 1. Титул
        title = Text("ФРАЗА → ТОКЕНЫ → ЧИСЛА", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=60)
        subtitle = Text("модель дополняет текст токен за токеном", font=FONT, color=PYL, font_size=40)
        subtitle.next_to(title, DOWN)
        header = VGroup(title, subtitle)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1.5)
        self.play(header.animate.shift(UP * 3.4).scale(0.55))
        self.wait(0.5)

        # 2. Фраза — поговорка бабушки Алисы
        caption = Text("поговорка бабушки Алисы", font=FONT, color=PYL, font_size=32)
        phrase = Text("Без труда не вытащишь и рыбку из пруда", font=FONT, color=BEGEZ, font_size=38)
        caption.move_to(UP * 1.9)
        phrase.next_to(caption, DOWN, buff=0.4)
        self.play(Write(caption))
        self.play(Write(phrase))
        self.wait(2.0)

        # 2.5. Что такое токен
        self.pokazat_chto_takoe_token(caption, phrase, subtitle)

        # 3. Разбивка на токены (две строки)
        pair_list = list(zip(PHRASE_TOKENS, TOKEN_COLORS))
        rows, boxes = tokens_in_rows(
            pair_list, break_at=ROW_BREAK, font_size=34, row_gap=1.25,
        )
        rows.move_to(UP * 0.35)

        self.add(rows)
        self.play(FadeIn(rows), run_time=2.5)
        self.wait(1.2)

        # 4. Каждый токен — это число (ID)
        ids = VGroup()
        for (_, tid), box in zip(PHRASE_TOKENS, boxes):
            num = Text(str(tid), font=FONT, color=LUMINOFOR, weight=BOLD, font_size=28)
            num.next_to(box, DOWN, buff=0.18)
            ids.add(num)
        self.play(LaggedStart(*[Write(n) for n in ids], lag_ratio=0.12), run_time=2.5)
        self.wait(0.8)
        note = Text("модель видит только числа", font=FONT, color=PYL, font_size=36)
        note.next_to(ids, DOWN, buff=0.45)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.5)

        # 5. Переход к дополнению
        given_boxes = [
            token_chip(tid, tok, color, id_size=30, word_size=16)
            for (tok, tid), color in zip(GIVEN_TOKENS, TOKEN_COLORS[:ROW_BREAK])
        ]
        given = VGroup(*given_boxes)
        given.arrange(RIGHT, buff=0.12)
        if given.width > config.frame_width - 1.2:
            given.scale_to_fit_width(config.frame_width - 1.2)
        given.move_to(DOWN * 2.0)
        row1, row2 = rows[0], rows[1]
        self.play(
            FadeOut(row1),
            FadeOut(row2),
            FadeOut(ids),
            FadeOut(note),
            run_time=0.6,
        )
        self.remove(rows, *boxes, ids, note)
        self.wait(0.4)
        hint = Text("получен текст: «Без труда не вытащишь и»", font=FONT, color=BEGEZ, font_size=38)
        hint.move_to(UP * 2.2)
        self.play(FadeIn(given, shift=UP * 0.2), FadeIn(hint, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(hint))

        # 6. Циклическое дополнение (модель видит номера, слово — подпись)
        seq = given
        for step in NEXT_STEPS:
            chosen_tok, chosen_id = step["token"]
            cands = step["candidates"]

            panel_title = Text("выбираем следующий токен", font=FONT, color=PYL, font_size=34)
            panel_title.move_to(UP * 2.45)
            self.play(FadeIn(panel_title, shift=DOWN * 0.2))

            cand_group = VGroup()
            for text, tid, prob in cands:
                chip = token_chip(tid, text, BOLOTO, id_size=26, word_size=13)
                pct = Text(f"{int(prob * 100)}%", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=30)
                row = VGroup(chip, pct).arrange(RIGHT, buff=0.5)
                cand_group.add(row)
            cand_group.arrange(DOWN, buff=0.2)
            cand_group.move_to(UP * 0.1)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in cand_group], lag_ratio=0.15), run_time=1.2)
            self.wait(0.6)

            chosen_chip = cand_group[0]
            self.play(
                chosen_chip[0].animate.set_stroke(LUMINOFOR, width=8),
                chosen_chip.animate.scale(1.06),
                run_time=0.35,
            )
            self.wait(0.4)

            new_box = token_chip(chosen_id, chosen_tok, LUMINOFOR, id_size=30, word_size=16)
            new_box.move_to(chosen_chip.get_center())
            self.play(new_box.animate.move_to(seq.get_right() + RIGHT * 0.7))
            seq.add(new_box)
            seq.arrange(RIGHT, buff=0.1)
            if seq.width > config.frame_width - 1.2:
                seq.scale_to_fit_width(config.frame_width - 1.2)
            seq.move_to(DOWN * 2.0)
            self.play(seq.animate)
            self.play(FadeOut(panel_title), FadeOut(cand_group))
            self.wait(0.7)

        # 6.5. Пояснение: почему модель оперирует числами
        self.pokazat_pochemu_chisla()

        # 7. Температура: без разброса ответы одинаковые
        self.pokazat_temperaturu(seq, title)

        # 8. Финальный кадр
        clear_screen(self)

        end = VGroup(
            Text("ФРАЗА → ТОКЕНЫ → ЧИСЛА → НОВЫЙ ТОКЕН", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=42),
            Text("так модель «пишет» ответ: токен за токеном, по вероятностям", font=FONT, color=BEGEZ, font_size=30),
            Text("температура задаёт разброс — иначе ответы как у робота", font=FONT, color=BEGEZ, font_size=28),
            Text("проверяем результат — не доверяем на слово", font=FONT, color=PYL, font_size=26),
        )
        end.arrange(DOWN, buff=0.45)
        if end.width > config.frame_width - 1.0:
            end.scale_to_fit_width(config.frame_width - 1.0)
        end.move_to(ORIGIN)
        self.play(Write(end))
        self.wait(3.0)

    def pokazat_temperaturu(self, seq, title):
        """Температура — две подсцены, затем итоговое сравнение двух колонок.

        Подсцена 1 (Т≈0): график вероятностей слева, попытки справа. Каждая
        попытка появляется последовательно — сначала «попытка n», потом фраза;
        на графике подсвечивается выбранный токен (всегда «рыбку»).
        Подсцена 2 (Т≈1): новый график слева, новые попытки справа, подсветка
        токена меняется от попытки к попытке (рыбку → лодку → всё).
        В конце вторая подсцена прячется, показываются две колонки текстов
        попыток (как в сравнении) и итоговый вывод внизу.
        """
        clear_screen(self)

        scene_title = Text(
            "ТЕМПЕРАТУРА: РАЗБРОС ОТВЕТОВ",
            font=FONT, color=LUMINOFOR, weight=BOLD, font_size=38,
        )
        scene_title.to_edge(UP, buff=0.7)
        context = Text(
            "«Без труда не вытащишь и…» — какой токен дальше?",
            font=FONT, color=BEGEZ, font_size=28,
        )
        context.next_to(scene_title, DOWN, buff=0.35)
        self.play(FadeIn(scene_title), FadeIn(context), run_time=0.6)
        self.wait(0.5)

        def prob_bars(probs):
            bars = VGroup()
            for tok, prob in probs:
                h = max(prob * 2.8, 0.15)
                bar = RoundedRectangle(
                    width=0.75, height=h, corner_radius=0.05,
                    fill_color=RZHAVYI, fill_opacity=0.35,
                    stroke_color=CHERN, stroke_width=4,
                )
                lbl = Text(tok.strip(), font=FONT, color=BEGEZ, font_size=20, weight=BOLD)
                lbl.next_to(bar, DOWN, buff=0.12)
                pct = Text(f"{int(prob * 100)}%", font=FONT, color=LUMINOFOR, font_size=18, weight=BOLD)
                pct.next_to(bar, UP, buff=0.08)
                bars.add(VGroup(bar, lbl, pct))
            bars.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            return bars

        def highlight(bars, idx):
            anims = []
            for i, bg in enumerate(bars):
                bar = bg[0]
                color = LUMINOFOR if i == idx else RZHAVYI
                opacity = 1.0 if i == idx else 0.35
                anims.append(bar.animate.set_fill(color, opacity=opacity))
            self.play(*anims, run_time=0.35)
            self.play(bars[idx][0].animate.scale(1.12), run_time=0.15)
            self.play(bars[idx][0].animate.scale(1 / 1.12), run_time=0.15)

        def make_attempt(idx, ending):
            label = Text(f"попытка {idx}", font=FONT, color=PYL, font_size=22, weight=BOLD)
            word = ending.strip()
            phrase = MarkupText(
                f'<b>…и <span foreground="{LUMINOFOR}">{word}</span> из пруда.</b>',
                font=FONT, font_size=26, color=BEGEZ,
            )
            row = VGroup(label, phrase).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            return label, phrase, row

        def banner(text, color):
            t = Text(text, font=FONT, color=WHITE, font_size=22, weight=BOLD)
            r = RoundedRectangle(
                width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.1,
                fill_color=color, fill_opacity=0.88, stroke_color=CHERN, stroke_width=4,
            )
            t.move_to(r)
            return VGroup(r, t)

        # --- Подсцена 1: Т ≈ 0 (без разброса) ---
        low_hdr = Text("Т ≈ 0 — без разброса", font=FONT, color=PYL, font_size=30, weight=BOLD)
        low_hdr.move_to(UP * 1.55)
        self.play(FadeIn(low_hdr), run_time=0.5)
        self.wait(0.2)

        low_bars = prob_bars([(" рыбку", 0.87), (" лодку", 0.06), (" всё", 0.04)])
        low_bars.scale(0.9).move_to(LEFT * 3.6 + DOWN * 0.3)
        self.play(FadeIn(low_bars, shift=UP * 0.15), run_time=0.6)
        self.wait(0.2)

        low_attempts = VGroup()
        low_slots = [UP * 1.1, ORIGIN, DOWN * 1.1]
        low_data = [(" рыбку", BEGEZ, 0), (" рыбку", BEGEZ, 0), (" рыбку", BEGEZ, 0)]
        for i, (ending, color, tok_idx) in enumerate(low_data):
            label, phrase, row = make_attempt(i + 1, ending)
            row.move_to(RIGHT * 3.6 + DOWN * 0.3 + low_slots[i])
            self.play(FadeIn(label), run_time=0.35)
            self.wait(0.15)
            highlight(low_bars, tok_idx)
            self.play(FadeIn(phrase), run_time=0.35)
            self.wait(0.35)
            low_attempts.add(row)
        self.wait(0.6)

        # --- Подсцена 2: Т ≈ 1 (с разбросом) ---
        self.play(
            FadeOut(low_hdr), FadeOut(low_bars), FadeOut(low_attempts),
            run_time=0.5,
        )
        self.wait(0.2)

        high_hdr = Text("Т ≈ 1 — с разбросом", font=FONT, color=LUMINOFOR, font_size=30, weight=BOLD)
        high_hdr.move_to(UP * 1.55)
        self.play(FadeIn(high_hdr), run_time=0.5)
        self.wait(0.2)

        high_bars = prob_bars([(" рыбку", 0.45), (" лодку", 0.30), (" всё", 0.25)])
        high_bars.scale(0.9).move_to(LEFT * 3.6 + DOWN * 0.3)
        self.play(FadeIn(high_bars, shift=UP * 0.15), run_time=0.6)
        self.wait(0.2)

        high_attempts = VGroup()
        high_data = [(" рыбку", BEGEZ, 0), (" лодку", LUMINOFOR, 1), (" всё", BEGEZ, 2)]
        for i, (ending, color, tok_idx) in enumerate(high_data):
            label, phrase, row = make_attempt(i + 1, ending)
            row.move_to(RIGHT * 3.6 + DOWN * 0.3 + low_slots[i])
            self.play(FadeIn(label), run_time=0.35)
            self.wait(0.15)
            highlight(high_bars, tok_idx)
            self.play(FadeIn(phrase), run_time=0.35)
            self.wait(0.35)
            high_attempts.add(row)
        self.wait(0.6)

        # --- Итог: вторая подсцена прячется, две колонки попыток + вывод ---
        self.play(
            FadeOut(high_hdr), FadeOut(high_bars), FadeOut(high_attempts),
            run_time=0.5,
        )
        self.wait(0.2)

        low_col_hdr = Text("Т ≈ 0", font=FONT, color=PYL, font_size=30, weight=BOLD)
        low_col_hdr.move_to(LEFT * 3.9 + UP * 1.6)
        high_col_hdr = Text("Т ≈ 1", font=FONT, color=LUMINOFOR, font_size=30, weight=BOLD)
        high_col_hdr.move_to(RIGHT * 3.9 + UP * 1.6)

        low_attempts.move_to(LEFT * 3.9 + DOWN * 0.2)
        high_attempts.move_to(RIGHT * 3.9 + DOWN * 0.2)
        self.play(
            FadeIn(low_col_hdr), FadeIn(high_col_hdr),
            FadeIn(low_attempts, shift=UP * 0.1), FadeIn(high_attempts, shift=UP * 0.1),
            run_time=0.7,
        )
        self.wait(0.5)

        low_overlay = banner("без разброса — все одинаковые", RZHAVYI)
        low_overlay.move_to(low_attempts.get_center())
        high_overlay = banner("разброс — ответы разные", LUMINOFOR)
        high_overlay.move_to(high_attempts.get_center())
        self.play(FadeIn(low_overlay, scale=0.9), FadeIn(high_overlay, scale=0.9), run_time=0.5)
        self.wait(0.8)

        conclusion = Text(
            "без температуры все ответы одинаковые, с температурой — разные",
            font=FONT, color=LUMINOFOR, weight=BOLD, font_size=34,
        )
        if conclusion.width > config.frame_width - 1.0:
            conclusion.scale_to_fit_width(config.frame_width - 1.0)
        conclusion.to_edge(DOWN, buff=0.6)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(2.0)

        self.play(
            FadeOut(scene_title), FadeOut(context),
            FadeOut(low_col_hdr), FadeOut(high_col_hdr),
            FadeOut(low_attempts), FadeOut(high_attempts),
            FadeOut(low_overlay), FadeOut(high_overlay), FadeOut(conclusion),
            run_time=0.5,
        )

    def pokazat_pochemu_chisla(self):
        """Почему модель оперирует числами (ID), а не словами напрямую."""
        clear_screen(self)

        title = Text(
            "ПОЧЕМУ МОДЕЛЬ ОПЕРИРУЕТ ЧИСЛАМИ",
            font=FONT, color=LUMINOFOR, weight=BOLD, font_size=42,
        )
        title.to_edge(UP, buff=0.7)
        self.play(Write(title))
        self.wait(0.6)

        theses = VGroup(
            Text("Число однозначно: без опечаток и заглавных букв",
                 font=FONT, color=BEGEZ, font_size=22),
            Text("Число универсально: не зависит от языка и текста",
                 font=FONT, color=BEGEZ, font_size=22),
        ).arrange(DOWN, buff=0.35)
        theses.move_to(UP * 1.0)
        self.play(Succession(*[Write(t) for t in theses]), run_time=4.0)
        self.wait(1.0)

        # Мини-схема: слово → номер
        arrow = Text("→", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=40)
        pairs = [("рыбку", 29012), ("пруда", 48444), (" и", 516)]
        diagram = VGroup()
        for word, tid in pairs:
            w = Text(word, font=FONT, color=PYL, font_size=26, weight=BOLD)
            n = token_chip(tid, "", BOLOTO, id_size=26, word_size=14)
            diagram.add(VGroup(w, arrow.copy(), n).arrange(RIGHT, buff=0.25))
        diagram.arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in diagram], lag_ratio=0.2), run_time=1.2)
        self.wait(3.5)

        self.play(
            FadeOut(title), FadeOut(theses), FadeOut(diagram),
            run_time=0.5,
        )

    def pokazat_chto_takoe_token(self, caption, phrase, subtitle):
        """Пояснение: токен = слово, часть слова или знак; пример разбиения слова."""
        self.play(FadeOut(subtitle), run_time=0.3)

        title = Text(
            "ТОКЕН — СЛОВО, ЧАСТЬ СЛОВА ИЛИ ЗНАК",
            font=FONT, color=LUMINOFOR, weight=BOLD, font_size=38,
        )
        title.to_edge(UP, buff=1.1)

        types = VGroup(
            Text("• целое слово: «Без»", font=FONT, color=BEGEZ, font_size=30),
            Text("• часть слова: «выта» + «щишь»", font=FONT, color=BEGEZ, font_size=30),
            Text("• знак: «.»", font=FONT, color=BEGEZ, font_size=30),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        types.next_to(title, DOWN, buff=0.5)

        ex_word = token_box("Без", BOLOTO, font_size=32)
        ex_word_lbl = Text("слово", font=FONT, color=PYL, font_size=24)
        ex_word_lbl.next_to(ex_word, DOWN, buff=0.15)
        ex_word_grp = VGroup(ex_word, ex_word_lbl)

        ex_whole = token_box("вытащишь", OLIVA, font_size=32)
        ex_whole_lbl = Text("части слова", font=FONT, color=PYL, font_size=24)
        ex_whole_lbl.next_to(ex_whole, DOWN, buff=0.15)
        ex_split_grp = VGroup(ex_whole, ex_whole_lbl)

        ex_dot = token_box(".", PYL, font_size=32)
        ex_dot_lbl = Text("знак", font=FONT, color=PYL, font_size=24)
        ex_dot_lbl.next_to(ex_dot, DOWN, buff=0.15)
        ex_dot_grp = VGroup(ex_dot, ex_dot_lbl)

        examples = VGroup(ex_word_grp, ex_split_grp, ex_dot_grp).arrange(RIGHT, buff=1.0)
        examples.next_to(types, DOWN, buff=0.55)

        self.play(
            FadeOut(caption),
            phrase.animate.scale(0.65).move_to(DOWN * 2.6),
        )
        self.play(FadeIn(title, shift=DOWN * 0.15))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in types], lag_ratio=0.15))
        self.wait(0.5)

        self.play(FadeIn(ex_word_grp, shift=UP * 0.15))
        self.wait(0.4)
        self.play(FadeIn(ex_split_grp, shift=UP * 0.15))
        self.wait(0.6)

        split_center = ex_whole.get_center()
        ex_part1 = token_box("выта", RZHAVYI, font_size=32)
        ex_part2 = token_box("щишь", RZHAVYI, font_size=32)
        arrow = Text("→", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=40)
        split_result = VGroup(ex_part1, arrow, ex_part2).arrange(RIGHT, buff=0.15)
        split_result.move_to(split_center)
        ex_whole_lbl.next_to(split_result, DOWN, buff=0.15)
        self.play(
            FadeOut(ex_whole),
            FadeIn(split_result, shift=UP * 0.05),
            run_time=0.9,
        )
        ex_split_grp.remove(ex_whole)
        ex_split_grp.add(split_result)
        ex_whole_lbl.next_to(split_result, DOWN, buff=0.15)
        self.wait(0.4)

        self.play(FadeIn(ex_dot_grp, shift=UP * 0.15))
        self.wait(1.5)

        self.play(
            FadeOut(title), FadeOut(types), FadeOut(examples), FadeOut(phrase),
            run_time=0.6,
        )
