#!/usr/bin/env python3
"""Folleto A5 para bares de València — listo para imprimir.

Genera:
  bares/folleto-A5-con-sangre.pdf   2 páginas 154x216 mm (imprenta / copistería)
  bares/A4-2-por-hoja.pdf           A4 horizontal, 2 folletos por hoja, con marcas de corte (casa)
  bares/cartel-A4.pdf               cartel A4 para la barra o el escaparate

Estética buscada: dos tintas (negro + rojo teja) sobre papel crema, foto en semitono,
marcas hechas a mano (subrayado, ticks, precio "escrito"), sello girado y grano de papel.
Nada de degradados, sombras ni iconos: eso es lo que hace que algo parezca generado.
"""
import os, random
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode

# ---------------------------------------------------------------- ajustes
INK     = HexColor("#1A1612")
RED     = HexColor("#B5342A")
CREAM   = HexColor("#F7F2E8")
CREAM_D = HexColor("#EBE1CE")
DJ = "/usr/share/fonts/truetype/dejavu/"
F_BOLD, F_REG, F_SERIF, F_SERIFB, F_MONO = "DjB", "DjR", "DjS", "DjSB", "DjM"
RF = "DjRF"
WHATSAPP = "https://wa.me/34601580269?text=CARTA"
WEB      = "joaq-card-connect.lovable.app"

A5W, A5H = 148 * mm, 210 * mm
BLEED = 3 * mm


