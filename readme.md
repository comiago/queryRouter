- 

# 🚀 QueryRouter

**QueryRouter** is a lightweight, modular local tool that transforms your browser's address bar into a powerful command center. Powered by a local FastAPI server, you can define custom search shortcuts (e.g., `yt:music`, `gh:fastapi`) through a simple YAML file, effortlessly bypassing the search engine restrictions of modern browsers.

---

## ✨ Features

- **⚡ Hot-Reload**: Edit the `config.yaml` file and changes are applied instantly—no server restart required.
- **🌐 Cross-Browser**: Works seamlessly across Brave, Chrome, Safari, Firefox, and Edge.
- **🛠️ Clean Architecture**: Modular structure divided into Parser, Router, and Models for maximum extensibility.
- **🖥️ Integrated CLI**: Manage the tool with simple commands via the built-in command-line interface (e.g., `qr start`).
- **🥷 Background Mode**: Support for invisible startup execution on Windows (via VBS script) and macOS (via native LaunchAgents).

---

## 📂 Project Structure

```text
.
├── config.yaml          # Your shortcut database
├── pyproject.toml       # Python package configuration
├── queryRouter/         # Application core
│   ├── config/          # Dynamic YAML config loader
│   ├── models/          # Pydantic data schemas
│   ├── parser/          # Query extraction logic
│   ├── router/          # Redirection logic
│   ├── cli.py           # Command-line interface
│   └── server.py        # FastAPI server
└── run_router.vbs       # Invisible launcher (Windows only)
```

## 🚀 Installation

1. Ensure you have **Python 3.8+** installed on your system.

2. Clone or download this repository.

3. Open your terminal in the project directory and install it in editable mode:

   Bash

   ```
   pip install -e .
   ```

------

## ⚙️ Configuration (`config.yaml`)

Customize your shortcuts by editing the `config.yaml` file in the project root. Use `{query}` as a placeholder for the text you type after the colon (e.g., typing `yt:tutorial` will replace `{query}` with `tutorial`).

YAML

```
default_engine: "[https://www.google.com/search?q=](https://www.google.com/search?q=)"

shortcuts:
  yt:
    url: "[https://www.youtube.com/](https://www.youtube.com/)"
    search: "[https://www.youtube.com/results?search_query=](https://www.youtube.com/results?search_query=){query}"
  gm:
    url: "[https://mail.google.com/](https://mail.google.com/)"
    search: "[https://mail.google.com/mail/u/](https://mail.google.com/mail/u/){query}/"
  ig:
    url: "[https://www.instagram.com/](https://www.instagram.com/)"
    search: "[https://www.instagram.com/](https://www.instagram.com/){query}"
  gh:
    url: "[https://github.com/](https://github.com/)"
    search: "[https://github.com/search?q=](https://github.com/search?q=){query}"
```

------

## 💻 CLI Usage

The tool can be invoked from anywhere in your terminal using the `qr` command.

- **Start the server manually**:

  Bash

  ```
  qr start
  ```

- **Install as a background service (macOS only)**:

  Bash

  ```
  qr install
  ```

- **Remove the background service (macOS only)**:

  Bash

  ```
  qr uninstall
  ```

------

## 🌐 Browser Configuration

To activate QueryRouter, you must instruct your browser to send searches to the local server.

### Brave / Chrome / Edge

1. Go to your browser Settings and look for **"Search engine"** or **"Site search"**.
2. Add a new search engine:
   - **Search engine**: `QueryRouter`
   - **Shortcut**: `@q` (or set it as Default)
   - **URL with %s in place of query**: `http://127.0.0.1:8080/search?q=%s`

### Safari (macOS)

Since Safari doesn't allow adding custom search engines natively, install the free **Keyword Search** extension and set the Search URL to: `http://127.0.0.1:8080/search?q={query}`

### Automatic Startup (Windows)

To start the router when you log in without keeping a terminal window open:

1. Ensure the `run_router.vbs` file is in your project folder.
2. Press `Win + R`, type `shell:startup`, and press Enter.
3. Drag a shortcut of the `.vbs` file into this folder.

------

## 🛠️ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)**: For lightning-fast HTTP redirects.
- **[Typer](https://typer.tiangolo.com/)**: For the modern CLI experience.
- **[Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/)**: For robust data validation.
- **PyYAML**: For dynamic configuration loading.