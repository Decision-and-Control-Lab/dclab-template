# Template Presentazione Beamer — Decision & Control Lab

Template LaTeX/Beamer (tema Metropolis) per presentazioni a conferenze,
Decision & Control Lab, Politecnico di Bari.

> ⚠️ **Prima di iniziare, rinomina il progetto** (il nome della cartella
> su GitHub, oppure il nome del progetto su Overleaf) da
> `dclab-template-beamer` a qualcosa che identifichi la tua
> presentazione, ad esempio `slide-nomeconvegno-2026`. Non lavorare
> mantenendo il nome generico del template: rende difficile distinguere
> i tuoi file da quelli di altre presentazioni e da versioni future del
> template.

## Cosa non modificare

Non toccare i file nella cartella `00-settings` (in particolare
`style.sty` e `mcode.sty`): contengono il tema, i loghi e la notazione
matematica condivisa dal laboratorio.

## Come iniziare

1. Crea un account su [Overleaf](https://www.overleaf.com/).
2. Importa il progetto in versione ZIP su Overleaf seguendo
   [questa guida](https://www.overleaf.com/learn/how-to/Uploading_a_project).
3. **Rinomina il progetto** (vedi sopra).
4. Apri `main.tex` e modifica **solo** il blocco `CONFIGURA QUI` in
   cima al file: titolo, sottotitolo, autori, istituto, data e i loghi
   da mostrare in basso a destra su ogni slide (0, 1, 2, 3 o più: basta
   aggiungere o togliere un percorso dalla lista `\loghi`).

## Struttura delle cartelle

| Cartella/file | Contenuto |
|---|---|
| `00-settings/` | Tema, loghi — non modificare |
| `02-figures/` | Immagini richiamate con `\includegraphics` |
| `03-code/matlab/`, `03-code/python/` | Codice sorgente richiamato con `\lstinputlisting` |
| `references.bib` | Bibliografia (BibTeX) |
| `main.tex` | Configurazione + slide di esempio |

## Scrivere i contenuti

Le slide di esempio dopo `\begin{document}` mostrano come usare
sezioni, blocchi, tabelle, formule, algoritmi, animazioni, figure,
codice e riferimenti bibliografici col tema Metropolis: sostituiscile
con i tuoi contenuti, rimuovendo quelle che non servono.

- **Immagini**: mettile in `02-figures/` e richiamale con
  `\includegraphics{02-figures/nomefile}`, come nella slide "Figures".
- **Codice**: mettilo nella sottocartella del linguaggio,
  `03-code/matlab/` o `03-code/python/`, e richiamalo con
  `\lstinputlisting{...}` (per Python aggiungi l'opzione
  `[style=pythonstyle]`), come nella slide "Code".
- **Bibliografia**: aggiungi le voci in `references.bib` e citale con
  `\cite{nomeRiferimento}`.

## Problemi comuni

- **`\verb` o codice verbatim non funziona**: assicurati che il frame
  sia dichiarato con `\begin{frame}[fragile]{...}` — qualunque frame
  che contenga `\verb`, `verbatim` o `\lstinputlisting` deve avere
  l'opzione `[fragile]`, altrimenti la compilazione si interrompe.
- **Riferimenti bibliografici che compaiono come "?"**: su Overleaf,
  imposta il compilatore su **pdfLaTeX** e riesegui la compilazione da
  zero dopo aver aggiunto una citazione (questo template usa BibTeX
  classico, non biblatex/biber).
- **I loghi non compaiono**: controlla i percorsi nella lista
  `\renewcommand{\loghi}{...}`; per non mostrare alcun logo lasciala
  vuota (`\renewcommand{\loghi}{}`).

## Versione PowerPoint

Se preferisci lavorare in PowerPoint invece che in LaTeX, esiste un
template equivalente in `dclab-template-ppt` con la stessa identità
grafica (riquadro colorato, loghi in basso a destra).

## Non toccare

Le righe di `main.tex` marcate `NON MODIFICARE` caricano la classe
beamer, il tema Metropolis e il pacchetto del laboratorio: lasciale
come sono.
