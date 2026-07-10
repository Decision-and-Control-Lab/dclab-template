# Template Tesi — Decision & Control Lab

Template LaTeX per la redazione della tesi di laurea con il Decision &
Control Lab, Politecnico di Bari.

> ⚠️ **Prima di iniziare, rinomina il progetto** (il nome della cartella
> su GitHub, oppure il nome del progetto su Overleaf) da
> `dclab-template-tesi` a qualcosa che identifichi la tua tesi, ad
> esempio `tesi-cognome` o `tesi-nome-cognome`. Non lavorare mantenendo
> il nome generico del template: rende difficile distinguere i tuoi
> file da quelli di altri studenti e da versioni future del template.

## Cosa non modificare

Non toccare i file nella cartella `00-settings` (in particolare
`style.sty` e `mcode.sty`): contengono l'impaginazione, i pacchetti e la
notazione matematica condivisa dal laboratorio. Se pensi che qualcosa
vada cambiato lì, parlane prima con il relatore.

## Come iniziare

1. Crea un account su [Overleaf](https://www.overleaf.com/) (oppure usa
   una distribuzione LaTeX locale come TinyTeX/TeX Live, se preferisci
   compilare sul tuo computer).
2. Importa il progetto in versione ZIP su Overleaf seguendo
   [questa guida](https://www.overleaf.com/learn/how-to/Uploading_a_project).
3. **Rinomina il progetto** (vedi sopra).
4. Apri `main.tex` e modifica **solo** il blocco `CONFIGURA QUI` in
   cima al file: titolo, autore, relatore, correlatori, materia, corso
   di laurea, dipartimento, anno accademico, lingua e logo del
   frontespizio.

## Struttura delle cartelle

| Cartella/file | Contenuto |
|---|---|
| `00-settings/` | Stile, classe, loghi — non modificare |
| `01-chapters/` | Capitoli della tesi (`capitolo1.tex`, ...), dedica, sommario, liberatoria, appendice |
| `02-figures/` | Immagini richiamate con `\includegraphics` |
| `03-code/matlab/`, `03-code/python/` | Codice sorgente richiamato con `\lstinputlisting` |
| `references.bib` | Bibliografia (BibTeX) |
| `main.tex` | Punto di ingresso: configurazione + struttura del documento |

## Scrivere i contenuti

- **Capitoli**: aggiungi il testo nei file dentro `01-chapters/`. Per
  aggiungere o rimuovere un capitolo, aggiungi/togli la relativa riga
  `\input{...}` in `main.tex`.
- **Immagini**: mettile in `02-figures/` e richiamale con
  `\includegraphics{02-figures/nomefile}`.
- **Codice**: mettilo nella sottocartella del linguaggio,
  `03-code/matlab/` o `03-code/python/`, e richiamalo con
  `\lstinputlisting{...}` (per Python aggiungi l'opzione
  `[style=pythonstyle]`, già definita in `style.sty`). Vedi l'esempio
  in `01-chapters/appendiceA.tex`.
- **Bibliografia**: aggiungi le voci in `references.bib` (si trovano
  cercando l'articolo su Google Scholar → "Cita" → BibTeX) e citale nel
  testo con `\cite{nomeRiferimento}`.

## Problemi comuni

- **"File not found" in compilazione**: quasi sempre un percorso
  sbagliato in un `\input`, `\includegraphics` o `\lstinputlisting` —
  controlla che il file esista esattamente in quel percorso (maiuscole/
  minuscole comprese).
- **Riferimenti bibliografici che compaiono come "?"**: su Overleaf,
  imposta il compilatore su **pdfLaTeX** e assicurati che il menu
  "Recompile from scratch" sia stato eseguito almeno una volta dopo aver
  aggiunto una nuova citazione (biblatex/biber richiede più passaggi).
- **Il logo non compare**: controlla che il percorso in
  `\renewcommand{\logo}{...}` punti a un file esistente dentro
  `00-settings/`.

## Non toccare

Le sezioni di `main.tex` marcate `NON MODIFICARE` caricano i pacchetti e
generano automaticamente il frontespizio: lasciale come sono.
