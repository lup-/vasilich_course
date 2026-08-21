#!/usr/bin/env python3
"""
Генерация комикс-панелей через Google Gemini API (nano banana 2 lite).

Использование:
  python scripts/gen_comic_images.py 5 2.1            # урок 5, кадр 2.1
  python scripts/gen_comic_images.py 5               # урок 5, все кадры
  python scripts/gen_comic_images.py                  # первый неготовый кадр курса
  python scripts/gen_comic_images.py --all            # все неготовые кадры
  python scripts/gen_comic_images.py 5 2.1 --dry-run # только показать промпт/refs
  python scripts/gen_comic_images.py --sem sem2       # только sem2
  python scripts/gen_comic_images.py -y              # без подтверждения
"""

import os
import sys
import re
import json
import base64
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

try:
    import requests
except ImportError:
    print("ERROR: requests не установлен. pip install requests", file=sys.stderr)
    sys.exit(1)

# ============== КОНСТАНТЫ И ДЕФОЛТЫ (nano banana 2 lite) ==============
DEFAULT_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-3.1-flash-lite-image"
DEFAULT_API_KEY_ENV = "GEMINI_API_KEY"
DEFAULT_API_FORMAT = "gemini"
DEFAULT_N_REF = 4
DEFAULT_ASPECT = "1:1"
DEFAULT_TIMEOUT = 120

# Утверждённые описания персонажей из world-bible.md
CHARACTERS = {
    "Василич": (
        "мужчина 50-60 лет, ушанка с опущенными ушами, нос картошкой, безумные глаза с маленькими зрачками, "
        "щетина, грязный ватник болотного цвета, кибер-протезы рук (металлические, с суставами, шлангами, проводами), "
        "рваные штаны с металлическими шарнирами на коленях, грубые сапоги"
    ),
    "Алиса": (
        "женщина 70+ лет, короткая пепельно-сиреневая (лавандовая) стрижка, глубокие морщины, "
        "дерзкий макияж: тёмные готические смоки-айс, пирсинг-септум и лабрет, круглые очки для чтения на цепочке, "
        "вместо левого глаза — светящийся фиолетово-синий кибер-имплант с проводами и микросхемами, "
        "коричневый джемпер свободного кроя, большая татуировка с технологичным узором на груди"
    ),
    "Директор": (
        "лысина с остатками тёмных волос по бокам, красное лицо, глубокие морщины, злые глаза, крупный нос, "
        "двойной подбородок, за массивной деревянной трибуной, кулак поднят вверх, "
        "помятый советский костюм болотного цвета, сероватая рубашка, тёмный галстук"
    ),
    "Бухгалтерша": (
        "платиновая «химия» с начёсом и отросшими тёмными корнями, яркий макияж (стрелки, накладные ресницы, розовая помада), "
        "короткое яркое платье или юбка-карандаш, капрон с затяжкой, туфли на каблуках со стёртыми набойками, "
        "облупившийся лак на ногтях, визгливая, суетливая"
    ),
    "Кладовщик": (
        "пожилой мужик в зумерской модной одежде: оверсайз-худи с нашивкой «СКЛАД №2», широкие штаны-карго, "
        "кроссовки, кепка-бакетхет или шапка-бини, ухоженная причёска (фейд с окраской), подкрученные усы, "
        "аккуратно остриженная борода, сыплет зумерским сленгом"
    ),
    "Инженер-наладчик": (
        "рабочая спецовка, защитные очки, инструменты на поясе, практический вид, появляется в семестре 2"
    ),
    "Заводчане": (
        "рабочие в робах, каски, грязные, фоновые группы"
    ),
    "Электроник-84": (
        "монументальная ЭВМ-машина с лампами, перфолентой, кнопками, скрипкой на корпусе, "
        "табло: «ERROR 404: ГЕНИЙ НЕ НАЙДЕН», зелёная жижа в колбе"
    ),
}

