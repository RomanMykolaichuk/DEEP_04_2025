from flask import Flask, render_template, request, redirect, url_for, session
from utils.groq_client import generate_scene_and_options
from utils.tts_generator import generate_audio
from utils.gemini_client import generate_image
import os
from dotenv import load_dotenv
from flask import send_file
from utils.zip_exporter import export_story_zip


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "your-secret-key")  # session

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session['topic'] = request.form['topic']
        session['scenes'] = []
        session['choices'] = []
        session['total_scenes'] = int(request.form['num_scenes'])
        return redirect(url_for("story"))

    return render_template("index.html")

@app.route("/story", methods=["GET", "POST"])
def story():
    scenes = session.get('scenes', [])
    choices = session.get('choices', [])
    topic = session.get('topic', '')
    total_scenes = session.get('total_scenes', 5)


    if request.method == "POST":
        selected_option = request.form['option']
        choices.append(selected_option)
        session['choices'] = choices

    if len(scenes) < total_scenes:
        scene_text, options = generate_scene_and_options(topic, scenes, choices)
        scenes.append({'text': scene_text, 'options': options})
        session['scenes'] = scenes
    else:
        zip_path = export_story_zip(scenes, choices, topic.strip().replace(" ", "_"))
        session['zip_path'] = zip_path
        return render_template("finished.html", scenes=scenes, choices=choices)
    
    scene_index = len(scenes)
    audio_path = generate_audio(scene_text, scene_index)
    image_path = generate_image(scene_text, scene_index)

    scenes[-1]["audio"] = audio_path
    scenes[-1]["image"] = image_path

    return render_template(
        "scene.html",
        scene=scenes[-1],
        scene_number=len(scenes)
    )

@app.route("/download-zip")
def download_zip():
    zip_path = session.get('zip_path')
    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return "ZIP file not found", 404

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
