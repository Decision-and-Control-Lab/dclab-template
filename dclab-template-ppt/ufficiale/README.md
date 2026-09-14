# Template PowerPoint ufficiale — Decision & Control Lab

`Template_presentazioni_ppt.pptx` è il **template ufficiale del laboratorio**: ha due schemi diapositiva (slide master) già pronti, ciascuno con le proprie diapositive di esempio (titolo, una slide di contenuto con le indicazioni tipografiche, una slide di chiusura). **Usa questo per le presentazioni del laboratorio.**

> ⚠️ **Prima di iniziare, rinomina il file** (e la cartella del progetto, se lo condividi via GitHub o cartella condivisa) in qualcosa che identifichi la tua presentazione, ad esempio `slide-nomeconvegno-2026.pptx`. Non lavorare mantenendo il nome generico del template: rende difficile distinguere la tua versione da quella originale e da altre presentazioni.

## Come iniziare

1. Apri il file con PowerPoint (lo schema diapositiva e i font potrebbero non essere riprodotti fedelmente da LibreOffice o Google Slides: per questo template è consigliato usare PowerPoint).
2. **Rinomina il file** (vedi sopra).
3. Nella prima slide, sostituisci titolo, sottotitolo, nome e informazioni aggiuntive con i tuoi.
4. Aggiungi le tue slide di contenuto duplicando quella di esempio (slide 2), così mantieni font e impaginazione corrette.

## Modificare il piè di pagina (nome, email, loghi)

Il piè di pagina ("Pag. `<numero>` — Nome Cognome (email: nome.cognome@poliba.it)") e i loghi **non vanno modificati slide per slide**: sono impostati nello schema diapositiva e si aggiornano su tutte le slide in un colpo solo.

1. Vai su **Visualizza → Schema diapositiva**.
2. Nel riquadro a sinistra troverai gli schemi disponibili: seleziona quello che vuoi usare (se ce n'è più di uno, scegli quello pensato per il tuo tipo di presentazione, o elimina quello che non ti serve dal menu contestuale).
3. Modifica il testo del piè di pagina con il tuo nome ed email.
4. Se serve, sostituisci le immagini dei loghi trascinando la nuova immagine al posto della vecchia.
5. Torna alla visualizzazione normale (**Visualizza → Normale**): le modifiche si applicano a tutte le slide che usano quello schema.

## Font e stile del testo

Il template usa una tipografia precisa, definita nello schema diapositiva:

- **Titoli delle slide**: font *Lato Black*, dimensione 22pt.
- **Testo del corpo**: font *Lato*, dimensione 18pt.
- **Enfasi** (parole o frasi da sottolineare): grassetto, colore `#2A6099`.

Se il tuo computer non ha il font *Lato* installato, PowerPoint lo sostituisce automaticamente con un font simile: per un risultato fedele, [scarica e installa Lato](https://fonts.google.com/specimen/Lato) (gratuito) prima di lavorare al file.

## Aggiungere nuove slide

Per non perdere lo stile del template, **duplica una slide esistente** (tasto destro sulla slide nel pannello a sinistra → Duplica diapositiva) invece di crearne una vuota da un layout generico: eviti di dover reimpostare manualmente font, piè di pagina e loghi.

## Problemi comuni

- **Il font non è quello del template**: se apri il file su un computer senza *Lato* installato, PowerPoint sostituisce automaticamente con un font simile — il layout potrebbe spostarsi leggermente. Verifica sempre l'aspetto finale sul computer che userai per presentare.
- **Un'immagine appare sfocata**: usa immagini ad alta risoluzione (almeno 150-200 dpi alla dimensione finale) invece di ridimensionare molto un'immagine piccola.
- **Ho modificato il piè di pagina/logo su una slide ma non sulle altre**: quasi certamente l'hai modificato in visualizzazione normale invece che nello schema diapositiva. Rifai la modifica da **Visualizza → Schema diapositiva**.

## Alternative

- Versione PowerPoint più semplice, senza schema diapositiva: [`../semplice`](../semplice).
- Versione LaTeX/Beamer equivalente, con supporto nativo a formule, bibliografia e codice sorgente: `dclab-template-beamer`.
