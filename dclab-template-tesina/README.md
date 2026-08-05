# Template Tesina — Decision & Control Lab

Template LaTeX per la redazione di tesine per il laboratorio di Teoria
dei sistemi, Decision & Control Lab, Politecnico di Bari.

> ⚠️ **Prima di iniziare, rinomina il progetto** (il nome della cartella
> su GitHub, oppure il nome del progetto su Overleaf) da
> `dclab-template-tesina` a qualcosa che identifichi la tua tesina, ad
> esempio `tesina-cognome`. Non lavorare mantenendo il nome generico del
> template: rende difficile distinguere i tuoi file da quelli di altri
> studenti e da versioni future del template.

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
   cima al file: titolo, studenti, tutor, materia, corso di laurea,
   dipartimento, anno accademico, lingua e loghi del frontespizio.

## Struttura delle cartelle

| Cartella/file | Contenuto |
|---|---|
| `00-settings/` | Stile, classe, loghi — non modificare |
| `02-figures/` | Immagini richiamate con `\includegraphics` |
| `03-code/matlab/`, `03-code/python/` | Codice sorgente richiamato con `\lstinputlisting` |
| `references.bib` | Bibliografia (BibTeX) |
| `main.tex` | Configurazione, contenuto e appendice codice |

## Scrivere i contenuti

Il contenuto della tesina va scritto direttamente in `main.tex`, dopo
il sommario (abstract). Le sezioni di esempio già presenti (equazioni,
tabelle, algoritmi, immagini, elenchi, teoremi) mostrano come usare i
comandi principali di LaTeX: sostituiscile con i tuoi contenuti man
mano che procedi, così da non perdere il riferimento a come si scrive
ciascun elemento.

- **Immagini**: mettile in `02-figures/` e richiamale con
  `\includegraphics{02-figures/nomefile}`.
- **Codice**: mettilo nella sottocartella del linguaggio,
  `03-code/matlab/` o `03-code/python/`, e richiamalo con
  `\lstinputlisting{...}` (per Python aggiungi l'opzione
  `[style=pythonstyle]`). Vedi l'esempio in appendice a `main.tex`.
- **Bibliografia**: aggiungi le voci in `references.bib` (si trovano
  cercando l'articolo su Google Scholar → "Cita" → BibTeX) e citale nel
  testo con `\cite{nomeRiferimento}`. I riferimenti sono numerati in
  ordine di citazione; citandone più di uno insieme
  (`\cite{rif1,rif2,rif3}`) vengono compattati automaticamente in `[1-3]`.
  Per i siti web usa il tipo `@misc` con il campo `howpublished`, come
  nelle voci di esempio già presenti nel file.

## Problemi comuni

- **"File not found" in compilazione**: controlla il percorso esatto
  (maiuscole/minuscole comprese) in `\includegraphics` o
  `\lstinputlisting`.
- **Riferimenti bibliografici che compaiono come `[?]`**: succede quando
  la bibliografia non è ancora stata rigenerata. Su Overleaf imposta il
  compilatore su **pdfLaTeX** e premi *Recompile* una seconda volta: la
  bibliografia richiede un passaggio in più per essere aggiornata. Se
  dopo due compilazioni il problema resta, controlla che la chiave usata
  in `\cite{...}` corrisponda esattamente a quella nel file
  `references.bib` (maiuscole/minuscole comprese).
- **I loghi del frontespizio non compaiono**: controlla i percorsi in
  `\renewcommand{\logosinistra}{...}` e `\renewcommand{\logodestra}{...}`.

## Non toccare

Le sezioni di `main.tex` marcate `NON MODIFICARE` caricano i pacchetti
e generano automaticamente il frontespizio: lasciale come sono.
