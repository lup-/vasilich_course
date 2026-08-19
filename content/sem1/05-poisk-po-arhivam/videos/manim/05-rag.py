# -*- coding: utf-8 -*-
"""RAG: вопрос → вектор → поиск → топ-2 документов → модель → ответ. Технический ролик Manim (ManimCE)
для занятия 05.

Одна мысль: чтобы модель отвечала по документам, вопрос вместе с найденными в индексе документами
отдают модели: RAG = вопрос + документы из архива → ответ по источникам, который можно проверить.

Сюжет ролика:
    1) Вопрос зелёным на чёрном: «СКОЛЬКО ПОРОШКА ЕСТЬ НА СКЛАДЕ?»
    2) 3D-пространство смысла (как в ролике про эмбеддинги): векторная БД — четыре кластера-документа
       (НАКЛАДНАЯ, ВЕДОМОСТЬ, ПРИКАЗ, ИНСТРУКЦИЯ). Слова вопроса появляются зелёными сферами
       с зелёными подписями, усредняются в точку «ВОПРОС». Слова каждого документа усредняются в его
       центр-вектор. Поиск в индексе: расстояния от «ВОПРОС» до центров документов; два самых близких
       (НАКЛАДНАЯ, ВЕДОМОСТЬ) подсвечиваются — топ-2.
    3) Схема: сначала «ОБЫЧНЫЙ ЗАПРОС» — вопрос без контекста летит в модель, получает неправильный ответ.
       Затем заголовок меняется на «RAG», появляется векторная база с документами (топ-2 подсвечены).
       Вопрос и топ-2 документов летят в центр, сверху пристыковывается системный промпт,
       стопка уходит в модель — модель отвечает «ЕСТЬ 2 МЕШКА», ответ возвращается в диалог.
    4) Вывод: RAG = вопрос + документы из архива → правдивый ответ.

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 5 \
        05-rag.py RagArkhyv
"""

from manim import *
import numpy as np


PHOSPHOR = "#B6FF3C"   # кислотно-зелёный люминофор экранов
SWAMP    = "#4A5D23"   # болотный зелёный
RUST     = "#8C4A2F"   # ржавый
DUST     = "#8A8A7A"   # пыльный серый
BEIGE    = "#D8C9A3"   # бежевый
OLIVE    = "#556B2F"   # тёмно-оливковый
INK      = "#111111"   # чёрный контур
CYAN     = "#46B3AD"   # приглушённый циан
AMBER    = "#E3B23C"   # приглушённый янтарный
RUST_ACC = "#C8703C"   # приглушённый оранж-ржавый

L = 6.0                 # размер трёхмерной сетки
CENTER3 = np.array([L / 2, L / 2, L / 2])
PHI_F, THETA_F = 52 * DEGREES, 25 * DEGREES
ROLL = 3 * DEGREES      # небольшой разворот всей 3D-картинки (z остаётся вертикальной)
ZOOM_F = 0.62           # базовый зум 3D-сцены (сетка на весь кадр)
FRAME_CENTER = CENTER3

LABEL_FONT = 28
LABEL_SCALE = 0.36
BASE_UP = 0.12          # подъём подписи над точкой вдоль «верх» камеры (было 0.30)

QUESTION_TEXT = "СКОЛЬКО ПОРОШКА ЕСТЬ НА СКЛАДЕ?"
QUESTION_WORDS = ["СКОЛЬКО", "ПОРОШКА", "ЕСТЬ", "НА", "СКЛАДЕ"]
QUESTION_CENTER = np.array([4.4, 4.4, 2.4])

# ручная доводка подписей слов вопроса (мировые единицы вдоль R=вправо, U=вверх)
Q_LABEL_NUDGE = {
    "ПОРОШКА": (0.434, 0.0),   # правее на полслова
    "ЕСТЬ":     (0.0, -0.318),  # ниже на 3 высоты строки
    "НА":       (-0.627, 0.0),  # левее: левый край на уровне правого края СКЛАДЕ, + ширина 'Н'
    "СКЛАДЕ":   (0.073, 0.126), # выше на высоту строки, правее на ширину 'Е'
}

