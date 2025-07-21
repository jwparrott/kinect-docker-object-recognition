from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tracker_node import deduplicate

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    objs = deduplicate()
    html = "<h2>Tracked Objects</h2><ul>"
    for o in objs:
        html += f"<li>x={o['x']:.1f}, y={o['y']:.1f}, depth={o['depth']:.1f}</li>"
    html += "</ul>"
    return html
