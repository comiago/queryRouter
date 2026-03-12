import logging
from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
from .parser import QueryParser
from .router import Router

# --- LOGGING SETUP ---
# This creates a router.log file in the same folder as your config.yaml
log_file = Path(__file__).parent.parent / "router.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler() # Also prints to the terminal
    ]
)
logger = logging.getLogger("queryRouter.server")

app = FastAPI()
parser = QueryParser()
router = Router()

class NewShortcut(BaseModel):
    keyword: str
    url: str
    search: Optional[str] = None

# --- API & SEARCH ROUTES ---

@app.get("/search")
async def search(q: str = Query(...), request: Request = None):
    # Log the incoming search and the client's IP address
    client_ip = request.client.host if request else "Unknown"
    logger.info(f"🔍 Search request from {client_ip}: '{q}'")
    
    parsed = parser.parse(q)
    target = router.get_destination(parsed)
    
    logger.info(f"🚀 Redirecting to: {target}")
    return RedirectResponse(url=target)

@app.get("/api/config")
async def get_config():
    return router.loader.load()

@app.post("/api/shortcuts")
async def add_shortcut(item: NewShortcut):
    logger.info(f"✍️ Request to add/edit shortcut: '{item.keyword}'")
    data = router.loader.load()
    
    new_entry = {"url": item.url}
    if item.search:
        new_entry["search"] = item.search
        
    if "shortcuts" not in data:
        data["shortcuts"] = {}
        
    data["shortcuts"][item.keyword] = new_entry
    router.loader.save(data)
    return {"status": "success"}

@app.delete("/api/shortcuts/{keyword}")
async def delete_shortcut(keyword: str):
    logger.warning(f"🗑️ Request to delete shortcut: '{keyword}'")
    data = router.loader.load()
    
    if "shortcuts" in data and keyword in data["shortcuts"]:
        del data["shortcuts"][keyword]
        router.loader.save(data)
        return {"status": "success", "message": f"'{keyword}' deleted."}
        
    logger.error(f"⚠️ Attempted to delete non-existent shortcut: '{keyword}'")
    return {"status": "error", "message": "Shortcut not found."}


# --- THE WEB DASHBOARD (GUI) ---

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QueryRouter Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans p-8">
    <div class="max-w-5xl mx-auto">
        
        <header class="flex justify-between items-center mb-10 border-b border-gray-700 pb-4">
            <h1 class="text-3xl font-bold text-blue-400">🚀 QueryRouter</h1>
            <span class="text-sm bg-gray-800 px-3 py-1 rounded-full text-gray-400 font-mono">v0.6.0</span>
        </header>

        <div class="bg-gray-800 p-6 rounded-xl shadow-lg mb-8 border border-gray-700">
            <h2 id="formTitle" class="text-xl font-semibold mb-4 text-white">Add New Shortcut</h2>
            <form id="addForm" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm text-gray-400 mb-1">Keyword(s) (comma separated)</label>
                    <input type="text" id="k_keyword" required placeholder="e.g., yt, tube, video" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white focus:border-blue-500 outline-none transition">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-1">Base URL</label>
                    <input type="url" id="k_url" required class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white focus:border-blue-500 outline-none transition">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-1">Search Template (use {query})</label>
                    <input type="text" id="k_search" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white focus:border-blue-500 outline-none transition">
                </div>
                <div class="md:col-span-3 flex justify-end mt-2 gap-3">
                    <button type="button" onclick="resetForm()" class="text-gray-400 hover:text-white px-4 py-2 hidden" id="cancelBtn">Cancel Edit</button>
                    <button type="submit" id="submitBtn" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-6 rounded transition shadow-lg">
                        + Save Shortcut
                    </button>
                </div>
            </form>
        </div>

        <h2 class="text-xl font-semibold mb-4 text-gray-300">Active Shortcuts</h2>
        <div id="shortcutsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            </div>

    </div>

    <script>
        async function loadShortcuts() {
            try {
                const res = await fetch('/api/config');
                const data = await res.json();
                const grid = document.getElementById('shortcutsGrid');
                grid.innerHTML = '';

                for (const [key, val] of Object.entries(data.shortcuts || {})) {
                    const safeSearch = val.search ? val.search.replace(/'/g, "\\'") : '';
                    const safeUrl = val.url ? val.url.replace(/'/g, "\\'") : '';
                    
                    grid.innerHTML += `
                        <div class="bg-gray-800 p-5 rounded-lg border border-gray-700 hover:border-blue-500 transition shadow group relative">
                            
                            <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition flex gap-3 bg-gray-800 pl-2">
                                <button onclick="editShortcut('${key}', '${safeUrl}', '${safeSearch}')" class="text-yellow-500 hover:text-yellow-400" title="Edit">✏️</button>
                                <button onclick="deleteShortcut('${key}')" class="text-red-500 hover:text-red-400" title="Delete">🗑️</button>
                            </div>

                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xl font-bold text-blue-400 font-mono">${key.split(',').map(k => k.trim()).join(' <span class="text-gray-500 text-sm">or</span> ')}</span>
                            </div>
                            <p class="text-sm text-gray-300 truncate pr-12" title="${val.url}">🔗 ${val.url}</p>
                            ${val.search ? `<p class="text-xs text-gray-500 mt-2 truncate bg-gray-900 p-2 rounded">🔍 ${val.search.replace('{query}', '<span class="text-yellow-500 font-bold">{query}</span>')}</p>` : ''}
                        </div>
                    `;
                }
            } catch (error) {
                console.error("Failed to load shortcuts:", error);
            }
        }

        function editShortcut(keyword, url, search) {
            document.getElementById('k_keyword').value = keyword;
            document.getElementById('k_url').value = url;
            document.getElementById('k_search').value = search;
            
            document.getElementById('formTitle').innerText = `✏️ Edit Shortcut`;
            document.getElementById('submitBtn').innerText = "Update Shortcut";
            document.getElementById('submitBtn').classList.replace('bg-blue-600', 'bg-yellow-600');
            document.getElementById('cancelBtn').classList.remove('hidden');
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
            document.getElementById('k_url').focus();
        }

        async function deleteShortcut(keyword) {
            if(confirm(`Are you sure you want to delete this shortcut?`)) {
                await fetch(`/api/shortcuts/${encodeURIComponent(keyword)}`, { method: 'DELETE' });
                loadShortcuts(); 
            }
        }

        function resetForm() {
            document.getElementById('addForm').reset();
            document.getElementById('formTitle').innerText = "Add New Shortcut";
            document.getElementById('submitBtn').innerText = "+ Save Shortcut";
            document.getElementById('submitBtn').classList.replace('bg-yellow-600', 'bg-blue-600');
            document.getElementById('cancelBtn').classList.add('hidden');
        }

        document.getElementById('addForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                keyword: document.getElementById('k_keyword').value.trim().toLowerCase(),
                url: document.getElementById('k_url').value.trim(),
                search: document.getElementById('k_search').value.trim() || null
            };

            await fetch('/api/shortcuts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            resetForm();
            loadShortcuts();
        });

        loadShortcuts();
    </script>
</body>
</html>
"""

@app.get("/")
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)