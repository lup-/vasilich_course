"""Занятие 02, слайд 3. Технический ролик «Фраза → токены → дополнение» (ManimCE).

Что показывает (одна мысль): модель читает текст по кусочкам и дополняет его дальше —
токен за токеном.
  1. Фраза «Без труда не вытащишь и рыбку из пруда» (поговорка бабушки Алисы) нарезается
     на токены-под-слова, каждый получает свой ID — модель видит только числа.
  2. Затем модель циклически дополняет текст: получив «Без труда не вытащишь и», она по
     вероятностям выбирает следующий токен « рыбку», потом « из», « пруда», «.» — так
     «пишется» продолжение, 3–4 слова.

Запуск (ManimCE, требуется установленный Manim):
    manim -r 1920,1080 -f 30 03-tokenizaciya.py Tokenizaciya
    # или через профиль качества: manim -qm 03-tokenizaciya.py Tokenizaciya

Выход: videos/03-tokenizaciya.mp4 — подключается в `video_url` слайда 3 (video_type: direct).

Детерминизм: рендер не использует случайность — один и тот же скрипт даёт один и тот же ролик.
"""

from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#141A14"

# Палитра из comic-style.md: болотный/ржавый/пыльный/бежевый + кислотно-зелёный люминофор.
LUMINOFOR = "#7CFC00"
BOLOTO = "#4A5D3A"
RZHAVYI = "#8A5A33"
PYL = "#B8A98A"
BEGEZ = "#D8CBAC"
OLIVA = "#3E4A2F"
CHERN = "#1A1A1A"

# Шрифт без засечек, поддерживающий кириллицу.
FONT = "DejaVu Sans"

# Вся фраза токенами-под-словами (ID иллюстративные, точные зависят от токенизатора модели).
PHRASE_TOKENS = [
    ("Без", 12834),
    (" труда", 5021),
    (" не", 610),
    (" вытащишь", 3842),
    (" и", 516),
    (" рыбку", 29012),
    (" из", 398),
    (" пруда", 48444),
    (".", 13),
]

TOKEN_COLORS = [BOLOTO, RZHAVYI, PYL, BOLOTO, OLIVA, RZHAVYI, PYL, BOLOTO, OLIVA]

# Для циклического дополнения: дан старт «Без труда не вытащишь и», дальше модель выбирает
# следующий токен по вероятностям (кандидаты + вероятность выбраны).
GIVEN_TOKENS = PHRASE_TOKENS[:5]
NEXT_STEPS = [
    {
        "token": (" рыбку", 29012),
        "candidates": [(" рыбку", 0.87), (" лодку", 0.06), (" всё", 0.04)],
    },
    {
        "token": (" из", 398),
        "candidates": [(" из", 0.92), (" на", 0.03), (" для", 0.02)],
    },
    {
        "token": (" пруда", 48444),
        "candidates": [(" пруда", 0.90), (" озера", 0.05), (" реки", 0.02)],
    },
    {
        "token": (".", 13),
        "candidates": [(".", 0.94), ("!", 0.03), ("…", 0.02)],
    },
]


