# -*- coding: utf-8 -*-
"""Вызов инструментов: руки для модели. Технический ролик Manim (ManimCE) для занятия 06.

Одна мысль: для живых данных RAG не годится — нужен вызов инструмента; модель сама решает вызвать
инструмент, формирует вызов спец-токеном, обвязка выполняет скрипт и возвращает реальный результат,
модель отвечает по нему.

Сцены:
  0. «RAG НЕ ВСЕГДА ПОДХОДИТ» (ч. 1): запрос уходит в модель, из векторной базы валятся ордера
     (обработанные тускнеют), +/- подписи сваливаются кучей к Василичу (куча растёт сверху вниз);
     индикатор «КОНТЕКСТНОЕ ОКНО» под столбцом модели: зелёный → жёлтый (90%) → красный перелив
     (заливка уходит за правый край кадра); чипы «А ИНВЕНТАРИЗАЦИЯ?», «А ВОЗВРАТЫ?», «А БРАК?»
     ровной стопкой поверх кучи; «ДУМАЮ...» гаснет, модель отвечает мигающими плашками-ошибками
     одной ширины; Василич спокойный → злой → супер-злой.
  0b. «RAG НЕ ПОДХОДИТ, ЕСЛИ ДАННЫЕ ЖИВЫЕ» (ч. 2): список погода / новости / показания датчиков /
      остатки на складе — пункты зачёркиваются по одному; мост: живые данные берём вызовом инструмента.
  1. «ВЫЗОВ ИНСТРУМЕНТА ПОД КАПОТОМ»: три колонки UI / ОБВЯЗКА (HARNESS, пониже) / МОДЕЛЬ (LLM) без фона;
     снаружи под обвязкой — блоки «СКРИПТ GET_SKLAD.PY» (pandas: read_csv + groupby с суммой) и
     «JSON ИНСТРУМЕНТА» с командой запуска python get_sklad.py — той же ширины, что и колонка.
     Запрос появляется в UI; копия летит в обвязку, где к нему добавляются чип «СИСТЕМНЫЙ ПРОМПТ
     СКЛАДА» (прилетает снизу) и чип инструмента «get_sklad tool: остатки склада» (вылетает из
     json-блока) — без спец-токенов; тёмным чипам — светлый бордюр. Пакет летит в модель; ответ со
     спец-токенами (<|im_start|>, <|plugin_call|>, <|im_end|> — как в занятии 02) возвращается
     в обвязку, сегмент вызова подсвечивается, окно модели очищается; вертикальная стрелка от чипа
     ответа ведёт к заголовку скрипта; скрипт вспыхивает ярко-зелёным с чёрным текстом, в UI под
     запросом мигает «ЗАПУСК СКРИПТА...» (остаётся до конца сцены); скрипт тускнеет, в обвязку
     возвращается json-ответ, от него отделяется чип «РЕЗУЛЬТАТ РАБОТЫ СКРИПТА» и встаёт в UI;
     все пять чипов обвязки выстраиваются стопкой (межчипное расстояние) и летят в модель копией;
     ответ «НА СКЛАДЕ ПОРОШОК И СОДА. ЦЕМЕНТА НЕТ» формируется под стопкой, окно модели очищается;
     ответ копией возвращается в обвязку под стопку, второй копией уходит в UI.
  2. Вывод: ИНСТРУМЕНТ — РУКИ МОДЕЛИ.

Внешние ассеты (см. videos/README.md): videos/Vasilych_calm.png, videos/Vasilych_angry.png,
videos/Vasilych_super_angry.png — портреты Василича (1024×1024) для смены настроения.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 6 \
        06-vyzov-instrumentov.py VyzovInstrumentov
"""

import os
import random

from manim import *


