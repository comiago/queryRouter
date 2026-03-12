import typer
import uvicorn
import os
import shutil
from pathlib import Path
from .server import app as fastapi_app

app = typer.Typer(no_args_is_help=True)

@app.command()
def start(port: int = 8080, host: str = "127.0.0.1"):
    """🚀 Start the redirect server."""
    typer.echo(f"Running on http://{host}:{port}")
    uvicorn.run("queryRouter.server:app", host=host, port=port, reload=True)

@app.command()
def install():
    """🍎 Install as a background service (macOS)."""
    if os.name != 'posix':
        typer.echo("❌ This command is for macOS only.")
        return

    qr_path = shutil.which("qr")
    if not qr_path:
        typer.echo("❌ Error: Run 'pip install -e .' first.")
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
    typer.echo("✅ Service installed and started!")

@app.command()
def uninstall():
    """🗑 Remove the background service (macOS)."""
    plist_path = Path.home() / "Library/LaunchAgents/com.user.queryrouter.plist"
    if plist_path.exists():
        os.system(f"launchctl unload {plist_path}")
        os.remove(plist_path)
        typer.echo("✅ Service removed.")

if __name__ == "__main__":
    app()