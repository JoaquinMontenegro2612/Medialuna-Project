#!/usr/bin/env python3
"""Recorta y ajusta la foto de perfil para LinkedIn / InfoJobs / JobToday.

Uso:  python3 tools/make_profile_photos.py <foto_original.jpg>
      (por defecto usa la elegida en SRC)

No cambia la cara: solo encuadra, corrige luz/color y añade un degradado
suave para que el fondo (azulejo) pese menos.
"""
import sys, os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# --- la foto elegida (ver README: nitidez 518, mejor expresión) ---
SRC = "foto/original/IMG-20260909-WA0008.jpg"

# --- encuadre: valores medidos sobre la composición 1200x1600 ---
# cabeza: arriba ~9 % de la altura, barbilla ~27 %, centro de la cara ~45,5 % del ancho
HEAD_TOP = 0.155
CHIN = 0.400
HEAD_CENTER_X = 0.455
SIDE_FACTOR = 1.80      # lado del cuadrado = 1.80 x altura de la cabeza (~44 % de la altura de la foto)
TOP_MARGIN = 0.09       # aire por encima de la cabeza, en fracción del cuadrado
EYE_LINE = 0.42         # la línea de los ojos debe quedar a ~42 % del encuadre


def crop_square(im, head_top_f=HEAD_TOP, cx_f=HEAD_CENTER_X, side_f=SIDE_FACTOR, top_margin=TOP_MARGIN):
    w, h = im.size
    head_top = head_top_f * h
    chin = CHIN * h
    head_h = chin - head_top
    side = int(head_h * side_f)
    side = min(side, h, w)
    x0 = int(cx_f * w - side / 2)
    y0 = int(head_top - top_margin * side)
    x0 = max(0, min(x0, w - side))
    y0 = max(0, min(y0, h - side))
    return im.crop((x0, y0, x0 + side, y0 + side))


def grade(im):
    """Luz, color y contraste: tono cálido neutro, sin efectos raros."""
    im = im.convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.045)
    im = ImageEnhance.Contrast(im).enhance(1.075)
    im = ImageEnhance.Color(im).enhance(0.94)      # azulejo menos saturado
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=58, threshold=3))
    return im


def vignette(im, strength=0.26, start=0.46):
    """Degradado radial: centra la atención en la cara y disimula el fondo."""
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2.0, h * 0.44
    d = np.sqrt(((xx - cx) / (w * 0.62)) ** 2 + ((yy - cy) / (h * 0.62)) ** 2)
    m = np.clip((d - start) / (1.0 - start), 0, 1)
    m = m * m * (3 - 2 * m)                         # smoothstep
    mask = 1.0 - strength * m
    arr = np.asarray(im).astype(np.float32) * mask[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def warm_shadow(im, amount=0.06):
    """Sombra ligeramente cálida en las esquinas, en vez de negro puro."""
    arr = np.asarray(im).astype(np.float32)
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w * 0.7)) ** 2 + ((yy - h * 0.44) / (h * 0.7)) ** 2)
    m = np.clip((d - 0.55) / 0.75, 0, 1)[..., None]
    tint = np.array([42.0, 34.0, 28.0])             # marrón cálido
    arr = arr * (1 - amount * m) + tint * (amount * m)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def make(src, out_dir="foto", sizes=(800, 400, 600)):
    im = Image.open(src)
    im = crop_square(im)
    im = im.resize((1600, 1600), Image.LANCZOS)
    im = grade(im)
    im = warm_shadow(im)
    im = vignette(im)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for s in sizes:
        p = os.path.join(out_dir, f"perfil-{s}.jpg")
        im.resize((s, s), Image.LANCZOS).save(p, quality=92, optimize=True)
        paths.append(p)
    return paths


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    for p in make(src):
        print("ok", p)
