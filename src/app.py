from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

TASKS = [
    {"id": 1, "title": "Write a clear commit message", "done": True},
    {"id": 2, "title": "Run the test suite", "done": False},
    {"id": 3, "title": "Open a pull request", "done": False},
]


def add_task(tasks, title):
    title = title.strip()
    if title:
        next_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": next_id, "title": title, "done": False})
    return tasks


def toggle_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return tasks


def remove_task(tasks, task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    return tasks


def page(tasks):
    completed = sum(task["done"] for task in tasks)
    percent = round(completed / len(tasks) * 100) if tasks else 0
    task_rows = "".join(
        f"""<li class='task {'done' if task['done'] else ''}'>
          <form method='post'><input type='hidden' name='action' value='toggle'><input type='hidden' name='id' value='{task['id']}'><button class='check' aria-label='Toggle task'>{'&#10003;' if task['done'] else ''}</button></form>
          <span>{escape(task['title'])}</span>
          <form method='post'><input type='hidden' name='action' value='delete'><input type='hidden' name='id' value='{task['id']}'><button class='delete' aria-label='Delete task'>&times;</button></form>
        </li>"""
        for task in tasks
    )
    empty = "<p class='empty'>Nothing here yet. Add a task above to start.</p>" if not tasks else ""
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Action Board</title><style>
:root {{ --ink:#102a43; --muted:#627d98; --paper:#f7f9f7; --teal:#0f766e; --coral:#f9735b; --line:#d9e2ec; }}
* {{ box-sizing:border-box }} body {{ margin:0; color:var(--ink); background:var(--paper); font:16px system-ui,sans-serif }}
body:before {{ content:''; display:block; height:5px; background:var(--coral) }} main {{ width:min(700px,calc(100% - 32px)); margin:70px auto }}
.brand {{ color:var(--teal); font-weight:800; letter-spacing:.08em; text-transform:uppercase; font-size:12px }} h1 {{ font-size:clamp(40px,8vw,70px); line-height:1; margin:12px 0 }} h1 em {{ color:var(--coral); font-style:normal }} .intro {{ color:var(--muted); margin-bottom:38px }}
.board {{ padding:28px; background:white; border:1px solid var(--line); border-radius:8px; box-shadow:0 14px 35px #102a4314 }} .board-head {{ display:flex; justify-content:space-between; align-items:end; gap:20px }} h2 {{ margin:0; font-size:24px }} .progress {{ color:var(--muted); font-size:13px }}
.add {{ display:flex; gap:8px; margin:25px 0 16px }} input[type=text] {{ min-width:0; flex:1; padding:12px; border:1px solid var(--line); border-radius:5px; font:inherit }} button {{ cursor:pointer; border:0; font:inherit }} .add button {{ padding:0 16px; color:white; background:var(--ink); border-radius:5px; font-weight:700 }}
ul {{ padding:0; margin:0; list-style:none }} .task {{ display:flex; align-items:center; gap:12px; padding:14px 0; border-top:1px solid #edf1f3 }} .task span {{ flex:1 }} .task.done span {{ color:#829ab1; text-decoration:line-through }} .check,.delete {{ width:24px; height:24px; padding:0; background:transparent }} .check {{ color:white; border:1px solid #9fb3c2; border-radius:50% }} .done .check {{ background:var(--teal); border-color:var(--teal) }} .delete {{ color:#9fb3c2; font-size:21px }} .delete:hover {{ color:var(--coral) }} .empty {{ color:var(--muted); text-align:center; padding:20px }}
@media(max-width:500px) {{ main {{ margin:45px auto }} .board {{ padding:20px }} .add {{ flex-direction:column }} .add button {{ min-height:44px }} }}
</style></head><body><main><div class='brand'>A / Action Board</div><h1>Move ideas from <em>queued</em> to done.</h1><p class='intro'>A tiny Python task board for your GitHub Actions demo.</p>
<section class='board'><div class='board-head'><h2>Release checklist</h2><span class='progress'>{percent}% complete</span></div>
<form class='add' method='post'><input type='hidden' name='action' value='add'><input name='title' type='text' maxlength='80' placeholder='Add a release task...' required><button>Add task</button></form>
<ul>{task_rows}</ul>{empty}</section></main></body></html>"""


class ActionBoardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page(TASKS).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode())
        action = form.get("action", [""])[0]
        if action == "add":
            add_task(TASKS, form.get("title", [""])[0])
        elif action in {"toggle", "delete"}:
            task_id = int(form.get("id", [0])[0])
            (toggle_task if action == "toggle" else remove_task)(TASKS, task_id)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("localhost", 8000), ActionBoardHandler)
    print("Action Board running at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Action Board")
        server.server_close()
