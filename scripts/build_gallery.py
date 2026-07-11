#!/usr/bin/env python3
"""Build the LaTeX template gallery.
"""

from __future__ import annotations

import argparse
import html
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlencode, quote

try:
    import yaml
except ImportError:  # pragma: no cover - exercised in clean CI environments
    yaml = None  # type: ignore[assignment]


IGNORED_DISCOVERY_DIRS = {
    ".git", ".github", ".codex", ".agents", "scripts", "site", "website",
    "assets", "templates", "node_modules", "dist", "build", "_build",
    "vendor", "work", "outputs", "__pycache__",
}
ZIP_IGNORED_DIRS = {
    ".git", ".github", "build", "_build", "dist", "__pycache__",
    ".pytest_cache", ".mypy_cache", "node_modules",
}
LATEX_TEMP_SUFFIXES = {
    ".aux", ".bbl", ".bcf", ".blg", ".dvi", ".fdb_latexmk", ".fls",
    ".glo", ".glg", ".gls", ".idx", ".ilg", ".ind", ".lof", ".log",
    ".lot", ".nav", ".out", ".run.xml", ".snm", ".synctex", ".toc",
    ".vrb", ".xdv",
}
ENGINE_FLAGS = {"pdflatex": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex", "latexmk": "-pdf"}
DOCUMENTCLASS_RE = re.compile(r"\\documentclass(?:\s*\[[^\]]*\])?\s*\{", re.IGNORECASE)


class GalleryError(RuntimeError):
    """An expected, user-actionable gallery error."""


class MetadataError(GalleryError):
    """Invalid template metadata."""


class MainFileError(GalleryError):
    """Unable to determine one unambiguous main TeX document."""


class BuildError(GalleryError):
    """A template could not be compiled or rendered."""


@dataclass(frozen=True)
class GalleryConfig:
    site_title: str
    base_url: str
    github_repository: str
    github_branch: str
    output_gallery: Path
    output_stylesheet: Path
    output_pdfs: Path
    output_previews: Path
    output_downloads: Path
    preview_dpi: int = 144
    compile_timeout_seconds: int = 600

    @classmethod
    def from_file(cls, path: Path, root: Path) -> "GalleryConfig":
        raw = load_yaml(path)
        if not isinstance(raw, Mapping):
            raise GalleryError(f"Configurazione {path} deve contenere una mappa YAML.")

        def string_value(key: str, default: str = "") -> str:
            value = raw.get(key, default)
            if value is None:
                return ""
            if not isinstance(value, str):
                raise GalleryError(f"Configurazione {path}: {key} deve essere una stringa.")
            return value.strip()

        def integer_value(key: str, default: int) -> int:
            value = raw.get(key, default)
            try:
                parsed = int(value)
            except (TypeError, ValueError) as exc:
                raise GalleryError(f"Configurazione {path}: {key} deve essere un intero.") from exc
            if parsed <= 0:
                raise GalleryError(f"Configurazione {path}: {key} deve essere maggiore di zero.")
            return parsed

        def relative_path(key: str, default: str) -> Path:
            value = string_value(key, default)
            candidate = Path(value)
            if not value or candidate.is_absolute() or ".." in candidate.parts:
                raise GalleryError(f"Configurazione {path}: {key} deve essere un percorso relativo dentro il repository.")
            return candidate

        def environment_or_config(name: str, default: str) -> str:
            return os.environ.get(name, "").strip() or default

        base_url = environment_or_config("GALLERY_BASE_URL", string_value("base_url")).rstrip("/")
        if not base_url.startswith(("http://", "https://")):
            raise GalleryError("Imposta base_url in gallery.yml oppure GALLERY_BASE_URL a un URL http(s) assoluto.")
        github_repository = environment_or_config("GALLERY_GITHUB_REPOSITORY", string_value("github_repository"))
        github_branch = environment_or_config("GALLERY_GITHUB_BRANCH", string_value("github_branch", "main"))
        if not github_repository or not github_branch:
            raise GalleryError("github_repository e github_branch non possono essere vuoti.")

        values: dict[str, Any] = {
            "site_title": string_value("site_title", "LaTeX template gallery"),
            "base_url": base_url,
            "github_repository": github_repository,
            "github_branch": github_branch,
            "output_gallery": relative_path("output_gallery", "templates/index.html"),
            "output_stylesheet": relative_path("output_stylesheet", "templates/gallery.css"),
            "output_pdfs": relative_path("output_pdfs", "assets/templates/pdfs"),
            "output_previews": relative_path("output_previews", "assets/templates/previews"),
            "output_downloads": relative_path("output_downloads", "assets/templates/downloads"),
            "preview_dpi": integer_value("preview_dpi", 144),
            "compile_timeout_seconds": integer_value("compile_timeout_seconds", 600),
        }
        return cls(**values)


@dataclass(frozen=True)
class TemplateMetadata:
    title: str
    description: str
    main: str | None
    engine: str
    author: str
    tags: tuple[str, ...]
    order: int
    preview_page: int


@dataclass(frozen=True)
class Template:
    directory: Path
    main_file: Path
    metadata: TemplateMetadata
    slug: str

    @property
    def name(self) -> str:
        return self.directory.name


@dataclass(frozen=True)
class BuiltTemplate:
    template: Template
    pdf_path: Path
    preview_path: Path
    zip_path: Path


def load_yaml(path: Path) -> Any:
    if yaml is None:
        raise GalleryError("PyYAML non è installato. Esegui `python -m pip install -r requirements.txt`.")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise MetadataError(f"YAML non valido in {path}: {exc}") from exc
    except OSError as exc:
        raise MetadataError(f"Impossibile leggere {path}: {exc}") from exc


def read_metadata(template_dir: Path) -> TemplateMetadata:
    path = template_dir / "template.yml"
    raw = load_yaml(path) if path.exists() else {}
    if raw is None:
        raw = {}
    if not isinstance(raw, Mapping):
        raise MetadataError(f"{path} deve contenere una mappa YAML.")

    def string_value(key: str, default: str = "") -> str:
        value = raw.get(key, default)
        if value is None:
            return ""
        if not isinstance(value, str):
            raise MetadataError(f"{path}: {key} deve essere una stringa.")
        return value.strip()

    title = string_value("title", template_dir.name) or template_dir.name
    description = string_value("description")
    main = string_value("main") or None
    engine = string_value("engine", "pdflatex").lower()
    if engine not in ENGINE_FLAGS:
        raise MetadataError(f"{path}: engine '{engine}' non supportato (usa pdflatex, xelatex o lualatex).")
    author = string_value("author")

    tags_value = raw.get("tags", [])
    if tags_value is None:
        tags_value = []
    if isinstance(tags_value, str):
        tags = (tags_value.strip(),) if tags_value.strip() else ()
    elif isinstance(tags_value, Sequence) and not isinstance(tags_value, (bytes, bytearray)):
        tags = tuple(str(tag).strip() for tag in tags_value if str(tag).strip())
    else:
        raise MetadataError(f"{path}: tags deve essere una lista o una stringa.")
    try:
        order = int(raw.get("order", 0))
    except (TypeError, ValueError) as exc:
        raise MetadataError(f"{path}: order deve essere un intero.") from exc
    try:
        preview_page = int(raw.get("preview_page", 1))
    except (TypeError, ValueError) as exc:
        raise MetadataError(f"{path}: preview_page deve essere un intero.") from exc
    if preview_page < 1:
        raise MetadataError(f"{path}: preview_page deve essere almeno 1.")
    return TemplateMetadata(title, description, main, engine, author, tags, order, preview_page)


def iter_tex_files(directory: Path) -> list[Path]:
    result: list[Path] = []
    for current, dirnames, filenames in os.walk(directory):
        current_path = Path(current)
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORED_DISCOVERY_DIRS and not (current_path / name).is_symlink())
        result.extend(Path(current) / name for name in sorted(filenames) if (Path(current) / name).suffix.lower() == ".tex" and not (Path(current) / name).is_symlink())
    return sorted(result, key=lambda item: item.relative_to(directory).as_posix().lower())


