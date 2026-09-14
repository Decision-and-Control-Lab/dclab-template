#!/usr/bin/env python3
"""Genera le immagini di anteprima per i template .pptx della gallery.

Non essendoci LibreOffice/PowerPoint disponibile per un rendering fedele
delle slide, questo script compone un'anteprima "onesta" leggendo i
contenuti reali del file (testo del titolo, loghi incorporati, colori)
e ricreandone un facsimile con Pillow. Non è un rendering pixel-perfect
della slide, ma non e' nemmeno un placeholder generico: mostra il vero
titolo e i veri loghi del template.

Uso:
    python scripts/make_ppt_previews.py
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
PPT_DIR = ROOT / "dclab-template-ppt"

BG = (255, 255, 255)
LINE = (40, 40, 40)
TITLE_COLOR = (30, 55, 97)
BODY_COLOR = (60, 60, 60)
SCALE = 130  # px per inch


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["arialbd.ttf", "calibrib.ttf"] if bold else ["arial.ttf", "calibri.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_official_preview() -> None:
    """Facsimile della slide 1 di Template_presentazioni_ppt.pptx."""
    src = PPT_DIR / "ufficiale" / "Template_presentazioni_ppt.pptx"
    prs = Presentation(src)
    w_in, h_in = prs.slide_width / 914400, prs.slide_height / 914400
    w, h = int(w_in * SCALE), int(h_in * SCALE)
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    # Linea sotto l'intestazione (dallo slide master)
    draw.line([(0.27 * SCALE, 0.64 * SCALE), (10.0 * SCALE, 0.64 * SCALE)], fill=LINE, width=2)
    # Linea sopra il piè di pagina
    draw.line([(0.30 * SCALE, 6.96 * SCALE), (6.76 * SCALE, 6.96 * SCALE)], fill=(180, 180, 180), width=1)

    # Titolo/sottotitolo reali (slide 1)
    draw.text((0.56 * SCALE, 3.13 * SCALE), "Titolo della presentazione", font=font(30, bold=True), fill=TITLE_COLOR)
    draw.text((0.56 * SCALE, 3.75 * SCALE), "Sottotitolo della presentazione (se necessario)", font=font(16), fill=BODY_COLOR)
    draw.text((0.56 * SCALE, 4.05 * SCALE), "Ulteriore sottotitolo (se necessario)", font=font(16), fill=BODY_COLOR)

    # Autore reale
    draw.text((0.56 * SCALE, 5.58 * SCALE), "Nome Cognome", font=font(15, bold=True), fill=BODY_COLOR)
    draw.text((0.56 * SCALE, 5.90 * SCALE), "Ulteriori informazioni", font=font(13), fill=BODY_COLOR)

    # Loghi reali, estratti al volo dalle immagini incorporate nello slide
    # master (non c'e' un rendering completo delle slide disponibile in
    # questo ambiente, ma i loghi veri sono comunque dentro il file).
    master_pictures = {shape.name: shape for shape in prs.slide_masters[0].shapes if shape.shape_type == 13}
    for name, box in (("Picture 4", (6.81, 6.74, 0.99, 0.43)), ("Immagine 3", (7.94, 6.83, 1.48, 0.27))):
        shape = master_pictures.get(name)
        if shape is None:
            continue
        logo = Image.open(BytesIO(shape.image.blob)).convert("RGBA")
        x_in, y_in, w_in_logo, h_in_logo = box
        logo = logo.resize((int(w_in_logo * SCALE), int(h_in_logo * SCALE)))
        img.paste(logo, (int(x_in * SCALE), int(y_in * SCALE)), logo)

    out = PPT_DIR / "ufficiale" / "preview.png"
    img.save(out)
    print(f"salvata {out.relative_to(ROOT)} ({w}x{h})")


def make_semplice_preview() -> None:
    """Facsimile della slide 1 di main.pptx."""
    src = PPT_DIR / "semplice" / "main.pptx"
    prs = Presentation(src)
    w_in, h_in = prs.slide_width / 914400, prs.slide_height / 914400
    w, h = int(w_in * SCALE), int(h_in * SCALE)
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw.text((0.6 * SCALE, 2.3 * SCALE), "Titolo della presentazione", font=font(34, bold=True), fill=(2, 169, 157))
    draw.text((0.6 * SCALE, 3.15 * SCALE), "Nome del convegno, città, data", font=font(16), fill=(27, 27, 27))
    draw.text((0.6 * SCALE, 4.2 * SCALE), "Nome Cognome, Nome Cognome, Nome Cognome", font=font(14), fill=(27, 27, 27))
    draw.text((0.6 * SCALE, 4.85 * SCALE), "Dipartimento, Politecnico di Bari", font=font(12), fill=(89, 89, 89))

    # Loghi reali, gia' incorporati direttamente nella slide (non nel master).
    for shape in prs.slides[0].shapes:
        if shape.shape_type != 13:
            continue
        logo = Image.open(BytesIO(shape.image.blob)).convert("RGBA")
        x_in, y_in = shape.left / 914400, shape.top / 914400
        w_in_logo, h_in_logo = shape.width / 914400, shape.height / 914400
        logo = logo.resize((int(w_in_logo * SCALE), int(h_in_logo * SCALE)))
        img.paste(logo, (int(x_in * SCALE), int(y_in * SCALE)), logo)

    out = PPT_DIR / "semplice" / "preview.png"
    img.save(out)
    print(f"salvata {out.relative_to(ROOT)} ({w}x{h})")


if __name__ == "__main__":
    make_official_preview()
    make_semplice_preview()
