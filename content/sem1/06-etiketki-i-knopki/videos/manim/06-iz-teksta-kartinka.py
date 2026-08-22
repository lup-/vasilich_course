__doc__ = '''Из текста — картинка (диффузия). Технический ролик Manim (ManimCE) для занятия 06.

Одна мысль: картинка рождается из текста-промпта через диффузию. Ролик показывает, как учат
диффузионную модель и как она потом генерирует:
  - ПРЯМОЙ ПРОЦЕСС: чистая этикетка → гауссов шум (t = 1 … 1000), картинка становится неузнаваемой.
   - ОБРАТНЫЙ ПРОЦЕСС / ОБУЧЕНИЕ: U-Net учится предсказывать добавленный шум; текст-промпт подаётся
     в U-Net вместе с картинкой (блок промпта даёт стрелку на каждом шаге). Веса (коэффициенты U-Net)
     сначала нулевые — первая попытка разделить шум неверна, после перестройки весов разделение точное.
  - ГЕНЕРАЦИЯ: случайный шум → модель шаг за шагом вычитает «лишний» шум с учётом промпта → этикетка.
  - ДВА ВАРИАНТА: разный стартовый шум → разные этикетки.
  - ПОЧЕМУ ШУМ: у шума статистика одинакова (гауссов колокол), у картинок распределения разные —
    поэтому сеть ищет общие закономерности именно в шуме; растерянный смайлик у картинок.
  - ФИНАЛ: современные модели сочетают диффузионные элементы с трансформерами.

Внешние ассеты (см. videos/README.md):
  - videos/этикетка порошка.png     (целевая этикетка «ПОРОШОК-МАКС»)
  - videos/этикетка порошка 2.png   (альтернативный вариант из другого шума)
  - videos/этикетка глицерина.png, videos/этикетка мыла.png (таблица «почему шум», сцена why_noise)

Запуск:
    python -m manim render -ql -p --format mp4 --resolution 1920,1080 --fps 30 --seed 6         06-iz-teksta-kartinka.py IzTekstaKartinka
'''
import os
import random
import numpy as np
from PIL import Image
from manim import *
PHOSPHOR = '#B6FF3C'
SWAMP = '#4A5D23'
RUST = '#8C4A2F'
DUST = '#8A8A7A'
BEIGE = '#D8C9A3'
OLIVE = '#556B2F'
INK = '#111111'
WHITE = '#F2F2EA'
VIDEOS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def label(text,color=BEIGE,font_size=24,weight=BOLD):
  return Text(text,font='DejaVu Sans',font_size=font_size,color=color,weight=weight)

def rgba_to_mobject(rgba,height=3.6):
  im = Image.fromarray(rgba,mode='RGBA')
  m = ImageMobject(im)
  m.set_height(height)
  return m

def load_rgba(path):
  return np.array(Image.open(path).convert('RGBA'))