def contains_documentclass(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.lstrip().startswith("%"):
                    continue
                if DOCUMENTCLASS_RE.search(line):
                    return True
    except OSError:
        return False
    return False


def path_inside(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def resolve_main_file(template_dir: Path, metadata: TemplateMetadata) -> Path:
    if metadata.main:
        candidate = template_dir / Path(metadata.main)
        if not path_inside(candidate, template_dir) or candidate.suffix.lower() != ".tex":
            raise MainFileError(f"{template_dir / 'template.yml'}: main deve indicare un file .tex interno.")
        if not candidate.is_file():
            raise MainFileError(f"{template_dir / 'template.yml'}: main non trovato: {metadata.main}")
        return candidate
    default_main = template_dir / "main.tex"
    if default_main.is_file():
        return default_main
    documentclass_files = [path for path in iter_tex_files(template_dir) if contains_documentclass(path)]
    if len(documentclass_files) == 1:
        return documentclass_files[0]
    if not documentclass_files:
        raise MainFileError(f"{template_dir}: nessun file .tex principale trovato (manca main.tex e non c'è \\documentclass).")
    names = ", ".join(path.relative_to(template_dir).as_posix() for path in documentclass_files)
    raise MainFileError(f"{template_dir}: più file .tex con \\documentclass, specifica main in template.yml: {names}")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", normalized).strip("-._").lower() or "template"


def find_nested_git(root: Path) -> list[Path]:
    nested: list[Path] = []
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        names = [*filenames, *dirnames]
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for name in names:
            candidate = current_path / name
            if name == ".git" and candidate != root / ".git":
                nested.append(candidate)
    return sorted(set(nested))


def discover_templates(root: Path) -> tuple[list[Template], list[str]]:
    candidates: list[Path] = []
    errors: list[str] = []
    for current, dirnames, _ in os.walk(root):
        current_path = Path(current)
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORED_DISCOVERY_DIRS and not (current_path / name).is_symlink())
        if current_path == root:
            continue
        metadata_path = current_path / "template.yml"
        tex_files = iter_tex_files(current_path)
        if not tex_files and not metadata_path.exists():
            continue
        try:
            metadata = read_metadata(current_path)
            resolve_main_file(current_path, metadata)
        except GalleryError as exc:
            if current_path.parent == root or metadata_path.exists():
                errors.append(str(exc))
            continue
        candidates.append(current_path)

    selected: list[Path] = []
    for candidate in sorted(candidates, key=lambda path: (len(path.relative_to(root).parts), path.as_posix().lower())):
        if any(parent in selected for parent in candidate.parents):
            continue
        selected.append(candidate)

    templates: list[Template] = []
    slugs: set[str] = set()
    for directory in sorted(selected, key=lambda path: path.as_posix().lower()):
        try:
            metadata = read_metadata(directory)
            main_file = resolve_main_file(directory, metadata)
        except GalleryError as exc:
            errors.append(str(exc))
            continue
        slug = slugify(directory.name)
        if slug in slugs:
            errors.append(f"Slug duplicato '{slug}' per {directory}.")
            continue
        slugs.add(slug)
        templates.append(Template(directory, main_file, metadata, slug))
    return templates, sorted(set(errors))


def normalize_relative(path: Path) -> str:
    return path.as_posix().lstrip("./")


def run_command(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise BuildError(f"Comando non trovato: {command[0]}. Installa le dipendenze richieste.") from exc
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f"Comando scaduto dopo {timeout} secondi: {' '.join(command)}") from exc


def compile_template(template: Template, build_dir: Path, timeout: int) -> Path:
    latexmk = shutil.which("latexmk")
    if not latexmk:
        raise BuildError("latexmk non è installato o non è nel PATH.")
    main_relative = normalize_relative(template.main_file.relative_to(template.directory))
    for source_dir, dirnames, _ in os.walk(template.directory):
        source_path = Path(source_dir)
        dirnames[:] = [
            name for name in dirnames
            if name not in ZIP_IGNORED_DIRS
            and name not in IGNORED_DISCOVERY_DIRS
            and not (source_path / name).is_symlink()
        ]
        relative = source_path.relative_to(template.directory)
        if relative != Path("."):
            (build_dir / relative).mkdir(parents=True, exist_ok=True)

    command = [latexmk, ENGINE_FLAGS[template.metadata.engine], "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"-outdir={build_dir.resolve()}", main_relative]
    result = run_command(command, cwd=template.directory, timeout=timeout)
    if result.returncode != 0:
        output = (result.stdout or "").strip()
        raise BuildError(f"Compilazione fallita per {template.name} (engine {template.metadata.engine}).\n{output[-9000:]}")
    expected = build_dir / f"{template.main_file.stem}.pdf"
    if expected.is_file():
        return expected
    generated = sorted(build_dir.glob("*.pdf"))
    if len(generated) == 1:
        return generated[0]
    raise BuildError(f"latexmk non ha prodotto il PDF atteso per {template.name}: {expected.name}")


def find_existing_pdf(template: Template) -> Path | None:
    for candidate in (template.main_file.with_suffix(".pdf"), template.directory / "main.pdf"):
        if candidate.is_file():
            return candidate
    return None


def make_preview(pdf_path: Path, output_path: Path, page: int, dpi: int) -> None:
    tool = shutil.which("pdftoppm") or shutil.which("pdftocairo")
    if not tool:
        raise BuildError("Né pdftoppm né pdftocairo sono disponibili per generare la preview.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = output_path.with_suffix("")
    if output_path.exists():
        output_path.unlink()
    command = [tool, "-png", "-f", str(page), "-l", str(page), "-r", str(dpi), "-singlefile", str(pdf_path), str(prefix)]
    result = run_command(command, cwd=pdf_path.parent, timeout=120)
    if result.returncode != 0 or not output_path.is_file():
        raise BuildError(f"Preview fallita per {pdf_path.name}.\n{(result.stdout or '')[-4000:]}")


def is_latex_temp(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".synctex.gz") or name.endswith(".run.xml") or path.suffix.lower() in LATEX_TEMP_SUFFIXES


def source_files_for_zip(template: Template) -> Iterable[tuple[Path, Path]]:
    generated_pdfs = {template.main_file.with_suffix(".pdf").resolve(), (template.directory / "main.pdf").resolve()}
    for current, dirnames, filenames in os.walk(template.directory):
        current_path = Path(current)
        dirnames[:] = sorted(name for name in dirnames if name not in ZIP_IGNORED_DIRS and not (current_path / name).is_symlink())
        for filename in sorted(filenames):
            source = current_path / filename
            if source.is_symlink() or source.resolve() in generated_pdfs or is_latex_temp(source) or filename in {".DS_Store", "Thumbs.db"}:
                continue
            yield source, source.relative_to(template.directory)


def build_zip(template: Template, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_zip: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{template.slug}-", suffix=".zip", dir=output_path.parent, delete=False) as handle:
            temporary_zip = Path(handle.name)
        with zipfile.ZipFile(temporary_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for source, relative in source_files_for_zip(template):
                archive.write(source, normalize_relative(relative))
        os.replace(temporary_zip, output_path)
        temporary_zip = None
    finally:
        if temporary_zip and temporary_zip.exists():
            temporary_zip.unlink()


def public_url(base_url: str, relative_path: Path) -> str:
    return f"{base_url.rstrip('/')}/{quote(normalize_relative(relative_path), safe='/')}"


def relative_url(from_file: Path, target: Path) -> str:
    value = posixpath.relpath(normalize_relative(target), start=normalize_relative(from_file.parent))
    return value if value != "." else "./"


def github_source_url(config: GalleryConfig, root: Path, template: Template) -> str:
    repo = quote(config.github_repository, safe="/")
    branch = quote(config.github_branch, safe="")
    folder = quote(normalize_relative(template.directory.relative_to(root)), safe="/")
    return f"https://github.com/{repo}/tree/{branch}/{folder}"


def render_gallery(config: GalleryConfig, root: Path, built: Sequence[BuiltTemplate]) -> None:
    output = root / config.output_gallery
    output.parent.mkdir(parents=True, exist_ok=True)
    all_tags = sorted({tag for item in built for tag in item.template.metadata.tags}, key=str.casefold)
    cards: list[str] = []
    for item in built:
        template = item.template
        title = html.escape(template.metadata.title)
        description = html.escape(template.metadata.description)
        author = html.escape(template.metadata.author)
        tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in template.metadata.tags)
        search_text = html.escape(" ".join((template.metadata.title, template.metadata.description, *template.metadata.tags)), quote=True)
        preview = html.escape(relative_url(config.output_gallery, item.preview_path), quote=True)
        pdf = html.escape(relative_url(config.output_gallery, item.pdf_path), quote=True)
        download = html.escape(relative_url(config.output_gallery, item.zip_path), quote=True)
        absolute_zip = public_url(config.base_url, item.zip_path)
        overleaf = "https://www.overleaf.com/docs?" + urlencode({"snip_uri": absolute_zip, "main_document": normalize_relative(template.main_file.relative_to(template.directory))})
        source = github_source_url(config, root, template)
        author_html = f'<p class="author">{author}</p>' if author else ""
        source_html = f'<a class="button button-secondary" href="{html.escape(source, quote=True)}" target="_blank" rel="noopener">Sorgenti su GitHub</a>'
        cards.append(f'''<article class="template-card" data-search="{search_text}" data-tags="{html.escape(" ".join(template.metadata.tags), quote=True)}" data-order="{template.metadata.order}" data-name="{html.escape(template.metadata.title, quote=True)}">
  <a class="preview-link" href="{pdf}" target="_blank" rel="noopener">
    <img src="{preview}" loading="lazy" alt="Anteprima della prima pagina di {title}">
  </a>
  <div class="card-body">
    <h2>{title}</h2>
    {author_html}
    <p class="description">{description}</p>
    <div class="tags" aria-label="Tag">{tags}</div>
    <div class="actions">
      <a class="button button-primary" href="{pdf}" target="_blank" rel="noopener">Anteprima PDF</a>
      <a class="button button-secondary" href="{download}" download>Scarica ZIP</a>
      <a class="button button-secondary" href="{html.escape(overleaf, quote=True)}" target="_blank" rel="noopener">Open in Overleaf</a>
      {source_html}
    </div>
  </div>
</article>''')

    tag_options = "".join(f'<option value="{html.escape(tag, quote=True)}">{html.escape(tag)}</option>' for tag in all_tags)
    stylesheet = html.escape(relative_url(config.output_gallery, config.output_stylesheet), quote=True)
    title = html.escape(config.site_title)
    cards_html = "\n".join(cards)
    document = f'''<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Galleria dei template LaTeX di D&amp;CLab">
  <title>{title}</title>
  <link rel="stylesheet" href="{stylesheet}">
</head>
<body>
  <header class="site-header"><div class="shell"><p class="eyebrow">Decision &amp; Control Lab</p><h1>{title}</h1><p class="intro">Template LaTeX del D&amp;C Lab.</p></div></header>
  <main class="shell" id="main-content">
    <section class="controls" aria-label="Filtra template">
      <div class="control"><label for="search">Cerca</label><input id="search" type="search" placeholder="Titolo, descrizione o tag" autocomplete="off"></div>
      <div class="control"><label for="tag-filter">Tag</label><select id="tag-filter"><option value="">Tutti i tag</option>{tag_options}</select></div>
      <div class="control"><label for="sort">Ordina</label><select id="sort"><option value="order">Ordine consigliato</option><option value="name">Alfabetico</option></select></div>
    </section>
    <p class="result-count" aria-live="polite">{len(built)} template</p>
    <section class="template-grid" data-template-grid aria-label="Template disponibili">{cards_html}</section>
    <noscript><p class="noscript">Attiva JavaScript per usare ricerca, filtro e ordinamento.</p></noscript>
  </main>
  <footer class="site-footer"><div class="shell"><p> </p></div></footer>
  <script>
    (() => {{
      const grid = document.querySelector('[data-template-grid]'); const cards = Array.from(grid.querySelectorAll('.template-card'));
      const search = document.querySelector('#search'); const tag = document.querySelector('#tag-filter'); const sort = document.querySelector('#sort'); const count = document.querySelector('.result-count');
      const apply = () => {{ const query = search.value.trim().toLocaleLowerCase(); const selectedTag = tag.value.toLocaleLowerCase(); let visible = 0;
        cards.forEach((card) => {{ const text = card.dataset.search.toLocaleLowerCase(); const tags = card.dataset.tags.toLocaleLowerCase().split(/\s+/).filter(Boolean); const matches = (!query || text.includes(query)) && (!selectedTag || tags.includes(selectedTag)); card.hidden = !matches; if (matches) visible += 1; }});
        count.textContent = `${{visible}} template${{visible === 1 ? '' : 's'}}`; }};
      sort.addEventListener('change', () => {{ const sorted = cards.slice().sort((a, b) => sort.value === 'name' ? a.dataset.name.localeCompare(b.dataset.name, 'it') : (Number(a.dataset.order) - Number(b.dataset.order)) || a.dataset.name.localeCompare(b.dataset.name, 'it')); sorted.forEach((card) => grid.appendChild(card)); }});
      search.addEventListener('input', apply); tag.addEventListener('change', apply);
    }})();
  </script>
</body>
</html>
'''
    output.write_text(document, encoding="utf-8")


def clean_generated_outputs(root: Path, config: GalleryConfig) -> None:
    for directory, suffixes in ((root / config.output_pdfs, {".pdf"}), (root / config.output_previews, {".png", ".webp"}), (root / config.output_downloads, {".zip"})):
        directory.mkdir(parents=True, exist_ok=True)
        for path in directory.iterdir():
            if path.is_file() and path.suffix.lower() in suffixes:
                path.unlink()


def build_one(template: Template, root: Path, config: GalleryConfig, temporary_root: Path, skip_compile: bool) -> BuiltTemplate:
    build_dir = temporary_root / template.slug
    build_dir.mkdir(parents=True, exist_ok=True)
    if skip_compile:
        pdf_source = find_existing_pdf(template)
        if not pdf_source:
            raise BuildError(f"--skip-compile richiesto ma non esiste un PDF precompilato per {template.name}.")
    else:
        pdf_source = compile_template(template, build_dir, config.compile_timeout_seconds)
    pdf_path = root / config.output_pdfs / f"{template.slug}.pdf"
    preview_path = root / config.output_previews / f"{template.slug}.png"
    zip_path = root / config.output_downloads / f"{template.slug}.zip"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_source, pdf_path)
    make_preview(pdf_path, preview_path, template.metadata.preview_page, config.preview_dpi)
    build_zip(template, zip_path)
    return BuiltTemplate(template, config.output_pdfs / pdf_path.name, config.output_previews / preview_path.name, config.output_downloads / zip_path.name)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Radice del repository.")
    parser.add_argument("--config", type=Path, help="File YAML di configurazione (default: gallery.yml).")
    parser.add_argument("--template", action="append", dest="templates", help="Limita l'esecuzione a una cartella template (ripetibile).")
    parser.add_argument("--skip-compile", action="store_true", help="Smoke test locale: usa un PDF già presente, senza latexmk.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.root.resolve(); config_path = (args.config or root / "gallery.yml").resolve()
    if not root.is_dir():
        print(f"Errore: repository non trovato: {root}", file=sys.stderr); return 2
    if not config_path.is_file():
        print(f"Errore: configurazione non trovata: {config_path}", file=sys.stderr); return 2
    try:
        config = GalleryConfig.from_file(config_path, root); templates, discovery_errors = discover_templates(root)
    except GalleryError as exc:
        print(f"Errore: {exc}", file=sys.stderr); return 2
    for nested in find_nested_git(root):
        print(f"Avviso: repository .git annidato rilevato e lasciato intatto: {nested}")
    for error in discovery_errors:
        print(f"Errore rilevamento template: {error}", file=sys.stderr)
    if discovery_errors:
        return 1
    if args.templates:
        requested = set(args.templates); templates = [item for item in templates if item.name in requested]; missing = sorted(requested - {item.name for item in templates})
        if missing:
            print(f"Errore: template non trovati: {', '.join(missing)}", file=sys.stderr); return 2
    if not templates:
        print("Errore: nessun template LaTeX rilevato.", file=sys.stderr); return 1
    templates.sort(key=lambda item: (item.metadata.order, item.metadata.title.casefold())); clean_generated_outputs(root, config)
    built: list[BuiltTemplate] = []; failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="latex-template-gallery-") as temporary:
        for template in templates:
            print(f"[{template.name}] main: {template.main_file.relative_to(template.directory)}")
            try:
                built.append(build_one(template, root, config, Path(temporary), args.skip_compile)); print(f"[{template.name}] PDF, preview e ZIP generati.")
            except GalleryError as exc:
                failures.append(f"{template.name}: {exc}"); print(f"[{template.name}] ERRORE: {exc}", file=sys.stderr)
    if failures:
        print("\nCompilazioni fallite:", file=sys.stderr)
        for failure in failures: print(f"- {failure}", file=sys.stderr)
        return 1
    render_gallery(config, root, built); print(f"Galleria aggiornata: {root / config.output_gallery}"); print(f"Template elaborati: {len(built)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
