# -*- coding: utf-8 -*-
"""Что значат числа в эмбеддинге. Технический ролик Manim (ManimCE) для занятия 05.

Сюжет ролика:
    1) Как модель учится: читает корпус текстов завода, делит текст на токены
       (у каждого свой номер в памяти), слово-токен узнают по окружению.
    2) Обучение в пространстве смысла — «угадайка»: модель прячет один токен
       и угадывает его по контексту. Догадка — ближайший токен к центру
       контекста. Ошиблась — токены предложения подтягиваются к центру
       контекста (научились). Угадала — так и оставляем.
    3) Координаты точек складываются в кластеры по смыслу; в конце — облёт
       сетки и 8 главных токенов.

Все 29 знаменательных токенов присутствуют с самого начала как случайные
точки внутри блоков своих смысловых кластеров; подписи появляются только у
токенов текущего предложения. После обучения близкие по смыслу собираются
в 4 явных кластера (цветовая разметка в финале). Раскладка: seed=105,
pull=0.40, min_dist=0.8, blob_r=1.4; из 15 шагов модель ровно 2 раза
угадывает (шаги 10 и 13).

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 5 \
        05-chisla.py Chisla
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
CYAN     = "#46B3AD"   # приглушённый циан (бытовая химия / стирка)
AMBER    = "#E3B23C"   # приглушённый янтарный (наука / расчёт)
RUST_ACC = "#C8703C"   # приглушённый оранж-ржавый (учёт / архив)

L = 6.0                 # размер трёхмерной сетки
CENTER3 = np.array([L / 2, L / 2, L / 2])
PHI_F, THETA_F = 52 * DEGREES, 25 * DEGREES
ROLL = 3 * DEGREES      # небольшой разворот всей 3D-картинки против часовой (z остаётся вертикальной)

# --- двухколоночная раскладка: слева весь текст, справа 3D-сетка ---------------
ZOOM_F = 0.60           # базовый зум 3D-сцены (правая колонка)
COL_3D_X = 2.8          # экранный x центра куба (правая колонка)
COL_3D_Y = 0.0          # экранный y центра куба
COL_WIDTH = 6.6         # ширина правой колонки для расчёта зума
LEFT_X = -3.7           # центр текстовой колонки слева

# базовый кадр камеры: куб CENTER3 проецируется на экран в точку (COL_3D_X, COL_3D_Y)
_BASE_CAM = ThreeDCamera(phi=PHI_F, theta=THETA_F, zoom=ZOOM_F,
                         frame_center=CENTER3)
_BASE_ROT = np.array(_BASE_CAM.get_rotation_matrix())


def screen_fc(zoom, center, dx=COL_3D_X, dy=COL_3D_Y):
    """frame_center, при котором точка center видна на экране в (dx, dy)."""
    return center - _BASE_ROT.T.dot(np.array([dx / zoom, dy / zoom, 0.0]))


FRAME_CENTER = screen_fc(ZOOM_F, CENTER3)

# --- пер-степ зум: предложение занимает основную часть правой колонки
ZOOM_FILL = 0.80        # доля колонки, на которую раздуваем предложение
ZOOM_K_MIN, ZOOM_K_MAX = 1.15, 2.6
DIM_OP = 0.15           # яркость «чужих» точек при зуме
ZOOM_RT = 0.8           # длительность хода зума

# --- параметры симуляции (подобраны поиском: см. /tmp/opencode/search_layout.py) --
SEED = 70
PULL = 0.40
REPEL_STEP = 0.5       # шаг отталкивания негативного сэмплирования
MIN_DIST = 0.8
BLOB_R = 1.4           # радиус блока кластера вокруг латентного центра
CLUSTER_SEP = 3.2      # мин. расстояние между латентными центрами кластеров

# --- подписи токенов в 3D -----------------------------------------------------
LABEL_FONT = 32
LABEL_SCALE = 0.34
BASE_UP = 0.30

# --- данные -------------------------------------------------------------------
WORDS = ["НАСЫПЬ", "ПОРОШОК", "БАК", "СМЕСИ", "ДОБАВЬ", "СОДА",
         "СТИРАЛЬНАЯ", "МАШИНА", "КИСЛОТА", "РАЗЪЕДАЕТ", "РЖАВЧИНА",
         "ТРУБЫ", "ФОРМУЛА", "РЕЦЕПТ", "АРХИВ", "ТЕОРЕМА", "ТРЕБУЕТ",
         "ДОКАЗАТЕЛЬСТВО", "ПРОВЕРЬ", "РАСЧЁТ", "СМЕТА", "ВАЛЕНКИ",
         "СУШАТСЯ", "ПЕЧКА", "НАКЛАДНАЯ", "ПОТЕРЯЛАСЬ", "НЕЙТРАЛИЗУЕТ",
         "СМЕШАЛИСЬ", "ПОВРЕДИЛА"]

KEYS8 = ["ПОРОШОК", "СОДА", "КИСЛОТА", "ФОРМУЛА", "ТЕОРЕМА", "РАСЧЁТ",
          "ВАЛЕНКИ", "НАКЛАДНАЯ"]

# 4 смысловых кластера (покрывают все 29 знаменательных токенов)
CLUSTERS = [
    ("СТИРКА", CYAN, ["НАСЫПЬ", "ПОРОШОК", "БАК", "СМЕСИ", "ДОБАВЬ", "СОДА",
                      "СТИРАЛЬНАЯ", "МАШИНА", "СМЕШАЛИСЬ"]),
    ("ХИМИЯ", PHOSPHOR, ["КИСЛОТА", "РАЗЪЕДАЕТ", "РЖАВЧИНА", "ТРУБЫ",
                         "НЕЙТРАЛИЗУЕТ", "ПОВРЕДИЛА"]),
    ("РАСЧЁТ", AMBER, ["ФОРМУЛА", "РЕЦЕПТ", "ТЕОРЕМА", "ТРЕБУЕТ",
                       "ДОКАЗАТЕЛЬСТВО", "ПРОВЕРЬ", "РАСЧЁТ", "СМЕТА"]),
    ("УЧЁТ", RUST_ACC, ["ВАЛЕНКИ", "СУШАТСЯ", "ПЕЧКА", "НАКЛАДНАЯ",
                        "ПОТЕРЯЛАСЬ", "АРХИВ"]),
]
CLUSTER_OF = {w: i for i, (_, _, members) in enumerate(CLUSTERS) for w in members}

# 36 токенов (29 знаменательных + 7 служебных) по порядку первого появления
FUNC = {"В", "ДЛЯ", "НА", "ИЗ", "ПО", "У", "И"}
TOKEN_ID = {"НАСЫПЬ": 1, "ПОРОШОК": 2, "В": 3, "БАК": 4, "ДЛЯ": 5,
            "СМЕСИ": 6, "ДОБАВЬ": 7, "СОДА": 8, "СТИРАЛЬНАЯ": 9,
            "МАШИНА": 10, "КИСЛОТА": 11, "РАЗЪЕДАЕТ": 12, "РЖАВЧИНА": 13,
            "НА": 14, "ТРУБЫ": 15, "ФОРМУЛА": 16, "ИЗ": 17, "РЕЦЕПТ": 18,
            "АРХИВ": 19, "ТЕОРЕМА": 20, "ТРЕБУЕТ": 21, "ДОКАЗАТЕЛЬСТВО": 22,
            "ПРОВЕРЬ": 23, "РАСЧЁТ": 24, "ПО": 25, "СМЕТА": 26,
            "ВАЛЕНКИ": 27, "СУШАТСЯ": 28, "У": 29, "ПЕЧКА": 30,
            "НАКЛАДНАЯ": 31, "ПОТЕРЯЛАСЬ": 32, "НЕЙТРАЛИЗУЕТ": 33,
            "И": 34, "СМЕШАЛИСЬ": 35, "ПОВРЕДИЛА": 36}

# корпус: предложения как их читает модель; пометка — номер токена
# (инфинитивные и падежные формы слова соответствуют своему токену)
CORPUS = [
    ("НАСЫПЬ", 1), ("ПОРОШОК", 2), ("В", 3), ("БАК", 4), ("ДЛЯ", 5), ("СМЕСИ", 6),
    ("ДОБАВЬ", 7), ("СОДУ", 8), ("В", 3), ("СТИРАЛЬНУЮ", 9), ("МАШИНУ", 10),
    ("КИСЛОТА", 11), ("РАЗЪЕДАЕТ", 12), ("РЖАВЧИНУ", 13), ("НА", 14), ("ТРУБАХ", 15),
    ("ФОРМУЛА", 16), ("ИЗ", 17), ("РЕЦЕПТА", 18), ("В", 3), ("АРХИВЕ", 19),
    ("ТЕОРЕМА", 20), ("ТРЕБУЕТ", 21), ("ДОКАЗАТЕЛЬСТВА", 22),
    ("ПРОВЕРЬ", 23), ("РАСЧЁТ", 24), ("ПО", 25), ("СМЕТЕ", 26),
    ("ВАЛЕНКИ", 27), ("СУШАТСЯ", 28), ("У", 29), ("ПЕЧКИ", 30),
    ("НАКЛАДНАЯ", 31), ("ПОТЕРЯЛАСЬ", 32), ("В", 3), ("АРХИВЕ", 19),
    ("СОДА", 8), ("НЕЙТРАЛИЗУЕТ", 33), ("КИСЛОТУ", 11), ("В", 3), ("РЕЦЕПТЕ", 18),
    ("ПОРОШОК", 2), ("И", 34), ("СОДА", 8), ("СМЕШАЛИСЬ", 35), ("В", 3), ("БАКЕ", 4),
    ("КИСЛОТА", 11), ("ПОВРЕДИЛА", 36), ("НАКЛАДНУЮ", 31),
]
CORPUS_SENT = [
    ("НАСЫПЬ ПОРОШОК В БАК ДЛЯ СМЕСИ", 6),
    ("ДОБАВЬ СОДУ В СТИРАЛЬНУЮ МАШИНУ", 5),
    ("КИСЛОТА РАЗЪЕДАЕТ РЖАВЧИНУ НА ТРУБАХ", 5),
    ("ФОРМУЛА ИЗ РЕЦЕПТА В АРХИВЕ", 5),
    ("ТЕОРЕМА ТРЕБУЕТ ДОКАЗАТЕЛЬСТВА", 3),
    ("ПРОВЕРЬ РАСЧЁТ ПО СМЕТЕ", 4),
    ("ВАЛЕНКИ СУШАТСЯ У ПЕЧКИ", 4),
    ("НАКЛАДНАЯ ПОТЕРЯЛАСЬ В АРХИВЕ", 4),
    ("СОДА НЕЙТРАЛИЗУЕТ КИСЛОТУ В РЕЦЕПТЕ", 5),
    ("ПОРОШОК И СОДА СМЕШАЛИСЬ В БАКЕ", 6),
    ("КИСЛОТА ПОВРЕДИЛА НАКЛАДНУЮ", 3),
]

# 15 шагов обучения: цель, контекст, исход, баннер (kind: ctx/tgt/fn)
STEPS = [
    {"target": "ПОРОШОК", "ctx": ["НАСЫПЬ", "БАК", "СМЕСИ"], "outcome": "wrong",
     "banner": [("НАСЫПЬ", "ctx"), ("???", "tgt"), ("В", "fn"), ("БАК", "ctx"),
                ("ДЛЯ", "fn"), ("СМЕСИ", "ctx")]},
    {"target": "СОДА", "ctx": ["ДОБАВЬ", "СТИРАЛЬНАЯ", "МАШИНА"], "outcome": "wrong",
     "banner": [("ДОБАВЬ", "ctx"), ("???", "tgt"), ("В", "fn"),
                ("СТИРАЛЬНУЮ", "ctx"), ("МАШИНУ", "ctx")]},
    {"target": "КИСЛОТА", "ctx": ["РАЗЪЕДАЕТ", "РЖАВЧИНА", "ТРУБЫ"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("РАЗЪЕДАЕТ", "ctx"), ("РЖАВЧИНУ", "ctx"),
                ("НА", "fn"), ("ТРУБАХ", "ctx")]},
    {"target": "ФОРМУЛА", "ctx": ["РЕЦЕПТ", "АРХИВ"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("ИЗ", "fn"), ("РЕЦЕПТА", "ctx"),
                ("В", "fn"), ("АРХИВЕ", "ctx")]},
    {"target": "ТЕОРЕМА", "ctx": ["ТРЕБУЕТ", "ДОКАЗАТЕЛЬСТВО"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("ТРЕБУЕТ", "ctx"), ("ДОКАЗАТЕЛЬСТВА", "ctx")]},
    {"target": "РАСЧЁТ", "ctx": ["ПРОВЕРЬ", "СМЕТА"], "outcome": "wrong",
     "banner": [("ПРОВЕРЬ", "ctx"), ("???", "tgt"), ("ПО", "fn"), ("СМЕТЕ", "ctx")]},
    {"target": "ВАЛЕНКИ", "ctx": ["СУШАТСЯ", "ПЕЧКА"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("СУШАТСЯ", "ctx"), ("У", "fn"), ("ПЕЧКИ", "ctx")]},
    {"target": "НАКЛАДНАЯ", "ctx": ["ПОТЕРЯЛАСЬ", "АРХИВ"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("ПОТЕРЯЛАСЬ", "ctx"), ("В", "fn"), ("АРХИВЕ", "ctx")]},
    {"target": "КИСЛОТА", "ctx": ["РАЗЪЕДАЕТ", "РЖАВЧИНА", "ТРУБЫ"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("РАЗЪЕДАЕТ", "ctx"), ("РЖАВЧИНУ", "ctx"),
                ("НА", "fn"), ("ТРУБАХ", "ctx")]},
    {"target": "КИСЛОТА", "ctx": ["РАЗЪЕДАЕТ", "РЖАВЧИНА", "ТРУБЫ"], "outcome": "correct",
     "banner": [("???", "tgt"), ("РАЗЪЕДАЕТ", "ctx"), ("РЖАВЧИНУ", "ctx"),
                ("НА", "fn"), ("ТРУБАХ", "ctx")]},
    {"target": "СОДА", "ctx": ["ПОРОШОК", "СМЕШАЛИСЬ", "БАК"], "outcome": "wrong",
     "banner": [("ПОРОШОК", "ctx"), ("И", "fn"), ("???", "tgt"),
                ("СМЕШАЛИСЬ", "ctx"), ("В", "fn"), ("БАКЕ", "ctx")]},
    {"target": "СОДА", "ctx": ["ПОРОШОК", "СМЕШАЛИСЬ", "БАК"], "outcome": "wrong",
     "banner": [("ПОРОШОК", "ctx"), ("И", "fn"), ("???", "tgt"),
                ("СМЕШАЛИСЬ", "ctx"), ("В", "fn"), ("БАКЕ", "ctx")]},
    {"target": "СОДА", "ctx": ["ПОРОШОК", "СМЕШАЛИСЬ", "БАК"], "outcome": "correct",
     "banner": [("ПОРОШОК", "ctx"), ("И", "fn"), ("???", "tgt"),
                ("СМЕШАЛИСЬ", "ctx"), ("В", "fn"), ("БАКЕ", "ctx")]},
    {"target": "КИСЛОТА", "ctx": ["СОДА", "НЕЙТРАЛИЗУЕТ", "РЕЦЕПТ"], "outcome": "wrong",
     "banner": [("СОДА", "ctx"), ("НЕЙТРАЛИЗУЕТ", "ctx"), ("???", "tgt"),
                ("В", "fn"), ("РЕЦЕПТЕ", "ctx")]},
    {"target": "КИСЛОТА", "ctx": ["ПОВРЕДИЛА", "НАКЛАДНАЯ"], "outcome": "wrong",
     "banner": [("???", "tgt"), ("ПОВРЕДИЛА", "ctx"), ("НАКЛАДНУЮ", "ctx")]},
]


# --- служебные функции ---------------------------------------------------------
def bubble(text, color, font_size=34):
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=INK, weight=BOLD)
    rect = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.5,
                            corner_radius=0.15, fill_color=color,
                            fill_opacity=1.0, stroke_color=INK, stroke_width=6)
    return VGroup(rect, t)


def phrase(parts, font_size=44):
    mobs = [Text(text, font="DejaVu Sans", font_size=font_size,
                 color=color, weight=BOLD)
            for text, color in parts]
    return VGroup(*mobs).arrange(RIGHT, buff=0.2)


def phrase_block(lines, font_size=44, buff=0.35):
    rows = [phrase(line, font_size=font_size) for line in lines]
    return VGroup(*rows).arrange(DOWN, buff=buff)


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


def label_facing_camera(text, font_size, color, target, phi=PHI_F, theta=THETA_F, scale=1.0):
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=color, weight=BOLD)
    if scale != 1.0:
        t.scale(scale)
    t._base = t.copy()
    t.apply_matrix(camera_basis(phi, theta))
    t.move_to(target)
    return t


def token_label(word, color, anchor, scale=LABEL_SCALE, font=LABEL_FONT,
                num_color=DUST):
    """Подпись токена «лицом к камере»: слово сверху, номер токена снизу."""
    w = Text(word, font="DejaVu Sans", font_size=font, color=color, weight=BOLD)
    n_txt = "???" if word == "???" else str(TOKEN_ID[word])
    n = Text(n_txt, font="DejaVu Sans",
             font_size=int(font * 0.7), color=num_color, weight=BOLD)
    g = VGroup(w, n).arrange(DOWN, buff=0.05)
    g.scale(scale)
    g._base = g.copy()
    g.apply_matrix(camera_basis(PHI_F, THETA_F))
    g.move_to(anchor)
    return g


def token_label_flat(word, color, scale, anchor, project, num_color=DUST):
    """Плоская подпись токена (слово сверху, номер снизу), следящая за проекцией."""
    w = Text(word, font="DejaVu Sans", font_size=LABEL_FONT, color=color,
             weight=BOLD)
    n = Text(str(TOKEN_ID[word]), font="DejaVu Sans",
             font_size=int(LABEL_FONT * 0.7), color=num_color, weight=BOLD)
    g = VGroup(w, n).arrange(DOWN, buff=0.05)
    g.scale(scale)
    g.fixed_in_frame = True

    def up(mob, dt):
        mob.move_to(project(anchor)[:3])

    g.add_updater(up)
    return g


def make_sim_camera():
    return ThreeDCamera(phi=PHI_F, theta=THETA_F, zoom=ZOOM_F,
                        frame_center=FRAME_CENTER)


def lowres_arrow(start, end, color, height=0.16, base_radius=0.05,
                 thickness=0.008, res=4):
    """3D-стрелка из низнополигонального древка и конуса (геометрия Arrow3D,
    но лёгкая для рендера)."""
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


def label_flat(text, font_size, color, scale, anchor, project):
    """Плоская подпись: каждый кадр ставится в проекцию 3D-якоря (fixed_in_frame
    + updater), поэтому всегда «смотрит на камеру» и дешёвая в рендере."""
    t = Text(text, font="DejaVu Sans", font_size=font_size,
             color=color, weight=BOLD)
    t.scale(scale)
    t.fixed_in_frame = True

    def up(mob, dt):
        mob.move_to(project(anchor)[:3])

    t.add_updater(up)
    return t


def cluster_centers(n_clusters, min_sep=CLUSTER_SEP, lo=1.4, hi=L - 1.4,
                    max_tries=8000):
    """Латентные центры кластеров — фиксированные вершины тетраэдра в кубе,
    чтобы четыре смысловых групп гарантированно не пересекались."""
    corners = np.array([
        [1.5, 1.5, 1.5],
        [1.5, 4.5, 4.5],
        [4.5, 1.5, 4.5],
        [4.5, 4.5, 1.5],
    ], dtype=float)
    return corners[:n_clusters]


def initial_positions(words, min_dist=MIN_DIST, cluster_of=None, centers=None,
                      blob_r=BLOB_R, max_tries=2000000):
    from collections import defaultdict
    groups = defaultdict(list)
    for i, w in enumerate(words):
        groups[cluster_of[w]].append(i)
    order = []
    for ci in range(len(centers)):
        order.extend(groups[ci])
    n = len(words)
    pos = np.zeros((n, 3))
    placed, tries = 0, 0
    # каждый токен стартует случайно внутри блока своего кластера (вокруг
    # латентного центра) — точки «не совсем случайные», после обучения сами
    # соберутся в явные, непересекающиеся кучки
    while placed < n and tries < max_tries:
        tries += 1
        i = order[placed]
        ci = cluster_of[words[i]]
        cand = centers[ci] + blob_r * (np.random.random(3) - 0.5) * 2.0
        cand = np.clip(cand, 0.5, L - 0.5)
        if all(np.linalg.norm(cand - pos[k]) >= min_dist for k in range(placed)):
            pos[i] = cand
            placed += 1
    if placed < n:
        raise RuntimeError("initial_positions: не хватило места в блоке кластера")
    return pos


def label_dims(word, font_size=LABEL_FONT, scale=LABEL_SCALE):
    t = Text("%s\n12" % word, font="DejaVu Sans", font_size=font_size,
             weight="BOLD")
    return t.width * scale, t.height * scale


def project(cam, p):
    return np.array(cam.project_point(np.array(p))[:2])


def deoverlap(cam, anchors, names):
    """Позиции подписей в 3D без наложений (AABB в экранной плоскости камеры)."""
    R, U, _ = camera_basis(PHI_F, THETA_F).T
    out = {w: np.asarray(anchors[w], float) + U * BASE_UP for w in names}
    half, scale = {}, {}
    for w in names:
        p = np.asarray(anchors[w], float)
        wd, hd = label_dims(w)
        s0 = project(cam, p)
        hw_s = np.linalg.norm(project(cam, p + R * wd / 2.0) - s0)
        hh_s = np.linalg.norm(project(cam, p + U * hd / 2.0) - s0)
        sr = np.linalg.norm(project(cam, p + R) - s0) or 1e-9
        su = np.linalg.norm(project(cam, p + U) - s0) or 1e-9
        half[w] = (max(hw_s, 0.10), max(hh_s, 0.05))
        scale[w] = (sr, su)
    for _ in range(50):
        moved = False
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
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
        if not moved:
            break
    return out


def sample_negatives(pool, exclude, k, rng):
    """k случайных токенов из pool, не входящих в exclude (без повторов)."""
    cand = [w for w in pool if w not in exclude]
    n = min(k, len(cand))
    idx = rng.choice(len(cand), size=n, replace=False)
    return [cand[i] for i in idx]


class Chisla(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)  # текст вступления не крутим; разворот только для 3D-вида (см. grid_3d)
        self.training_intro()
        self.corpus_scene()
        self.grid_3d()

    # --- 1. Вступление: как модель учится --------------------------------------
    def training_intro(self):
        p = phrase_block([
            [("ТОКЕН УЗНАЮТ ПО ОКРУЖЕНИЮ:", BEIGE)],
            [("КАКИЕ ТОКЕНЫ РЯДОМ —", PHOSPHOR)],
            [("ТАКОВ И СМЫСЛ.", PHOSPHOR)],
        ], font_size=38, buff=0.3)
        self.play(FadeIn(p, shift=UP * 0.15, lag_ratio=0.1), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(p, shift=UP * 0.05), run_time=0.4)

    # --- 2. Корпус текстов: токены и их номера ----------------------------------
    def corpus_scene(self):
        title = Text("КОРПУС ТЕКСТОВ ЗАВОДА", font="DejaVu Sans", font_size=40, color=PHOSPHOR,
                     weight=BOLD).to_edge(UP, buff=0.45)
        self.play(FadeIn(title), run_time=0.7)

        rows = VGroup()
        start = 0
        for i, (sent_text, n_tokens) in enumerate(CORPUS_SENT, start=1):
            row = VGroup()
            num = Text(f"{i}.", font="DejaVu Sans", font_size=14,
                       color=PHOSPHOR, weight=BOLD)
            blank = Text("0", font="DejaVu Sans", font_size=7,
                         color=PHOSPHOR, fill_opacity=0.0)
            num_cell = VGroup(num, blank).arrange(DOWN, buff=0.03)
            row.add(num_cell)
            for k in range(n_tokens):
                w, tid = CORPUS[start + k]
                word_t = Text(w, font="DejaVu Sans", font_size=14,
                              color=DUST if w in FUNC else BEIGE, weight=BOLD)
                id_t = Text(str(tid), font="DejaVu Sans", font_size=7,
                            color=DUST, weight=BOLD)
                cell = VGroup(word_t, id_t).arrange(DOWN, buff=0.03)
                row.add(cell)
            start += n_tokens
            row.arrange(RIGHT, buff=0.14)
            rows.add(row)
        rows.arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        rows.scale_to_fit_height(5.0)
        rows.move_to([0, 0.3, 0])

        for row in rows:
            self.play(FadeIn(row, shift=UP * 0.04), run_time=0.2)
        self.wait(1.8)

        cap1 = Text("МОДЕЛЬ ДЕЛИТ ТЕКСТ НА ТОКЕНЫ:", font="DejaVu Sans", font_size=30,
                    color=PHOSPHOR, weight=BOLD)
        cap2 = Text("ПОМЕТКА ПОД СЛОВОМ — НОМЕР ЕГО ТОКЕНА В ПАМЯТИ.",
                    font="DejaVu Sans", font_size=30, color=BEIGE, weight=BOLD)
        cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(4.6)

        cap3 = Text("ВСЕГО 36 ТОКЕНОВ, НО МЫ ОСТАНОВИМСЯ",
                    font="DejaVu Sans", font_size=30, color=BEIGE, weight=BOLD)
        cap4 = Text("НА ГЛАВНЫХ ДЛЯ НАГЛЯДНОСТИ.",
                    font="DejaVu Sans", font_size=30, color=BEIGE, weight=BOLD)
        capb = VGroup(cap3, cap4).arrange(DOWN, buff=0.2)
        capb.move_to(cap.get_center())
        self.play(ReplacementTransform(cap, capb), run_time=0.6)
        self.wait(4.4)
        self.play(FadeOut(capb), run_time=0.4)
        self.play(FadeOut(VGroup(rows, title)), run_time=0.5)

        hook = Text(
            "РАЗБРОСАЕМ ТОКЕНЫ ПО «КОМНАТЕ»\n"
            "И ПОИГРАЕМ В ИГРУ.\n"
            "В КАЖДОМ ПРЕДЛОЖЕНИИ СПРЯЧЕМ ПО ТОКЕНУ —\n"
            "А МОДЕЛЬ БУДЕТ УГАДЫВАТЬ.\n"
            "ЦЕЛЬ ИГРЫ — ПОДОБРАТЬ ТОКЕНАМ\n"
            "ПРАВИЛЬНОЕ ОКРУЖЕНИЕ.",
            font="DejaVu Sans", font_size=30, weight=BOLD,
            t2c={
                "РАЗБРОСАЕМ ТОКЕНЫ ПО «КОМНАТЕ»": PHOSPHOR,
                "И ПОИГРАЕМ В ИГРУ.": PHOSPHOR,
                "В КАЖДОМ ПРЕДЛОЖЕНИИ СПРЯЧЕМ ПО ТОКЕНУ —": BEIGE,
                "А МОДЕЛЬ БУДЕТ УГАДЫВАТЬ.": BEIGE,
                "ЦЕЛЬ ИГРЫ — ПОДОБРАТЬ ТОКЕНАМ": PHOSPHOR,
                "ПРАВИЛЬНОЕ ОКРУЖЕНИЕ.": PHOSPHOR,
            },
        )
        hook.move_to(ORIGIN)
        self.play(AddTextLetterByLetter(hook, time_per_char=0.035), run_time=3.2)
        self.wait(6.0)
        self.play(FadeOut(hook, shift=UP * 0.05), run_time=0.4)

    # --- 2.5 Поясняющая чёрная карточка (фон скрывает 3D-сцену) ----------------
    def black_card(self, lines, font_size=34, hold=3.0, title_color=BEIGE):
        rect = Rectangle(width=40, height=24, color=BLACK, fill_opacity=1.0,
                         stroke_opacity=0.0)
        rect.fixed_in_frame = True
        txt = VGroup()
        for i, item in enumerate(lines):
            if isinstance(item, tuple):
                t, c = item
            else:
                t, c = item, (title_color if i == 0 else BEIGE)
            txt.add(Text(t, font="DejaVu Sans", font_size=font_size,
                         color=c, weight=BOLD))
        txt.arrange(DOWN, buff=0.3).center()
        txt.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(rect, txt)
        self.play(FadeIn(rect), FadeIn(txt, lag_ratio=0.1), run_time=0.45)
        self.wait(hold)
        self.play(FadeOut(rect), FadeOut(txt), run_time=0.45)
        self.remove(rect, txt)

    # --- 3. Обучение-«угадайка» в пространстве смысла ---------------------------
    def grid_3d(self):
        self.move_camera(phi=PHI_F, theta=THETA_F, zoom=ZOOM_F, gamma=ROLL,
                         frame_center=FRAME_CENTER, run_time=1.5)

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

        axes = VGroup(
            lowres_arrow([0, 0, 0], [L, 0, 0], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
            lowres_arrow([0, 0, 0], [0, L, 0], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
            lowres_arrow([0, 0, 0], [0, 0, L], SWAMP, height=0.35,
                         base_radius=0.12, thickness=0.035),
        )
        self.play(Create(grid, lag_ratio=0.02), run_time=1.6)
        self.play(FadeIn(axes), run_time=0.5)

        # Симуляция: стартовые позиции 29 токенов и правила игры
        np.random.seed(SEED)
        centers = cluster_centers(len(CLUSTERS), CLUSTER_SEP)
        init = initial_positions(WORDS, MIN_DIST, CLUSTER_OF, centers)
        pos = dict(zip(WORDS, init))
        sim_cam = make_sim_camera()
        neg_rng = np.random.default_rng(SEED + 777)

        dots = {w: Dot3D(point=pos[w], radius=0.06, color=DUST,
                         resolution=(2, 2)) for w in WORDS}
        dots_group = VGroup(*dots.values())

        self.play(FadeIn(dots_group, lag_ratio=0.04), run_time=0.9)
        self.wait(1.2)

        # колесо предложений: last_banner — предыдущее (наверху), top_mob —
        # текущее в центре, bot_mob — следующее (внизу)
        last_banner = None
        top_mob = None
        bot_mob = None
        shown_A = False       # карточка «Сближение» — один раз, перед притяжением
        shown_B = False       # карточка «Негативное сэмплирование» — перед отталкиванием

        for step_idx, sdata in enumerate(STEPS, start=1):
            target, ctx, outcome = sdata["target"], sdata["ctx"], sdata["outcome"]
            sent = ctx + [target]
            centroid = np.mean([pos[w] for w in ctx], axis=0)
            cands = [w for w in WORDS if w not in ctx]
            guess = min(cands, key=lambda w: np.linalg.norm(pos[w] - centroid))
            good = (outcome == "correct")
            gcolor = PHOSPHOR if good else RUST

            # колесо предложений: текущее в центре, предыдущее сверху (мало и
            # полупрозрачно), следующее снизу (мало и полупрозрачно); при
            # переходе — прокрутка вверх
            scroll_anims = []
            if step_idx > 1:
                if top_mob is not None:
                    scroll_anims.append(FadeOut(top_mob, run_time=0.25))
                if last_banner is not None:
                    scroll_anims.append(
                        last_banner.animate.move_to([LEFT_X, 2.35, 0])
                        .scale(0.5).set_opacity(0.45))
                    top_mob = last_banner
                if bot_mob is not None:
                    scroll_anims.append(
                        bot_mob.animate.move_to([LEFT_X, 0.9, 0]).set_opacity(0.0))
            if scroll_anims:
                self.play(*scroll_anims, run_time=0.3)

            # баннер предложения со спрятанным токеном (знаки ??? всегда на отдельной строке)
            def make_banner(guess_text=None, guess_color=None):
                def build_line(parts_in):
                    if not parts_in:
                        return None
                    mobs = []
                    for t, kind in parts_in:
                        if kind == "tgt":
                            if guess_text is None:
                                col, txt = BEIGE, "???"
                            else:
                                col, txt = guess_color, guess_text
                        elif kind == "fn":
                            col, txt = DUST, t
                        else:
                            col, txt = BEIGE, t
                        mobs.append(Text(txt, font="DejaVu Sans", font_size=30,
                                         color=col, weight=BOLD))
                    row = VGroup(*mobs).arrange(RIGHT, buff=0.14)
                    row.scale_to_fit_width(min(row.width, 6.6))
                    return row

                parts = sdata["banner"]
                tgt_idx = next(i for i, (t, k) in enumerate(parts) if k == "tgt")
                parts_before = parts[:tgt_idx]
                parts_tgt = [parts[tgt_idx]]
                parts_after = parts[tgt_idx + 1:]

                lines = []
                r1 = build_line(parts_before)
                if r1 is not None:
                    lines.append(r1)
                r2 = build_line(parts_tgt)
                lines.append(r2)
                r3 = build_line(parts_after)
                if r3 is not None:
                    lines.append(r3)

                b = VGroup(*lines).arrange(DOWN, buff=0.22)
                b.move_to([LEFT_X, 0.2, 0])
                wmap = {}
                for line in b:
                    for m in line:
                        if m.text == "???":
                            wmap[target] = m
                        else:
                            wmap[m.text] = m
                return b, r2, wmap

            banner, banner_tgt, word_mobs = make_banner()
            self.add_fixed_in_frame_mobjects(banner)
            self.play(FadeIn(banner), run_time=0.3)

            # следующее предложение (низ колеса) — полупрозрачно и меньше
            if step_idx < len(STEPS):
                nsent = " ".join(STEPS[step_idx]["ctx"]
                                 + [STEPS[step_idx]["target"]])
                bot_mob = Text(nsent, font="DejaVu Sans", font_size=18,
                               color=BEIGE, weight=BOLD)
                bot_mob.fixed_in_frame = True
                bot_mob.move_to([LEFT_X, -1.9, 0]).set_opacity(0.45)
                self.add_fixed_in_frame_mobjects(bot_mob)
                self.play(FadeIn(bot_mob, run_time=0.25))
            else:
                bot_mob = None

            # подсветка контекстных токенов
            ctx_halos = VGroup(*[
                Dot3D(point=pos[w], radius=0.12, color=BEIGE, fill_opacity=0.30,
                      resolution=(2, 2))
                for w in ctx
            ])
            if step_idx == 1:
                # сфера цели «???» подсвечивается сразу вместе с остальными
                # контекстными сферами, а не только при мигании своего слова
                target_halo = Dot3D(point=pos[target], radius=0.12, color=BEIGE,
                                    fill_opacity=0.30, resolution=(2, 2))
                self.play(FadeIn(ctx_halos), FadeIn(target_halo), run_time=0.25)
            else:
                self.play(FadeIn(ctx_halos), run_time=0.25)

            # подписи токенов предложения (слово сверху, номер снизу; без наложений)
            anchors = {w: pos[w] for w in sent}
            lab_pos = deoverlap(sim_cam, anchors, sent)
            if step_idx == 1:
                # ЗУМ на пока ещё не подписанные сферы — показываем, как слова
                # одно за другим «посвечиваются» (получают подпись)
                sim_cam.reset_rotation_matrix()
                _ps = [np.array(sim_cam.project_point(pos[w]))[:2] for w in sent]
                _bw = max(p[0] for p in _ps) - min(p[0] for p in _ps)
                _bh = max(p[1] for p in _ps) - min(p[1] for p in _ps)
                _k = float(np.clip(ZOOM_FILL * COL_WIDTH / max(_bw, _bh, 1e-6),
                                   ZOOM_K_MIN, ZOOM_K_MAX))
                _tz = ZOOM_F * _k
                _tfc = screen_fc(_tz, centroid)
                self.move_camera(frame_center=_tfc, zoom=_tz, run_time=ZOOM_RT)
                self.wait(0.3)
                labels_list = []
                for w in sent:
                    lab = token_label("???" if w == target else w, BEIGE,
                                      lab_pos[w])
                    self.add(lab)
                    wm = word_mobs.get(w)
                    for _ in range(3):
                        blink = [lab.animate.set_opacity(0.15)]
                        if wm is not None:
                            blink.append(wm.animate.set_opacity(0.15))
                        if w == target and target_halo is not None:
                            blink.append(target_halo.animate.set_opacity(0.1))
                        self.play(*blink, run_time=0.13)
                        unblink = [lab.animate.set_opacity(1.0)]
                        if wm is not None:
                            unblink.append(wm.animate.set_opacity(1.0))
                        if w == target and target_halo is not None:
                            unblink.append(target_halo.animate.set_opacity(0.5))
                        self.play(*unblink, run_time=0.13)
                    # мигание перестало — слово и подпись стали устойчивыми
                    self.wait(1.0)
                    labels_list.append(lab)
                labels = VGroup(*labels_list)
            else:
                labels = VGroup(*[
                    token_label("???" if w == target else w, BEIGE, lab_pos[w])
                    for w in sent
                ])
                target_halo = Dot3D(point=pos[target], radius=0.16, color=BEIGE,
                                    fill_opacity=0.5, resolution=(2, 2))
                self.play(FadeIn(labels, shift=UP * 0.12), FadeIn(target_halo),
                          run_time=0.3)

            # --- 1. Модель угадывает в 3D (справа): сначала центр контекста,
            #        затем линия от центра к догадке ---
            R_basis, U_basis, _ = camera_basis(PHI_F, THETA_F).T
            # зум к точкам предложения — ДО того, как модель угадает слово
            sim_cam.reset_rotation_matrix()
            _ps = [np.array(sim_cam.project_point(pos[w]))[:2] for w in sent]
            _bw = max(p[0] for p in _ps) - min(p[0] for p in _ps)
            _bh = max(p[1] for p in _ps) - min(p[1] for p in _ps)
            _k = ZOOM_FILL * COL_WIDTH / max(_bw, _bh, 1e-6)
            _k = float(np.clip(_k, ZOOM_K_MIN, ZOOM_K_MAX))
            _tz = ZOOM_F * _k
            _tfc = screen_fc(_tz, centroid)
            _dim = VGroup(*[dots[w] for w in WORDS if w not in sent and w != guess])
            self.move_camera(frame_center=_tfc, zoom=_tz, gamma=ROLL,
                             added_anims=[_dim.animate.set_opacity(DIM_OP)],
                             run_time=ZOOM_RT)
            self.wait(0.3)
            if step_idx == 1:
                self.black_card([
                    ("МОДЕЛЬ УГАДЫВАЕТ СЛОВО", PHOSPHOR),
                    ("выбирает ближайшее к центру", BEIGE),
                    ("группы слов из предложения", BEIGE),
                ], hold=5.0)
                # анимированная отрисовка центра: из каждого слова к центру
                # тянутся зелёные пунктиры (штрихи-цилиндры), сходятся в центре;
                # центр вспыхивает зелёной сферой и немного мигает, пунктиры гаснут
                connectors = VGroup()
                per_word = []
                for w in sent:
                    start = np.array(pos[w])
                    end = np.array(centroid)
                    vec = end - start
                    length = np.linalg.norm(vec)
                    n_dash = 6
                    dash_len = length / n_dash * 0.6
                    word_segs = []
                    for i in range(n_dash):
                        a = start + vec * (i / n_dash)
                        b = start + vec * (i / n_dash) + vec * (dash_len / length)
                        seg = Line3D(a, b, thickness=0.01, color=PHOSPHOR,
                                     resolution=4)
                        word_segs.append(seg)
                        connectors.add(seg)
                    per_word.append(word_segs)
                # штрихи появляются по очереди: сначала все первые (у слов),
                # затем вторые и т.д. — волна от слов к центру
                segs_ordered = [word_segs[i] for i in range(n_dash)
                                for word_segs in per_word]
                self.play(LaggedStart(*[FadeIn(s) for s in segs_ordered],
                                      lag_ratio=0.05), run_time=1.3)
                cent_dot = Dot3D(point=centroid, radius=0.1, color=PHOSPHOR,
                                fill_opacity=0.95, resolution=(2, 2))
                self.play(FadeIn(cent_dot, scale=1.5), run_time=0.3)
                for _ in range(3):
                    self.play(cent_dot.animate.set_opacity(0.4), run_time=0.12)
                    self.play(cent_dot.animate.set_opacity(0.95), run_time=0.12)
                self.play(FadeOut(connectors), run_time=0.3)
            else:
                cent_dot = Dot3D(point=centroid, radius=0.08, color=PHOSPHOR,
                                 fill_opacity=0.9, resolution=(2, 2))
                self.play(FadeIn(cent_dot), run_time=0.25)
            guess_halo = Dot3D(point=pos[guess], radius=0.12, color=BEIGE,
                               fill_opacity=0.30, resolution=(2, 2))
            if guess in sent:
                guess_label_3d = labels[sent.index(guess)]
                if step_idx == 1:
                    line = dashed_line3d(centroid, pos[guess], BEIGE,
                                         thickness=0.008, opacity=0.30)
                    self.play(FadeIn(line), run_time=0.4)
                    self.play(FadeIn(guess_halo), run_time=0.3)
                else:
                    line = dashed_line3d(centroid, pos[guess], BEIGE,
                                         thickness=0.008, opacity=0.30)
                    self.play(FadeIn(line), run_time=0.4)
                    self.play(FadeIn(guess_halo), run_time=0.3)
            else:
                guess_lab_pos = pos[guess] + U_basis * BASE_UP
                guess_label_3d = token_label(guess, BEIGE, guess_lab_pos)
                if step_idx == 1:
                    line = dashed_line3d(centroid, pos[guess], BEIGE,
                                         thickness=0.008, opacity=0.30)
                    self.play(FadeIn(line), run_time=0.4)
                    self.play(FadeIn(guess_halo), FadeIn(guess_label_3d),
                              run_time=0.3)
                else:
                    line = dashed_line3d(centroid, pos[guess], BEIGE,
                                         thickness=0.008, opacity=0.30)
                    self.play(FadeIn(line), run_time=0.4)
                    self.play(FadeIn(guess_halo), FadeIn(guess_label_3d),
                              run_time=0.3)

            # --- 2. Пролёт подписи из 3D к строке ??? в левом баннере ---
            start_proj = self.camera.project_point(guess_label_3d.get_center())
            start_2d = np.array([start_proj[0], start_proj[1], 0.0])
            tgt_2d = banner_tgt.get_center()

            fly_word = Text(guess, font="DejaVu Sans", font_size=30,
                            color=BEIGE, weight=BOLD)
            fly_word.move_to(start_2d)
            fly_word.fixed_in_frame = True
            self.add_fixed_in_frame_mobjects(fly_word)
            self.play(fly_word.animate.move_to(tgt_2d), run_time=0.45)

            # «угаданное» слово появляется вместо ??? в нейтральном бежевом цвете
            banner_neutral, guess_row, _ = make_banner(guess_text=guess,
                                                       guess_color=BEIGE)
            self.add_fixed_in_frame_mobjects(banner_neutral)
            self.remove(fly_word, banner)
            banner = banner_neutral

            # слово мигает, прежде чем окраситься в нужный цвет — 3D-сфера тоже мигает
            for _ in range(3):
                self.play(guess_row.animate.set_opacity(0.15),
                          guess_halo.animate.set_opacity(0.15), run_time=0.13)
                self.play(guess_row.animate.set_opacity(1.0),
                          guess_halo.animate.set_opacity(0.55), run_time=0.13)

            # --- 3. Цвет меняется на зелёный (успех) или красный (промах) ---
            #        линия от центра к слову остаётся бежевой
            banner_colored, _, _ = make_banner(guess_text=guess, guess_color=gcolor)
            self.add_fixed_in_frame_mobjects(banner_colored)
            self.play(
                ReplacementTransform(banner, banner_colored),
                guess_halo.animate.set_color(gcolor),
                run_time=0.35,
            )
            banner = banner_colored
            last_banner = banner
            self.wait(1.0)

            # вердикт — поверх центрального предложения
            verdict = bubble("УГАДАЛА!" if good else "НЕ УГАДАЛА", gcolor)
            verdict.move_to(banner.get_center())
            self.add_fixed_in_frame_mobjects(verdict)
            self.play(FadeIn(verdict, scale=0.85), run_time=0.35)

            # --- Позитивное сэмплирование: ВЫПОЛНЯЕМ ДО негативного ---
            if not good and not shown_A:
                self.black_card([
                    "ПОЗИТИВНОЕ СЭМПЛИРОВАНИЕ",
                    "Слова, что встречаются рядом,",
                    "модель притягивает к центру контекста.",
                ], hold=5.0, title_color=PHOSPHOR)
                shown_A = True
                self.wait(2.0)

            if not good:
                # стрелки от токенов предложения к центру (центр уже показан)
                arrows = VGroup(*[
                    lowres_arrow(pos[w], centroid, PHOSPHOR)
                    for w in sent
                ])
                self.wait(0.6)
                self.play(FadeIn(arrows), run_time=0.3)
                # стрелки тянутся от сфер к центру: хвост едет со сферой,
                # нос всегда смотрит в фиксированный центр
                for idx_a, w in enumerate(sent):
                    arrows[idx_a].add_updater(
                        lambda m, w=w: m.become(
                            lowres_arrow(dots[w].get_center(), centroid, PHOSPHOR))
                    )

                new_pos = {w: pos[w] + (centroid - pos[w]) * PULL for w in sent}
                new_lab = deoverlap(sim_cam, new_pos, sent)
                moves = [dots[w].animate.move_to(new_pos[w]) for w in sent]
                for w in sent:
                    lab_idx = sent.index(w)
                    moves.append(labels[lab_idx].animate.move_to(new_lab[w]))
                for i, w in enumerate(ctx):
                    moves.append(ctx_halos[i].animate.move_to(new_pos[w]))
                moves.append(target_halo.animate.move_to(new_pos[target]))
                self.play(*moves, run_time=0.6)
                for a in arrows:
                    a.clear_updaters()
                self.play(FadeOut(arrows), run_time=0.3)
                for w in sent:
                    pos[w] = new_pos[w]
            else:
                self.play(target_halo.animate.scale(1.6), run_time=0.25)
                self.play(target_halo.animate.scale(1 / 1.6), run_time=0.25)

            # откат зума — ДО негативного сэмплирования, чтобы было видно
            # всё пространство, куда разлетаются «лишние» слова
            self.move_camera(frame_center=FRAME_CENTER, zoom=ZOOM_F, gamma=ROLL,
                             added_anims=[dots_group.animate.set_opacity(1.0)],
                             run_time=ZOOM_RT)
            self.wait(0.3)

            # --- Негативное сэмплирование: со 2-го шага отталкиваем
            #         3 случайных «неправильных» токена от центра контекста ---
            if step_idx >= 2:
                if not shown_B:
                    self.black_card([
                        "НЕГАТИВНОЕ СЭМПЛИРОВАНИЕ",
                        "чтобы все не сползлось",
                        "в одну точку, случайные",
                        "слова нужно отодвигать",
                    ], hold=6.5, title_color=RUST)
                    shown_B = True
                negs = sample_negatives(WORDS, set(sent) | {guess}, 3, neg_rng)
                neg_words = []
                neg_arrows = []
                neg_halos = []
                for w in negs:
                    d = pos[w] - centroid
                    if np.linalg.norm(d) < 1e-6:
                        continue
                    neg_words.append(w)
                    # стрелка ОТ центра НАРУЖУ — обратное направление
                    # относительно стрелок «в центр» (притяжения)
                    neg_arrows.append(lowres_arrow(centroid, pos[w], RUST))
                    neg_halos.append(Dot3D(point=pos[w], radius=0.11, color=RUST,
                                           fill_opacity=0.40, resolution=(2, 2)))
                if neg_words:
                    neg_arrows = VGroup(*neg_arrows)
                    neg_halos = VGroup(*neg_halos)
                    self.play(FadeIn(neg_arrows, lag_ratio=0.05),
                              FadeIn(neg_halos, lag_ratio=0.05), run_time=0.3)
                    moves = []
                    new_neg = {}
                    for idx, w in enumerate(neg_words):
                        d = pos[w] - centroid
                        nd = np.linalg.norm(d)
                        new_neg[w] = np.clip(pos[w] + d / nd * REPEL_STEP,
                                             0.5, L - 0.5)
                        delta = new_neg[w] - pos[w]
                        moves.append(dots[w].animate.move_to(new_neg[w]))
                        # гало едет вместе со сферой, а стрелка тянется от
                        # центра к слову: хвост всегда в центре, наконечник —
                        # на движущейся сфере
                        moves.append(neg_halos[idx].animate.move_to(new_neg[w]))
                        neg_arrows[idx].add_updater(
                            lambda m, w=w: m.become(
                                lowres_arrow(centroid, dots[w].get_center(), RUST))
                        )
                    self.play(*moves, run_time=0.5)
                    for a in neg_arrows:
                        a.clear_updaters()
                    self.play(FadeOut(neg_arrows), FadeOut(neg_halos), run_time=0.3)
                    for w in new_neg:
                        pos[w] = new_neg[w]

            # очистка шага (баннер НЕ гасим — он уходит наверх как «предыдущее»
            # предложение в колесе)
            clean_anims = [
                FadeOut(ctx_halos), FadeOut(target_halo), FadeOut(guess_halo),
                FadeOut(line), FadeOut(verdict), FadeOut(labels),
                FadeOut(cent_dot)
            ]
            if guess not in sent:
                clean_anims.append(FadeOut(guess_label_3d))
            self.play(*clean_anims, run_time=0.25)

        # --- Финал: 4 смысловых кластера ------------------------------------
        # сначала убираем баннер и текст слева, потом показываем чёрную карточку
        wheel_mobs = [m for m in (last_banner, top_mob, bot_mob) if m is not None]
        self.play(*[FadeOut(m, run_time=0.3) for m in wheel_mobs])

        self.black_card([
            ("ОБУЧЕНИЕ ЗАКАНЧИВАЕТСЯ,", PHOSPHOR),
            ("когда модель прогнала все предложения 3-5 раз,", BEIGE),
            ("либо когда перестала обучаться.", BEIGE),
        ], hold=5.0)
        final_top = VGroup(
            Text("ОБУЧЕНИЕ ЗАВЕРШЕНО.\nБЛИЗКИЕ ТОЧКИ — БЛИЗКИЙ СМЫСЛ",
                 font="DejaVu Sans", font_size=28, color=PHOSPHOR, weight=BOLD),
        ).to_edge(UP, buff=0.55).to_edge(LEFT, buff=0.55)
        self.add_fixed_in_frame_mobjects(final_top)
        self.play(FadeIn(final_top), run_time=0.5)

        proj = self.camera.project_point
        # центры кластеров по финальным позициям
        cluster_cc = [np.mean([pos[w] for w in members], axis=0)
                      for _, _, members in CLUSTERS]

        # перекраска всех 29 точек в цвет их кластера (явное выделение групп)
        recolor = [dots[w].animate.set_color(CLUSTERS[CLUSTER_OF[w]][1])
                   for w in WORDS]
        self.play(*recolor, run_time=0.5)

        # 8 главных подписей — в цвете своего кластера (слово сверху, номер снизу)
        key_anchors = {w: pos[w] for w in KEYS8}
        key_lab_pos = deoverlap(sim_cam, key_anchors, KEYS8)
        key_labels = VGroup(*[
            token_label_flat(w, CLUSTERS[CLUSTER_OF[w]][1], LABEL_SCALE,
                             key_lab_pos[w], proj)
            for w in KEYS8
        ])
        self.add_fixed_in_frame_mobjects(*key_labels)
        self.play(FadeIn(key_labels, lag_ratio=0.08), run_time=0.9)

        # легенда слева: цвет → примеры слов кластера (без названий тем)
        legend_rows = []
        for name, color, members in CLUSTERS:
            sw = Square(side_length=0.3, color=color, fill_color=color,
                        fill_opacity=1.0, stroke_color=INK, stroke_width=3)
            ex = ", ".join(members[:3])
            txt = Text(ex, font="DejaVu Sans",
                        font_size=18, color=color, weight=BOLD)
            legend_rows.append(VGroup(sw, txt).arrange(RIGHT, buff=0.18))
        legend = VGroup(*legend_rows).arrange(DOWN, buff=0.22,
                                              aligned_edge=LEFT)
        legend.move_to([LEFT_X - 0.4, -0.4, 0])
        self.add_fixed_in_frame_mobjects(legend)
        self.play(FadeIn(legend), run_time=0.6)

        # удерживаем финальную картину с кластерами и легендой
        self.wait(4.5)

        # скрываем легенду, заголовок и подписи вместе
        self.play(FadeOut(legend), FadeOut(final_top), FadeOut(key_labels), run_time=0.5)

        # "порошок" — его позиция и слово
        powder = "ПОРОШОК"
        powder_pos = np.array(pos[powder])

        # подвинуть камеру так, чтобы в кадре были (0,0,0) и порошок,
        # и они оказались по центру экрана
        origin = np.array([0.0, 0.0, 0.0])
        mid = (origin + powder_pos) / 2.0
        dist = np.linalg.norm(powder_pos - origin)
        needed_zoom = ZOOM_F * (L / max(dist * 1.6, 1.0))
        new_zoom = float(np.clip(needed_zoom, ZOOM_F * 0.5, ZOOM_F * 2.5))
        self.move_camera(frame_center=mid, zoom=new_zoom, run_time=1.5)
        self.wait(0.3)

        # стрелка от начала координат к "порошок" — зелёная, непрозрачная
        arrow_powder = Arrow3D(start=origin, end=powder_pos,
                                color=PHOSPHOR, thickness=0.012,
                                height=0.18, base_radius=0.06)
        self.play(FadeIn(arrow_powder), run_time=0.5)

        # НЕ подсвечиваем сферу "порошок" — только стрелка указывает

        # слово "Порошок" — зелёное, над координатами
        word_mob = Text("Порошок", font="DejaVu Sans", font_size=28,
                        color=PHOSPHOR, weight=BOLD)
        word_proj = self.camera.project_point(powder_pos + np.array([0, 0.2, 0]))
        word_mob.move_to([word_proj[0], word_proj[1], 0])
        word_mob.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(word_mob)
        self.play(Write(word_mob), run_time=0.4)

        # координаты под словом (в квадратных скобках)
        coord_text = f"[{powder_pos[0]:.2f}, {powder_pos[1]:.2f}, {powder_pos[2]:.2f}]"
        coord_mob = Text(coord_text, font="DejaVu Sans", font_size=22,
                         color=PHOSPHOR, weight=BOLD)
        coord_proj = self.camera.project_point(powder_pos - np.array([0, 1.2, 0]))
        coord_mob.move_to([coord_proj[0], coord_proj[1], 0])
        coord_mob.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(coord_mob)
        self.play(Write(coord_mob), run_time=0.5)

        self.wait(1.5)

        # плавно скрыть ВСЮ 3D-сцену, оставить только слово и координаты
        self.play(FadeOut(dots_group), FadeOut(key_labels),
                  FadeOut(arrow_powder), FadeOut(axes), FadeOut(grid),
                  run_time=1.0)

        # слово и координаты уходят наверх и центрируются
        self.play(
            word_mob.animate.scale(1.3).move_to([0, 0.8, 0]),
            coord_mob.animate.move_to([0, -0.2, 0]),
            run_time=1.0
        )

        # текст-пояснение печатается снизу (разбит на строки)
        explain = Text(
            "Координаты этой точки — вектор —\n"
            "и называется эмбеддингом.",
            font="DejaVu Sans", font_size=30, color=BEIGE, weight=BOLD,
            t2c={"эмбеддингом": PHOSPHOR}
        )
        explain.move_to([0, -1.5, 0])
        explain.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(explain)
        self.play(AddTextLetterByLetter(explain, time_per_char=0.03), run_time=2.5)
        self.wait(3.0)
        self.play(FadeOut(explain), FadeOut(word_mob), FadeOut(coord_mob),
                  run_time=0.5)

        # финальный экран: 3 числа мало, реальные эмбеддинги — 384
        final1 = Text(
            "ДЛЯ РЕАЛЬНОГО ЯЗЫКА 3 ЧИСЛА — МАЛО.",
            font="DejaVu Sans", font_size=30, color=BEIGE, weight=BOLD,
        )
        final2 = Text(
            "МОДЕЛИ ИСПОЛЬЗУЮТ ЭМБЕДДИНГИ\nИЗ 384 ИЛИ БОЛЕЕ ИЗМЕРЕНИЙ.",
            font="DejaVu Sans", font_size=30, color=PHOSPHOR, weight=BOLD,
            t2c={"384": PHOSPHOR}
        )
        final = VGroup(final1, final2).arrange(DOWN, buff=0.3)
        final.move_to(ORIGIN)
        final.fixed_in_frame = True
        self.add_fixed_in_frame_mobjects(final)
        self.play(AddTextLetterByLetter(final, time_per_char=0.03), run_time=3.0)
        self.wait(4.0)