# Регулярки для детекта героев (порядок важен: длинные имена раньше)
CHARACTER_PATTERNS = {
    "Василич": [r"Василич\b(?!-5\.7)"],
    "Алиса": [r"\bАлиса\b"],
    "Директор": [r"\bДиректор\b"],
    "Бухгалтерша": [r"\bБухгалтерша\b"],
    "Кладовщик": [r"\bКладовщик\b"],
    "Инженер": [r"Инженер[- ]наладчик|\bИнженер\b"],
    "Заводчане": [r"\bЗаводчане\b"],
    "Электроник-84": [r"Электроник[- ]84|\bЭлектроник\b(?!-5\.7)"],
}

# Встроенный дефолтный стилевой суффикс (если нет в comic.md)
DEFAULT_STYLE_SUFFIX = (
    "Однокадровый комикс, русский гаражный киберпанк, славпанк, стиль простого сатирического веб-комикса, "
    "плоские цвета, жирный чёрный контур, гротескная карикатура, нелепые лица, абсурдная атмосфера, "
    "высокие технологии из мусора и синей изоленты, советский ретро-футуризм, 2d art, --ar 1:1"
)

# ============== МЕЛКИЕ УТИЛИТЫ ==============
def load_env(path: Optional[Path] = None) -> Dict[str, str]:
    """Мини-парсер .env — без внешних зависимостей."""
    env = dict(os.environ)
    candidates = []
    if path:
        candidates.append(path)
    candidates.append(Path.cwd() / ".env")
    candidates.append(Path(__file__).parent / ".env")
    for p in candidates:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_png(path: Path, b64: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


# ============== ПАРСИНГ COMIC.MD ==============
class Panel:
    def __init__(self, frame_id: str, slide_num: int, text: str, idx_in_slide: int):
        self.frame_id = frame_id       # "2.1"
        self.slide_num = slide_num     # 16
        self.text = text               # полный текст блока Кадр
        self.idx_in_slide = idx_in_slide  # 1-based внутри слайда

    @property
    def out_filename(self) -> str:
        return f"{self.idx_in_slide:02d}.png"

    @property
    def slide_folder(self) -> str:
        return f"slide-{self.slide_num:02d}"

    def detect_characters(self) -> List[str]:
        found = []
        for char, patterns in CHARACTER_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, self.text, re.IGNORECASE):
                    found.append(char)
                    break
        return found


class Comic:
    def __init__(self, lesson_path: Path):
        self.lesson_path = lesson_path
        self.comic_path = lesson_path / "comic.md"
        self.raw = read_text(self.comic_path)
        self.style_suffix = self._extract_style_suffix()
        self.scenes = self._parse_scenes()  # list of (slide_num, [Panel])

    def _extract_style_suffix(self) -> str:
        # Ищем блок "**Общий стилевой суффикс (для всех кадров):**" и берём следующую цитату/текст
        m = re.search(r"\*\*Общий стилевой суффикс[^:]*:\*\*\s*(?:>\s*)?(.+?)(?:\n\s*---|\n\s*## |\Z)", self.raw, re.DOTALL)
        if m:
            suffix = m.group(1).strip()
            # убрать маркдаун-цитату >
            suffix = re.sub(r"^>\s?", "", suffix, flags=re.MULTILINE).strip()
            if suffix:
                return suffix
        return DEFAULT_STYLE_SUFFIX

    def _parse_scenes(self) -> List[Tuple[int, List[Panel]]]:
        scenes = []
        text = self.raw
        # Разбиваем по сценам: "## Сцена N" или "### Сцена N"
        scene_splits = re.split(r"\n(?=#{2,3}\s+Сцена\s+\d+)", text)
        for chunk in scene_splits:
            if not chunk.strip():
                continue
            # Номер слайда в этой сцене
            slide_num = None
            m = re.search(r"\*\*Слайд\s+(\d+)\*\*", chunk)
            if not m:
                m = re.search(r"Слайд:\s*(\d+)", chunk)
            if m:
                slide_num = int(m.group(1))
            else:
                continue

            # Извлекаем кадры: поддерживаем оба формата
            # 1) ### Кадр X.Y ...
            # 2) Кадр X.Y: ...
            panels = []
            # Находим все вхождения начала кадра
            panel_starts = [(m.start(), m.group(1).rstrip(".")) for m in re.finditer(r"(?:###\s+)?Кадр\s+([\d.]+)[:\s]", chunk)]
            for i, (start_pos, frame_id) in enumerate(panel_starts):
                end_pos = panel_starts[i+1][0] if i+1 < len(panel_starts) else len(chunk)
                panel_text = chunk[start_pos:end_pos].strip()
                panels.append((frame_id, panel_text))

            # Создаём Panel объекты с idx_in_slide = 1..N
            panel_objs = [Panel(fid, slide_num, txt, i+1) for i, (fid, txt) in enumerate(panels)]
            if panel_objs:
                scenes.append((slide_num, panel_objs))
        return scenes

    def get_panel(self, frame_id: str) -> Optional[Tuple[int, Panel]]:
        """Возвращает (slide_num, Panel) для заданного frame_id (e.g. '2.1')."""
        for slide_num, panels in self.scenes:
            for p in panels:
                if p.frame_id == frame_id:
                    return slide_num, p
        return None

    def all_panels(self) -> List[Tuple[int, Panel]]:
        """Все панели: список (slide_num, Panel)."""
        out = []
        for slide_num, panels in self.scenes:
            for p in panels:
                out.append((slide_num, p))
        return out

    def slide_nums(self) -> Set[int]:
        return {sn for sn, _ in self.scenes}

    def panels_for_slide(self, slide_num: int) -> List[Panel]:
        for sn, panels in self.scenes:
            if sn == slide_num:
                return panels
        return []


