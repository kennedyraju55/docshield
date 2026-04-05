"""DocShield — Privacy-First Medical Document Assistant.
All processing happens locally via Ollama. No data ever leaves your machine.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from docshield.ollama_backend import OllamaBackend
from docshield.image_utils import preprocess_image

app = Flask(__name__)
backend = OllamaBackend()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    """Check if Ollama is running and model is available."""
    return jsonify(backend.health_check())


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze uploaded document image or pasted text."""
    image_b64 = None
    text = None

    if "image" in request.files:
        file = request.files["image"]
        image_b64 = preprocess_image(file.read())
    elif request.is_json:
        data = request.get_json()
        text = data.get("text", "").strip()
        image_b64 = data.get("image_b64")

    if not image_b64 and not text:
        return jsonify({"error": "No image or text provided"}), 400

    def generate():
        # Import agents here to avoid circular imports
        from docshield.agents.orchestrator import Orchestrator
        orchestrator = Orchestrator(backend)

        context = {"image_b64": image_b64, "text": text}
        for event in orchestrator.run(context):
            yield f"data: {json.dumps(event)}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DocShield -- Privacy-First Medical Document Assistant")
    print("  All processing happens locally. No data leaves your machine.")
    print("=" * 60)
    print(f"\n  Open in browser: http://localhost:5000")
    print(f"  AI Model: {backend.model} (via Ollama)\n")
    app.run(debug=False, host="127.0.0.1", port=5000, threaded=True)