DOC_NAMES = ["НАКЛАДНАЯ", "ВЕДОМОСТЬ", "ПРИКАЗ", "ИНСТРУКЦИЯ"]
TOP2 = {"НАКЛАДНАЯ", "ВЕДОМОСТЬ"}      # два самых близких к вопросу документа
DOC_CENTERS = {
    "НАКЛАДНАЯ": (2.9, 1.6, 1.5),
    "ВЕДОМОСТЬ": (5.0, 1.7, 2.2),
    "ПРИКАЗ": (1.4, 4.9, 4.8),
    "ИНСТРУКЦИЯ": (1.3, 1.7, 4.6),
}
DOC_COLORS = {
    "НАКЛАДНАЯ": BEIGE,
    "ВЕДОМОСТЬ": AMBER,
    "ПРИКАЗ": RUST_ACC,
    "ИНСТРУКЦИЯ": CYAN,
}
DOC_WORDS = {
    "НАКЛАДНАЯ": ["ПОРОШОК", "МЕШКИ", "ПРИХОД", "СКЛАД", "ОСТАТКИ"],
    "ВЕДОМОСТЬ": ["СКЛАД", "ОСТАТКИ", "УЧЁТ", "ПОРОШОК", "МЕШКИ"],
    "ПРИКАЗ": ["ПОСТАВКА", "МЕШКИ", "НОМЕР", "ПОДПИСЬ", "ПОПОЛНЕНИЕ"],
    "ИНСТРУКЦИЯ": ["НОРМА", "РАСХОД", "ПОРОШОК", "ЦЕХ", "КОМПЛЕКТЫ"],
}


# --- общие блоки -----------------------------------------------------------
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


def camera_dir(phi, theta):
    return np.array([np.sin(phi) * np.cos(theta),
                     np.sin(phi) * np.sin(theta),
                     np.cos(phi)])


def camera_basis(phi, theta):
    d = camera_dir(phi, theta)
    right = np.array([np.cos(theta + np.pi / 2),
                      np.sin(theta + np.pi / 2), 0.0])
    up = np.cross(d, right)
    return np.column_stack([right, up, d])


def project(cam, p):
    return np.array(cam.project_point(np.array(p))[:2])


def label_dims(word, font_size=LABEL_FONT, scale=LABEL_SCALE):
    t = Text(word, font="DejaVu Sans", font_size=font_size, weight="BOLD")
    return t.width * scale, t.height * scale


def deoverlap(cam, anchors, names, obstacles=None, spring=0.12):
    """Позиции подписей в 3D без наложений (AABB в экранной плоскости камеры).
    obstacles — имена из anchors, которые являются неподвижными препятствиями
    (пересечение с ними запрещено, но они не двигаются и не возвращаются)."""
    R, U, _ = camera_basis(PHI_F, THETA_F).T
    all_names = list(names) + (list(obstacles) if obstacles else [])
    out = {w: np.asarray(anchors[w], float) + U * BASE_UP for w in all_names}
    half, scale = {}, {}
    for w in all_names:
        p = np.asarray(anchors[w], float)
        wd, hd = label_dims(w)
        s0 = project(cam, p)
        hw_s = np.linalg.norm(project(cam, p + R * wd / 2.0) - s0)
        hh_s = np.linalg.norm(project(cam, p + U * hd / 2.0) - s0)
        sr = np.linalg.norm(project(cam, p + R) - s0) or 1e-9
        su = np.linalg.norm(project(cam, p + U) - s0) or 1e-9
        half[w] = (max(hw_s, 0.10), max(hh_s, 0.05))
        scale[w] = (sr, su)
    for _ in range(80):
        moved = False
        for i in range(len(all_names)):
            for j in range(i + 1, len(all_names)):
                a, b = all_names[i], all_names[j]
                pa = project(cam, out[a])
                pb = project(cam, out[b])
                ov_x = (half[a][0] + half[b][0]) - abs(pa[0] - pb[0])
                ov_y = (half[a][1] + half[b][1]) - abs(pa[1] - pb[1])
                if ov_x <= 0.02 and ov_y <= 0.02:
                    continue
                if ov_x > 0.02 and ov_y > 0.02:
                    axis = "x" if ov_x <= ov_y else "y"
                elif ov_x > 0.02:
                    axis = "x"
                else:
                    axis = "y"
                if axis == "x":
                    total = ov_x + 0.03
                    sign = 1.0 if pa[0] <= pb[0] else -1.0
                    out[a] = out[a] - R * (sign * total * 0.6 / scale[a][0])
                    out[b] = out[b] + R * (sign * total * 0.6 / scale[b][0])
                else:
                    total = ov_y + 0.03
                    sign = 1.0 if pa[1] <= pb[1] else -1.0
                    out[a] = out[a] - U * (sign * total * 0.6 / scale[a][1])
                    out[b] = out[b] + U * (sign * total * 0.6 / scale[b][1])
                moved = True
        if obstacles:
            for w in names:
                target = np.asarray(anchors[w], float) + U * BASE_UP
                out[w] = out[w] + (target - out[w]) * spring
        if not moved:
            break
    return {w: out[w] for w in names}