# ============== ГЛОБАЛЬНЫЙ ИНДЕКС ГОТОВЫХ КАДРОВ ==============
class ReadyIndex:
    """Строит маппинг: герой -> список (sem, lesson_dir, slide_num, panel_idx, png_path)."""
    def __init__(self, content_root: Path):
        self.content_root = content_root
        self.hero_to_refs: Dict[str, List[Tuple[str, Path]]] = {}
        self._build()

    def _build(self):
        for sem_dir in sorted(self.content_root.iterdir()):
            if not sem_dir.is_dir() or not sem_dir.name.startswith(("sem1", "sem2")):
                continue
            sem = sem_dir.name
            for lesson_dir in sorted(sem_dir.iterdir()):
                if not lesson_dir.is_dir() or lesson_dir.name in ("course-slides.md", "extra"):
                    continue
                # Пропускаем не-уроки (например, extra)
                if not re.match(r"^\d{2}-", lesson_dir.name):
                    continue
                comic_path = lesson_dir / "comic.md"
                if not comic_path.exists():
                    continue
                comic = Comic(lesson_path=lesson_dir)
                for slide_num, panel in comic.all_panels():
                    png_path = lesson_dir / f"slide-{slide_num:02d}" / panel.out_filename
                    if png_path.exists():
                        heroes = panel.detect_characters()
                        for h in heroes:
                            self.hero_to_refs.setdefault(h, []).append(
                                (sem, lesson_dir, slide_num, panel.idx_in_slide, png_path)
                            )

    def get_refs_for_heroes(self, heroes: List[str], exclude_lesson: Path, max_refs: int = 4) -> List[Path]:
        """Собрать уникальные reference-пути для заданных героев, исключая exclude_lesson."""
        seen = set()
        refs = []
        # Приоритет: другие уроки, потом свой урок
        for h in heroes:
            for sem, less_dir, sld, idx, pth in self.hero_to_refs.get(h, []):
                if less_dir == exclude_lesson:
                    continue
                if pth not in seen:
                    seen.add(pth)
                    refs.append(pth)
                    if len(refs) >= max_refs:
                        return refs
        # Если мало — добираем из своего урока
        if len(refs) < max_refs:
            for h in heroes:
                for sem, less_dir, sld, idx, pth in self.hero_to_refs.get(h, []):
                    if less_dir != exclude_lesson:
                        continue
                    if pth not in seen:
                        seen.add(pth)
                        refs.append(pth)
                        if len(refs) >= max_refs:
                            return refs
        return refs[:max_refs]


# ============== УРОК / СЕМЕСТР ==============
def find_lesson_dir(content_root: Path, sem: Optional[str], lesson_num: int) -> Optional[Path]:
    if sem is None:
        sem = "sem1"  # дефолт для явного указания урока
    sem_dir = content_root / sem
    if not sem_dir.exists():
        return None
    pattern = f"{lesson_num:02d}-*"
    matches = list(sem_dir.glob(pattern))
    if len(matches) == 1:
        return matches[0]
    return None


