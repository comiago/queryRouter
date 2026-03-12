import typer
import uvicorn
import os
import shutil
from pathlib import Path
from .server import app as fastapi_app

app = typer.Typer(no_args_is_help=True)

@app.command()
def start(port: int = 8080, host: str = "127.0.0.1"):
    """🚀 Avvia il server di redirect."""
    typer.echo(f"Running on http://{host}:{port}")
    uvicorn.run("queryRouter.server:app", host=host, port=port, reload=True)

@app.command()
def install():
    """🍎 Installa come servizio di background (macOS)."""
    if os.name != 'posix':
        typer.echo("❌ Questo comando è pensato per macOS.")
        return

    qr_path = shutil.which("qr")
    if not qr_path:
        typer.echo("❌ Errore: Esegui prima 'pip install -e .'")
        return

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.queryrouter</string>
    <key>ProgramArguments</key>
    <array>
        <string>{qr_path}</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>"""

    plist_path = Path.home() / "Library/LaunchAgents/com.user.queryrouter.plist"
    with open(plist_path, "w") as f:
        f.write(plist_content)
    
    os.system(f"launchctl load {plist_path}")
    typer.echo("✅ Servizio installato e avviato!")

@app.command()
def uninstall():
    """🗑 Rimuove il servizio di background (macOS)."""
    plist_path = Path.home() / "Library/LaunchAgents/com.user.queryrouter.plist"
    if plist_path.exists():
        os.system(f"launchctl unload {plist_path}")
        os.remove(plist_path)
        typer.echo("✅ Servizio rimosso.")

if __name__ == "__main__":
    app()