def lowres_arrow(start, end, color, height=0.16, base_radius=0.05,
                 thickness=0.008, res=4):
    """3D-стрелка из низнополигонального древка и конуса (лёгкая для рендера)."""
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    vec = end - start
    length = np.linalg.norm(vec)
    direction = vec / length if length > 1e-9 else np.array([0.0, 0.0, 1.0])
    shaft = Line3D(start, end - height * direction, thickness=thickness,
                   color=color, resolution=res)
    cone = Cone(direction=direction, base_radius=base_radius, height=height,
                resolution=res, stroke_width=0)
    cone.set_fill(color).set_stroke(color, opacity=0.0)
    cone.shift(end)
    arrow = VGroup(shaft, cone)
    arrow.set_fill(color, opacity=0.45).set_stroke(color, opacity=0.0)
    return arrow


def dashed_line3d(start, end, color, thickness=0.008, dash_len=0.06, gap_len=0.04,
                  opacity=1.0):
    """Пунктирная 3D-линия из коротких отрезков Line3D."""
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    vec = end - start
    length = np.linalg.norm(vec)
    if length < 1e-9:
        return VGroup()
    direction = vec / length
    segs = VGroup()
    pos_along = 0.0
    while pos_along < length - 1e-6:
        a = start + direction * pos_along
        b = start + direction * min(pos_along + dash_len, length)
        seg = Line3D(a, b, thickness=thickness, color=color, resolution=4)
        seg.set_opacity(opacity)
        segs.add(seg)
        pos_along += dash_len + gap_len
    return segs


def blob_positions(center, n, blob_r, min_dist, rng):
    """n точек внутри блока радиуса blob_r вокруг центра, без пересечений."""
    center = np.asarray(center, dtype=float)
    out = []
    for _ in range(n * 200):
        if len(out) >= n:
            break
        cand = center + blob_r * (rng.random(3) * 2.0 - 1.0)
        cand = np.clip(cand, 0.6, L - 0.6)
        if all(np.linalg.norm(cand - p) >= min_dist for p in out):
            out.append(cand)
    if len(out) < n:
        raise RuntimeError("blob_positions: не удалось разложить точки")
    return np.array(out)