def get_lesson_title(lesson_dir: Path) -> str:
    slides_plan = lesson_dir / "slides-plan.md"
    if not slides_plan.exists():
        return lesson_dir.name
    text = read_text(slides_plan)
    m = re.search(r"^#\s+Занятие\s+\d+\.\s*[«\"](.+?)[»\"]", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # fallback: первая строка после #
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return lesson_dir.name


# ============== ПРОМПТ И API ==============
def build_prompt(panel: Panel, style_suffix: str, ref_heroes: List[str], ref_paths: List[Path]) -> str:
    # Текст кадра без маркдаун-заголовков
    panel_text = panel.text
    # Убираем заголовок ### Кадр X.Y ...
    panel_text = re.sub(r"^###\s+Кадр\s+[\d.]+\s*[—-]?\s*.*?\n", "", panel_text)
    # Убираем маркдаун **жирное** для чистоты
    panel_text = re.sub(r"\*\*(.+?)\*\*", r"\1", panel_text)

    parts = []
    parts.append(panel_text.strip())
    parts.append(style_suffix.strip())

    if ref_heroes:
        parts.append("Используй ПРИЛОЖЕННЫЕ reference-изображения как эталон стиля и персонажей.")
        parts.append("Герои на панели (держи дизайн идентичным эталонам):")
        for h in ref_heroes:
            desc = CHARACTERS.get(h, "")
            if desc:
                parts.append(f" - {h}: {desc}")

    parts.append("Формат: квадрат, 1:1.")
    return "\n\n".join(parts)


def call_gemini_api(prompt: str, ref_paths: List[Path], api_url: str, model: str, api_key: str) -> bytes:
    """Вызов Google Gemini generateContent. Возвращает PNG bytes."""
    # Подготавливаем parts
    parts = [{"text": prompt}]
    for rp in ref_paths:
        with open(rp, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        parts.append({"inline_data": {"mime_type": "image/png", "data": b64}})

    body = {
        "contents": [{"parts": parts}]
    }

    url = api_url.format(model=model) if "{model}" in api_url else f"{api_url}/{model}:generateContent"

    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }

    resp = requests.post(url, headers=headers, json=body, timeout=DEFAULT_TIMEOUT)
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:500]}")

    data = resp.json()

    # Ищем inline_data в ответе
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"Пустой ответ: {json.dumps(data)[:500]}")

    for cand in candidates:
        content = cand.get("content", {})
        for part in content.get("parts", []):
            inline = part.get("inline_data")
            if inline and inline.get("mime_type", "").startswith("image/"):
                img_b64 = inline.get("data")
                if img_b64:
                    return base64.b64decode(img_b64)

    raise RuntimeError(f"Нет изображения в ответе: {json.dumps(data)[:500]}")


# ============== ОСНОВНАЯ ЛОГИКА ==============
def scan_course(content_root: Path, sem_filter: Optional[str] = None) -> List[Tuple[str, Path, Comic]]:
    """Возвращает список (sem, lesson_dir, Comic) в порядке курса."""
    out = []
    sem_dirs = []
    if sem_filter:
        sem_dirs = [content_root / sem_filter] if (content_root / sem_filter).exists() else []
    else:
        for sd in sorted(content_root.iterdir()):
            if sd.is_dir() and sd.name in ("sem1", "sem2"):
                sem_dirs.append(sd)
    for sem_dir in sem_dirs:
        sem = sem_dir.name
        for lesson_dir in sorted(sem_dir.iterdir()):
            if not lesson_dir.is_dir() or lesson_dir.name in ("course-slides.md", "extra"):
                continue
            if not re.match(r"^\d{2}-", lesson_dir.name):
                continue
            comic_path = lesson_dir / "comic.md"
            if comic_path.exists():
                out.append((sem, lesson_dir, Comic(lesson_dir)))
    return out


def is_slide_ready(lesson_dir: Path, slide_num: int, expected_panels: int) -> bool:
    slide_dir = lesson_dir / f"slide-{slide_num:02d}"
    if not slide_dir.exists():
        return False
    pngs = list(slide_dir.glob("*.png"))
    return len(pngs) >= expected_panels


