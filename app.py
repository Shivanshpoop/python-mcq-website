"""A dependency-free Python MCQ quiz server.

Run: python app.py
Then open http://127.0.0.1:8000
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8000

def load_questions():
    return json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))

class QuizHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/questions":
            public = [{k: q[k] for k in ("id", "question", "options", "category")}
                      for q in load_questions()]
            return self.send_json(200, {"questions": public})
        if self.path in ("/", "/index.html"):
            return self.serve_static("index.html", "text/html; charset=utf-8")
        if self.path == "/style.css":
            return self.serve_static("style.css", "text/css; charset=utf-8")
        if self.path == "/script.js":
            return self.serve_static("script.js", "text/javascript; charset=utf-8")
        self.send_error(404, "Not found")

    def serve_static(self, filename, content_type):
        body = (ROOT / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/submit":
            return self.send_error(404, "Not found")
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 100_000:
                return self.send_json(400, {"error": "Invalid request size"})
            submitted = json.loads(self.rfile.read(length))
            answers = submitted.get("answers", {})
            questions = load_questions()
            by_id = {str(q["id"]): q for q in questions}
            correct = 0
            details = []
            for qid, question in by_id.items():
                chosen = answers.get(qid)
                is_correct = chosen == question["answer"]
                correct += int(is_correct)
                details.append({
                    "id": qid,
                    "correct": is_correct,
                    "correct_answer": question["answer"],
                    "explanation": question["explanation"]
                })
            total = len(questions)
            self.send_json(200, {
                "score": correct,
                "total": total,
                "percentage": round(correct / total * 100) if total else 0,
                "details": details
            })
        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_json(400, {"error": "Please submit valid JSON."})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

if __name__ == "__main__":
    print(f"MCQ Quiz running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), QuizHandler).serve_forever()
