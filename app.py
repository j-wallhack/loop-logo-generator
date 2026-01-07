"""Flask application for loop logo generator."""

import io

from flask import Flask, jsonify, render_template, request, send_file
from PIL import Image

from animations import VALID_ANIMATION_TYPES, build_frames
from utils import parse_color


app = Flask(__name__)


def generate_loop_gif(
    image_file, 
    animation_type: str, 
    frames: int, 
    frame_duration_ms: int, 
    bg_color: str
) -> io.BytesIO:
    """
    Generate a looping GIF with the specified animation.
    
    Args:
        image_file: File object containing the source image
        animation_type: Type of animation to apply
        frames: Number of frames in the animation
        frame_duration_ms: Duration of each frame in milliseconds
        bg_color: Background color as hex string
    
    Returns:
        BytesIO buffer containing the generated GIF
    """
    source = Image.open(image_file).convert("RGBA")
    bg_rgba = parse_color(bg_color)
    frame_sequence = build_frames(source, animation_type, frames, bg_rgba)

    # Convert to palette mode to keep GIF size reasonable
    palette_frames = [
        frame.convert("P", palette=Image.ADAPTIVE, colors=256) 
        for frame in frame_sequence
    ]

    buffer = io.BytesIO()
    palette_frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=palette_frames[1:],
        loop=0,
        duration=frame_duration_ms,
        disposal=2,
    )
    buffer.seek(0)
    return buffer


@app.get("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    """API endpoint to generate GIF from uploaded image."""
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "Missing image file"}), 400

    animation_type = (request.form.get("animation_type") or "left").lower()
    if animation_type not in VALID_ANIMATION_TYPES:
        animation_type = "left"

    try:
        frames = int(request.form.get("frames", 24))
    except (TypeError, ValueError):
        frames = 24
    frames = max(2, min(frames, 240))

    try:
        frame_duration_ms = int(request.form.get("frame_duration", 50))
    except (TypeError, ValueError):
        frame_duration_ms = 50
    frame_duration_ms = max(10, min(frame_duration_ms, 5000))

    bgcolor = request.form.get("bgcolor", "#000000")

    try:
        gif_buffer = generate_loop_gif(
            file, animation_type, frames, frame_duration_ms, bgcolor
        )
    except Exception as exc:
        return jsonify({"error": f"Failed to create GIF: {exc}"}), 500

    return send_file(
        gif_buffer,
        mimetype="image/gif",
        download_name="loop.gif",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
