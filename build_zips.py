#!/usr/bin/env python3
"""Genera uno zip "pronto per la distribuzione" per ciascun template.

Per ogni cartella dclab-template-* nella directory corrente:
- esclude i file di compilazione LaTeX (aux, log, out, toc, lof, lot,
  bcf, run.xml, bbl, blg, nav, snm, vrb, fdb_latexmk, fls, synctex.gz)
  e il PDF compilato (main.pdf), cosi' il pacchetto contiene solo i
  sorgenti;
- esclude cartelle/file non pertinenti alla distribuzione (.git,
  .claude, .gitattributes, __pycache__, .DS_Store, Thumbs.db);
- azzera i metadati del file .pptx (autore/ultimo autore salvati da
  PowerPoint/python-pptx), che altrimenti riportano il nome di chi lo
  ha creato;
- scrive lo zip in dist/<nome-template>.zip.

Uso:
    python build_zips.py
"""

import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# File/estensioni di compilazione LaTeX da escludere
BUILD_EXTENSIONS = {
    ".aux", ".log", ".out", ".toc", ".lof", ".lot", ".bcf", ".bbl",
    ".blg", ".nav", ".snm", ".vrb", ".fls", ".fdb_latexmk", ".synctex.gz",
}
BUILD_FILENAMES = {"main.pdf", "main.run.xml"}

# Cartelle/file da non includere mai nello zip
EXCLUDE_DIR_NAMES = {".git", ".claude", "__pycache__", "dist"}
EXCLUDE_FILE_NAMES = {".gitattributes", ".DS_Store", "Thumbs.db"}


def is_build_artifact(path: Path) -> bool:
    if path.name in BUILD_FILENAMES:
        return True
    if path.name.endswith(".synctex.gz"):
        return True
    return path.suffix in BUILD_EXTENSIONS


def strip_pptx_metadata(pptx_path: Path) -> None:
    """Svuota i campi autore/ultimo-autore nei metadati del pptx."""
    try:
        from pptx import Presentation
    except ImportError:
        print(f"  [avviso] python-pptx non installato, metadati di {pptx_path.name} non modificati")
        return
    prs = Presentation(pptx_path)
    core = prs.core_properties
    core.author = ""
    core.last_modified_by = ""
    prs.save(pptx_path)


def collect_files(template_dir: Path):
    for dirpath, dirnames, filenames in os.walk(template_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIR_NAMES]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fname in EXCLUDE_FILE_NAMES:
                continue
            if is_build_artifact(fpath):
                continue
            yield fpath


def build_zip_for(template_dir: Path) -> Path:
    name = template_dir.name
    DIST.mkdir(exist_ok=True)
    zip_path = DIST / f"{name}.zip"

    # Lavora su una copia temporanea per poter ripulire i metadati
    # senza toccare i file originali del progetto.
    tmp_dir = DIST / f"_tmp_{name}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    files = list(collect_files(template_dir))
    for src in files:
        rel = src.relative_to(template_dir)
        dst = tmp_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    for pptx in tmp_dir.rglob("*.pptx"):
        strip_pptx_metadata(pptx)

    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in tmp_dir.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(tmp_dir))

    shutil.rmtree(tmp_dir)
    return zip_path


def main():
    template_dirs = sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name.startswith("dclab-template")
    )
    if not template_dirs:
        print("Nessuna cartella dclab-template-* trovata.")
        return

    for d in template_dirs:
        zip_path = build_zip_for(d)
        size_kb = zip_path.stat().st_size / 1024
        print(f"{d.name} -> {zip_path.relative_to(ROOT)} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