def token_box(token, color, width=1.35, height=0.9, font_size=36):
    rect = RoundedRectangle(
        corner_radius=0.1,
        width=width,
        height=height,
        stroke_color=CHERN,
        stroke_width=5,
        fill_color=color,
        fill_opacity=1.0,
    )
    label = Text(token, font=FONT, color=WHITE, weight=BOLD, font_size=font_size)
    label.move_to(rect.get_center())
    return VGroup(rect, label)


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
        phrase = Text("Без труда не вытащишь и рыбку из пруда", font=FONT, color=BEGEZ, font_size=46)
        caption.move_to(UP * 1.9)
        phrase.next_to(caption, DOWN, buff=0.4)
        self.play(Write(caption))
        self.play(Write(phrase))
        self.wait(2.0)

        # 3. Разбивка на токены-под-слова
        boxes = VGroup()
        for (tok, _), color in zip(PHRASE_TOKENS, TOKEN_COLORS):
            boxes.add(token_box(tok, color))
        boxes.arrange(RIGHT, buff=0.1)
        boxes.scale_to_fit_width(config.frame_width - 1.6)
        boxes.move_to(UP * 1.0)

        self.play(FadeOut(VGroup(caption, phrase)))
        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in boxes], lag_ratio=0.12),
            run_time=3.0,
        )
        self.wait(1.2)

        # 4. Каждый токен — это число (ID)
        ids = VGroup()
        for (_, tid), box in zip(PHRASE_TOKENS, boxes):
            num = Text(str(tid), font=FONT, color=LUMINOFOR, weight=BOLD, font_size=30)
            num.next_to(box, DOWN, buff=0.2)
            ids.add(num)
        self.play(LaggedStart(*[Write(n) for n in ids], lag_ratio=0.15), run_time=2.5)
        self.wait(0.8)
        note = Text("модель видит только числа", font=FONT, color=PYL, font_size=36)
        note.next_to(ids, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.5)

        # 5. Переход к дополнению: оставляем только «данный» старт
        given = VGroup()
        for (tok, _), color in zip(GIVEN_TOKENS, TOKEN_COLORS):
            given.add(token_box(tok, color, width=1.35, height=0.9, font_size=36))
        given.arrange(RIGHT, buff=0.08)
        given.move_to(DOWN * 1.7)
        self.play(FadeOut(VGroup(boxes, ids, note)))
        self.wait(0.4)
        hint = Text("получен текст: «Без труда не вытащишь и»", font=FONT, color=BEGEZ, font_size=38)
        hint.move_to(UP * 2.2)
        self.play(FadeIn(given, shift=UP * 0.2), FadeIn(hint, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(hint))

        # 6. Циклическое дополнение: токен за токеном
        seq = given
        for i, step in enumerate(NEXT_STEPS):
            chosen_tok, chosen_id = step["token"]
            cands = step["candidates"]

            panel_title = Text("выбираем следующий токен", font=FONT, color=PYL, font_size=34)
            panel_title.move_to(UP * 2.2)
            self.play(FadeIn(panel_title, shift=DOWN * 0.2))

            cand_group = VGroup()
            for text, prob in cands:
                row = VGroup(
                    Text(text, font=FONT, color=WHITE, weight=BOLD, font_size=32),
                    Text(f"{int(prob * 100)}%", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=30),
                )
                row.arrange(RIGHT, buff=0.6)
                row.move_to(UP * (1.0 - i * 0.02) - 0.55 * len(cand_group))
                cand_group.add(row)
            cand_group.arrange(DOWN, buff=0.25)
            cand_group.move_to(UP * 0.6)
            self.play(LaggedStart(*[Write(r) for r in cand_group], lag_ratio=0.15), run_time=1.2)
            self.wait(0.6)

            chosen_row = cand_group[0]
            self.play(chosen_row.animate.set_color(BEGEZ))
            self.wait(0.4)

            # Выбранный токен отправляется в конец последовательности
            new_box = token_box(chosen_tok, LUMINOFOR, width=1.35, height=0.9, font_size=36)
            new_box.move_to(chosen_row.get_center())
            self.play(new_box.animate.move_to(seq.get_right() + RIGHT * 0.8))
            seq.add(new_box)
            seq.arrange(RIGHT, buff=0.08)
            seq.move_to(DOWN * 1.7)
            self.play(seq.animate)
            self.play(FadeOut(panel_title), FadeOut(cand_group))
            self.wait(0.7)

        # 7. Финальный кадр
        self.play(FadeOut(seq))
        end = VGroup(
            Text("ФРАЗА → ТОКЕНЫ → ЧИСЛА → НОВЫЙ ТОКЕН", font=FONT, color=LUMINOFOR, weight=BOLD, font_size=56),
            Text("так модель «пишет» ответ: токен за токеном, по вероятностям", font=FONT, color=BEGEZ, font_size=38),
            Text("проверяем результат — не доверяем на слово", font=FONT, color=PYL, font_size=34),
        )
        end.arrange(DOWN, buff=0.5)
        self.play(Write(end))
        self.wait(3.0)
