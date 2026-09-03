"""بيولّد أصول ملف السطب من logo.png:
  installer/app.ico            أيقونة اللانشر (multi-size)
  installer/wizard.bmp         صورة اللوحة الجانبية في الـ wizard (164x314)
  installer/wizard-small.bmp   الصورة الصغيرة أعلى يمين الـ wizard (55x58)
  installer/version_info.txt   ريسورس نسخة الـ exe لويندوز

التشغيل:  python installer/make_assets.py [VERSION]
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "installer"
LOGO = ROOT / "logo.png"

BG_TOP = (18, 26, 38)       # كحلي غامق
BG_BOT = (10, 9, 6)         # أسود دافئ
ACCENT = (79, 143, 214)     # لون الثيم
TEXT = (241, 233, 214)
DIM = (150, 140, 120)

VERSION = sys.argv[1] if len(sys.argv) > 1 else "2.0.0"


def _load_logo():
    if LOGO.exists():
        return Image.open(LOGO).convert("RGBA")
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 240, 240), fill=ACCENT + (255,))
    return img


def _font(size, bold=True):
    for name in (("segoeuib.ttf" if bold else "segoeui.ttf"), "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def _vgrad(w, h, top, bot):
    base = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        f = y / max(1, h - 1)
        draw.line(
            [(0, y), (w, y)],
            fill=tuple(round(top[i] + (bot[i] - top[i]) * f) for i in range(3)),
        )
    return base


def make_ico():
    logo = _load_logo()
    side = max(logo.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    canvas = canvas.resize((256, 256), Image.LANCZOS)
    OUT.mkdir(exist_ok=True)
    canvas.save(OUT / "app.ico",
                sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("wrote", OUT / "app.ico")


def _glow(img, cx, cy, r, color):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 22
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(70 * (1 - i / steps) ** 1.6)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=color + (a,))
    img.alpha_composite(layer)


def make_wizard():
    w, h = 164, 314
    img = _vgrad(w, h, BG_TOP, BG_BOT).convert("RGBA")
    _glow(img, w // 2, 96, 92, ACCENT)

    logo = _load_logo().resize((84, 84), Image.LANCZOS)
    img.alpha_composite(logo, ((w - 84) // 2, 54))

    d = ImageDraw.Draw(img)
    f_title = _font(30)
    tw = d.textlength("AURA", font=f_title)
    d.text(((w - tw) / 2, 156), "AURA", font=f_title, fill=TEXT)
    f_sub = _font(11, bold=False)
    sw = d.textlength("Minecraft Launcher", font=f_sub)
    d.text(((w - sw) / 2, 192), "Minecraft Launcher", font=f_sub, fill=DIM)

    d.line([(28, 224), (w - 28, 224)], fill=ACCENT + (120,), width=1)
    vw = d.textlength(f"v{VERSION}", font=f_sub)
    d.text(((w - vw) / 2, 236), f"v{VERSION}", font=f_sub, fill=DIM)

    img.convert("RGB").save(OUT / "wizard.bmp")
    print("wrote", OUT / "wizard.bmp")


def make_wizard_small():
    s = 55, 58
    img = _vgrad(*s, BG_TOP, BG_BOT).convert("RGBA")
    _glow(img, s[0] // 2, s[1] // 2, 34, ACCENT)
    logo = _load_logo().resize((40, 40), Image.LANCZOS)
    img.alpha_composite(logo, ((s[0] - 40) // 2, (s[1] - 40) // 2))
    img.convert("RGB").save(OUT / "wizard-small.bmp")
    print("wrote", OUT / "wizard-small.bmp")


def make_version_info():
    parts = (VERSION.split(".") + ["0", "0", "0", "0"])[:4]
    v = ", ".join(str(int(p) if p.isdigit() else 0) for p in parts)
    txt = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({v}), prodvers=({v}),
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)
  ),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', 'Aura'),
      StringStruct('FileDescription', 'Aura Minecraft Launcher'),
      StringStruct('FileVersion', '{VERSION}'),
      StringStruct('InternalName', 'Aura'),
      StringStruct('OriginalFilename', 'Aura.exe'),
      StringStruct('ProductName', 'Aura'),
      StringStruct('ProductVersion', '{VERSION}'),
    ])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    (OUT / "version_info.txt").write_text(txt, encoding="utf-8")
    print("wrote", OUT / "version_info.txt")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    make_ico()
    make_wizard()
    make_wizard_small()
    make_version_info()
    print("done — version", VERSION)