def find_next_unready_frame(content_root: Path, sem_filter: Optional[str]) -> Optional[Tuple[str, Path, int, Panel]]:
    """Найти первый неготовый кадр по курсу."""
    course = scan_course(content_root, sem_filter)
    for sem, lesson_dir, comic in course:
        for slide_num, panel in comic.all_panels():
            if not is_slide_ready(lesson_dir, slide_num, len(comic.panels_for_slide(slide_num))):
                return sem, lesson_dir, slide_num, panel
    return None


def collect_target_frames(args, content_root: Path, ready_idx: ReadyIndex) -> List[Tuple[str, Path, int, Panel, str, List[Path], str]]:
    """
    Возвращает список кортежей: (sem, lesson_dir, slide_num, panel, lesson_title, ref_paths, style_suffix)
    """
    targets = []

    if args.lesson is not None and args.frame is not None:
        # Явный урок + кадр: 5 2.1
        lesson_dir = find_lesson_dir(content_root, args.sem, args.lesson)
        if not lesson_dir:
            raise ValueError(f"Урок {args.lesson} не найден в {args.sem}")
        comic = Comic(lesson_dir)
        res = comic.get_panel(args.frame)
        if not res:
            raise ValueError(f"Кадр {args.frame} не найден в уроке {args.lesson}")
        slide_num, panel = res
        refs = ready_idx.get_refs_for_heroes(panel.detect_characters(), lesson_dir, args.n_refs)
        targets.append((args.sem, lesson_dir, slide_num, panel, get_lesson_title(lesson_dir), refs, comic.style_suffix))

    elif args.lesson is not None and args.frame is None:
        # Весь урок: все image_group кадры
        lesson_dir = find_lesson_dir(content_root, args.sem, args.lesson)
        if not lesson_dir:
            raise ValueError(f"Урок {args.lesson} не найден в {args.sem}")
        comic = Comic(lesson_dir)
        for slide_num, panel in comic.all_panels():
            refs = ready_idx.get_refs_for_heroes(panel.detect_characters(), lesson_dir, args.n_refs)
            targets.append((args.sem, lesson_dir, slide_num, panel, get_lesson_title(lesson_dir), refs, comic.style_suffix))

    elif args.all:
        # Все неготовые кадры курса
        course = scan_course(content_root, args.sem)
        for sem, lesson_dir, comic in course:
            for slide_num, panel in comic.all_panels():
                if not is_slide_ready(lesson_dir, slide_num, len(comic.panels_for_slide(slide_num))):
                    refs = ready_idx.get_refs_for_heroes(panel.detect_characters(), lesson_dir, args.n_refs)
                    targets.append((sem, lesson_dir, slide_num, panel, get_lesson_title(lesson_dir), refs, comic.style_suffix))

    else:
        # Режим «продолжить»: один следующий кадр
        nxt = find_next_unready_frame(content_root, args.sem)
        if not nxt:
            print("Все кадры уже готовы.")
            return []
        sem, lesson_dir, slide_num, panel = nxt
        comic = Comic(lesson_dir)
        refs = ready_idx.get_refs_for_heroes(panel.detect_characters(), lesson_dir, args.n_refs)
        targets.append((sem, lesson_dir, slide_num, panel, get_lesson_title(lesson_dir), refs, comic.style_suffix))

    return targets


def print_confirmation(targets, dry_run: bool):
    print("\n" + "=" * 60)
    print("ПЛАН ГЕНЕРАЦИИ")
    print("=" * 60)
    for i, (sem, lesson_dir, slide_num, panel, title, refs, style_suffix) in enumerate(targets, 1):
        print(f"\n[{i}] Урок: {title} ({lesson_dir.name})")
        print(f"    Кадр: {panel.frame_id}  →  Слайд: {slide_num}  →  Файл: slide-{slide_num:02d}/{panel.out_filename}")
        print(f"    Герои: {panel.detect_characters() or '—'}")
        print(f"    Reference: {len(refs)} шт. {[p.name for p in refs]}")
        print(f"    Сценарий:\n{panel.text[:500]}..." if len(panel.text) > 500 else f"    Сценарий:\n{panel.text}")
    print("=" * 60)
    if dry_run:
        print("DRY-RUN: генерация не выполняется.")
        return False
    return True


