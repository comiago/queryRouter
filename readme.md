# 🚀 QueryRouter

**QueryRouter** è un tool locale leggero e modulare che trasforma la barra degli indirizzi del tuo browser in una centrale di comando. Grazie a un server locale in FastAPI, puoi definire scorciatoie di ricerca personalizzate (es. `yt:musica`, `gh:fastapi`) tramite un semplice file YAML, aggirando le restrizioni dei browser moderni.

---

## ✨ Caratteristiche

- **⚡ Hot-Reload**: Modifica il file `config.yaml` e i cambiamenti sono applicati istantaneamente, senza bisogno di riavviare il server.
- **🌐 Cross-Browser**: Funziona contemporaneamente su Brave, Chrome, Safari, Firefox e Edge.
- **🛠️ Architettura Pulita**: Struttura modulare suddivisa in Parser, Router e Models per la massima estensibilità.
- **🖥️ CLI Integrata**: Gestisci il tool con comandi semplici grazie all'interfaccia a riga di comando (es. `qr start`).
- **🥷 Background Mode**: Supporto per l'esecuzione invisibile all'avvio su Windows (via script VBS) e macOS (tramite LaunchAgents nativi).

---

## 📂 Struttura del Progetto

```text
.
├── config.yaml          # Database delle tue scorciatoie
├── pyproject.toml       # Configurazione del pacchetto Python
├── queryRouter/         # Core del programma
│   ├── config/          # Loader dinamico del file YAML
│   ├── models/          # Schemi dati Pydantic
│   ├── parser/          # Logica di estrazione query
│   ├── router/          # Logica di reindirizzamento
│   ├── cli.py           # Interfaccia a riga di comando
│   └── server.py        # API FastAPI
└── run_router.vbs       # Launcher invisibile (Solo Windows)
```

## 🚀 Installazione

1. Assicurati di avere **Python 3.8+** installato sul tuo sistema.

2. Clona o scarica questa repository.

3. Apri il terminale nella cartella del progetto ed esegui l'installazione in modalità sviluppo:

   Bash

   ```
   pip install -e .
   ```

------

## ⚙️ Configurazione (`config.yaml`)

Personalizza le tue scorciatoie modificando il file `config.yaml` nella root del progetto. Usa `{query}` come segnaposto per il testo che inserirai dopo i due punti (es. scrivendo `yt:tutorial` il sistema inserirà `tutorial` al posto di `{query}`).

YAML

```
default_engine: "https://www.google.com/search?q="

shortcuts:
  yt:
    url: "https://www.youtube.com/"
    search: "https://www.youtube.com/results?search_query={query}"
  gm:
    url: "https://mail.google.com/"
    search: "https://mail.google.com/mail/u/{query}/"
  ig:
    url: "https://www.instagram.com/"
    search: "https://www.instagram.com/{query}"
  gh:
    url: "https://github.com/"
    search: "https://github.com/search?q={query}"
```

------

## 💻 Utilizzo della CLI

Il tool è invocabile da qualsiasi punto del terminale tramite il comando `qr`.

- **Avviare il server manualmente**:

  Bash

  ```
  qr start
  ```

- **Installare come servizio di background (Solo macOS)**:

  Bash

  ```
  qr install
  ```

- **Rimuovere il servizio di background (Solo macOS)**:

  Bash

  ```
  qr uninstall
  ```

------

## 🌐 Configurazione del Browser

Per attivare QueryRouter, devi istruire il tuo browser a inviare le ricerche al server locale.

### Brave / Chrome / Edge

1. Vai nelle Impostazioni del browser e cerca **"Motori di ricerca"** o **"Ricerca nei siti"**.
2. Aggiungi un nuovo motore di ricerca:
   - **Nome**: `QueryRouter`
   - **Scorciatoia**: `@q` (o impostalo come Predefinito)
   - **URL**: `http://127.0.0.1:8080/search?q=%s`

### Safari (macOS)

Poiché Safari non permette l'aggiunta manuale di motori di ricerca, installa l'estensione gratuita **Keyword Search** e imposta l'URL di ricerca su: `http://127.0.0.1:8080/search?q={query}`

### Esecuzione Automatica (Windows)

Per avviare il router all'accensione del PC senza finestre visibili:

1. Assicurati di aver creato il file `run_router.vbs` con il comando di avvio.
2. Premi `Win + R`, digita `shell:startup` e invio.
3. Trascina un collegamento del file `.vbs` in questa cartella.

------

## 🛠️ Tecnologie Utilizzate

- **[FastAPI](https://fastapi.tiangolo.com/)**: Per redirect HTTP ultra-veloci.
- **[Typer](https://typer.tiangolo.com/)**: Per la gestione dei comandi CLI.
- **[Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/)**: Per la validazione strutturata dei dati.
- **PyYAML**: Per la lettura dinamica della configurazione.