def make_pixelated(rgba,block):
  h,w = rgba.shape[:2]
  pil = Image.fromarray(rgba,mode='RGBA')
  small = pil.resize((max(1,w//block),max(1,h//block)),resample=Image.BILINEAR)
  return np.array(small.resize((w,h),resample=Image.NEAREST))

def make_noise(h,w,seed=6,alpha=255):
  rnd = random.Random(seed)
  arr = np.array([rnd.randint(0,255) for _ in range(w*h*3)],dtype=np.uint8).reshape(h,w,3)
  out = np.empty((h,w,4),dtype=np.uint8)
  out[:,:,:3] = arr
  out[:,:,3] = alpha
  return out

def make_block_noise(rgba,block,seed=6):
  h,w = rgba.shape[:2]
  sh = max(1,h//block)
  sw = max(1,w//block)
  rnd = random.Random(seed)
  small = np.array([rnd.randint(0,255) for _ in range(sw*sh*3)],dtype=np.uint8).reshape(sh,sw,3)
  up = Image.fromarray(small,mode='RGB').resize((w,h),resample=Image.NEAREST)
  out = np.empty((h,w,4),dtype=np.uint8)
  out[:,:,:3] = np.array(up)
  out[:,:,3] = 255
  return out

def diffusion_frame(rgba,t,bmax=30,seed=6):
  h,w = rgba.shape[:2]
  a = t/1000
  b = max(1,int(round(1+a*bmax-1)))
  pix = make_pixelated(rgba,b)
  nse = make_block_noise(rgba,b,seed=seed+int(t)//10)
  pix_op = min(1,a/0.25)
  nse_op = max(0,min(1,a-0.3/0.5))
  def blend(a1,a2,alpha):
    return a1.astype(np.float32)*1-alpha+a2.astype(np.float32)*alpha.astype(np.uint8)

  stage = blend(rgba,pix,pix_op)
  out = blend(stage,nse,nse_op) if nse_op > 0 else stage
  out = np.array(out)
  return out

class Num(VGroup):
  def __init__(self,v,fs,color):
    self.num_fs = fs
    self.num_color = color
    self.num_val = int(round(v))
    super().__init__(Text(str(self.num_val),font='DejaVu Sans',font_size=fs,color=color))

  def set_value(self,v):
    v = int(round(v))
    if v == self.num_val:
      return self
    self.num_val = v
    c = self.get_center()
    self.remove(self[0])
    self.add(Text(str(v),font='DejaVu Sans',font_size=self.num_fs,color=self.num_color))
    self.move_to(c)
    return self

class IzTekstaKartinka(Scene):
  def construct(self):
    pass
    self.forward_process()
    self.reverse_training()
    self.generation()
    self.two_variants()
    self.why_noise()
    self.hybrid_note()

  def stage_card(self,text,sub=None):
    rect = Rectangle(width=40,height=24,color=INK,fill_opacity=1,stroke_width=0)
    t = Text(text,font='DejaVu Sans',font_size=30,color=PHOSPHOR,weight=BOLD)
    if t.width > 13.5:
      t.scale(13.5/t.width)

    t.move_to(ORIGIN)
    self.add(rect)
    self.play(FadeIn(rect),run_time=0.3)
    self.play(AddTextLetterByLetter(t,time_per_char=0.04),run_time=2.2)
    sub_t = None
    if sub is not None:
      sub_t = Text(sub,font='DejaVu Sans',font_size=20,color=BEIGE,weight=BOLD)
      if sub_t.width > 12.5:
        sub_t.scale(12.5/sub_t.width)

      sub_t.next_to(t,DOWN,buff=0.4)
      self.play(FadeIn(sub_t),run_time=0.4)
    self.wait(1.2)
    if sub_t is not None:
      self.play(FadeOut(rect),FadeOut(sub_t),t.animate.to_edge(UP,buff=0.45),run_time=0.8)
    else:
      self.play(FadeOut(rect),t.animate.to_edge(UP,buff=0.45),run_time=0.8)
    return t

  def forward_process(self):
    rgba = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка.png'))
    title = self.stage_card('ЭТАП 1: СОЗДАНИЕ ЗАШУМЛЕННЫХ КАРТИНОК')
    prompt = Text('ОПИСАНИЕ ИЗОБРАЖЕНИЯ: ЭТИКЕТКА СТИРАЛЬНОГО ПОРОШКА «МАКС»',font='DejaVu Sans',font_size=18,color=BEIGE,weight=BOLD)
    if prompt.width > 13.5:
      prompt.scale(13.5/prompt.width)

    prompt.next_to(title,DOWN,buff=0.2)
    self.play(FadeIn(prompt),run_time=0.4)
    stations = [0,250,500,750,1000]
    xs = [-5.6,-2.8,0,2.8,5.6]
    img_h = 2.3
    def make_label(val):
      num = Num(val,20,PHOSPHOR)
      txt = label('шаг=',PHOSPHOR,20)
      return Group(txt,num).arrange(RIGHT,buff=0.28)

    y_c = DOWN*0.2
    lab_dy = img_h/2+0.35
    def place(im,x):
      im.move_to(x*RIGHT+y_c)

    def place_lab(lb,x):
      lb.move_to(x*RIGHT+y_c+DOWN*lab_dy)

    noise_rgba = make_block_noise(rgba,18,seed=6)
    new_clean = lambda : rgba_to_mobject(rgba,height=img_h)
    new_noise = lambda : rgba_to_mobject(noise_rgba,height=img_h)
    img0 = new_clean()
    lab0 = make_label(0)
    place(img0,xs[0])
    place_lab(lab0,xs[0])
    self.play(FadeIn(img0),FadeIn(lab0),run_time=0.4)
    bases = [img0]
    overs = [None]
    trav = lab0
    s0 = trav.copy()
    self.add(s0)
    labs = [s0]
    for k in range(1,len(stations)):
      t1 = stations[k]
      t0 = stations[k-1]
      ex = xs[k]
      sx = xs[k-1]
      base = new_clean()
      over = new_noise()
      place(base,sx)
      place(over,sx)
      over.set_opacity(t0/1000)

      self.play(FadeIn(base),FadeIn(over),run_time=0.15)
      for f in labs+[trav]:
        self.bring_to_front(f)
      bases.append(base)
      overs.append(over)
      tracker = ValueTracker(0)
      def upd(mobj,tr=tracker,s=sx,e=ex,a=t0,b=t1,ba=base,ov=over):
        al = tr.get_value()
        x = s+(e-s)*al
        ba.move_to(x*RIGHT+y_c)
        ov.move_to(x*RIGHT+y_c)
        op = (a+al*(b-a))/1000
        ov.set_opacity(op)

      def lab_upd(mobj,tr=tracker,s=sx,e=ex,a=t0,b=t1):
        al = tr.get_value()
        mobj[1].set_value(a+al*(b-a))
        mobj[1].next_to(mobj[0],RIGHT,buff=0.28)
        mobj.move_to((s+(e-s)*al)*RIGHT+y_c+DOWN*lab_dy)

      base.add_updater(upd)
      trav.add_updater(lab_upd)
      self.play(tracker.animate.set_value(1),run_time=1.6,rate_func=linear)
      base.clear_updaters()
      trav.clear_updaters()
      place(base,ex)
      place(over,ex)
      trav[1].set_value(t1)
      trav[1].next_to(trav[0],RIGHT,buff=0.28)
      place_lab(trav,ex)
      over.set_opacity(t1/1000)
      if k < len(stations)-1:
        stamp = trav.copy()
        self.add(stamp)
        labs.append(stamp)

    labs.append(trav)

    y_u = UP*1.3
    y_l = DOWN*2
    y_m = (y_u+y_l)/2
    rise = [bases[i].animate.move_to(xs[i]*RIGHT+y_u) for i in range(len(xs))]
    rise += [overs[i].animate.move_to(xs[i]*RIGHT+y_u) for i in range(1,len(xs))]
    rise += [labs[i].animate.move_to(xs[i]*RIGHT+y_m) for i in range(len(xs))]
    self.play(*rise)
    bottom_overs = []
    drop = []
    for i in range(1,len(xs)):
      b = new_noise()
      b.set_opacity(stations[i]/1000)
      b.move_to(xs[i]*RIGHT+y_u)
      self.add(b)
      bottom_overs.append(b)
      drop.append(b.animate.move_to(xs[i]*RIGHT+y_l))

    self.play(*drop)
    bottom_text = label('ЭТАЛОННЫЙ НАЛОЖЕННЫЙ ШУМ',PHOSPHOR,22)
    bottom_text.move_to(ORIGIN+DOWN*3.45)
    self.play(FadeIn(bottom_text),run_time=0.5)
    self.wait(1.6)
    everything = Group(*bases,*labs,*bottom_overs,*[o for o in overs if o is not None],bottom_text)
    self.play(FadeOut(everything),FadeOut(title),FadeOut(prompt),run_time=0.4)

  def reverse_training(self):
    def make_prompt(top,bot):
      t1 = Text(top,font='DejaVu Sans',font_size=13,color=INK,weight=BOLD)
      t2 = Text(bot,font='DejaVu Sans',font_size=13,color=INK,weight=BOLD)
      return VGroup(t1,t2).arrange(DOWN,buff=0.05)

    title = self.stage_card('ЭТАП 2: U-NET УЧИТСЯ ОЧИЩАТЬ КАРТИНКУ','U-NET - U-образная архитектура нейросети')
    weights = VGroup()
    grows = 11
    gcols = 9
    dot_r = 0.03
    max_r = 0.16
    rnd = random.Random(13)
    holes = []
    for r in range(grows):
      for c in range(gcols):
        circ = Circle(radius=dot_r,fill_color=DUST,fill_opacity=0.9,stroke_width=0)
        circ._tv = rnd.random()
        if c in (3,4,5) and r < grows-3:
          holes.append(circ)
        weights.add(circ)

    weights.arrange_in_grid(rows=grows,cols=gcols,buff=0.34)
    weights.remove(*holes)
    weights.move_to(ORIGIN)
    self.play(FadeIn(weights),run_time=0.6)
    unet_t = label('ВЕСА U-NET',PHOSPHOR,22)
    unet_t.next_to(weights,DOWN,buff=0.25)
    self.play(FadeIn(unet_t),run_time=0.6)
    dust_rgb = np.array([int(DUST[1:3],16),int(DUST[3:5],16),int(DUST[5:7],16)])/255
    phos_rgb = np.array([int(PHOSPHOR[1:3],16),int(PHOSPHOR[3:5],16),int(PHOSPHOR[5:7],16)])/255
    def _hex(rgb):
      r, g, b = (int(255*x) for x in np.clip(rgb,0,1))
      return f'#{r:02x}{g:02x}{b:02x}'

    def _set_circ(c,r):
      c.scale(2*r/c.width)

    prog = ValueTracker(0)
    def weights_upd(g):
      pv = prog.get_value()
      for c in g:
        a = c._tv*pv
        r = dot_r+(max_r-dot_r)*a
        _set_circ(c,r)
        c.set_fill(color=_hex(dust_rgb*(1-a)+phos_rgb*a),opacity=0.9)

    weights.add_updater(weights_upd)
    def mk_chk(text,color):
      box = RoundedRectangle(width=2.2,height=0.7,corner_radius=0.1,fill_color=color,fill_opacity=1,stroke_color=color,stroke_width=4)
      txt = label(text,INK,18)
      txt.move_to(box)
      return VGroup(box,txt)

    def blink(mobj):
      for _ in range(2):
        self.play(mobj.animate.set_opacity(0.25),run_time=0.13)
        self.play(mobj.animate.set_opacity(1),run_time=0.13)

    IN_POS = LEFT*4.8
    PROMPT_POS = LEFT*4.8+UP*1.7
    CLEAN_POS = RIGHT*3.4+UP*1.6
    SEPNOISE_POS = RIGHT*3.4+DOWN*1.7
    REF_POS = RIGHT*5.9+DOWN*1.7
    CHK_POS = RIGHT*4.6+DOWN*1.7
    stations = [250,500,750,1000]
    train_amt = 1/len(stations)
    sources = [('этикетка порошка','ЭТИКЕТКА ПОРОШКА','МАКС'),('этикетка глицерина','ЭТИКЕТКА ДЛЯ ГЛИЦЕРИНА','«ПАР»'),('этикетка мыла','ЭТИКЕТКА ХОЗЯЙСТВЕННОГО МЫЛА','«БАННОЕ»'),('этикетка порошка 2','ЭТИКЕТКА ПОРОШКА','МАКС')]
    rbox = RoundedRectangle(width=4.6,height=2.8,corner_radius=0.15,fill_opacity=0,stroke_color=PHOSPHOR,stroke_width=3)
    rbox.move_to(RIGHT*4.65+DOWN*1.7)
    rcap = label('ЦЕЛЕВОЙ РЕЗУЛЬТАТ',BEIGE,16)
    rcap.next_to(rbox,UP,buff=0.15)
    self.play(Create(rbox),FadeIn(rcap),run_time=0.5)
    for idx,t in enumerate(stations):
      op = t/1000
      png,ptop,pbot = sources[idx]

      is_last = idx == len(stations)-1
      rgba = load_rgba(os.path.join(VIDEOS_DIR,png+'.png'))
      noise_rgba = make_block_noise(rgba,18,seed=6)
      wrong_rgba = make_block_noise(rgba,18,seed=77)
      objs = []
      ref_m = rgba_to_mobject(noise_rgba,height=2).set_opacity(op)
      ref_m.move_to(REF_POS)
      ref_l = label('ЭТАЛОННЫЙ ШУМ',BEIGE,12)
      ref_l.next_to(ref_m,DOWN,buff=0.1)
      self.play(FadeIn(ref_m),FadeIn(ref_l),run_time=0.4)
      objs += [ref_m,ref_l]
      def run_pass(pred_rgba,pred_op,over_rgba,over_op,chk_text,chk_color):
        base_m = rgba_to_mobject(rgba,height=2)
        over_m = rgba_to_mobject(noise_rgba,height=2).set_opacity(op)
        in_img = Group(base_m,over_m).move_to(IN_POS)
        in_l = label(f'''ШАГ={t}''',BEIGE,14)
        in_l.next_to(in_img,DOWN,buff=0.1)
        ptxt = make_prompt(ptop,pbot)
        pbox = RoundedRectangle(width=ptxt.width+0.6,height=0.9,corner_radius=0.1,fill_color=BEIGE,fill_opacity=1,stroke_color=INK,stroke_width=4)
        pbox.move_to(PROMPT_POS)
        ptxt.move_to(pbox)

        self.play(FadeIn(in_img),FadeIn(in_l),FadeIn(pbox),FadeIn(ptxt),run_time=0.4)
        blink(Group(pbox,ptxt))
        self.play(in_img.animate.move_to(ORIGIN),in_l.animate.set_x(0),pbox.animate.move_to(ORIGIN+UP*1.5),ptxt.animate.move_to(ORIGIN+UP*1.5),run_time=0.8)
        self.remove(in_img,in_l)
        pred = rgba_to_mobject(pred_rgba,height=2).set_opacity(pred_op).move_to(ORIGIN)
        clean = rgba_to_mobject(rgba,height=2).move_to(ORIGIN)
        if over_rgba is not None:
          cr = rgba_to_mobject(over_rgba,height=2).set_opacity(over_op)
          clean = Group(clean,cr).move_to(ORIGIN)
        self.add(pred,clean)
        self.play(FadeOut(pbox),FadeOut(ptxt),pred.animate.move_to(SEPNOISE_POS),clean.animate.move_to(CLEAN_POS),run_time=0.8)
        chk = mk_chk(chk_text,chk_color).move_to(CHK_POS)
        self.play(FadeIn(chk),run_time=0.3)
        blink(chk)
        return pred,clean,chk

      wrong_pred,wrong_clean,chk = run_pass(wrong_rgba,min(1,op*0.8+0.15),wrong_rgba,0.35,'НЕ СОВПАЛО',RUST)
      carrow = CurvedArrow(CHK_POS+UP*0.35,ORIGIN,color=RUST,stroke_width=5,angle=PI/3)
      self.play(Create(carrow),run_time=0.5)
      tr_box = RoundedRectangle(width=3.6,height=0.9,corner_radius=0.1,fill_color=PHOSPHOR,fill_opacity=0.2,stroke_color=PHOSPHOR,stroke_width=3)
      tr_txt = label('ВЕСА\nПЕРЕСТРАИВАЮТСЯ',INK,18)
      tr_txt.move_to(tr_box)
      tr = VGroup(tr_box,tr_txt).next_to(unet_t,DOWN,buff=0.2)
      self.play(FadeIn(tr),run_time=0.25)
      def _blink(mob):
        if int(self.time*8)%2 == 0:
          mob.set_opacity(1)
        else:
          mob.set_opacity(0.25)

      tr.add_updater(_blink)
      def ring_rad(c,pv):
        return dot_r+(max_r-dot_r)*c._tv*pv+0.07

      changed = [c for c in weights if c._tv >= 0.5]
      rings = VGroup()
      for c in changed:
        rings.add(Circle(radius=ring_rad(c,prog.get_value()),color=YELLOW,stroke_width=2.5).move_to(c))

      def ring_upd(rg):
        pv = prog.get_value()
        for ring,c in zip(rg,changed):
          so = ring.get_stroke_opacity()
          ring.become(Circle(radius=ring_rad(c,pv),color=YELLOW,stroke_width=2.5))
          ring.move_to(c)
          ring.set_stroke(opacity=so)

      rings.add_updater(ring_upd)
      self.bring_to_front(carrow)
      carrow.add_updater(lambda m: m.shift(ORIGIN))
      self.play(FadeIn(rings),prog.animate.set_value(min(1,prog.get_value()+train_amt)),run_time=1.7,rate_func=linear)
      rings.clear_updaters()
      tr.remove_updater(_blink)
      carrow.clear_updaters()
      self.play(FadeOut(tr),FadeOut(rings),run_time=0.25)
      self.play(FadeOut(carrow),run_time=0.2)
      self.play(FadeOut(wrong_pred),FadeOut(wrong_clean),FadeOut(chk),run_time=0.2)

      right_pred,right_clean,chk2 = run_pass(noise_rgba,op,None,0,'СОВПАЛИ',PHOSPHOR)
      objs += [right_pred,right_clean,chk2]

      if is_last:
        continue

      self.play(FadeOut(Group(*objs)),run_time=0.3)

    weights.clear_updaters()
    self.play(FadeOut(Group(title,ref_m,ref_l,right_pred,right_clean,chk2)),run_time=0.4)
    title = self.stage_card('ЭТАП 3: МОДЕЛЬ ГОТОВА, ГЕНЕРАЦИЯ')
    self.wait(0.6)
    rbox_top = RoundedRectangle(width=2.4,height=2.4,corner_radius=0.15,fill_opacity=0,stroke_color=PHOSPHOR,stroke_width=3)
    rbox_top.move_to(CLEAN_POS)
    rcap_top = label('ЦЕЛЕВОЙ РЕЗУЛЬТАТ',BEIGE,16)
    rcap_top.next_to(rbox_top,DOWN,buff=0.15)
    self.play(Transform(rbox,rbox_top),Transform(rcap,rcap_top),run_time=0.8)
    weila = load_rgba(os.path.join(VIDEOS_DIR,'этикетка мыла.png'))
    gen_noise = make_block_noise(weila,18,seed=99)
    g_in = rgba_to_mobject(gen_noise,height=2).move_to(IN_POS)
    g_in_l = label('запрос',BEIGE,14)
    g_in_l.next_to(g_in,DOWN,buff=0.1)
    gptxt = make_prompt('ЭТИКЕТКА ХОЗЯЙСТВЕННОГО МЫЛА','«БАННОЕ»')
    gpbox = RoundedRectangle(width=gptxt.width+0.6,height=0.9,corner_radius=0.1,fill_color=BEIGE,fill_opacity=1,stroke_color=INK,stroke_width=4)
    gpbox.move_to(PROMPT_POS)
    gptxt.move_to(gpbox)
    self.play(FadeIn(g_in),FadeIn(g_in_l),FadeIn(gpbox),FadeIn(gptxt),run_time=0.4)
    self.play(g_in.animate.move_to(ORIGIN),g_in_l.animate.move_to(ORIGIN+DOWN*1),gpbox.animate.move_to(ORIGIN+UP*1.5),gptxt.animate.move_to(ORIGIN+UP*1.5),run_time=0.8)
    self.remove(g_in,g_in_l)
    gclean = rgba_to_mobject(weila,height=2).move_to(ORIGIN)
    gnoise = rgba_to_mobject(gen_noise,height=2).move_to(ORIGIN)
    self.add(gclean,gnoise)
    self.play(FadeOut(gpbox),FadeOut(gptxt),gclean.animate.move_to(CLEAN_POS),gnoise.animate.move_to(SEPNOISE_POS),run_time=0.8)
    self.wait(2)
    self.play(gclean.animate.scale(1.6).move_to(ORIGIN),FadeOut(Group(rbox,rcap,gnoise,weights,unet_t)),run_time=1.0)
    self.wait(1.5)
    self._stage3_leftover = Group(title,gclean)

  def generation(self):
    rgba = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка.png'))
    h,w = rgba.shape[None:2]
    lo = getattr(self,'_stage3_leftover',None)
    if lo is not None:
      self.play(FadeOut(lo),run_time=0.5)
    body = Text('Обученная модель использует промпт\nи картинку со случайным шумом.\nОна как скульптор — берёт случайный шум\nи отсекает всё лишнее.',font='DejaVu Sans',font_size=28,weight=BOLD,line_spacing=1.2,t2c={'Обученная модель использует промпт':BEIGE,'и картинку со случайным шумом.':BEIGE,'Она как скульптор — берёт случайный шум':PHOSPHOR,'и отсекает всё лишнее.':PHOSPHOR})
    body.move_to(ORIGIN)
    title = label('ГЕНЕРАЦИЯ ПОСЛЕ ОБУЧЕНИЯ',PHOSPHOR,30)
    title.next_to(body,UP,buff=0.8)
    self.play(FadeIn(title),run_time=0.6)
    self.play(AddTextLetterByLetter(body,time_per_char=0.03),run_time=4.5)
    self.wait(3.0)
    self.play(FadeOut(body,shift=UP*0.05),title.animate.to_edge(UP,buff=0.5),run_time=0.6)
    center = ORIGIN
    clean = rgba_to_mobject(rgba,height=4.2).move_to(center)
    noise = rgba_to_mobject(make_noise(h,w,seed=6),height=4.2).move_to(center)
    noise.set_opacity(1)
    note = label('ПРОМПТ: ЭТИКЕТКА СТИРАЛЬНОГО ПОРОШКА «МАКС»',BEIGE,24)
    note.next_to(clean,UP,buff=0.2)
    self.add(note,clean,noise)
    step_lbl = label('ШАГ ОЧИСТКИ:',PHOSPHOR,22)
    step_num = Num(0,22,PHOSPHOR).set_opacity(0)
    step_l = Group(step_lbl,step_num).arrange(RIGHT,buff=0.28)
    step_l.next_to(clean,DOWN,buff=0.25)
    self.play(FadeIn(step_l),run_time=0.3)
    prog = ValueTracker(0)
    def num_upd(g):
      v = int(round(prog.get_value()*1000))
      g[1].set_value(v)
      g[1].next_to(g[0],RIGHT,buff=0.28)
      g[1].set_opacity(1 if v>0 else 0)

    step_l.add_updater(num_upd)
    noise.add_updater(lambda m: m.set_opacity(1-prog.get_value()))
    self.play(prog.animate.set_value(1),run_time=4,rate_func=linear)
    step_l.clear_updaters()
    noise.clear_updaters()
    self.wait(1.2)
    self.play(FadeOut(Group(title,clean,noise,step_l,note)),run_time=0.4)

  def two_variants(self):
    rgba1 = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка.png'))
    rgba2 = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка 2.png'))
    h,w = rgba1.shape[None:2]
    title = label('РАЗНЫЙ ШУМ — РАЗНЫЙ РЕЗУЛЬТАТ',PHOSPHOR,30)
    title.to_edge(UP,buff=0.6)
    self.play(FadeIn(title),run_time=0.6)
    c1 = LEFT*3.4+DOWN*0.3
    c2 = RIGHT*3.4+DOWN*0.3
    clean1 = rgba_to_mobject(rgba1,height=4.2).move_to(c1)
    clean2 = rgba_to_mobject(rgba2,height=4.2).move_to(c2)
    n1 = rgba_to_mobject(make_noise(h,w,seed=11),height=4.2).move_to(c1)
    n2 = rgba_to_mobject(make_noise(h,w,seed=23),height=4.2).move_to(c2)
    self.add(clean1,clean2,n1,n2)
    t1 = label('ШУМ A',DUST,22).next_to(n1,DOWN,buff=0.15)
    t2 = label('ШУМ B',DUST,22).next_to(n2,DOWN,buff=0.15)
    self.play(FadeIn(t1),FadeIn(t2),run_time=0.4)
    self.play(n1.animate.set_opacity(0),n2.animate.set_opacity(0),run_time=4.5,rate_func=linear)
    self.play(FadeOut(n1),FadeOut(n2),run_time=0.2)
    sub = label('ОДИН ПРОМПТ, РАЗНЫЙ СТАРТОВЫЙ ШУМ — КАРТИНКИ РАЗНЫЕ',BEIGE,22)
    sub.next_to(title,DOWN,buff=0.3)
    self.play(FadeIn(sub),run_time=0.5)
    self.wait(2)
    self.play(FadeOut(Group(title,clean1,clean2,t1,t2,sub)),run_time=0.4)

  def why_noise(self):
    title = self.stage_card('ПОЧЕМУ СЕТЬ УЧИТСЯ НА ШУМЕ?')
    REDX = '#FF5252'
    cols = [-5.1,-1.7,1.7,5.1]
    rows = [1.2,-0.69,-2.58]

    def mini_plot(fn):
      ax = Line(ORIGIN,RIGHT*2.6,color=DUST,stroke_width=2)
      ay = Line(ORIGIN,UP*1.3,color=DUST,stroke_width=2)
      pts = []
      for i in range(61):
        x = -1.2+i*2.4/60
        X = 0.05+(x+1.2)/2.4*2.5
        pts.append(np.array([X,min(1.22,fn(x)),0]))
      cv = VMobject(color=PHOSPHOR,stroke_width=3)
      cv.set_points_as_corners(pts)
      return Group(ax,ay,cv)

    def gauss(mu,sig,amp):
      return lambda x: amp*np.exp(-((x-mu)/sig)**2)

    noise_seeds = [41,57,73]
    gaussians = [gauss(0.0,0.44,1.0),gauss(0.05,0.41,0.96),gauss(-0.05,0.47,1.02)]
    wild = [
      lambda x: 0.62*np.exp(-((x+0.55)/0.20)**2)+0.95*np.exp(-((x-0.5)/0.26)**2),
      lambda x: 0.72*np.exp(-(x/0.9)**4)+0.18*np.exp(-(x/2.2)**2),
      lambda x: np.exp(-((x+0.85)/0.14)**2)+0.15*np.exp(-((x+0.1)/0.7)**2)]
    label_files = ['этикетка порошка.png','этикетка глицерина.png','этикетка мыла.png']

    col_items = [[],[],[],[]]
    for r_i,y in enumerate(rows):
      n = rgba_to_mobject(make_noise(160,160,seed=noise_seeds[r_i]),height=1.5)
      n.move_to(cols[0]*RIGHT+y*UP)
      col_items[0].append(n)
      p = mini_plot(gaussians[r_i]).move_to(cols[1]*RIGHT+y*UP)
      col_items[1].append(p)
      im = load_rgba(os.path.join(VIDEOS_DIR,label_files[r_i]))
      lab = rgba_to_mobject(im,height=1.62)
      lab.move_to(cols[2]*RIGHT+y*UP)
      col_items[2].append(lab)
      wp = mini_plot(wild[r_i]).scale(0.92).move_to(cols[3]*RIGHT+y*UP)
      col_items[3].append(wp)

    flat = [m for c in col_items for m in c]
    self.play(LaggedStart(*[FadeIn(m) for m in flat],lag_ratio=0.06),run_time=2.2)
    self.wait(3)

    rect = Rectangle(width=40,height=24,color=INK,fill_opacity=1,stroke_width=0)
    card_lines = VGroup(
      label('У ШУМА СТАТИСТИКА ОДИНАКОВАЯ:',BEIGE,30),
      label('ЯРКОСТИ РАСПРЕДЕЛЕНЫ ПО',BEIGE,30),
      label('НОРМАЛЬНОМУ РАСПРЕДЕЛЕНИЮ.',BEIGE,30),
      label('У КАРТИНОК ХАРАКТЕРИСТИКИ РАЗНЫЕ —',BEIGE,30),
      label('ОБЩУЮ ЗАКОНОМЕРНОСТЬ ВЫДЕЛИТЬ ТРУДНЕЕ.',BEIGE,30)).arrange(DOWN,buff=0.32).move_to(ORIGIN)
    self.add(rect)
    self.play(FadeIn(rect),run_time=0.3)
    for ln in card_lines:
      self.play(AddTextLetterByLetter(ln,time_per_char=0.02),run_time=0.7)
    self.wait(1.4)
    self.play(FadeOut(rect),*[FadeOut(l) for l in card_lines],run_time=0.5)

    self.play(FadeOut(title),run_time=0.4)

    def smiley(cx,cy,fill,mouth_fn,qmark):
      c = cx*RIGHT+cy*UP
      f = Circle(radius=0.40,color=fill,fill_color=fill,fill_opacity=1,stroke_width=0).move_to(c)
      e1 = Dot(c+LEFT*0.14+UP*0.12,radius=0.038,color=INK)
      e2 = Dot(c+RIGHT*0.14+UP*0.12,radius=0.038,color=INK)
      mo = mouth_fn(c)
      q = label('?',REDX,22,weight=BOLD).next_to(f,UR,buff=0.02) if qmark else None
      return [f,e1,e2,mo]+([q] if q is not None else [])

    def wavy(c):
      pts = [c+LEFT*0.17+k*RIGHT*0.068-DOWN*0.055+UP*(0.042 if k%2==1 else 0.0) for k in range(6)]
      m = VMobject(color=INK,stroke_width=3.5)
      m.set_points_as_corners(pts[:-1])
      return m

    def grin(c):
      return Arc(radius=0.17,start_angle=5*PI/4,angle=PI/2,color=INK,stroke_width=3.5).move_to(c+DOWN*0.08)

    def badge(text,bg):
      t = label(text,INK,20)
      box = RoundedRectangle(corner_radius=0.08,width=t.width+0.34,height=t.height+0.24,color=bg,fill_color=bg,fill_opacity=1,stroke_width=0)
      t.move_to(box.get_center())
      return Group(box,t)

    red_frame = SurroundingRectangle(Group(*col_items[3]),color=REDX,buff=0.12,stroke_width=4)
    grn_frame = SurroundingRectangle(Group(*col_items[1]),color=PHOSPHOR,buff=0.12,stroke_width=4)
    cap_rz = label('РАЗНЫЕ!',REDX,26,BOLD)
    cap_rz.next_to(red_frame,UP,buff=0.12)
    bdg_r = badge('НЕ РАЗОБРАЛАСЬ!',REDX)
    bdg_r.next_to(cap_rz,UP,buff=0.10)
    face_c = bdg_r.get_top()+UP*(0.10+0.40)
    red_set = smiley(cols[3],face_c[1],REDX,wavy,True)

    cap_od = label('ОДИНАКОВЫЕ',PHOSPHOR,26,BOLD)
    cap_od.next_to(grn_frame,UP,buff=0.12)
    bdg_g = badge('РАЗОБРАЛАСЬ',PHOSPHOR)
    bdg_g.next_to(cap_od,UP,buff=0.10)
    gface_c = bdg_g.get_top()+UP*(0.10+0.40)
    grn_set = smiley(cols[1],gface_c[1],PHOSPHOR,grin,False)

    self.play(Create(red_frame),FadeIn(cap_rz),run_time=0.6)
    self.play(Create(red_set[0]),run_time=0.4)
    self.play(*[Create(m) if isinstance(m,VMobject) else FadeIn(m) for m in red_set[1:]],FadeIn(bdg_r),run_time=0.5)
    self.wait(0.7)
    self.play(Create(grn_frame),FadeIn(cap_od),run_time=0.6)
    self.play(Create(grn_set[0]),run_time=0.4)
    self.play(*[Create(m) if isinstance(m,VMobject) else FadeIn(m) for m in grn_set[1:]],FadeIn(bdg_g),run_time=0.5)
    self.wait(2)
    self.play(*[FadeOut(m) for m in flat+[red_frame,cap_rz,bdg_r]+red_set+[grn_frame,cap_od,bdg_g]+grn_set],run_time=0.5)

  def hybrid_note(self):
    lines = VGroup(
      label('СОВРЕМЕННЫЕ МОДЕЛИ СОЧЕТАЮТ',PHOSPHOR,30),
      label('ДИФФУЗИОННЫЕ ЭЛЕМЕНТЫ',PHOSPHOR,30),
      label('С ТРАНСФОРМЕРАМИ',PHOSPHOR,30)).arrange(DOWN,buff=0.35).move_to(ORIGIN)
    for ln in lines:
      self.play(AddTextLetterByLetter(ln,time_per_char=0.03),run_time=0.9)
    self.wait(2.2)
    self.play(FadeOut(lines),run_time=0.5)
