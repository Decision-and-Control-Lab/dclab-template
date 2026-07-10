# Template Relazione Tirocinio — Decision & Control Lab

Template LaTeX per la relazione finale di tirocinio, Decision & Control
Lab, Politecnico di Bari.

> ⚠️ **Prima di iniziare, rinomina il progetto** (il nome della cartella
> su GitHub, oppure il nome del progetto su Overleaf) da
> `dclab-template-relazione-tirocinio` a qualcosa che identifichi la
> tua relazione, ad esempio `relazione-tirocinio-cognome`. Non lavorare
> mantenendo il nome generico del template: rende difficile distinguere
> i tuoi file da quelli di altri studenti e da versioni future del
> template.

## Cosa non modificare

Non toccare i file nella cartella `00-settings` (in particolare
`style.sty`, `document.cls` e `mcode.sty`): contengono l'impaginazione,
i pacchetti e la notazione matematica condivisa dal laboratorio.

## Come iniziare

1. Crea un account su [Overleaf](https://www.overleaf.com/).
2. Importa il progetto in versione ZIP su Overleaf seguendo
   [questa guida](https://www.overleaf.com/learn/how-to/Uploading_a_project).
3. **Rinomina il progetto** (vedi sopra).
4. Apri `main.tex` e modifica **solo** il blocco `CONFIGURA QUI` in
   cima al file: studenti, tutor, corso di laurea, tipo di tirocinio
   (interno/esterno), periodo, lingua e loghi del frontespizio.

## Struttura delle cartelle

| Cartella/file | Contenuto |
|---|---|
| `00-settings/` | Stile, classe, loghi — non modificare |
| `02-figures/` | Immagini richiamate con `\includegraphics` |
| `03-code/matlab/`, `03-code/python/` | Codice sorgente richiamato con `\lstinputlisting` |
| `references.bib` | Bibliografia (BibTeX) |
| `main.tex` | Configurazione, sezioni della relazione e guida a LaTeX in appendice |

## Scrivere i contenuti

Compila le sezioni già presenti in `main.tex`: Obiettivi, Descrizione
dell'azienda/ente (solo per tirocini esterni), Attività svolte,
Risultati conseguiti. In fondo al file trovi un'appendice con una guida
rapida a LaTeX (equazioni, tabelle, algoritmi, immagini, codice): è
pensata per chi non ha mai usato LaTeX, rimuovila una volta presa
confidenza con lo strumento.

- **Immagini**: mettile in `02-figures/` e richiamale con
  `\includegraphics{02-figures/nomefile}`.
- **Codice**: se durante il tirocinio hai scritto del codice, mettilo
  nella sottocartella del linguaggio (`03-code/matlab/` o
  `03-code/python/`) e richiamalo con `\lstinputlisting{...}` (per
  Python aggiungi l'opzione `[style=pythonstyle]`). Vedi l'esempio
  nella guida in appendice.
- **Bibliografia**: aggiungi le voci in `references.bib` e citale nel
  testo con `\cite{nomeRiferimento}`.

## Problemi comuni

- **"File not found" in compilazione**: controlla il percorso esatto
  (maiuscole/minuscole comprese) in `\includegraphics` o
  `\lstinputlisting`.
- **Riferimenti bibliografici che compaiono come "?"**: su Overleaf,
  imposta il compilatore su **pdfLaTeX** e riesegui la compilazione da
  zero ("Recompile from scratch") dopo aver aggiunto una citazione.
- **I loghi del frontespizio non compaiono**: controlla i percorsi in
  `\renewcommand{\logosinistra}{...}` e `\renewcommand{\logodestra}{...}`.

## Non toccare

Le sezioni di `main.tex` marcate `NON MODIFICARE` caricano i pacchetti
e generano automaticamente il frontespizio: lasciale come sono.
