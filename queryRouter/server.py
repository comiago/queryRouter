from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from .parser import QueryParser
from .router import Router

app = FastAPI()
parser = QueryParser()
router = Router()

@app.get("/search")
async def search(q: str = Query(...)):
    parsed = parser.parse(q)
    target = router.get_destination(parsed)
    return RedirectResponse(url=target)