def ask_confirm() -> bool:
    try:
        ans = input("Сгенерировать? [y/N]: ").strip().lower()
        return ans in ("y", "yes", "д", "да")
    except (EOFError, KeyboardInterrupt):
        return False


def main():
    parser = argparse.ArgumentParser(description="Генерация комикс-панелей (nano banana 2 lite)")
    parser.add_argument("lesson", nargs="?", type=int, help="Номер урока (1-16)")
    parser.add_argument("frame", nargs="?", help="Номер кадра из comic.md (например, 2.1)")
    parser.add_argument("--sem", choices=["sem1", "sem2"], default=None, help="Семестр (по умолчанию оба)")
    parser.add_argument("--all", action="store_true", help="Сгенерировать все неготовые кадры курса")
    parser.add_argument("--yes", "-y", action="store_true", help="Не спрашивать подтверждение")
    parser.add_argument("--dry-run", action="store_true", help="Только показать план, не вызывать API")
    parser.add_argument("--n-refs", type=int, default=DEFAULT_N_REF, help=f"Макс. reference-картинок (def {DEFAULT_N_REF})")
    parser.add_argument("--env", type=Path, help="Путь к .env файлу")
    parser.add_argument("--aspect", default=DEFAULT_ASPECT, help=f"Соотношение сторон (def {DEFAULT_ASPECT}, not used by current API)")
    args = parser.parse_args()

    # Валидация аргументов
    if args.frame and args.lesson is None:
        parser.error("Номер кадра требует указания урока: `python script.py 5 2.1`")
    if args.all and args.lesson is not None:
        parser.error("--all несовместим с явным номером урока")

    # Конфиг
    env = load_env(args.env)
    api_url = env.get("IMAGE_API_URL", DEFAULT_API_URL)
    model = env.get("IMAGE_MODEL", DEFAULT_MODEL)
    api_key = env.get(DEFAULT_API_KEY_ENV) or env.get("GOOGLE_API_KEY")
    api_format = env.get("IMAGE_API_FORMAT", DEFAULT_API_FORMAT)
    n_refs = args.n_refs
    # aspect = args.aspect  # not used by current API

    if not api_key and not args.dry_run:
        print(f"ERROR: API ключ не найден. Задайте {DEFAULT_API_KEY_ENV} или GOOGLE_API_KEY в .env или окружении.", file=sys.stderr)
        sys.exit(1)

    if api_format != "gemini" and not args.dry_run:
        print(f"ERROR: Поддерживается только IMAGE_API_FORMAT=gemini (текущий: {api_format})", file=sys.stderr)
        sys.exit(1)

    content_root = Path(__file__).parent.parent / "content"
    if not content_root.exists():
        print(f"ERROR: Папка content не найдена: {content_root}", file=sys.stderr)
        sys.exit(1)

    # Строим индекс готовых кадров
    ready_idx = ReadyIndex(content_root)

    # Собираем целевые кадры
    try:
        targets = collect_target_frames(args, content_root, ready_idx)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if not targets:
        print("Нечего генерировать.")
        return

    # Подтверждение
    if not print_confirmation(targets, args.dry_run):
        return
    if not args.yes and not args.dry_run:
        if not ask_confirm():
            print("Отмена.")
            return

    # Генерация
    for sem, lesson_dir, slide_num, panel, title, refs, style_suffix in targets:
        prompt = build_prompt(panel, style_suffix, panel.detect_characters(), refs)
        out_path = lesson_dir / f"slide-{slide_num:02d}" / panel.out_filename
        if out_path.exists():
            print(f"  ⊘ Уже существует: {out_path.relative_to(content_root)}")
            continue
        print(f"  → Генерация {panel.frame_id} → {out_path.relative_to(content_root)}...")
        try:
            img_bytes = call_gemini_api(prompt, refs, api_url, model, api_key)
            write_png(out_path, base64.b64encode(img_bytes).decode("ascii"))
            print(f"  ✓ Сохранено: {out_path.name} ({len(img_bytes)} байт)")
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")


if __name__ == "__main__":
    main()