def make_flat_label(scene, text, color, font_size=LABEL_FONT, scale=LABEL_SCALE,
                    anchor=None):
    """Подпись «лицом к камере»: применяем матрицу камеры заранее,
    затем ставим в 3D-положение anchor. Не fixed_in_frame — подпись
    ездит с камерой как 3D-объект, но всегда ориентирована в экранную плоскость."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=color, weight=BOLD)
    t.scale(scale)
    # ориентируем в плоскость камеры
    t.apply_matrix(camera_basis(PHI_F, THETA_F))
    t.move_to(anchor if anchor is not None else ORIGIN)
    return t


class RagArkhyv(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)
        self.question_intro()
        self.space_3d()
        self.rag_layout()
        self.final_lesson()

    # --- 1. Вопрос зелёным на чёрном (0–5 с) ---------------------------------
    def question_intro(self):
        q = Text("СКОЛЬКО ПОРОШКА\nЕСТЬ НА СКЛАДЕ?", font="DejaVu Sans",
                 font_size=54, color=PHOSPHOR, weight=BOLD)
        self.play(FadeIn(q), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(q), run_time=0.5)

    # --- служебные -------------------------------------------------------------------
    def show_caption(self, text, color=PHOSPHOR, font_size=28, wait=1.2,
                     letters=False):
        cap = Text(text, font="DejaVu Sans", font_size=font_size,
                   color=color, weight=BOLD)
        cap.scale_to_fit_width(13.5)
        cap.to_edge(DOWN, buff=0.45)
        cap.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(cap)
        if letters:
            self.play(AddTextLetterByLetter(cap, time_per_char=0.035),
                      run_time=0.5 + len(text) * 0.035)
        else:
            self.play(FadeIn(cap), run_time=0.5)
        self.wait(wait)
        self.play(FadeOut(cap), run_time=0.35)
        self.remove(cap)

    def reset_camera_2d(self):
        self.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0,
                         frame_center=ORIGIN, run_time=0.5)

    def make_grid(self):
        grid = VGroup()
        step = L / 4.0
        vals = np.arange(0.0, L + 1e-9, step)
        for i in vals:
            grid.add(Line3D([0, i, 0], [L, i, 0], thickness=0.008, color=DUST,
                            resolution=4))
            grid.add(Line3D([i, 0, 0], [i, L, 0], thickness=0.008, color=DUST,
                            resolution=4))
            grid.add(Line3D([0, 0, i], [L, 0, i], thickness=0.008, color=DUST,
                            resolution=4))
            grid.add(Line3D([i, 0, 0], [i, 0, L], thickness=0.008, color=DUST,
                            resolution=4))
            grid.add(Line3D([0, i, 0], [0, i, L], thickness=0.008, color=DUST,
                            resolution=4))
            grid.add(Line3D([0, 0, i], [0, L, i], thickness=0.008, color=DUST,
                            resolution=4))
        grid.set_fill(opacity=0.1).set_stroke(opacity=0.0)
        return grid

    def make_axes(self):
        return VGroup(
            lowres_arrow([0, 0, 0], [L, 0, 0], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
            lowres_arrow([0, 0, 0], [0, L, 0], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
            lowres_arrow([0, 0, 0], [0, 0, L], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
        )

    # --- 2. 3D-пространство смысла: индекс, вопрос, поиск, топ-2 (5–43 с) ----
    def space_3d(self):
        self.move_camera(phi=PHI_F, theta=THETA_F, zoom=ZOOM_F, gamma=ROLL,
                         frame_center=FRAME_CENTER, run_time=1.2)

        grid = self.make_grid()
        axes = self.make_axes()
        self.play(Create(grid, lag_ratio=0.02), run_time=1.4)
        self.play(FadeIn(axes), run_time=0.5)

        # заголовок 3D-сцены
        title_3d = Text("ВЕКТОРНАЯ БАЗА ДАННЫХ", font="DejaVu Sans",
                        font_size=40, color=PHOSPHOR, weight=BOLD)
        title_3d.to_edge(UP, buff=0.3)
        title_3d.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(title_3d)
        self.play(FadeIn(title_3d), run_time=0.8)

        up_vec = camera_basis(PHI_F, THETA_F).T[1]
        R_basis = camera_basis(PHI_F, THETA_F).T[0]

        # --- кластеры-документы ---------------------------------------------------
        rng = np.random.default_rng(5)
        blob = {}
        doc_centroids = {}
        doc_dots = {}
        for name in DOC_NAMES:
            pts = blob_positions(DOC_CENTERS[name], len(DOC_WORDS[name]),
                                 0.55, 0.32, rng)
            blob[name] = pts
            doc_centroids[name] = np.mean(pts, axis=0)
            doc_dots[name] = VGroup(*[
                Dot3D(point=p, radius=0.06, color=DOC_COLORS[name],
                      resolution=(2, 2)) for p in pts
            ])
        dots_all = VGroup(*[d for name in DOC_NAMES for d in doc_dots[name]])
        self.play(FadeIn(dots_all, lag_ratio=0.04), run_time=1.0)

        doc_anchors = {name: np.asarray(DOC_CENTERS[name], float) + up_vec * 0.5
                       for name in DOC_NAMES}
        doc_pos = deoverlap(self.camera, doc_anchors, DOC_NAMES)
        doc_labels = {}
        for name in DOC_NAMES:
            lab = make_flat_label(self, name, DOC_COLORS[name], anchor=doc_pos[name])
            doc_labels[name] = lab
        self.play(*[FadeIn(doc_labels[n]) for n in DOC_NAMES], run_time=0.8)
        self.show_caption("ВЕКТОРНАЯ БД: РАЗЛОЖЕННЫЕ ЭМБЕДДИНГИ ДОКУМЕНТОВ",
                          wait=1.6, letters=True)

        # --- слова вопроса: зелёные сферы с зелёными подписями -----------------
        q_rng = np.random.default_rng(11)
        q_pos = {}
        placed = []
        for w in QUESTION_WORDS:
            p = None
            for _ in range(2000):
                cand = QUESTION_CENTER + (q_rng.random(3) - 0.5) * 2.0 * 1.05
                cand = np.clip(cand, 0.8, L - 0.8)
                if all(np.linalg.norm(cand - pp) >= 0.55 for pp in placed):
                    p = cand
                    break
            q_pos[w] = p
            placed.append(p)
        q_centroid = np.mean(list(q_pos.values()), axis=0)

        q_spheres = {w: Dot3D(point=q_pos[w], radius=0.09, color=PHOSPHOR,
                              fill_opacity=0.95, resolution=(2, 2))
                     for w in QUESTION_WORDS}

        zoom_q = ZOOM_F * 1.7
        self.move_camera(frame_center=q_centroid, zoom=zoom_q, gamma=ROLL,
                         run_time=1.0)
        self.wait(0.3)
        # подписи слов вопроса — «лицом к камере», деоверлап с учётом позиций документов
        combined_anchors = {**q_pos, **doc_pos}
        lab_anchors = deoverlap(self.camera, combined_anchors, QUESTION_WORDS,
                                obstacles=DOC_NAMES)
        q_labels = {}
        for w in QUESTION_WORDS:
            dx, dy = Q_LABEL_NUDGE.get(w, (0.0, 0.0))
            anchor = lab_anchors[w] + R_basis * dx + up_vec * dy
            lab = make_flat_label(self, w, PHOSPHOR, anchor=anchor)
            q_labels[w] = lab
        self.play(
            LaggedStart(*[FadeIn(q_spheres[w]) for w in QUESTION_WORDS],
                        lag_ratio=0.15),
            *[FadeIn(q_labels[w]) for w in QUESTION_WORDS],
            run_time=1.2,
        )
        self.show_caption("СЛОВА ВОПРОСА — ТОЧКИ В ПРОСТРАНСТВЕ СМЫСЛА",
                          wait=1.4, letters=True)

        # --- усреднение слов вопроса → вектор «ВОПРОС» -------------------------
        # пунктирные линии с обновлением: хвост следует за сферой, голова — в центре
        connectors = VGroup()
        for w in QUESTION_WORDS:
            line = dashed_line3d(q_pos[w], q_centroid, PHOSPHOR,
                                 thickness=0.01, opacity=0.5)
            # замыкаем w в лямбде
            line.add_updater(
                lambda m, w=w: m.become(
                    dashed_line3d(q_spheres[w].get_center(), q_centroid, PHOSPHOR,
                                  thickness=0.01, opacity=0.5))
            )
            connectors.add(line)
        self.play(FadeIn(connectors, lag_ratio=0.08), run_time=1.0)
        q_cent_dot = Dot3D(point=q_centroid, radius=0.13, color=PHOSPHOR,
                           fill_opacity=0.95, resolution=(2, 2))
        self.play(FadeIn(q_cent_dot, scale=1.4), run_time=0.4)
        q_cent_label = make_flat_label(self, "ВОПРОС", PHOSPHOR,
                                       anchor=q_centroid + up_vec * 0.5)
        self.play(FadeIn(q_cent_label), run_time=0.4)
        self.show_caption("УСРЕДНЕНИЕ СЛОВ → ОДИН ВЕКТОР ВОПРОСА", wait=1.2, letters=True)
        self.play(
            *[q_spheres[w].animate.move_to(q_centroid).set_opacity(0.0)
              for w in QUESTION_WORDS],
            *[FadeOut(q_labels[w]) for w in QUESTION_WORDS],
            run_time=0.7,
        )
        # чистим апдейтеры перед удалением
        for c in connectors:
            c.clear_updaters()
        self.play(FadeOut(connectors), run_time=0.3)
        self.wait(0.5)

        # --- откат зума --------------------------------------------------------
        self.move_camera(frame_center=FRAME_CENTER, zoom=ZOOM_F, gamma=ROLL,
                         run_time=1.0)
        self.wait(0.3)

        # --- усреднение слов документов → центры-векторы ---------------------------
        doc_cent_dots = {}
        for name in DOC_NAMES:
            cc = doc_centroids[name]
            conns = VGroup()
            for p in blob[name]:
                conns.add(*dashed_line3d(p, cc, DOC_COLORS[name],
                                         thickness=0.008, opacity=0.35))
            self.play(FadeIn(conns, lag_ratio=0.1), run_time=0.8)
            cd = Dot3D(point=cc, radius=0.12, color=DOC_COLORS[name],
                       fill_opacity=0.95, resolution=(2, 2))
            self.play(FadeIn(cd, scale=1.3), run_time=0.35)
            doc_cent_dots[name] = cd
            self.play(doc_dots[name].animate.set_opacity(0.0),
                      FadeOut(conns), run_time=0.5)
            self.wait(0.3)
        self.show_caption("У КАЖДОГО ДОКУМЕНТА — СВОЙ ВЕКТОР: СРЕДНЕЕ ЕГО СЛОВ",
                          wait=1.4, letters=True)

        # --- поиск в индексе: расстояния до «ВОПРОС» ---------------------------
        order = sorted(DOC_NAMES,
                       key=lambda n: np.linalg.norm(doc_centroids[n]
                                                    - q_centroid))
        dist_lines = {}
        dist_labels = {}
        for name in order:
            cc = doc_centroids[name]
            line = dashed_line3d(q_centroid, cc, BEIGE, thickness=0.012,
                                 opacity=0.6)
            dist_lines[name] = line
            d = np.linalg.norm(cc - q_centroid)
            txt = f"{d:.1f}".replace(".", ",")
            mid = (q_centroid + cc) / 2.0 + up_vec * 0.3
            lab = make_flat_label(self, txt, BEIGE, font_size=26, scale=0.5,
                                  anchor=mid)
            dist_labels[name] = lab
        self.play(LaggedStart(*[FadeIn(dist_lines[n]) for n in order],
                              lag_ratio=0.25), run_time=1.2)
        self.play(*[FadeIn(dist_labels[n]) for n in order], run_time=0.6)
        self.show_caption("ПОИСК В ИНДЕКСЕ: РАССТОЯНИЕ ДО ВЕКТОРА ВОПРОСА",
                          wait=1.6, letters=True)

        # --- топ-2 самых близких документа ------------------------------------------
        top2 = order[:2]
        # сразу подсвечиваем их зелёным
        for name in top2:
            self.play(doc_cent_dots[name].animate.set_color(PHOSPHOR),
                      doc_labels[name].animate.set_color(PHOSPHOR),
                      run_time=0.3)
        # повторяем «вспышки» несколько раз, пока видна 3D-сцена
        top2_dots = [doc_cent_dots[n] for n in top2]
        for _ in range(3):
            self.play(*[Flash(d, color=PHOSPHOR, line_length=0.6,
                              num_lines=10) for d in top2_dots],
                      run_time=0.6)
            self.wait(0.25)
        self.show_caption("ТОП-2 БЛИЖАЙШИХ ДОКУМЕНТА", wait=1.6, letters=True)
        # ещё пара пульсаций на фоне надписи
        for _ in range(2):
            self.play(*[Flash(d, color=PHOSPHOR, line_length=0.6,
                              num_lines=10) for d in top2_dots],
                      run_time=0.6)
            self.wait(0.25)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.reset_camera_2d()

    # --- 3. Сцена: сначала «ОБЫЧНЫЙ ЗАПРОС», потом RAG -----------------------------
    def rag_layout(self):
        # 1) Заголовок «ОБЫЧНЫЙ ЗАПРОС» — красный
        title = Text("ОБЫЧНЫЙ ЗАПРОС", font="DejaVu Sans", font_size=44,
                     color=RUST, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.4)

        # диалог слева: вопрос
        hist_header = Text("ДИАЛОГ", font="DejaVu Sans", font_size=24,
                           color=PHOSPHOR, weight=BOLD)
        hist_header.move_to((-4.6, 2.7, 0))
        q = bubble("СКОЛЬКО ПОРОШКА\nЕСТЬ НА СКЛАДЕ?", BEIGE,
                   font_size=18, hpad=0.28, wpad=0.4)
        q.move_to((-4.6, 1.9, 0))
        self.play(FadeIn(hist_header), FadeIn(q), run_time=0.8)
        self.wait(0.5)

        # модель справа
        model = RoundedRectangle(width=3.4, height=4.75, corner_radius=0.1,
                                 fill_opacity=0.0, stroke_color=RUST,
                                 stroke_width=8)
        model.move_to((4.3, 0.0, 0))
        model_t = Text("МОДЕЛЬ", font="DejaVu Sans", font_size=28,
                       color=RUST, weight=BOLD)
        model_t.move_to(model.get_center() + DOWN * 2.07)
        self.play(FadeIn(model), FadeIn(model_t), run_time=0.8)
        self.wait(0.4)

        # вопрос летит в центр БЕЗ векторной базы и документов
        q_c = q.copy()
        self.play(q_c.animate.move_to((0.0, 0.8, 0)), run_time=1.2)

        # системный промпт добавляется сверху
        sys_p = bubble("СИСТЕМНЫЙ ПРОМПТ", OLIVE, font_size=18, hpad=0.28,
                       wpad=0.4)
        sys_p.next_to(q_c, UP, buff=0.22)
        self.play(FadeIn(sys_p), run_time=0.6)

        # стопка летит в модель
        stack = VGroup(sys_p, q_c)
        self.play(stack.animate.scale(0.72)
                  .move_to(model.get_center() + UP * 0.8), run_time=1.4)

        # неправильный ответ (красный) — в две строки
        ans_wrong = bubble("МЕШКОВ 30\nНЕБОСЬ", RUST, font_size=20,
                           hpad=0.3, wpad=0.45)
        ans_wrong.move_to(model.get_center() + DOWN * 1.15)
        self.play(FadeIn(ans_wrong), run_time=0.8)
        self.wait(0.6)

        # текст внизу про ответ из головы — печатается побуквенно
        self.show_caption("БЕЗ ДОКУМЕНТОВ — ИЗ ГОЛОВЫ: МОЖЕТ ПРИВРАТЬ",
                          color=RUST, font_size=26, wait=1.5, letters=True)
        self.show_caption("ПРОВЕРЯЙ!",
                          color=BEIGE, font_size=24, wait=1.0, letters=True)

        # всё гасим, кроме заголовка и диалога
        self.play(FadeOut(sys_p), FadeOut(q_c), FadeOut(ans_wrong),
                  FadeOut(model), FadeOut(model_t),
                  run_time=0.6)
        self.wait(0.4)

        # 2) Переход к RAG: заголовок становится зелёным «RAG»
        self.play(Transform(title, Text("RAG", font="DejaVu Sans",
                     font_size=56, color=PHOSPHOR, weight=BOLD).to_edge(UP)),
                  run_time=0.8)
        self.wait(0.4)

        # модель обводка становится зелёной
        model_new = RoundedRectangle(width=3.4, height=4.75, corner_radius=0.1,
                                     fill_opacity=0.0, stroke_color=PHOSPHOR,
                                     stroke_width=8)
        model_new.move_to((4.3, 0.0, 0))
        model_t_new = Text("МОДЕЛЬ", font="DejaVu Sans", font_size=28,
                           color=PHOSPHOR, weight=BOLD)
        model_t_new.move_to(model_new.get_center() + DOWN * 2.07)
        cap1 = Text("ОТВЕЧАЕТ ПО", font="DejaVu Sans", font_size=16,
                    color=BEIGE, weight=BOLD)
        cap2 = Text("ДОКУМЕНТАМ", font="DejaVu Sans", font_size=16,
                    color=BEIGE, weight=BOLD)
        model_cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.08)
        model_cap.next_to(model_new, DOWN, buff=0.35)
        self.play(Transform(model, model_new), Transform(model_t, model_t_new),
                  FadeIn(model_cap), run_time=0.8)
        self.wait(0.4)

        # векторная база под диалогом: 4 документа в столбик, топ-2 подсвечены
        bubbles = []
        for i, name in enumerate(DOC_NAMES):
            color = PHOSPHOR if name in TOP2 else DUST
            b = bubble(f"ДОКУМЕНТ {i + 1}: {name}", color, font_size=14,
                       hpad=0.18, wpad=0.28)
            bubbles.append(b)
        grid2 = VGroup(*bubbles).arrange(DOWN, buff=0.1)
        grid2.move_to((-4.6, -1.5, 0))
        base_box = RoundedRectangle(width=grid2.width + 0.6,
                                    height=grid2.height + 0.5,
                                    corner_radius=0.12, stroke_color=PHOSPHOR,
                                    stroke_width=5)
        base_box.move_to(grid2.get_center())
        base_t = Text("ВЕКТОРНАЯ БАЗА", font="DejaVu Sans", font_size=18,
                      color=PHOSPHOR, weight=BOLD)
        base_t.next_to(base_box, UP, buff=0.1)
        self.play(FadeIn(base_t), Create(base_box), FadeIn(grid2), run_time=0.8)
        self.wait(0.5)

        # вопрос и топ-2 документов летят в центр — ПОСЛЕДОВАТЕЛЬНО
        q_c2 = q.copy()
        d1_c = bubbles[0].copy()
        d2_c = bubbles[1].copy()
        sys_p2 = bubble("СИСТЕМНЫЙ ПРОМПТ", OLIVE, font_size=16, hpad=0.22,
                        wpad=0.35)
        self.add(q_c2, d1_c, d2_c)

        # измеряем целевую раскладку стопки (arrange перемещает копии в центр)
        target_stack = VGroup(sys_p2, q_c2, d1_c, d2_c).arrange(DOWN, buff=0.15)
        target_stack.move_to((0.0, 0.5, 0))
        tgt_q = q_c2.get_center().copy()
        tgt_d1 = d1_c.get_center().copy()
        tgt_d2 = d2_c.get_center().copy()

        # возвращаем копии в исходные позиции, откуда они полетят
        q_c2.move_to(q.get_center())
        d1_c.move_to(bubbles[0].get_center())
        d2_c.move_to(bubbles[1].get_center())

        # 1) вопрос летит в центр
        self.play(q_c2.animate.move_to(tgt_q), run_time=1.0)
        # 2) документы летят в центр
        self.play(d1_c.animate.move_to(tgt_d1),
                  d2_c.animate.move_to(tgt_d2), run_time=1.0)
        # 3) системный промпт появляется сверху
        self.play(FadeIn(sys_p2), run_time=0.6)
        self.wait(0.3)

        # center_stack для следующего шага (полета в модель)
        center_stack = VGroup(sys_p2, q_c2, d1_c, d2_c)

        # стопка летит в модель
        self.play(center_stack.animate.scale(0.8)
                  .move_to(model_new.get_center() + UP * 0.8), run_time=1.4)

        # правильный ответ (зелёный)
        ans = bubble("ЕСТЬ 2 МЕШКА", PHOSPHOR, font_size=22, hpad=0.3, wpad=0.45)
        ans.move_to(model_new.get_center() + DOWN * 1.15)
        self.play(FadeIn(ans), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(sys_p2), FadeOut(q_c2), FadeOut(d1_c), FadeOut(d2_c),
                  run_time=0.5)
        self.play(ans.animate.move_to((-4.6, 1.1, 0)), run_time=1.2)
        self.wait(0.5)

        # финальный текст: «ДАННЫЕ В ЗАПРОСЕ → ПРАВДИВЫЙ ОТВЕТ» печатается
        cap = Text("ДАННЫЕ В ЗАПРОСЕ → ПРАВДИВЫЙ ОТВЕТ",
                   font="DejaVu Sans", font_size=28, color=PHOSPHOR, weight=BOLD)
        cap.to_edge(DOWN, buff=0.25)
        cap.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(cap)
        self.play(AddTextLetterByLetter(cap, time_per_char=0.03),
                  run_time=0.5 + len(cap.text) * 0.03)
        self.wait(2.0)
        self.play(FadeOut(cap), run_time=0.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    # --- 4. Финальный вывод -------------------------------------------------------
    def final_lesson(self):
        # две колонки: знает факты / не знает
        left_box = RoundedRectangle(width=6.0, height=4.2, corner_radius=0.15,
                                    fill_color=PHOSPHOR, fill_opacity=0.1,
                                    stroke_color=PHOSPHOR, stroke_width=5)
        left_box.move_to(LEFT * 3.5)
        right_box = RoundedRectangle(width=6.0, height=4.2, corner_radius=0.15,
                                     fill_color=RUST, fill_opacity=0.1,
                                     stroke_color=RUST, stroke_width=5)
        right_box.move_to(RIGHT * 3.5)

        left_t = Text("МОДЕЛЬ ЗНАЕТ ФАКТЫ", font="DejaVu Sans",
                      font_size=22, color=PHOSPHOR, weight=BOLD)
        left_t.move_to(left_box.get_top() + DOWN * 0.55)

        right_t = Text("МОДЕЛЬ НЕ ЗНАЕТ ФАКТОВ", font="DejaVu Sans",
                       font_size=22, color=RUST, weight=BOLD)
        right_t.move_to(right_box.get_top() + DOWN * 0.55)

        left_items = VGroup(
            Text("→ Документы в контексте", font="DejaVu Sans", font_size=17, color=BEIGE),
            Text("→ RAG: вопрос + документы", font="DejaVu Sans", font_size=17, color=BEIGE),
            Text("→ ПРАВДИВЫЙ ОТВЕТ", font="DejaVu Sans", font_size=20, color=PHOSPHOR, weight=BOLD),
            Text("→ Можно проверить", font="DejaVu Sans", font_size=17, color=BEIGE),
        ).arrange(DOWN, buff=0.25)
        left_items.move_to(left_box.get_center() + DOWN * 0.1)

        right_items = VGroup(
            Text("→ Контекст пуст", font="DejaVu Sans", font_size=17, color=BEIGE),
            Text("→ Обычный запрос", font="DejaVu Sans", font_size=17, color=BEIGE),
            Text("→ ВЫДУМЫВАЕТ", font="DejaVu Sans", font_size=19, color=RUST, weight=BOLD),
            Text("→ Невозможно проверить", font="DejaVu Sans", font_size=17, color=BEIGE),
        ).arrange(DOWN, buff=0.25)
        right_items.move_to(right_box.get_center() + DOWN * 0.1)

        self.play(FadeIn(left_box), FadeIn(right_box), run_time=0.8)
        self.play(FadeIn(left_t), FadeIn(right_t), run_time=0.6)
        self.play(FadeIn(left_items, lag_ratio=0.2), FadeIn(right_items, lag_ratio=0.2), run_time=1.2)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
