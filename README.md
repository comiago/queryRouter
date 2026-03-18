# 🚀 QueryRouter

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/comiago/queryRouter)](LICENSE)
[![Stars](https://img.shields.io/github/stars/comiago/queryRouter)](https://github.com/comiago/queryRouter/stargazers)
[![Issues](https://img.shields.io/github/issues/comiago/queryRouter)](https://github.com/comiago/queryRouter/issues)
[![Last Commit](https://img.shields.io/github/last-commit/comiago/queryRouter)](https://github.com/comiago/queryRouter)

## 🎬 Demo

![QueryRouter Demo](assets/demo.gif)

**QueryRouter** turns your browser’s address bar into a **powerful command center**.

Instead of relying on the limited custom search systems built into modern browsers, QueryRouter runs a lightweight local server that lets you define **fast, flexible search shortcuts**.

Type things like:

```
yt:lofi hip hop
gh:fastapi
wiki:rome
maps:pisa
```

…and instantly jump to the right website.

All powered by a **local FastAPI router** you fully control.

---

## ✨ Features

* ⚡ **Instant Shortcuts**
  Define custom commands like `yt:music` or `gh:fastapi`.

* 🔄 **Hot Reload Configuration**
  Edit `config.yaml` and changes apply instantly.

* 🌐 **Cross-Browser Support**
  Works with Brave, Chrome, Firefox, Edge, and Safari.

* 🧠 **Smart Query Parsing**
  Lightweight parsing system designed for speed.

* 🎨 **Web Dashboard**
  Manage shortcuts from a clean web UI.

* 🖥 **CLI Tooling**
  Control the router with simple `qr` commands.

* 🥷 **Background Mode**
  Run silently on system startup.

* 🧩 **Modular Architecture**
  Clean separation between parser, router, and models.

---

# ⚡ Quick Example

Your browser becomes a **command line for the internet**.

| Query           | Result           |
| --------------- | ---------------- |
| `yt:lofi`       | Search YouTube   |
| `gh:fastapi`    | Search GitHub    |
| `wiki:rome`     | Open Wikipedia   |
| `maps:florence` | Open Google Maps |

---

# 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/comiago/queryRouter.git
cd queryRouter
```

Install the project:

```bash
pip install -e .
```

Start the router:

```bash
qr start
```

Then configure your browser search engine to:

```
http://127.0.0.1:9191/search?q=%s
```

Your address bar is now powered by **QueryRouter**.

---

# ⚙️ Configuration

All shortcuts are defined in a simple YAML file.

`config.yaml`

```yaml
port: 9191
separator: ":"
default_engine: "https://www.google.com/search?q="

shortcuts:
  yt, tube:
    url: "https://www.youtube.com/"
    search: "https://www.youtube.com/results?search_query={query}"

  gh:
    url: "https://github.com/"
    search: "https://github.com/search?q={query}"
```

Changes are applied **instantly** thanks to hot-reload.

---

# 🌐 Browser Setup

To use QueryRouter you must configure your browser to forward searches to the local server.

### Chrome / Brave / Edge

Go to:

```
Settings → Search engine → Manage search engines
```

Add a new engine:

| Field    | Value                               |
| -------- | ----------------------------------- |
| Name     | QueryRouter                         |
| Shortcut | @q                                  |
| URL      | `http://127.0.0.1:9191/search?q=%s` |

Set it as **default**.

---

### Safari (macOS)

Safari does not allow custom search engines natively.

Install the extension:

Custom Search Engine (Mac App Store)

Then configure:

```
http://127.0.0.1:9191/search?q={query}
```

---

# 🖥 CLI Commands

QueryRouter includes a built-in CLI.

| Command        | Description                        |
| -------------- | ---------------------------------- |
| `qr start`     | Start the router server            |
| `qr install`   | Install background service (macOS) |
| `qr uninstall` | Remove background service          |

---

# 🧩 Architecture

QueryRouter follows a **simple modular architecture** designed for maintainability.

```
Browser Request
       │
       ▼
 FastAPI Endpoint
       │
       ▼
     Parser
       │
       ▼
     Router
       │
       ▼
  Redirect URL
```

### Components

**Parser**

Extracts the shortcut and query from the input.

Example:

```
yt:music
```

becomes:

```
shortcut → yt
query → music
```

---

**Router**

Resolves the shortcut using the configuration file and constructs the final URL.

---

**Models**

Pydantic models used for validation and structured configuration.

---

# 🏠 Dashboard

QueryRouter includes a lightweight dashboard for managing shortcuts.

Access it directly from your browser by typing:

```
qr
home
dash
```

---

# 🥷 Background Execution

Run QueryRouter automatically on system startup.

---

### macOS

Uses LaunchAgents.

Install service:

```bash
qr install
```

Remove service:

```bash
qr uninstall
```

---

### Windows

Use the startup folder.

1. Press `Win + R`
2. Run:

```
shell:startup
```

3. Create a shortcut to:

```
run_router.vbs
```

QueryRouter will now run silently in the background.

---

### 🐧 Linux (systemd)

On modern Linux distributions you can run QueryRouter as a **systemd service** so it starts automatically at boot.

Create the service file:

```bash
sudo nano /etc/systemd/system/queryrouter.service
```

Paste the following configuration:

```ini
[Unit]
Description=QueryRouter Service
After=network.target

[Service]
User=<your_username>
WorkingDirectory=/path/to/queryRouter
ExecStart=/path/to/queryRouterVenv/bin/qr start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Replace:

* `<your_username>` with your system username
* `/path/to/queryRouter` with the project directory
* `/path/to/queryRouterVenv` with your virtual environment path

Save the file and reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service to start automatically on boot:

```bash
sudo systemctl enable queryrouter.service
```

Start the service immediately (optional):

```bash
sudo systemctl start queryrouter.service
```

You can check the status with:

```bash
sudo systemctl status queryrouter.service
```

---

# 🛠 Built With

* FastAPI
* Typer
* Pydantic
* PyYAML
* TailwindCSS

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Support the Project

If you find QueryRouter useful, consider giving the repository a star.

It helps others discover the project and motivates further development.
