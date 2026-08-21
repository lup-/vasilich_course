__doc__ = '''Из текста — картинка (диффузия). Технический ролик Manim (ManimCE) для занятия 06.

Одна мысль: картинка рождается из текста-промпта через диффузию. Ролик показывает, как учат
диффузионную модель и как она потом генерирует:
  - ПРЯМОЙ ПРОЦЕСС: чистая этикетка → гауссов шум (t = 1 … 1000), картинка становится неузнаваемой.
   - ОБРАТНЫЙ ПРОЦЕСС / ОБУЧЕНИЕ: U-Net учится предсказывать добавленный шум; текст-промпт подаётся
     в U-Net вместе с картинкой (блок промпта даёт стрелку на каждом шаге). Веса (коэффициенты U-Net)
     сначала нулевые — первая попытка разделить шум неверна, после перестройки весов разделение точное.
  - ГЕНЕРАЦИЯ: случайный шум → модель шаг за шагом вычитает «лишний» шум с учётом промпта → этикетка.
  - ДВА ВАРИАНТА: разный стартовый шум → разные этикетки.

Внешние ассеты (см. videos/README.md):
  - videos/этикетка порошка.png     (целевая этикетка «ПОРОШОК-МАКС»)
  - videos/этикетка порошка 2.png   (альтернативный вариант из другого шума)

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

class IzTekstaKartinka(Scene):
  def construct(self):
    pass
    self.forward_process()
    self.reverse_training()
    self.generation()
    self.two_variants()
    self.final_message()

  def forward_process(self):
    rgba = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка.png'))
    title = Text('ЭТАП 1: СОЗДАНИЕ ЗАШУМЛЕННЫХ КАРТИНОК',font='DejaVu Sans',font_size=30,color=PHOSPHOR,weight=BOLD)
    if title.width > 13.5:
      title.scale(13.5/title.width)

    title.to_edge(UP,buff=0.4)
    self.play(FadeIn(title),run_time=0.6)
    prompt = Text('ОПИСАНИЕ ИЗОБРАЖЕНИЯ: ЭТИКЕТКА СТИРАЛЬНОГО ПОРОШКА «МАКС»',font='DejaVu Sans',font_size=18,color=BEIGE,weight=BOLD)
    if prompt.width > 13.5:
      prompt.scale(13.5/prompt.width)

    prompt.next_to(title,DOWN,buff=0.2)
    self.play(FadeIn(prompt),run_time=0.4)
    stations = [0,250,500,750,1000]
    xs = [-5.6,-2.8,0,2.8,5.6]
    img_h = 2.3
    def make_label(val):
      num = DecimalNumber(val,num_decimal_places=0,font_size=20,color=PHOSPHOR)
      txt = label('шаг=',PHOSPHOR,20)
      return Group(txt,num).arrange(RIGHT,buff=0.1)

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
    labs = [lab0]
    for k in range(1,len(stations)):
      t1 = stations[k]
      t0 = stations[k-1]
      ex = xs[k]
      sx = xs[k-1]
      base = new_clean()
      over = new_noise()
      lab = make_label(t0)
      place(base,sx)
      place(over,sx)
      place_lab(lab,sx)
      over.set_opacity(t0/1000)

      self.play(FadeIn(base),FadeIn(over),FadeIn(lab),run_time=0.15)
      bases.append(base)
      overs.append(over)
      labs.append(lab)
      tracker = ValueTracker(0)
      def upd(mobj,tr=tracker,s=sx,e=ex,a=t0,b=t1,ba=base,ov=over,lb=lab):
        al = tr.get_value()
        x = s+(e-s)*al
        ba.move_to(x*RIGHT+y_c)
        ov.move_to(x*RIGHT+y_c)
        lb.move_to(x*RIGHT+y_c+DOWN*lab_dy)
        op = (a+al*(b-a))/1000
        ov.set_opacity(op)
        lb[1].set_value(a+al*(b-a))

      base.add_updater(upd)
      self.play(tracker.animate.set_value(1),run_time=1.6,rate_func=linear)
      base.clear_updaters()
      place(base,ex)
      place(over,ex)
      place_lab(lab,ex)
      over.set_opacity(t1/1000)
      lab[1].set_value(t1)

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

    title = label('ЭТАП 2: U-NET УЧИТСЯ ОЧИЩАТЬ КАРТИНКУ',PHOSPHOR,30)
    title.to_edge(UP,buff=0.45)
    self.play(FadeIn(title),run_time=0.6)
    weights = VGroup()
    grows = 11
    gcols = 9
    dot_r = 0.03
    max_r = 0.16
    rnd = random.Random(13)
    for r in range(grows):
      for c in range(gcols):
        circ = Circle(radius=dot_r,fill_color=DUST,fill_opacity=0.9,stroke_width=0)
        circ._tv = rnd.random()
        weights.add(circ)

    weights.arrange_in_grid(rows=grows,cols=gcols,buff=0.34)
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
      for _ in range(3):
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
      tr = VGroup(tr_box,tr_txt).move_to(ORIGIN)
      self.play(FadeIn(tr),run_time=0.25)
      def _blink(mob):
        if int(self.time*8)%2 == 0:
          mob.set_opacity(1)
        else:
          mob.set_opacity(0.25)

      tr.add_updater(_blink)
      self.play(prog.animate.set_value(min(1,prog.get_value()+train_amt)),run_time=1.7,rate_func=linear)
      tr.remove_updater(_blink)
      self.play(FadeOut(tr),run_time=0.2)
      self.play(FadeOut(carrow),run_time=0.2)
      self.play(FadeOut(wrong_pred),FadeOut(wrong_clean),FadeOut(chk),run_time=0.2)

      right_pred,right_clean,chk2 = run_pass(noise_rgba,op,None,0,'СОВПАЛИ',PHOSPHOR)
      objs += [right_pred,right_clean,chk2]

      if is_last:
        continue

      self.play(FadeOut(Group(*objs)),run_time=0.3)

    new_title = Text('ЭТАП 3: МОДЕЛЬ ГОТОВА, ГЕНЕРАЦИЯ',font='DejaVu Sans',font_size=30,color=PHOSPHOR,weight=BOLD)
    if new_title.width > 13.5:
      new_title.scale(13.5/new_title.width)

    new_title.to_edge(UP,buff=0.45)
    self.play(FadeOut(title),FadeIn(new_title),run_time=0.5)
    title = new_title
    self.play(FadeOut(Group(ref_m,ref_l,right_pred,right_clean,chk2)),run_time=0.3)
    rbox2 = RoundedRectangle(width=2.4,height=2.4,corner_radius=0.15,fill_opacity=0,stroke_color=PHOSPHOR,stroke_width=3)
    rbox2.move_to(CLEAN_POS)
    rcap2 = label('ЦЕЛЕВОЙ РЕЗУЛЬТАТ',BEIGE,16)
    rcap2.next_to(rbox2,DOWN,buff=0.15)
    self.play(Transform(rbox,rbox2),Transform(rcap,rcap2),run_time=0.5)
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
    weights.clear_updaters()
    self.play(FadeOut(Group(title,weights,unet_t,rbox,rcap,gclean,gnoise)),run_time=0.4)

  def generation(self):
    rgba = load_rgba(os.path.join(VIDEOS_DIR,'этикетка порошка.png'))
    h,w = rgba.shape[None:2]
    title = label('ГЕНЕРАЦИЯ ПОСЛЕ ОБУЧЕНИЯ',PHOSPHOR,30)
    title.to_edge(UP,buff=0.5)
    self.play(FadeIn(title),run_time=0.6)
    body = Text('Обученная модель использует промпт\nи картинку со случайным шумом.\nОна как скульптор — берёт случайный шум\nи отсекает всё лишнее.',font='DejaVu Sans',font_size=28,weight=BOLD,line_spacing=1.2,t2c={'Обученная модель использует промпт':BEIGE,'и картинку со случайным шумом.':BEIGE,'Она как скульптор — берёт случайный шум':PHOSPHOR,'и отсекает всё лишнее.':PHOSPHOR})
    body.move_to(ORIGIN)
    self.play(AddTextLetterByLetter(body,time_per_char=0.03),run_time=4.5)
    self.wait(3.0)
    self.play(FadeOut(body,shift=UP*0.05),run_time=0.4)
    center = ORIGIN+DOWN*0.4
    clean = rgba_to_mobject(rgba,height=4.2).move_to(center)
    noise = rgba_to_mobject(make_noise(h,w,seed=6),height=4.2).move_to(center)
    noise.set_opacity(1)
    self.play(FadeIn(clean),FadeIn(noise),run_time=0.5)
    step_lbl = label('ШАГ ОЧИСТКИ:',PHOSPHOR,22)
    step_num = DecimalNumber(0,num_decimal_places=0,font_size=22,color=PHOSPHOR)
    step_l = Group(step_lbl,step_num).arrange(RIGHT,buff=0.12)
    step_l.to_edge(DOWN,buff=0.5)
    self.play(FadeIn(step_l),run_time=0.3)
    steps = [0.78,0.52,0.28,0]
    for i,op in enumerate(steps,start=1):
      self.play(noise.animate.set_opacity(op),run_time=1,rate_func=linear)
      self.play(step_num.animate.set_value(i),run_time=0.1)

    note = label('ИЗ ХАОСА ПРОСТУПАЕТ ЭТИКЕТКА',BEIGE,24)
    note.next_to(clean,UP,buff=0.2)
    self.play(FadeIn(note),run_time=0.5)
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
    self.play(FadeIn(clean1),FadeIn(clean2),FadeIn(n1),FadeIn(n2),run_time=0.5)
    t1 = label('ШУМ A',DUST,22).next_to(n1,DOWN,buff=0.15)
    t2 = label('ШУМ B',DUST,22).next_to(n2,DOWN,buff=0.15)
    self.play(FadeIn(t1),FadeIn(t2),run_time=0.4)
    self.play(n1.animate.set_opacity(0),n2.animate.set_opacity(0),run_time=4.5,rate_func=linear)
    self.play(FadeOut(n1),FadeOut(n2),run_time=0.2)
    sub = label('ОДИН ПРОМПТ, РАЗНЫЙ СТАРТОВЫЙ ШУМ — КАРТИНКИ РАЗНЫЕ',BEIGE,22)
    sub.to_edge(DOWN,buff=0.5)
    self.play(FadeIn(sub),run_time=0.5)
    self.wait(2)
    self.play(FadeOut(Group(title,clean1,clean2,t1,t2,sub)),run_time=0.4)

  def final_message(self):
    main = label('ИЗ ТЕКСТА — КАРТИНКА',PHOSPHOR,44).move_to(UP*0.7)
    sub = label('ШУМ + ПРОМПТ → ДИФФУЗИЯ → КАРТИНКА. ОДИН ПРОМПТ — ПОХОЖИЕ, НО НЕ ОДИНАКОВЫЕ.',BEIGE,24).next_to(main,DOWN,buff=0.6)
    sub2 = label('МЕТА-ПРОМПТ ЗАДАЁТ ГРАНИЦЫ: ОПАСНОЕ НЕ РИСУЕМ',BEIGE,22)
    sub2.next_to(sub,DOWN,buff=0.4)
    self.play(FadeIn(main),run_time=1)
    self.play(FadeIn(sub),FadeIn(sub2),run_time=1)
    self.wait(4)
    self.play(FadeOut(main),FadeOut(sub),FadeOut(sub2),run_time=0.5)