def register_fonts():
    pdfmetrics.registerFont(TTFont(F_BOLD, DJ + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont(F_REG, DJ + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont(F_SERIF, DJ + "DejaVuSerif.ttf"))
    pdfmetrics.registerFont(TTFont(F_SERIFB, DJ + "DejaVuSerif-Bold.ttf"))
    pdfmetrics.registerFont(TTFont(F_MONO, DJ + "DejaVuSansMono.ttf"))
    pdfmetrics.registerFont(TTFont(RF, DJ + "DejaVuSansMono-Bold.ttf"))


# ---------------------------------------------------------------- foto
def build_photo(src="foto/original/IMG-20260909-WA0008.jpg"):
    """Retrato 4:5 en dos tintas, con grano: parece impreso, no renderizado."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    head_h = 0.245 * h
    W = int(head_h * 1.55)
    H = int(W * 5 / 4)
    x0 = int(0.455 * w - W / 2)
    y0 = int(0.155 * h - 0.115 * H)
    crop = im.crop((x0, y0, x0 + W, y0 + H))

    g = ImageOps.grayscale(crop)
    g = ImageOps.autocontrast(g, cutoff=0.5)
    g = ImageEnhance.Contrast(g).enhance(2.05)
    g = ImageEnhance.Brightness(g).enhance(1.22)
    lv = 4
    g = Image.fromarray((np.round(np.asarray(g) / 255 * lv) / lv * 255).astype(np.uint8))
    out = ImageOps.colorize(g, black=INK.hexval().replace("0x", "#"),
                            white=CREAM.hexval().replace("0x", "#"))
    arr = np.asarray(out).astype(np.int16)
    rng = np.random.default_rng(11)
    arr = np.clip(arr + rng.normal(0, 7, arr.shape[:2])[:, :, None], 0, 255).astype(np.uint8)
    p = "bares/_foto-2tintas.jpg"
    Image.fromarray(arr).save(p, quality=95)
    return p


def build_grain(w=760, h=1075, seed=5):
    """Textura de papel: ruido muy suave en PNG con transparencia."""
    rng = np.random.default_rng(seed)
    n = rng.normal(128, 26, (h, w)).clip(0, 255).astype(np.uint8)
    alpha = np.full((h, w), 26, dtype=np.uint8)
    rgba = np.dstack([n, n, n, alpha])
    p = "bares/_grano.png"
    Image.fromarray(rgba, "RGBA").save(p)
    return p


def build_qr(url, path="bares/_qr.png"):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=12, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1A1612", back_color="#F7F2E8").convert("RGB")
    img.save(path)
    return path


# ---------------------------------------------------------------- mano
class Hand:
    """Pequeñas imperfecciones controladas: es lo que separa un folleto
    de una plantilla. Semilla fija para que el resultado sea reproducible."""

    def __init__(self, seed=3):
        self.r = random.Random(seed)

    def wobble_text(self, c, x, y, text, font, size, color, tilt=2.4, jitter=0.5,
                    track=0.0, scale=1.0):
        """Texto 'escrito': cada letra con una rotación y un desvío mínimo."""
        c.saveState()
        c.setFillColor(color)
        cx = x
        for ch in text:
            wch = pdfmetrics.stringWidth(ch, font, size) + track
            c.saveState()
            c.translate(cx, y + self.r.uniform(-jitter, jitter))
            c.rotate(self.r.uniform(-tilt, tilt))
            c.scale(scale, 1)
            c.setFont(font, size)
            c.drawString(0, 0, ch)
            c.restoreState()
            cx += wch
        c.restoreState()
        return cx

    def underline(self, c, x0, x1, y, color, width=1.7, sag=0.9):
        """Subrayado a rotulador: no es una línea recta y se pasa del final."""
        p = c.beginPath()
        p.moveTo(x0, y + 0.4)
        mid = (x0 + x1) / 2
        p.curveTo(mid - (x1 - x0) * .18, y + sag, mid + (x1 - x0) * .18, y - sag * .7,
                  x1 + 1.4, y + self.r.uniform(-.5, .5))
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.setLineCap(1)
        c.drawPath(p, stroke=1, fill=0)
        # segunda pasada más fina: el rotulador repasa
        p2 = c.beginPath()
        p2.moveTo(x0 + 0.8, y - 0.7)
        p2.curveTo(mid, y - 1.2, mid + 3, y + 0.3, x1 - 0.6, y - 0.3)
        c.setLineWidth(width * 0.55)
        c.drawPath(p2, stroke=1, fill=0)

    def tick(self, c, x, y, size, color, width=1.5):
        """Check dibujado a mano alzada."""
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.setLineCap(1)
        p = c.beginPath()
        p.moveTo(x, y + size * 0.42)
        p.curveTo(x + size * 0.18, y + size * 0.28, x + size * 0.30, y + size * 0.02,
                  x + size * 0.46, y - size * 0.48)
        p.curveTo(x + size * 0.78, y + size * 0.12, x + size * 1.05, y + size * 0.55,
                  x + size * 1.22, y + size * 0.80)
        c.drawPath(p, stroke=1, fill=0)

    def crooked_box(self, c, x, y, w, h, fill=None, stroke=None, lw=1.2, wob=0.6):
        """Rectángulo con las esquinas un poco torcidas."""
        p = c.beginPath()
        pts = [(x + self.r.uniform(-wob, wob), y + self.r.uniform(-wob, wob)),
               (x + w + self.r.uniform(-wob, wob), y + self.r.uniform(-wob, wob)),
               (x + w + self.r.uniform(-wob, wob), y + h + self.r.uniform(-wob, wob)),
               (x + self.r.uniform(-wob, wob), y + h + self.r.uniform(-wob, wob))]
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close()
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        c.drawPath(p, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)

    def arrow(self, c, x0, y0, x1, y1, color, lw=1.6):
        """Flecha curvada a mano alzada con punta de dos trazos."""
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        c.setLineCap(1)
        p = c.beginPath()
        p.moveTo(x0, y0)
        p.curveTo(x0 + (x1 - x0) * .35, y0 + (y1 - y0) * .75,
                  x0 + (x1 - x0) * .70, y1 + (y1 - y0) * .22, x1, y1)
        c.drawPath(p, stroke=1, fill=0)
        import math
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (-0.55, 0.45):
            p2 = c.beginPath()
            p2.moveTo(x1, y1)
            p2.lineTo(x1 - 2.4 * math.cos(ang + d), y1 - 2.4 * math.sin(ang + d))
            c.drawPath(p2, stroke=1, fill=0)


# ---------------------------------------------------------------- piezas
def para(c, x, y, text, font, size, color, width, leading=None, tracking=0.0,
         align="left", upper=False):
    """Texto con salto de línea manual por palabras. Devuelve la Y final."""
    leading = leading or size * 1.32
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        f = font
        if tracking:
            tw = pdfmetrics.stringWidth(test, f, size) + tracking * (len(test) - 1)
        else:
            tw = pdfmetrics.stringWidth(test, f, size)
        if tw > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)

    c.setFont(font, size)
    c.setFillColor(color)
    for i, ln in enumerate(lines):
        s = ln.upper() if upper else ln
        if tracking:
            cx = x
            if align == "center":
                tw = pdfmetrics.stringWidth(s, font, size) + tracking * (len(s) - 1)
                cx = x + (width - tw) / 2
            for ch in s:
                c.drawString(cx, y - i * leading, ch)
                cx += pdfmetrics.stringWidth(ch, font, size) + tracking
        else:
            c.drawString(x, y - i * leading, s) if align == "left" else \
                c.drawCentredString(x + width / 2, y - i * leading, s)
    return y - (len(lines) - 1) * leading


def label(c, x, y, text, color=RED, size=6.6, tracking=1.9):
    c.setFillColor(color)
    c.setFont(F_BOLD, size)
    cx = x
    for ch in text.upper():
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, F_BOLD, size) + tracking


def photo(c, path, x, y, w, h):
    c.drawImage(path, x, y, w, h, mask=None)
    c.setStrokeColor(RED)
    c.setLineWidth(0.9)
    c.rect(x, y, w, h, stroke=1, fill=0)


def grain(c, path, w, h):
    c.saveState()
    c.setFillAlpha(0.30)
    c.drawImage(path, 0, 0, w, h, mask="auto")
    c.restoreState()


def qr_block(c, path, x, y, size, caption=None):
    c.drawImage(path, x, y, size, size)
    if caption:
        c.setFillColor(INK)
        c.setFont(F_MONO, 4.9)
        c.drawString(x - 1, y - 4.2, caption)


# ---------------------------------------------------------------- anverso
def front(c, Hnd, photo_path, grain_path, qr_path):
    W, H = A5W, A5H
    M = 13 * mm

    c.setFillColor(CREAM)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)

    # --- cabecera
    label(c, M, 197 * mm, "Bares · cafeterías · terrazas · València", RED)
    c.setFillColor(INK)
    c.setFont(F_MONO, 5.6)
    c.drawRightString(W - M, 197 * mm, "noviembre 2026")

    # --- titular
    c.saveState()
    c.translate(M, 185 * mm)
    c.scale(0.93, 1)
    c.setFillColor(INK)
    c.setFont(F_BOLD, 24)
    c.drawString(0, 0, "TU CARTA")
    c.drawString(0, -8.6 * mm, "EN UN QR")
    c.setFillColor(RED)
    c.drawString(0, -17.2 * mm, "QUE CAMBIAS TÚ.")
    c.restoreState()

    Hnd.underline(c, M, M + 79 * mm, 164.6 * mm, RED, width=2.0)

    # --- entradilla (cursiva por inclinación)
    sub_y = 156.5 * mm
    c.saveState()
    c.translate(M, sub_y)
    c.transform(1, 0, -0.16, 1, 0, 0)
    rel = para(c, 0, 0, "Cada vez que cambias un precio, ¿reimprimes la carta entera? "
                        "Se acabó: la editas desde el móvil en dos minutos.",
               F_SERIF, 8.5, INK, 106 * mm, leading=11.0)
    c.restoreState()

    # --- tres puntos con tick
    items = [
        "Cambias precios, platos o fotos desde el móvil. Sin llamar a nadie.",
        "Sales en Google con fotos, horarios y cómo llegar, cuando te buscan en el barrio.",
        "Contestación automática en WhatsApp, también un viernes a las 22:30.",
    ]
    yy = 141 * mm
    for txt in items:
        Hnd.tick(c, M, yy - 0.5 * mm, 3.4 * mm, RED, width=1.3)
        yy = para(c, M + 5.8 * mm, yy, txt, F_REG, 7.8, INK, 98 * mm, leading=9.9) - 4.8 * mm

    # --- foto
    ph_w, ph_h = 46 * mm, 57.5 * mm
    px, py = M, 56 * mm
    photo(c, photo_path, px, py, ph_w, ph_h)

    # --- ficha de precio girada
    c.saveState()
    c.translate(84 * mm, 100 * mm)
    c.rotate(-3.2)
    c.setFillColor(CREAM)
    c.setStrokeColor(INK)
    c.setLineWidth(1.0)
    c.rect(-23 * mm, -12 * mm, 46 * mm, 24 * mm, stroke=1, fill=1)
    c.setFillColor(INK)
    c.setFont(F_MONO, 4.9)
    c.drawCentredString(0, 7.6 * mm, "TODO INCLUIDO")
    # precio anterior tachado
    c.setFont(F_MONO, 7.4)
    c.setFillColor(HexColor("#6B6259"))
    c.drawCentredString(0, 2.2 * mm, "490 €")
    c.setStrokeColor(RED)
    c.setLineWidth(1.2)
    c.setLineCap(1)
    c.line(-7.0 * mm, 3.6 * mm, 7.0 * mm, 2.6 * mm)
    c.setLineWidth(0.6)
    c.line(-6.4 * mm, 2.5 * mm, 6.6 * mm, 3.3 * mm)
    Hnd.wobble_text(c, -11 * mm, -9.4 * mm, "290 €", F_BOLD, 18, RED, tilt=2.0, jitter=0.4)
    c.restoreState()

    c.setFillColor(INK)
    c.setFont(F_MONO, 4.8)
    c.drawString(60 * mm, 78 * mm, "para los 2 primeros bares de València,")
    c.drawString(60 * mm, 74.6 * mm, "a cambio de una reseña y una foto.")

    # --- CTA
    c.setFillColor(INK)
    c.setFont(F_BOLD, 8.4)
    c.drawString(60 * mm, 66 * mm, "Mándame «CARTA» por WhatsApp")
    c.drawString(60 * mm, 61.6 * mm, "y en 24 h te enseño la tuya.")
    c.setFillColor(RED)
    c.setFont(RF, 13.4)
    c.drawString(60 * mm, 52 * mm, "601 580 269")
    c.setFillColor(INK)
    c.setFont(F_MONO, 4.9)
    c.drawString(60 * mm, 47.5 * mm, "contesto yo, no un bot")

    # --- sello pegado sobre la foto
    c.saveState()
    c.translate(35 * mm, 61 * mm)
    c.rotate(-7)
    c.setFillColor(CREAM)
    c.setStrokeColor(RED)
    c.setLineWidth(0.9)
    c.roundRect(-19 * mm, -4.6 * mm, 38 * mm, 9.2 * mm, 1.6 * mm, stroke=1, fill=1)
    c.setFillColor(RED)
    c.setFont(F_BOLD, 5.4)
    c.drawCentredString(0, -1.2 * mm, "HECHO A MANO EN PATRAIX")
    c.setFont(F_MONO, 4.4)
    c.drawCentredString(0, -3.6 * mm, "sin plantillas · sin humo")
    c.restoreState()

    # --- pie
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.line(M, 33 * mm, W - M, 33 * mm)

    c.setFillColor(INK)
    c.setFont(F_MONO, 5.1)
    c.drawString(M, 27.6 * mm, "5 años detrás de la barra (Hotel Arts BCN, mi propia cafetería)")
    c.drawString(M, 23.6 * mm, "y 2 años montando software para empresas. Patraix, València.")
    c.setFillColor(RED)
    c.setFont(F_MONO, 5.0)
    c.drawString(M, 18.6 * mm, WEB)

    c.setFillColor(INK)
    c.setFont(F_MONO, 5.0)
    c.drawString(M, 14.2 * mm, "@joaquinmontenegro2026 · te contesto el mismo día")
    qr_block(c, qr_path, W - M - 18 * mm, 12.5 * mm, 18 * mm, None)

    grain(c, grain_path, W, H)


def back(c, Hnd, photo_path, grain_path, qr_path):
    W, H = A5W, A5H
    M = 13 * mm

    c.setFillColor(CREAM)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)

    label(c, M, 197 * mm, "Lo que llevas, sin letra pequeña", RED)

    c.saveState()
    c.translate(M, 185.5 * mm)
    c.scale(0.93, 1)
    c.setFillColor(INK)
    c.setFont(F_BOLD, 16)
    c.drawString(0, 0, "TRES FORMAS.")
    c.setFillColor(RED)
    c.drawString(0, -7.4 * mm, "ELIGE LA TUYA.")
    c.restoreState()

    # --- oferta de arranque (arriba, es el gancho)
    Hnd.crooked_box(c, M - 1 * mm, 159 * mm, 124 * mm, 14 * mm,
                    fill=CREAM_D, stroke=None, wob=0.6)
    c.setFillColor(RED)
    c.setFont(F_BOLD, 5.6)
    c.drawString(M + 2.4 * mm, 168.4 * mm, "OFERTA DE ARRANQUE")
    c.setFillColor(INK)
    c.setFont(F_BOLD, 7.4)
    c.drawString(M + 40 * mm, 168.4 * mm, "los 2 primeros bares: el Bar conectado por 290 €")
    c.setFont(F_REG, 6.6)
    c.drawString(M + 2.4 * mm, 163.6 * mm, "A cambio de una reseña en Google y una foto del local. Después, precio de tarifa.")

    # --- packs
    packs = [
        ("CARTA QR", "290 €", "Tu carta digital con QR para las mesas, y la editas tú cuando quieras.",
         "Incluye diseño, alojamiento y el QR impreso.", False),
        ("BAR CONECTADO", "490 €", "Carta QR + ficha de Google + WhatsApp Business + 1 mes de cambios.",
         "Lo que coge casi todo el mundo.", True),
        ("RESERVAS Y AVISOS", "+190 €", "Reservas por WhatsApp con respuesta automática.",
         "Aviso cuando la mesa está lista.", False),
    ]
    y = 150 * mm
    for name, price, d1, d2, star in packs:
        if star:
            Hnd.crooked_box(c, M - 2.6 * mm, y - 15.4 * mm, 124 * mm, 19 * mm,
                            fill=CREAM_D, stroke=None, wob=0.5)
        c.setFillColor(INK)
        c.setFont(F_BOLD, 8.4)
        c.drawString(M, y, name)
        wname = pdfmetrics.stringWidth(name, F_BOLD, 8.4)
        if star:
            c.setFillColor(RED)
            c.setFont(F_BOLD, 5.0)
            c.drawString(M + wname + 3 * mm, y + 0.4 * mm, "LA MÁS PEDIDA")
        c.setFillColor(INK)
        c.setFont(RF, 8.4)
        c.drawRightString(W - M, y, price)
        c.setFont(F_REG, 7.0)
        c.drawString(M, y - 4.4 * mm, d1)
        c.drawString(M, y - 8.2 * mm, d2)
        y -= 21.0 * mm if star else 18.6 * mm

    # --- mantenimiento (una línea, sin raya)
    c.setFillColor(INK)
    c.setFont(F_BOLD, 7.0)
    c.drawString(M, 89 * mm, "Mantenimiento 39 €/mes")
    wm = pdfmetrics.stringWidth("Mantenimiento 39 €/mes", F_BOLD, 7.0)
    c.setFont(F_REG, 7.0)
    c.drawString(M + wm + 3 * mm, 89 * mm, "si quieres que lo lleve yo. Si no, es tuyo y lo llevas tú.")

    # --- preguntas
    label(c, M, 80 * mm, "Lo que me preguntan siempre", INK, size=6.2, tracking=1.5)
    faqs = [
        ("¿Cuánto tarda?", "Entre 5 y 7 días desde que me das la carta y las fotos. Te doy fecha al aceptar."),
        ("¿Pago todo antes?", "No. La mitad al empezar y la otra mitad al entregar."),
        ("¿Y si no me gusta?", "Dos rondas de cambios incluidas. Si algo no funciona, lo arreglo."),
    ]
    yy = 73 * mm
    for q, a in faqs:
        c.setFillColor(INK)
        c.setFont(F_BOLD, 7.2)
        c.drawString(M, yy, q)
        para(c, M, yy - 4.0 * mm, a, F_REG, 7.0, INK, 112 * mm, leading=9.0)
        yy -= 10.5 * mm

    # --- contacto
    cy = 40 * mm
    c.setStrokeColor(INK)
    c.setLineWidth(0.7)
    c.line(M, cy, W - M, cy)
    c.setFillColor(INK)
    c.setFont(RF, 12)
    c.drawString(M, cy - 6.6 * mm, "601 580 269")
    c.setFont(F_MONO, 4.9)
    c.drawString(M, cy - 11.0 * mm, "WhatsApp · llamada · joaquinmontenegro2612@gmail.com")
    c.setFillColor(RED)
    c.setFont(F_MONO, 4.8)
    c.drawString(M, cy - 15.0 * mm, WEB + "  ·  @joaquinmontenegro2026")
    c.setFillColor(INK)
    c.setFont(F_MONO, 4.6)
    c.drawString(M, cy - 18.6 * mm, "Joaquín Montenegro · Patraix, València")
    qr_block(c, qr_path, W - M - 16 * mm, cy - 19.5 * mm, 16 * mm, None)

    # cierre, escrito a mano: el detalle que hace que esto no parezca una plantilla
    Hnd.wobble_text(c, M, 13 * mm,
                    "Si has llegado hasta aquí leyendo, ya sé que te importa cómo va tu bar.",
                    F_MONO, 5.2, HexColor("#4A4239"), tilt=1.1, jitter=0.3)

    grain(c, grain_path, W, H)



# ---------------------------------------------------------------- cartel A4
def poster(c, Hnd, photo_path, grain_path, qr_path):
    W, H = 210 * mm, 297 * mm
    M = 17 * mm

    c.setFillColor(CREAM)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)

    label(c, M, 278 * mm, "Bares · cafeterías · terrazas · València", RED, size=8.2, tracking=2.4)
    c.setFillColor(INK)
    c.setFont(F_MONO, 6.6)
    c.drawRightString(W - M, 278 * mm, "noviembre 2026")

    # titular
    c.saveState()
    c.translate(M, 262 * mm)
    c.scale(0.92, 1)
    c.setFillColor(INK)
    c.setFont(F_BOLD, 39)
    c.drawString(0, 0, "TU CARTA,")
    c.drawString(0, -15.6 * mm, "EN UN QR")
    c.setFillColor(RED)
    c.drawString(0, -31.2 * mm, "QUE CAMBIAS TÚ.")
    c.restoreState()

    Hnd.underline(c, M, M + 143 * mm, 224 * mm, RED, width=2.6)

    c.saveState()
    c.translate(M, 211 * mm)
    c.transform(1, 0, -0.16, 1, 0, 0)
    para(c, 0, 0, "Cada vez que cambias un precio, ¿reimprimes la carta entera? "
                  "Se acabó: la editas desde el móvil en dos minutos.",
         F_SERIF, 11.4, INK, 150 * mm, leading=15.0)
    c.restoreState()

    # columna izquierda: tres puntos
    items = [
        "Cambias precios, platos o fotos desde el móvil. Sin llamar a nadie.",
        "Sales en Google con fotos, horarios y cómo llegar, cuando te buscan en el barrio.",
        "Contestación automática en WhatsApp, también un viernes a las 22:30.",
    ]
    yy = 180 * mm
    for txt in items:
        Hnd.tick(c, M, yy - 0.6 * mm, 4.6 * mm, RED, width=1.7)
        yy = para(c, M + 8 * mm, yy, txt, F_REG, 10.4, INK, 88 * mm, leading=13.2) - 7 * mm

    # garantía: llena el hueco con algo que importa
    gy = 136 * mm
    c.setStrokeColor(INK)
    c.setLineWidth(0.6)
    c.line(M, gy, M + 96 * mm, gy)
    c.setFillColor(INK)
    c.setFont(F_BOLD, 10.2)
    c.drawString(M, gy - 8 * mm, "No hace falta que sepas nada de tecnología.")
    para(c, M, gy - 14 * mm, "Te lo dejo funcionando y te enseño a cambiarlo "
                             "tú mismo en diez minutos.", F_SERIF, 9.6, INK, 96 * mm, leading=12.4)

    # foto
    ph_w, ph_h = 68 * mm, 85 * mm
    photo(c, photo_path, W - M - ph_w, 100 * mm, ph_w, ph_h)

    # sello sobre la foto
    c.saveState()
    c.translate(W - M - ph_w / 2, 96 * mm)
    c.rotate(-6)
    c.setFillColor(CREAM)
    c.setStrokeColor(RED)
    c.setLineWidth(1.1)
    c.roundRect(-28 * mm, -6 * mm, 56 * mm, 12 * mm, 2 * mm, stroke=1, fill=1)
    c.setFillColor(RED)
    c.setFont(F_BOLD, 7.4)
    c.drawCentredString(0, -1.6 * mm, "HECHO A MANO EN PATRAIX")
    c.setFont(F_MONO, 5.6)
    c.drawCentredString(0, -4.8 * mm, "sin plantillas · sin humo")
    c.restoreState()

    # banda roja de precio y contacto
    band_y, band_h = 44 * mm, 44 * mm
    c.setFillColor(RED)
    c.rect(-BLEED, band_y, W + 2 * BLEED, band_h, stroke=0, fill=1)

    c.setFillColor(CREAM)
    c.setFont(F_MONO, 6.4)
    c.drawString(M, band_y + 33 * mm, "TODO INCLUIDO · ALTA, DISEÑO Y DOMINIO")
    c.setFont(F_MONO, 7.2)
    c.drawString(M, band_y + 27.5 * mm, "antes 490 €")
    _w = pdfmetrics.stringWidth("antes 490 €", F_MONO, 7.2)
    c.setStrokeColor(CREAM)
    c.setLineWidth(0.9)
    c.line(M - 0.4 * mm, band_y + 28.7 * mm, M + _w + 0.6 * mm, band_y + 27.9 * mm)
    Hnd.wobble_text(c, M - 1 * mm, band_y + 13 * mm, "290 €", F_BOLD, 30, CREAM,
                    tilt=1.6, jitter=0.4)
    c.setFont(F_MONO, 6.2)
    c.drawString(M, band_y + 6 * mm, "para los 2 primeros bares")

    # CTA dentro de la banda
    cx = 112 * mm
    c.setFillColor(CREAM)
    c.setFont(F_BOLD, 11.6)
    c.drawString(cx, band_y + 31 * mm, "Mándame «CARTA»")
    c.drawString(cx, band_y + 25 * mm, "por WhatsApp y en")
    c.drawString(cx, band_y + 19 * mm, "24 h te enseño la tuya.")
    c.setFont(RF, 17)
    c.drawString(cx, band_y + 9 * mm, "601 580 269")
    c.setFont(F_MONO, 5.8)
    c.drawString(cx, band_y + 4.4 * mm, "contesto yo, no un bot")

    # pie
    c.setFillColor(INK)
    c.setFont(F_MONO, 6.4)
    c.drawString(M, 32 * mm, "5 años detrás de la barra (Hotel Arts BCN, mi propia cafetería)")
    c.drawString(M, 26.5 * mm, "y 2 años montando software para empresas. Joaquín Montenegro · Patraix, València")
    c.setFillColor(RED)
    c.drawString(M, 20.5 * mm, WEB + "  ·  @joaquinmontenegro2026  ·  joaquinmontenegro2612@gmail.com")
    qr_block(c, qr_path, W - M - 22 * mm, 16 * mm, 22 * mm, None)

    grain(c, grain_path, W, H)


# ---------------------------------------------------------------- salidas
def build():
    os.makedirs("bares", exist_ok=True)
    register_fonts()
    photo_path = build_photo()
    grain_path = build_grain()
    qr_path = build_qr(WHATSAPP)
    Hnd = Hand(3)

    # 1 · A5 con sangrado, 2 páginas
    p1 = "bares/folleto-A5-con-sangre.pdf"
    c = canvas.Canvas(p1, pagesize=(A5W + 2 * BLEED, A5H + 2 * BLEED))
    c.setTitle("Folleto bares · Joaquín Montenegro")
    c.translate(BLEED, BLEED)
    front(c, Hnd, photo_path, grain_path, qr_path)
    c.showPage()
    c.translate(BLEED, BLEED)
    back(c, Hand(9), photo_path, grain_path, qr_path)
    c.showPage()
    c.save()

    # 2 · A4 horizontal, dos folletos por hoja (para imprimir en casa y cortar)
    p2 = "bares/A4-2-por-hoja.pdf"
    a4w, a4h = 297 * mm, 210 * mm
    c = canvas.Canvas(p2, pagesize=(a4w, a4h))
    c.setTitle("Folleto bares · 2 por hoja")
    for page in range(2):
        for i in range(2):
            c.saveState()
            c.translate(i * A5W + 0.5 * mm, 0)
            if page == 0:
                front(c, Hand(3), photo_path, grain_path, qr_path)
            else:
                back(c, Hand(9), photo_path, grain_path, qr_path)
            c.restoreState()
        # línea de corte central
        c.setStrokeColor(Color(0.45, 0.45, 0.45))
        c.setLineWidth(0.3)
        c.setDash(2, 2)
        c.line(A5W + 0.5 * mm, 0, A5W + 0.5 * mm, A5H)
        c.setDash()
        # marcas de corte exteriores
        c.setLineWidth(0.4)
        c.setStrokeColor(Color(0, 0, 0))
        for yy in (0, A5H):
            c.line(0, yy, 4 * mm, yy)
            c.line(a4w - 4 * mm, yy, a4w, yy)
        c.showPage()
    c.save()

    # 3 · cartel A4
    p3 = "bares/cartel-A4.pdf"
    c = canvas.Canvas(p3, pagesize=(210 * mm + 2 * BLEED, 297 * mm + 2 * BLEED))
    c.setTitle("Cartel bares · Joaquín Montenegro")
    c.translate(BLEED, BLEED)
    poster(c, Hand(21), photo_path, grain_path, qr_path)
    c.showPage()
    c.save()

    for f in (p1, p2, p3):
        print("ok", f, os.path.getsize(f) // 1024, "KB")


if __name__ == "__main__":
    build()