PHOSPHOR = "#B6FF3C"   # кислотно-зелёный люминофор экранов
SWAMP    = "#4A5D23"   # болотный зелёный
RUST     = "#8C4A2F"   # ржавый
DUST     = "#8A8A7A"   # пыльный серый
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
INK      = "#111111"   # чёрный контур
YELLOWISH = "#E8C547"  # жёлтый сигнал «почти полно»
RED_ALERT = "#D0392B"  # красный сигнал переполнения
MONO     = "DejaVu Sans Mono"

VIDEOS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def bubble(text, color, font_size=34, stroke=INK):
    """Блок с закруглённой рамкой, контуром, надписью заглавными."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=stroke,
                            stroke_width=6)
    return VGroup(rect, t)


def vasilych_img(name, height=2.1):
    """Портрет Василича из videos/, единая высота для смены настроений."""
    img = ImageMobject(os.path.join(VIDEOS_DIR, name))
    img.set_height(height)
    return img


class VyzovInstrumentov(Scene):
    def construct(self):
        self.rag_ne_podxodit()
        self.rag_ne_podxodit_spisok()
        self.harness_i_tokeny()
        self.final_message()

    def _card(self, body_text, hold=2.0, body_time=2.0, font_size=30,
              color=BEIGE, mono=False):
        """Карточка-пояснение: экран накрывается чёрным, текст печатается
        по глифам; после паузы (hold) всё исчезает, сцена продолжается
        с места остановки."""
        font = MONO if mono else "DejaVu Sans"
        overlay = Rectangle(
            width=config.frame_width + 0.2,
            height=config.frame_height + 0.2,
            stroke_width=0, fill_color=BLACK, fill_opacity=1,
        )
        body_card = Text(body_text, font=font, font_size=font_size,
                         color=color, weight=BOLD if not mono else NORMAL)
        self.play(FadeIn(overlay), run_time=0.3)
        glyphs = body_card.family_members_with_points()
        self.play(LaggedStart(*[FadeIn(g) for g in glyphs], lag_ratio=0.04),
                  run_time=body_time)
        self.remove(*glyphs)
        self.add(body_card)
        self.wait(hold)
        self.play(FadeOut(overlay), FadeOut(body_card), run_time=0.7)

    # --- 0. RAG не всегда подходит: груда документов вместо инструмента (0–30 c) --
    def rag_ne_podxodit(self):
        rnd = random.Random(6)

        title = Text("RAG НЕ ВСЕГДА ПОДХОДИТ", font_size=42,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.8)

        # запрос (строим заранее — от него ширина столбца «МОДЕЛЬ»)
        q = bubble("КАКИЕ ПОЗИЦИИ\nЕСТЬ НА СКЛАДЕ?", BEIGE, font_size=22)

        # три столбца: векторная база / модель (чуть шире под чип запроса) /
        # Василич (без рамки)
        col_h = 4.8
        xs = [-4.8, 0.0, 4.8]

        def kolonka(x, label_text, w):
            rect = RoundedRectangle(width=w, height=col_h, corner_radius=0.1,
                                    fill_color=SWAMP, fill_opacity=0.0,
                                    stroke_color=DUST, stroke_width=5)
            rect.move_to([x, -0.15, 0])
            lab = Text(label_text, font_size=26, color=BEIGE,
                       weight=BOLD).next_to(rect, UP, buff=0.12)
            return rect, lab

        kb_rect, kb_lab = kolonka(xs[0], "ВЕКТОРНАЯ БАЗА", 3.5)
        md_rect, md_lab = kolonka(xs[1], "МОДЕЛЬ", q.width + 0.55)
        vas_x = xs[2]
        self.play(FadeIn(kb_rect), FadeIn(kb_lab),
                  FadeIn(md_rect), FadeIn(md_lab), run_time=0.8)

        # Василич: спокойный → злой → супер-злой
        v_calm = vasilych_img("Vasilych_calm.png").move_to([vas_x, 1.55, 0])
        v_angry = vasilych_img("Vasilych_angry.png").move_to(v_calm.get_center())
        v_super = vasilych_img("Vasilych_super_angry.png").move_to(v_calm.get_center())
        self.play(FadeIn(v_calm), run_time=0.8)

        # индикатор контекстного окна под центральным столбцом («МОДЕЛЬ»)
        track = RoundedRectangle(width=3.6, height=0.34, corner_radius=0.08,
                                 fill_color="#1A1A1A", fill_opacity=0.9,
                                 stroke_color=DUST, stroke_width=4)
        track.move_to([xs[1], -3.05, 0])
        bar_anchor = track.get_left() + RIGHT * 0.07
        bar = Rectangle(width=0.01, height=0.20, fill_color=PHOSPHOR,
                        fill_opacity=1.0, stroke_width=0)
        bar.move_to(bar_anchor + RIGHT * 0.005)
        bar_lab = Text("КОНТЕКСТНОЕ ОКНО", font_size=18, color=BEIGE,
                       weight=BOLD).next_to(track, DOWN, buff=0.12)
        self.play(FadeIn(track), FadeIn(bar), FadeIn(bar_lab), run_time=0.6)

        BAR_OFF_W = 9.2  # ширина заливки при полном переливе — за правый край кадра

        def bar_w(frac):
            """Ширина заливки; frac > 1 — вылет за трек и правый край кадра."""
            base = max(0.01, frac * (track.width - 0.14))
            if frac <= 1.0:
                return base
            k = min(1.0, (frac - 1.0) / 0.10)
            return base + k * (BAR_OFF_W - base)

        def bar_to(frac, colr=None, run_time=0.25):
            anims = [bar.animate.stretch_to_fit_width(bar_w(frac))
                     .move_to(bar_anchor + RIGHT * bar_w(frac) / 2)]
            if colr is not None:
                anims[0] = anims[0].set_color(colr)
            self.play(*anims, run_time=run_time)

        # запрос прилетает снизу в центральный столбец
        q.move_to([xs[1], -5.4, 0])
        self.add(q)
        self.play(q.animate.move_to([xs[1], 1.45, 0]), run_time=1.0)

        think = Text("ДУМАЮ...", font_size=26, color=PHOSPHOR,
                     weight=BOLD).move_to([xs[1], 0.55, 0])
        think.add_updater(lambda m: m.set_fill(
            opacity=1.0 if int(self.time / 0.4) % 2 == 0 else 0.15))
        self.play(FadeIn(think), run_time=0.4)

        # ордера заполняют векторную базу
        orders = [
            ("ПРИХОДНЫЙ ОРДЕР № 112", True),
            ("РАСХОДНЫЙ ОРДЕР № 87", False),
            ("ПРИХОДНЫЙ ОРДЕР № 118", True),
            ("РАСХОДНЫЙ ОРДЕР № 91", False),
            ("ПРИХОДНЫЙ ОРДЕР № 124", True),
            ("РАСХОДНЫЙ ОРДЕР № 95", False),
            ("ПРИХОДНЫЙ ОРДЕР № 130", True),
            ("РАСХОДНЫЙ ОРДЕР № 103", False),
        ]
        prihod = ["+100 КГ СОДЫ", "+40 КГ ПОРОШКА", "+60 КГ МЫЛА"]
        rashod = ["-20 КГ ЦЕМЕНТА", "-35 КГ СОДЫ", "-10 КГ МЫЛА"]

        cards = []
        for i, (name, _) in enumerate(orders):
            t = Text(name, font_size=14, color=INK, weight=BOLD)
            card = RoundedRectangle(width=3.05, height=0.44, corner_radius=0.06,
                                    fill_color=BEIGE, fill_opacity=1.0,
                                    stroke_color=INK, stroke_width=3)
            card.move_to([xs[0], 1.9 - i * 0.57, 0])
            t.move_to(card.get_center())
            cards.append(VGroup(card, t))
            self.play(FadeIn(cards[-1]), run_time=0.22)

        # куча под Василичем: растёт сверху вниз (от Василича к индикатору),
        # сетка посадочных мест, джиттер по seed
        pile_pts = []
        for r in range(7):
            for c in range(3):
                px = vas_x + (c - 1) * 1.15 + rnd.uniform(-0.35, 0.35)
                py = -0.50 - r * 0.36 + rnd.uniform(-0.06, 0.06)
                rot = rnd.uniform(-9, 9)
                pile_pts.append(([px, py, 0], rot))
        pile_idx = 0

        # ордера обрабатываются по очереди: потускнели — данные улетели в кучу
        for i, grp in enumerate(cards):
            _, is_prihod = orders[i]
            goods = prihod if is_prihod else rashod
            colr = PHOSPHOR if is_prihod else RED_ALERT

            self.play(grp.animate.set_opacity(0.30), run_time=0.25)
            if i == 2:  # на третьей накладной Василич злеет
                self.play(FadeOut(v_calm, run_time=0.2),
                          FadeIn(v_angry, run_time=0.2))
            for k in range(2):
                txt = goods[(i + k) % 3]
                m = Text(txt, font_size=15, color=colr, weight=BOLD)
                m.move_to(grp.get_center())
                pt, rot = pile_pts[pile_idx]
                pile_idx += 1
                self.play(m.animate.move_to(pt).rotate(rot), run_time=0.55)
            bar_to((i + 1) * 0.90 / len(orders))

        self.wait(0.3)
        bar_to(0.90, colr=YELLOWISH, run_time=0.4)

        # сверх плана: чипы «А ...?» выстраиваются ровной стопкой поверх кучи,
        # окно переливается через край
        words = [("А ИНВЕНТАРИЗАЦИЯ?", 0.96), ("А ВОЗВРАТЫ?", 1.02),
                 ("А БРАК?", 1.10)]
        chips = []
        for k, (wd, _) in enumerate(words):
            ch = bubble(wd, BEIGE, font_size=16)
            if k == 0:
                ch.move_to([vas_x, -0.30, 0])
            else:
                ch.next_to(chips[-1], DOWN, buff=0.18)
            chips.append(ch)
        for wi, ch in enumerate(chips):
            target = ch.get_center()
            ch.move_to([vas_x + rnd.uniform(-0.8, 0.8), -4.9, 0])
            self.add(ch)
            self.play(ch.animate.move_to(target), run_time=0.65)
            frac = words[wi][1]
            bar_to(frac, colr=YELLOWISH if frac <= 1.0 else RED_ALERT,
                   run_time=0.3)

        for _ in range(3):  # красный мигает — перелив
            self.play(bar.animate.set_fill(opacity=0.25), run_time=0.16)
            self.play(bar.animate.set_fill(opacity=1.0), run_time=0.16)

        # на переливе Василич в ярости
        self.play(FadeOut(v_angry, run_time=0.25),
                  FadeIn(v_super, run_time=0.25))

        # «ДУМАЮ...» гаснет — модель отвечает ошибками вместо результата
        think.clear_updaters()
        self.play(FadeOut(think), run_time=0.3)
        err1 = bubble("Ошибка: превышено\nвремя ожидания ответа", RUST,
                      font_size=16)
        err1.next_to(q, DOWN, buff=0.18)
        err2 = bubble("Ошибка:\nнедостаточно баланса", RUST, font_size=16)
        err2.next_to(err1, DOWN, buff=0.22)
        # плашки одинаковой ширины (рамку растягиваем, текст по центру)
        ew = max(err1[0].width, err2[0].width)
        for ec in (err1, err2):
            ec[0].stretch_to_fit_width(ew)
            ec[1].move_to(ec[0].get_center())
        self.play(FadeIn(err1), run_time=0.5)
        self.play(FadeIn(err2), run_time=0.5)

        def err_pulse(m):  # ошибки мигают, пока Василич в ярости
            op = 1.0 if int(self.time / 0.4) % 2 == 0 else 0.25
            m.set_fill(opacity=op)
            m.set_stroke(opacity=op)

        err1.add_updater(err_pulse)
        err2.add_updater(err_pulse)
        self.wait(3.5)  # пауза перед переходом — ошибки всё это время мигают

        err1.clear_updaters()
        err2.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    # --- 0b. RAG не подходит для живых данных: список с зачёркиванием ----------
    def rag_ne_podxodit_spisok(self):
        title = Text("RAG НЕ ПОДХОДИТ, ЕСЛИ ДАННЫЕ ЖИВЫЕ", font_size=38,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.7)
        self.wait(0.6)

        items = ["ПОГОДА", "НОВОСТИ", "ПОКАЗАНИЯ ДАТЧИКОВ", "ОСТАТКИ НА СКЛАДЕ"]
        rows = []
        for i, name in enumerate(items):
            t = Text(name, font_size=34, color=BEIGE, weight=BOLD)
            t.move_to([0, 2.0 - i * 1.05, 0])
            self.play(FadeIn(t), run_time=0.35)
            rows.append(t)
            self.wait(0.5)  # небольшая пауза перед зачёркиванием
            line = Line(start=t.get_left() + LEFT * 0.15,
                        end=t.get_right() + RIGHT * 0.15,
                        color=RED_ALERT, stroke_width=7)
            self.play(Create(line), run_time=0.35)
            rows[-1] = VGroup(t, line)
            self.wait(0.35)

        bridge = Text("ЖИВЫЕ ДАННЫЕ БЕРЁМ ВЫЗОВОМ ИНСТРУМЕНТА →", font_size=28,
                      color=YELLOWISH, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(bridge), run_time=0.7)
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    # --- 1. Вызов инструмента под капотом: UI → обвязка → модель (44–70 с) --------
    def harness_i_tokeny(self):
        X = 0.10  # межчипное расстояние в стопках

        def tok(text, color=DUST, fs=12):
            return Text(text, font=MONO, font_size=fs, color=color)

        def rus(text, fs=11, color=BEIGE):
            return Text(text, font_size=fs, color=color, weight=BOLD)

        def row_chip(parts, fill="#1C2412", pad_w=0.26, pad_h=0.16):
            # тёмным чипам — светлый бордюр, бежевым — чернильный
            stroke = INK if fill == BEIGE else DUST
            g = VGroup(*parts).arrange(RIGHT, buff=0.05)
            r = RoundedRectangle(width=g.width + pad_w, height=g.height + pad_h,
                                 corner_radius=0.06, fill_color=fill,
                                 fill_opacity=0.95, stroke_color=stroke,
                                 stroke_width=2)
            g.move_to(r.get_center())
            return VGroup(r, g)

        def frame_block(lines, fill, stroke=INK, sw=3, pad_w=0.28, pad_h=0.22):
            g = VGroup(*lines).arrange(DOWN, buff=0.06)
            r = RoundedRectangle(width=g.width + pad_w, height=g.height + pad_h,
                                 corner_radius=0.07, fill_color=fill,
                                 fill_opacity=0.95, stroke_color=stroke,
                                 stroke_width=sw)
            g.move_to(r.get_center())
            return VGroup(r, g)

        title = Text("ВЫЗОВ ИНСТРУМЕНТА ПОД КАПОТОМ", font_size=40,
                     color=PHOSPHOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.8)

        # три колонки: UI / обвязка (harness, пониже) / модель (LLM), без фона
        def kol(x, w, h, name):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.1,
                                 fill_opacity=0.0,
                                 stroke_color=DUST, stroke_width=5)
            r.move_to([x, 2.30 - h / 2, 0])
            lab = Text(name, font_size=19, color=BEIGE, weight=BOLD)
            lab.next_to(r, UP, buff=0.14)
            return r, lab

        ui_r, ui_lab = kol(-4.85, 4.15, 6.2, "ЭКРАН ПОЛЬЗОВАТЕЛЯ (UI)")
        ha_w = 4.5
        ha_r, ha_lab = kol(0.0, ha_w, 4.05, "ОБВЯЗКА (HARNESS)")
        ll_r, ll_lab = kol(4.85, 4.15, 6.2, "МОДЕЛЬ (LLM)")
        self.play(FadeIn(ui_r), FadeIn(ui_lab), FadeIn(ha_r), FadeIn(ha_lab),
                  FadeIn(ll_r), FadeIn(ll_lab), run_time=0.9)

        # снаружи под обвязкой: блок «СКРИПТ GET_SKLAD.PY» (ближе к колонке)
        # и под ним «JSON ИНСТРУМЕНТА» — той же ширины, что и колонка
        def widen_to_col(block):
            block[0].stretch_to_fit_width(ha_w)
            block[1].move_to(block[0].get_center())
            return block

        scr_lab = Text("СКРИПТ GET_SKLAD.PY", font_size=12, color=DUST,
                       weight=BOLD)
        scr_lab.next_to(np.array([0.0, -1.75, 0]), DOWN, buff=0.12)
        scr_b = frame_block(
            [tok('df = pd.read_csv("sklad.csv")'),
             tok('print(df.groupby("товар")["кг"].sum())')],
            fill="#141414", stroke=DUST, sw=3, pad_h=0.12)
        scr_b.move_to([0, scr_lab.get_bottom()[1] - 0.07 - scr_b.height / 2, 0])
        widen_to_col(scr_b)
        json_lab = Text("JSON ИНСТРУМЕНТА", font_size=12, color=DUST,
                        weight=BOLD).next_to(scr_b, DOWN, buff=0.08)
        json_b = frame_block(
            [tok('{"name": "get_sklad",', PHOSPHOR),
             tok(' "desc": "остатки sklad.csv",', PHOSPHOR),
             tok(' "cmd": "python get_sklad.py"}', PHOSPHOR)],
            fill="#101408", stroke=DUST, pad_h=0.12)
        json_b.move_to([0, json_lab.get_bottom()[1] - 0.07 - json_b.height / 2,
                        0])
        widen_to_col(json_b)
        self.play(FadeIn(scr_b), FadeIn(scr_lab),
                  FadeIn(json_b), FadeIn(json_lab), run_time=0.6)

        # 1. запрос появляется в UI
        q_txt = "КАКИЕ ПОЗИЦИИ\nЕСТЬ НА СКЛАДЕ?"
        q_ui = bubble(q_txt, BEIGE, font_size=17)
        q_ui.move_to([-4.85, 1.55, 0])
        self.play(FadeIn(q_ui), run_time=0.8)
        self.wait(0.4)

        # 2. копия запроса летит в обвязку; к ней ДОБАВЛЯЮТСЯ системный промпт
        #    и информация об инструменте (отдельные чипы, без спец-токенов)
        q_h = row_chip([rus("Какие позиции есть на складе?", 12, INK)],
                       fill=BEIGE)
        q_h.move_to(q_ui.get_center())
        self.add(q_h)
        self.play(q_h.animate.move_to([0, 0.95, 0]), run_time=0.8)
        self.wait(0.5)
        sys_ch = row_chip([rus("СИСТЕМНЫЙ ПРОМПТ СКЛАДА", 10)])
        sys_ch.move_to([-0.85, -4.6, 0])
        self.add(sys_ch)
        self.play(sys_ch.animate.move_to([0, 1.75, 0]), run_time=0.9)
        self.wait(0.5)
        tool_ch = row_chip([rus("get_sklad tool:", 11, PHOSPHOR),
                            rus("остатки склада")])
        tool_ch.move_to(json_b.get_center())
        self.add(tool_ch)
        self.play(tool_ch.animate.move_to([0, 1.35, 0]), run_time=0.9)
        self.wait(0.5)

        # Карточка 1: зачем обвязка
        self._card(
            "Обвязка добавляет к запросу системный промпт\n"
            "и описания инструментов",
            hold=2.0, body_time=4.0, font_size=30, color=BEIGE
        )

        # 3. копия пакета летит в модель
        pkt = VGroup(sys_ch.copy(), tool_ch.copy(), q_h.copy())
        pkt.arrange(DOWN, buff=X).move_to([0, 1.35, 0])
        self.add(pkt)
        self.play(pkt.animate.move_to([4.85, 0.85, 0]), run_time=1.0)
        self.wait(0.7)

        # 4. модель формирует ответ со спец-токенами вызова
        rep = frame_block(
            [tok("<|im_start|>assistant", RUST, 11),
             tok("<|plugin_call|> get_sklad({})", YELLOWISH, 12),
             tok("<|im_end|>", RUST, 11)],
            fill="#0F130A", stroke=DUST, pad_h=0.14)
        rep.move_to([4.85, -0.75, 0])
        self.play(FadeIn(rep), run_time=0.9)
        self.wait(0.6)

        # Карточка 2: спец-токен вызова
        self._card(
            "Обработав запрос модель решила, что для ответа ей\n"
            "нужны дополнительные данные. И она делает запрос\n"
            "к инструменту, используя спец-теги <|plugin_call|>\n"
            "(у других моделей тег свой: <tool_call> (Qwen),\n"
            "<|python_tag|> (Llama))",
            hold=2.5, body_time=5.0, font_size=26, color=BEIGE
        )

        # 5. ответ копией возвращается в обвязку; окно модели очищается
        rep_h = rep.copy()
        rep_h.move_to(rep.get_center())
        self.add(rep_h)
        self.play(rep_h.animate.move_to([0, -0.05, 0]), run_time=0.9)
        seg_h = rep_h[1][1]
        hl = SurroundingRectangle(seg_h, color=YELLOWISH, buff=0.05,
                                  stroke_width=3)
        self.play(Create(hl), run_time=0.5)
        self.wait(0.4)

        # Карточка 3: как обвязка расшифровывает вызов
        self._card(
            "По тегу и данным в ответе обвязка определяет,\n"
            "какой инструмент хочет использовать модель.\n"
            "Вызывает его, а потом передает модели результат",
            hold=2.0, body_time=4.0, font_size=30, color=BEIGE
        )

        self.play(FadeOut(pkt), FadeOut(rep), run_time=0.4)
        self.wait(0.3)

        # вертикальная стрелка от чипа вызова вниз к заголовку скрипта
        arr_script = Arrow(start=rep_h.get_bottom(), end=scr_lab.get_top(),
                           color=YELLOWISH, stroke_width=5, buff=0.08)
        self.play(GrowArrow(arr_script), run_time=0.8)
        self.wait(0.8)

        # 6. скрипт вспыхивает ярко-зелёным с чёрным текстом и запускается;
        #    в UI под запросом мигает «ЗАПУСК СКРИПТА...»
        run_lbl = Text("ЗАПУСК СКРИПТА...", font_size=16, color=PHOSPHOR,
                       weight=BOLD)
        run_lbl.move_to([-4.85,
                         q_ui.get_bottom()[1] - X - run_lbl.height / 2, 0])
        self.play(FadeIn(run_lbl),
                  scr_b[0].animate.set_fill(PHOSPHOR, opacity=1.0),
                  *[t.animate.set_color(INK) for t in scr_b[1]],
                  FadeOut(arr_script), run_time=0.5)
        run_lbl.add_updater(lambda m: m.set_fill(
            opacity=1.0 if int(self.time / 0.35) % 2 == 0 else 0.25))
        self.wait(1.4)

        # скрипт отработал: тускнеет, надпись в UI перестаёт мигать;
        # в обвязку возвращается json-ответ
        run_lbl.clear_updaters()
        run_lbl.set_fill(opacity=1.0)
        self.play(scr_b.animate.set_opacity(0.40), run_time=0.5)
        json_ans = row_chip([tok('{"порошок": 14, "сода": 8}', PHOSPHOR, 12)])
        json_ans.move_to([0, -1.10, 0])
        self.play(FadeIn(json_ans), run_time=0.8)
        self.wait(0.7)

        # от json-ответа отделяется чип «РЕЗУЛЬТАТ РАБОТЫ СКРИПТА» (в стиле
        # json-ответа) и встаёт в UI под «ЗАПУСК СКРИПТА...»
        res_ui = row_chip([rus("РЕЗУЛЬТАТ РАБОТЫ СКРИПТА", 12, PHOSPHOR)])
        res_ui.move_to(json_ans.get_center())
        res_y = run_lbl.get_bottom()[1] - X - res_ui.height / 2
        self.add(res_ui)
        self.play(res_ui.animate.move_to([-4.85, res_y, 0]), run_time=0.9)
        self.wait(0.5)

        # 7. все чипы обвязки выстраиваются стопкой на межчипном расстоянии
        #    (подсветка следует за сегментом вызова) и летят в модель копией
        five = VGroup(sys_ch, tool_ch, q_h, rep_h, json_ans)
        hl.add_updater(lambda m: m.move_to(seg_h.get_center()))
        self.play(five.animate.arrange(DOWN, buff=X).move_to([0, 0.55, 0]),
                  run_time=0.9)
        hl.clear_updaters()
        self.wait(0.5)
        pkt3 = VGroup(sys_ch.copy(), tool_ch.copy(), q_h.copy(),
                      rep_h.copy(), json_ans.copy())
        pkt3.arrange(DOWN, buff=X).move_to([0, 0.55, 0])
        self.add(pkt3)
        self.play(pkt3.animate.move_to([4.85, 0.55, 0]), run_time=1.0)
        self.wait(0.7)

        # ответ формируется под стопкой; окно модели очищается
        fin_ll = bubble("НА СКЛАДЕ ПОРОШОК И СОДА.\nЦЕМЕНТА НЕТ", OLIVE,
                        font_size=14)
        fin_y = 0.55 - pkt3.height / 2 - X - fin_ll.height / 2
        fin_ll.move_to([4.85, fin_y, 0])
        self.play(FadeIn(fin_ll), run_time=0.8)
        self.wait(0.7)
        self.play(FadeOut(pkt3), run_time=0.4)

        # 8. ответ копией возвращается в обвязку — под стопку,
        #    на межчипном расстоянии
        ans_h = fin_ll.copy()
        ans_y = 0.55 - five.height / 2 - X - ans_h.height / 2
        self.add(ans_h)
        self.play(ans_h.animate.move_to([0, ans_y, 0]), run_time=0.9)
        self.wait(0.9)

        # вторая копия идёт в UI и встаёт под «РЕЗУЛЬТАТ РАБОТЫ СКРИПТА»
        ans_ui = ans_h.copy()
        ui_ans_y = res_y - res_ui.height / 2 - X - ans_ui.height / 2
        self.add(ans_ui)
        self.play(ans_ui.animate.move_to([-4.85, ui_ans_y, 0]), run_time=1.0)
        self.wait(2.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    # --- 2. Вывод (70–77 с) ---------------------------------------------------
    def final_message(self):
        main = Text("ИНСТРУМЕНТ — РУКИ МОДЕЛИ", font_size=46,
                    color=PHOSPHOR, weight=BOLD).move_to(UP * 0.5)
        sub = Text("ВЫЗВАЛ → РЕАЛЬНЫЙ РЕЗУЛЬТАТ → ОТВЕТ ПО ДЕЛУ", font_size=30,
                   color=BEIGE, weight=BOLD).next_to(main, DOWN, buff=0.8)
        self.play(FadeIn(main), run_time=1.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(main), FadeOut(sub), run_time=0.5)
