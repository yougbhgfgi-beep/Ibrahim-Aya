# -*- coding: utf-8 -*-
"""
بيصنع صورة المعاينة (link preview) بتاعة اللينك:
assets/preview.jpg  1200x630  ← دي اللي بتظهر على واتساب/فيسبوك/تليجرام
assets/icon.png     أيقونة الموقع (favicon)

يشتغل مرة واحدة:  python assets/make_preview.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT = os.path.join(HERE, "..", "screenshot.png")          # صورة الموقع (اختياري)
PHOTO = os.path.join(HERE, "images", "photo1.jpeg")        # صورتها
OUT_PREVIEW = os.path.join(HERE, "preview.jpg")
OUT_ICON = os.path.join(HERE, "icon.png")

W, H = 1200, 630

# خطوط عربية من ويندوز
FONTS = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\tahomabd.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def font(size):
    for path in FONTS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.point((0, y), fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img.resize((w, h))


def center(draw, text, f, y, fill, w=W, stroke=0, stroke_fill=None):
    box = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
    x = (w - (box[2] - box[0])) / 2 - box[0]
    draw.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return box[3] - box[1]


def make_icon():
    size = 512
    ic = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=110, fill=(20, 12, 32, 255))
    d.ellipse([-70, 120, 260, 470], fill=(120, 20, 70, 150))
    d.ellipse([280, 180, 600, 480], fill=(40, 40, 120, 150))
    f = font(300)
    box = d.textbbox((0, 0), "❤", font=f)
    d.text(((size - (box[2] - box[0])) / 2 - box[0], (size - (box[3] - box[1])) / 2 - box[1] - 12),
           "❤", font=f, fill=(255, 90, 120, 255))
    ic.save(OUT_ICON)
    print("icon.png OK")


def make_preview():
    base = gradient(W, H, (23, 12, 36), (6, 8, 20))

    if os.path.exists(SHOT):
        try:
            shot = Image.open(SHOT).convert("RGB")
            shot = ImageOps.fit(shot, (W, H), method=Image.LANCZOS)
            shot = shot.filter(ImageFilter.GaussianBlur(14))
            base = Image.blend(base, shot, 0.35)
        except Exception:
            pass

    d = ImageDraw.Draw(base, "RGBA")

    # نجوم خفيفة
    import random
    random.seed(7)
    for _ in range(140):
        x, y = random.randint(0, W), random.randint(0, H)
        r = random.choice([1, 1, 1, 2])
        a = random.randint(60, 190)
        d.ellipse([x, y, x + r, y + r], fill=(255, 255, 255, a))

    # هالة وردية
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W / 2 - 300, -140, W / 2 + 300, 240], fill=(244, 63, 94, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    base = Image.alpha_composite(base.convert("RGBA"), glow)
    d = ImageDraw.Draw(base, "RGBA")

    # إطار
    d.rounded_rectangle([18, 18, W - 19, H - 19], radius=34, outline=(255, 255, 255, 60), width=3)

    # القلب
    fh = font(150)
    box = d.textbbox((0, 0), "❤", font=fh)
    d.text(((W - (box[2] - box[0])) / 2 - box[0], 34), "❤", font=fh, fill=(244, 63, 94, 255))

    f_names = font(112)
    center(d, "إبراهيم ❤ آية", f_names, 190, (255, 205, 220, 255), stroke=3, stroke_fill=(90, 10, 40, 255))

    f_line = font(46)
    center(d, "قصة حب محفورة في قلبي للأبد", f_line, 350, (235, 235, 245, 255))

    f_sub = font(32)
    center(d, "https://ibrahim-aya.vercel.app", f_sub, 450, (255, 150, 175, 255))

    f_small = font(27)
    center(d, "اضغطوا على اللينك وخشّوا بكلمة السر  ❤  LOVE", f_small, 530, (200, 200, 215, 255))

    base.convert("RGB").save(OUT_PREVIEW, "JPEG", quality=90, optimize=True)
    print("preview.jpg OK")


if __name__ == "__main__":
    make_icon()
    make_preview()
