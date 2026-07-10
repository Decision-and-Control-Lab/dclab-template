# D&CLab LaTeX templates

Questo repository contiene i template LaTeX del Decision & Control Lab e una
galleria HTML generata automaticamente. A ogni push su `main`, GitHub Actions
ricompila i documenti, crea le anteprime e gli archivi ZIP e pubblica l'intero
checkout su GitHub Pages.

## Struttura di un template

Una cartella viene riconosciuta automaticamente quando contiene almeno un file
`.tex` principale. La selezione del documento avviene in questo ordine:

1. `main` in `template.yml`;
2. `main.tex` nella cartella;
3. l'unico `.tex` che contiene `\\documentclass`.

Se più file soddisfano l'ultimo criterio, la build termina con un errore e
chiede di specificare `main`. Le cartelle di servizio come `.git`, `.github`,
`scripts`, `assets`, `templates`, `dist`, `build` e `vendor` non vengono
considerate. Eventuali repository `.git` annidati vengono solo segnalati.

Il file opzionale `template.yml` supporta questi metadati:

```yaml
title: Relazione di tirocinio
description: Template LaTeX per la relazione di tirocinio.
main: main.tex
engine: pdflatex
author: DCLab
tags:
  - tirocinio
  - relazione
order: 10
preview_page: 1
```

In assenza di metadati, il titolo coincide con il nome della cartella, la
descrizione resta vuota, il motore predefinito è `pdflatex` e la scheda viene
comunque generata. Sono supportati `pdflatex`, `xelatex` e `lualatex` tramite
`latexmk`.

## Aggiungere un nuovo template

1. Crea una nuova cartella nella radice e inserisci le sorgenti, incluso il
   file `.tex` principale.
2. Aggiungi `template.yml` solo se vuoi titolo, descrizione, tag, ordine,
   pagina di preview o motore diversi dai valori predefiniti.
3. Esegui il generatore localmente e controlla PDF, preview, ZIP e pagina HTML.
4. Fai push su `main`: il workflow aggiornerà automaticamente la galleria.

Gli ZIP contengono soltanto le sorgenti del template. Sono esclusi `.git`,
directory di build, file temporanei LaTeX, PDF compilati e preview generate.

## Test locale

Dipendenze Python:

```bash
python -m pip install -r requirements.txt
```

Sono inoltre necessari `latexmk`, almeno uno tra `pdflatex`/`xelatex`/`lualatex`
e `pdftoppm` (oppure `pdftocairo`). Il comando standard è:

```bash
python scripts/build_gallery.py
```

Per uno smoke test su un PDF già presente, utile su macchine senza TeX Live,
si può usare soltanto localmente:

```bash
python scripts/build_gallery.py --skip-compile --template dclab-template-beamer
```

Il comando completo non usa mai PDF preesistenti: se un template non compila,
stampa il log di `latexmk` e termina con codice diverso da zero. In questo caso
il job Pages non effettua il deploy e il sorgente difettoso va corretto.

## Output e configurazione URL

`gallery.yml` è il punto centrale di configurazione. Contiene il titolo del
sito, il base URL assoluto, il repository GitHub e i percorsi di output:

- `templates/index.html` e `templates/gallery.css`;
- `assets/templates/pdfs/`;
- `assets/templates/previews/`;
- `assets/templates/downloads/`.

Il base URL predefinito corrisponde al repository pubblico
`Decision-and-Control-Lab/dclab-template`. Per un custom domain o un diverso
percorso, modifica `base_url` oppure imposta la variabile GitHub Actions
`GALLERY_BASE_URL`. Sono disponibili anche `GALLERY_GITHUB_REPOSITORY` e
`GALLERY_GITHUB_BRANCH`. Il link “Open in Overleaf” usa sempre lo ZIP pubblico
assoluto e URL-encodato prodotto dalla build.

## GitHub Pages

Il workflow `.github/workflows/build-template-gallery.yml` parte su push verso
`main` e con avvio manuale. Installa Python 3.11, PyYAML, TeX Live, `latexmk`,
`poppler-utils`, `zip` e `biber`, quindi pubblica l'intero sito con le action
ufficiali di GitHub Pages. Nel repository GitHub:

1. apri **Settings → Pages**;
2. scegli **GitHub Actions** come source;
3. esegui il workflow oppure fai push su `main`.

Le impostazioni remote di Pages e l'eventuale custom domain non vengono
modificate dal codice del repository.

Il precedente `static.yml` è mantenuto solo come avviso manuale e non effettua
più deploy concorrenti: il workflow da usare è `build-template-gallery.yml`.

